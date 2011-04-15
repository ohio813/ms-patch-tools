#!/usr/bin/python
#
import getopt
import re
import os
import string
import shutil
import sys
import appParse
import shelve
import queryMSDB
import msPatchInfo

#
def getArch(arch, defArch):
    #print "%s, %s" % (arch, defArch)
    if arch in appParse.x86:
        return "x86"
    elif arch in appParse.x64:
        return "x64"
    elif arch in appParse.itanium:
        return "ia64"
    elif defArch in appParse.x86:
        return "x86"
    elif defArch in appParse.x64:
        return "x64"
    elif defArch in appParse.itanium:
        return "ia64"
    else:
        return "x86"

# this may not be perfect, it uses the following heuristic to assign a branch:
# if the [branch] column in the KB is filled in, use it
# else, assume it is vista/win7 and parse as per here:
# http://blogs.technet.com/b/mrsnrub/archive/2010/07/14/gdr-amp-ldr-the-next-generation.aspx
#
def getBranch(branch, version):
    if re.search("gdr", branch, re.I):
        return "GDR"
    elif re.search("qfe", branch, re.I):
        return "QFE"

    #split the version filed into 4 parts
    try:
        (major, minor, build, rev) = version.split(".")
    except:
        return "GDR"

    #Vista
    if build in ["6000", "6001", "6002"]:
        if rev[:2] in ["14", "16", "17", "18", "19", "63", "70"]:
            return "GDR"
        elif rev[:2] in ["20", "21", "22", "23", "65", "71"]:
            return "LDR"
        else:
            raise Exception, "Can't get branch of %s" % version

    #Win7
    if build in ["7600"]:
        if rev[:2] in ["14", "16", "17"]:
            return "GDR"
        elif rev[:2] in ["20", "21"]:
            return "LDR"
        else:
            raise Exception, "Can't get branch of %s" % version
    
    #
    return "GDR"

#
def getSP(sp):
    res = re.search(r'(\d+)', sp)
    if res:
        return res.group(0)
    return None

#
def parseDllInfo(infoLine, defaultArch):

    info = {}
    cols = infoLine.split()
    info["binary"] = string.upper(cols[0][1:-1])
    info["version"] = cols[1][1:-1]
    info["arch"] = getArch(cols[2][1:-1], defaultArch)
    info["branch"] = getBranch(cols[4][1:-1], info["version"])
    info["sp"] = getSP(cols[3][1:-1])

    return info

#
def slurpBulletins(bFile):

    bullID = None
    pInfo = None
    curBull = []
    bulletins = {}
    f = open(bFile, "r")

    #
    for line in f:

        #
        if string.find(line, "-[Retrieving file") != -1:
            bullID = line[string.find(line, "MS"):].strip()
        elif string.find(line, "--[Parsing KB") != -1 or len(line) < 10:
            continue
        elif string.find(line, "##################") != -1:
            bulletins[bullID] = curBull
            curBull = []
        elif line[0] == "[":
            pInfo = appParse.parseProdDesc(line[1:-2])
        elif line[0] == "+" or len(line) < 5:
            continue
        elif line[:2] != "|-" and string.find(line, "File name") == -1:
            try:
                dll = parseDllInfo(line[1:-2], pInfo[0])
            except Exception as err:
                print "Error parsing bulletin %s [%s]" % (bullID, err)
                sys.exit(1)

            dll["bulletin"] = bullID
            dll["target"] = pInfo
            curBull.append(dll)

    return bulletins

#
def usage(prog):
    print ("Usage: %s [ -g generate [bulletin file] ] [ -m manual update [bulletin file] ]\n"
            "\t<-d database file (default patch-info.db)> <-u automatically update db>" % (prog)
            )
    sys.exit(1)

#
if __name__ == "__main__":

    #
    bFile = None
    autoUpdate = doUpdate = False
    dbFile = "patch-info.db"

    #
    try:
        opts, args = getopt.getopt(sys.argv[1:], "g:m:d:u")
    except getopt.GetoptError, err:
        print str(err)
        usage(sys.argv[0])

    for o, a in opts:
        if o == "-g":
            bFile = a
        elif o == "-m":
            bFile = a
            doUpdate = True
        elif o == "-d":
            dbFile = a
        elif o == "-u":
            autoUpdate = True
        else:
            usage(sys.argv[0])

    if not bFile and not autoUpdate:
        usage(sys.argv[0])

    #backup the old DB file
    try:
        shutil.copyfile(dbFile, dbFile + ".bak")
    except IOError:
        pass
    
    dbh = shelve.open(dbFile)

    if doUpdate or autoUpdate:
        dllDict = dbh ["data"]
        print "Updating existing database %s" % (dbFile)
    else:
        dllDict = {}
        print "Creating new database %s" % (dbFile)
    
    #determine the most recent bulletin in the db, compare to most recent on ms site
    if autoUpdate:
        cur = queryMSDB.getLastBulletin(dllDict)
        patchInfo = msPatchInfo.msPatchFileInfo()
        latest = patchInfo.queryMostRecent()
        curYear = int(cur[2:4])
        curNum = int(cur[5:8])
        latestYear = int(latest[2:4])
        latestNum = int(latest[5:8], 10)
        
        if curYear < latestYear:
            print "Sorry, I can't update from last year automatically (cur %d, latest %d)" % (curYear, latestYear)
            sys.exit(0)

        if curNum == latestNum:
            print "Patch DB is all up to date (%d-%d is most recent)" % (latestYear, latestNum)
            sys.exit(0)

        print "Updating database from %d-%d to %d-%d" % (curYear, curNum, latestYear, latestNum)

        #ok, we need to update some bulletins, let's do it
        bFile = "bulletinInfo.txt"
        f = open(bFile, "wb")
        for n in xrange(curNum + 1, latestNum + 1):
            f.write("-[Retrieving file information for bulletin MS%.2d-%.3d\n" % (curYear, n))
            bInfo = patchInfo.getBulletinFileInfo(curYear, n)
            text = patchInfo.generateOutput(bInfo)
            f.write(text)
        f.close()

    bulletins= slurpBulletins(bFile)

    for (bID, dllList) in bulletins.items():

        for dll in dllList:
            entry = dllDict.setdefault(dll["binary"], [])
            entry.append(dll)

    dbh["data"] = dllDict

    dbh.close()

    #we created it, so delete it
    if autoUpdate:
        os.remove(bFile)
