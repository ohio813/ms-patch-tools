#!/usr/bin/python

#
import time
import re
import string
import sys
import os
import mechanize
from BeautifulSoup import *


#
class msPatchFileInfo:

    #
    def __init__(self):
        self.BR = mechanize.Browser()

    #
    def makeSoup(self, url):

        data = None
        for i in xrange(5):
            try:
                data = self.BR.open(url).get_data()
                break
            except:
                sys.stderr.write("Download of %s failed, sleeping for 5 and trying again (max 5 times)" % (url))
                time.sleep(5)

        if not data:
            sys.stderr.write("Failed to download %s after 5 tries" % (url))

        return BeautifulSoup(data)

    #
    def trimTarget(self, target):
        target = target.strip()
        if target.find("For all supported editions of") == 0:
            start = 30
        elif target.find("For all supported versions of") == 0:
            start = 30
        elif target.find("For all supported") == 0:
            start = 18
        else:
            start = 0
    
        if target[-1] == ":":
            return target[start:-1]
        else:
            return target[start:]

    #
    def findOldTarget(self, table):
        p = table.findPreviousSibling("p")
        if p.string:
            return self.trimTarget(p.string)
        else:
            return self.trimTarget(self.getStr(p))

    #this attempts to find the patch target in the KB page. unfortunately, MS is less than
    #consistent, and in a couple of bulletins doesn't even provide the info in the KB.
    def findTarget(self, cur):

            tmp = cur

            #it's one of these tags, or not there at all possibly
            while(tmp.name != "h4" and tmp.name != "h5" and tmp.name != "h3" and tmp.name != "b"):

                if tmp.previousSibling != None:
                    tmp = tmp.previousSibling
                else:
                    tmp = tmp.parent

                if not isinstance(tmp, Tag):
                    return None

            return self.trimTarget(self.getStr(tmp))

    #
    def normalizeOldFieldNames(self, table):

        fNames = {"file\s*name":"File name", "version":"File version", "cpu":"Platform",
                "sp":"SP requirement", "folder":"Service branch",
                "service\s*branch":"Service branch"}

        #row[0] has the column names
        row0 = table.findAll("tr")[0]
        
        #standardize case/name
        for i in xrange(len(row0.contents)):
            for k,v in fNames.iteritems():
                tdString = row0.contents[i].find(text=True)
                if(re.search(k, tdString, re.I)):
                    row0.contents[i].string = NavigableString(v)
                else:
                    row0.contents[i].string = NavigableString(tdString)
    
    #
    def normalizeFieldNames(self, table):

        fNames = {"file\s*name":"File name", "version":"File version", "cpu":"Platform",
                "sp":"SP requirement", "folder":"Service branch",
                "service\s*branch":"Service branch"}

        #standardize case/name
        for i in xrange(len(table.contents[0].contents)):
            for k,v in fNames.iteritems():
                if(re.search(k, table.contents[0].contents[i].string, re.I)):
                    table.contents[0].contents[i].string = v

    #
    def isVersionTable(self, table):

        #get rows
        trs = table.findAll("tr")

        #check columns
        if len(trs[0].contents) < 3:
            return False

        #no embedded table
        if table.find("table"):
            return False

        #just see if we can find name, version, size columns
        return (trs[0].find(text=re.compile("file\s*name", re.I)) and
                trs[0].find(text=re.compile("version", re.I)) and
                trs[0].find(text=re.compile("size", re.I)))

    #
    def guessTargetFromTitle(self, soup):
        title = soup.find("h1", "title")
        
        #MS09-062: Description of the security update for Microsoft Visual FoxPro 9.0 Service Pack 2: October 13, 2009
        start = string.find(title.string, "for the")
        if start == -1:
            start = string.find(title.string, "for")
            if start == -1:
                start = string.find(title.string, ":") + 2
            else:
                start += 4
        else:
            start += 8
        
        if string.find(title.string, ":") != string.rfind(title.string, ":"):
            return title.string[start:string.rfind(title.string, ":")]
        else:
            return title.string[start:]

    #
    def parseKB(self, url):

        print "--[Parsing KB: %s" % (url)
        soup = self.makeSoup(url)

        ret = []

        #find the file name tables
        for div in soup.findAll("div", "kb_tablewrapper"):

            #
            binaries = []

            #find parent table
            fTable = div.find('table')

            #heuristics to guess if it's a version info table
            if not self.isVersionTable(fTable):
                continue

            #hack for MS10-051, which adds unneeded <b> tags to <th> elements
            if fTable.contents[0].contents[0].string == None:
                for i in xrange(0, len(fTable.contents[0].contents)):
                    fTable.contents[0].contents[i].string = fTable.contents[0].contents[i].contents[0].string

            #check the first row to make sure it has at least 3 members:
            # file name, version, size
            if len(fTable.contents[0].contents) < 3 or not \
                        re.search("file\s*name", fTable.contents[0].contents[0].string, re.I):
                continue

            self.normalizeFieldNames(fTable)

            target = self.findTarget(fTable)
            if target is None:
                target = self.guessTargetFromTitle(soup)

            #
            fieldNames = fTable.contents[0].contents
            nFields = len(fieldNames)

            #iterate each row after the header
            for i in xrange(1, len(fTable.contents)):

                #each row is a different binary
                binary = {}
                row = fTable.contents[i]
                nCols = len(row.contents)
                fAdd = True

                if nCols < 2:
                    continue

                #iterate each column
                for x in xrange(0, nCols):

                    #there are broken bulletins (09-056) when this condition fails
                    if x < nFields:
                        field = fieldNames[x].string
                        field = " ".join(field.split()) #string extra whitespace
                        val = row.contents[x].string
                    else:
                        break

                    if field == "File version" and (val is None or string.find(val, "Not") != -1):
                        fAdd = False
                        break

                    if val is None or val == "":
                        continue

                    if re.search("not ", val, re.I):
                        val = "N/A"

                    #
                    binary[field] =  re.sub(r'\s', '', val)

                if fAdd:
                    binaries.append(binary)

            ret.append((target, binaries))

        return ret

    #
    def getNewFileInfo(self, soup, year, num):

        kbs = []

        #the 'td' argument is actually ignored since we use the text argument
        #luckily, as of 10/10, 'File Information' only appears once in the bulletin
        for td in soup.findAll("td"):
            
            for elem in td.findAll(text="File Information"):

                #findAll() above returns a NavigableString, which has no nextSibling
                #so we just do a findNext() instead of getting the parent td.nextSibling
                next_td = elem.findNext("td")
                for a in next_td.findAll("a"):
                    kbs.append(a['href'])

        #the deployment section contains multiple links to the same KB, hence the set
        kbs = set(kbs)
        results = []
        for link in kbs:
            results.append(self.parseKB(link))

        return results

    #find the first navigablestring object below elem
    def getStr(self, elem):
        s = elem.find(text=True)
        if s is not None:
            return s.strip()
        else:
            return None

    #
    def getOldFileInfo(self, soup, year, num):

        #
        ret = []
        found = False

        #find the update info subsection
        updateInfo = None
        for h3 in soup.findAll("h3"):
            if h3.find(text=["Security Update Information", "Security Update Deployment", " Security Update Information"]):
                updateInfo = h3
                break
        
        if updateInfo is None:
            updateInfo = soup

        #search for any tables that match the file name/version/size heuristic
        for table in updateInfo.findAllNext("table"):

            binaries = []

            #
            if not self.isVersionTable(table):
                continue
            found = True
 
            self.normalizeOldFieldNames(table)
            target = self.findOldTarget(table)

            #
            fieldNames = (table.find("tr")).contents
            nFields = len(fieldNames)
            rows = table.findAll("tr")
            nRows = len(rows)

            #iterate each row after the header
            for i in xrange(1, nRows):

                #each row is a different binary
                binary = {}
                row = rows[i]
                nCols = len(row.contents)
                fAdd = True

                if nCols < 2:
                    continue

                #iterate each column
                for x in xrange(0, nCols):

                    #there are broken bulletins (09-056) when this condition fails
                    if x < nFields:
                        field = fieldNames[x].string
                        field = " ".join(field.split()) #string extra whitespace
                        val = self.getStr(row.contents[x])
                    else:
                        break

                    if field == "File version" and (val is None or val == "" or string.find(val, "Not") != -1):
                        fAdd = False
                        break

                    if val is None or val == "":
                        continue

                    if re.search("not ", val, re.I):
                        val = "N/A"

                    #
                    binary[field] = re.sub(r'\s', '', val)

                if fAdd:
                    binaries.append(binary)

            ret.append((target, binaries))

        #some stupid old bulletins have KB links, MS07-057, MS07-069, MS08-010
        if not found:
            kbs = []
            for h5 in updateInfo.findAllNext("h5"):
                if self.getStr(h5) == "File Information":
                    for a in h5.findAllNext("a"):
                        if a.has_key('href') and string.find(a['href'], "http://support.microsoft.com/kb/") != -1:
                            kbs.append(a['href'])
            
            kbs = set(kbs)
            results = []
            for link in kbs:
                results.append(self.parseKB(link))
        else:
            results = [ret]
            
        return results

    #
    def getBulletinFileInfo(self, year, num):

        print "-[Retrieving file information for bulletin MS%.2d-%.3d" % (year, num)
        
        url = 'http://www.microsoft.com/technet/security/Bulletin/MS%.2d-%.3d.mspx' % (year, num)

        soup = self.makeSoup(url)

        if year > 8 or (year == 8 and num >= 18):
            return self.getNewFileInfo(soup, year, num)
        else:
            return self.getOldFileInfo(soup, year, num)

    #
    def queryMostRecent(self):
        soup = self.makeSoup("http://www.microsoft.com/technet/security/Current.aspx")
        try:
            resTable = soup.find("table", id="tblSBResults")
            firstBullRow = resTable.findAll("tr", limit=2)[1]
            link = firstBullRow.find("a")
        except Exception as err:
            print "Error querying most recent bulletin: %s" % (err)
            sys.exit(1)
        bull = os.path.splitext(link["href"].rpartition("/")[2])[0]
        return bull

    #
    def generateOutput(self, results):

        #return is a list of lists of tuples
        output = ""
        for res in results:
    
            for r in res:
                target = r[0]
                binaries = r[1]
             
                output += "\n[%s]\n" % (target)
                output += "+" + "-"*81 + "+\n"
                output += "|%-25s %-20s %-7s %-10s %-15s|\n" % ("File name", "File version", "Arch", "SP Req", "Branch")
                output += "|" + "-"*81 + "|\n"
             
                for binary in binaries:
                    fName = "[" + binary["File name"] + "]"
                    fVers = "[" + binary["File version"] + "]"
                    if binary.has_key("SP requirement"):
                        spReq = "[" + binary["SP requirement"] + "]"
                    else:
                        spReq = "[]"
                    if binary.has_key("Service branch"):
                        branch = "[" + binary["Service branch"] + "]"
                    else:
                        branch = "[]"
                    if binary.has_key("Platform"):
                        platform = "[" + binary["Platform"] + "]"
                    else:
                        platform = "[]"
    
                    output += "|%-25s %-20s %-7s %-10s %-15s|\n" % (fName, fVers, platform, spReq, branch)
    
                output += "+" + "-"*81 + "+\n"
    
        output += "#"*79 + "\n"
        return output

############################################
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Usage: %s <year> <bulletin num>\n\nExample: %s 8 20" % (sys.argv[0], sys.argv[0])
        sys.exit(1)

    yr = int(sys.argv[1])
    num = int(sys.argv[2])
    iPatch = msPatchFileInfo()
    results = iPatch.getBulletinFileInfo(yr, num)
    res = iPatch.generateOutput(results)
    res = ''.join(filter(lambda x:x in string.printable, res))
    print res
