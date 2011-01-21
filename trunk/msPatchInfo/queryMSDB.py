#!/usr/bin/python
#
import getopt
import re
import string
import sys
import appParse
import shelve


# pretty print an OS/APP token
def printTok(tok):
    tMap = {appParse.TPROPER:"PROPER", appParse.TARCH:"ARCH", appParse.TPUNC:"PUNC", appParse.TPREP:"PREP", appParse.TCONJ:"CONJ",
            appParse.TNUM:"NUM", appParse.TUNKNOWN:"UNKNOWN", appParse.TPROPER_SP:"SP", appParse.TPROPER_APP:"APP",
            appParse.TPROPER_OS:"OS"}
    tType = tMap[tok[0]]
    tVal = tok[1]

    #
    if isinstance(tVal, str):
        print "|---[%s, %s]" % (tType, tVal)
    elif isinstance(tVal, list):
        tStr = ""
        for t in tVal:
            tStr += t + " "
        print "|---[%s, %s]" % (tType, tStr)

# print a list of OS/APP tokens
def printToks(toks):
    for tok in toks:
        printTok(tok)

#
def usage(prog):
    print "Usage %s [ -d bulletin db ] [ -f binary ] < -v version regex > < -s service pack regex >\n" \
            "\t< -p product regex > < -b branch regex (GDR/QFE/LDR)(default GDR) > < -a x86/x64/ia64 (default x86) >\n" \
            "\t< -u sort by bulletin id instead of dll version > < -y verbose >\n" % (prog)
    sys.exit(1)

#compare two DLL/EXE version strings
def verSort(l, r):

    lV = l["version"].split(".")
    nl = len(lV)
    rV = r["version"].split(".")
    nr = len(rV)

    for i in xrange(0, min(nr, nl)):
        l = int(lV[i])
        r = int(rV[i])

        if l > r:
            return 1
        elif r > l:
            return -1
 
    if nl > nr:
        return 1
    elif nr > nl:
        return -1

    #equal
    return 0


#
def prodFilter(dlls, pRegEx):
    
    ret = []
    for dll in dlls:

        pInfo = dll["target"][1]

        #pInfo contains a list of (TYPE,VAL) tuples
        #(TPROPER_APP, "Windows XP")...
        res = filter(lambda tup: re.search(pRegEx, tup[1]) is not None, pInfo)
        if res:
            ret.append(dll)

    return ret

#
if __name__ == "__main__":

    #
    qBinary,qVers,qSP,qProd= None,None,None,None
    dbFile = "patch-info.db"
    qArch = "x86"
    qBranch = "GDR"
    bSort = False
    verbose = False

    #
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:f:v:s:p:b:a:uy")
    except getopt.GetoptError, err:
        print str(err)
        usage(sys.argv[0])

    for o, a in opts:

        if o == "-d":
            dbFile = a
        elif o == "-f":
            qBinary = string.upper(a)
        elif o == "-v":
            qVers = a
        elif o == "-s":
            qSP = a
        elif o == "-p":
            qProd = a
        elif o == "-b":
            qBranch = a
        elif o == "-a":
            if a not in ["x86", "x64", "ia64", "."]:
                usage(sys.argv[0])
            qArch = a
        elif o == "-u":
            bSort = True
        elif o == "-y":
            verbose = True
        else:
            usage(sys.argv[0])

    if not qBinary:
        usage(sys.argv[0])
    
    print "-{Querying db %s...\n" % (dbFile)
    
    #lookup the version structure list for the given binary
    msDB = shelve.open(dbFile)
    dllDict = msDB["data"]
    msDB.close()
    
    #find the target binary
    try:
        res = dllDict[qBinary]
    except KeyError:
        print "No entry for %s" % qBinary
        sys.exit(1)

    #architecture filter, default x86
    #this also filters the targets, as there can be x86 binary on x64 OS
    res = filter(lambda v: re.search(qArch, v["arch"]), res)
    res = filter(lambda v: re.search(qArch, v["target"][0]), res)
    
    #gdr/qfe filter, default to GDR
    res = filter(lambda v: v["branch"] and re.search(qBranch, v["branch"]), res)
    
    #version filter
    if qVers:
        res = filter(lambda v: re.search(qVers, v["version"]), res)
    
    #SP filter
    if qSP:
        res = filter(lambda v: v["sp"] and re.search(qSP, v["sp"]), res)

    #product name filter
    if qProd:
        res = prodFilter(res, qProd)

    #sort by version or bulletin
    if bSort:

        #turn the MSXX-YYY into an integer for sorting purposes
        res = sorted(res, key=lambda b:int(b["bulletin"][2:4])*1000 + int(b["bulletin"][5:]))
        
        #subsort by version
        out = []
        cur = []
        bul = res[0]["bulletin"]
        for r in res:
            if r["bulletin"] == bul:
                cur.append(r)
            else:
                cur = sorted(cur, cmp=verSort)
                out.extend(cur)
                cur = []
                bul = r["bulletin"]
                cur.append(r)

        #
        if cur:
            cur = sorted(cur, cmp=verSort)
            out.extend(cur)

        res = out
    else:
        res = sorted(res, cmp=verSort)
    
    curBull = None
    for dll in res:

        #
        if dll["bulletin"] != curBull:

            #print bulletin header
            print "+\n+\n+++ %s +++\n+" % (dll["bulletin"])
            curBull = dll["bulletin"]
            print "|--[%s %s (%s/%s)" % (dll["binary"], dll["version"], dll["arch"], dll["target"][0])
        else:
            print "|--[%s %s (%s/%s)" % (dll["binary"], dll["version"], dll["arch"], dll["target"][0])
        
        if verbose:
            if dll["sp"]:
                print "|---[SP level %s" % dll["sp"]
            print "|---[Branch %s" % dll["branch"]
            printToks(dll["target"][1])

