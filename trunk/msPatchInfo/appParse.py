#!/usr/bin/python

import re
import sys
import string
import difflib

#
msAppList = [
"Office 2007",
".Net Framework 1.0",
".Net Framework 1.1",
".Net Framework 2.0",
".Net Framework 3.5",
".NET Framework 3.5.1",
".Net Framework 4.0",
#"Acceleration Server 2006",
"Access 2000",
"Access 2000 Runtime",
"Access 2002",
"Access 2003",
"Access 2007",
"Access 97",
"BackOffice Resource Kit SE",
"BackOffice Server 2000",
"BackOffice Server 4.0",
"BizTalk Server 2000",
"BizTalk Server 2002",
"BizTalk Server 2004",
"CAPICOM",
"Commerce Server 2000",
"Commerce Server 2002",
"Content Management Server 2001",
"Content Management Server 2002",
"Digital Image Suite 2006",
"Entourage 2001 for Macintosh",
"Entourage v. X for Macintosh",
"Excel 2000",
"Excel 2001 for Macintosh",
"Excel 2002",
"Excel 2003",
"Excel 2004 for Macintosh",
"Excel 2007",
"Excel 97",
"Excel v. X for Macintosh",
"Excel Viewer 2003",
"Excel Viewer 2007",
"Exchange 2000 Enterprise Server",
"Exchange 2000 Server",
"Exchange Server 2003",
"Exchange Server 2007",
"Exchange Server 2010",
"Exchange Server 5.0",
"Exchange Server 5.5",
"Expression Web",
"Expression Web 2",
"Forefront Client Security",
"Forefront Threat Management Gateway Med Bus Edition",
"Forefront UAG 2010",
"FrontPage 2000",
"FrontPage 2000 Server Extensions",
"FrontPage 2002",
"FrontPage 2003",
"FrontPage 97",
"FrontPage 97 Personal Web Server 1.0",
"FrontPage 97 Server Extensions",
"FrontPage 98",
"FrontPage 98 Personal Web Server 1.0",
"FrontPage 98 Server Extensions",
"FrontPage Server Extensions 2000 64-bit",
"FrontPage Server Extensions 2002",
"FrontPage Server Extensions 2002 64-bit",
"Greetings 2000",
"Home Publishing 2000",
"Host Integration Server 2000",
"Host Integration Server 2004",
"Host Integration Server 2006",
"Hyper-V Server 2008",
"IE 5.1 for Macintosh",
"Index Server 2.0",
"Indexing Service for Windows 2000",
"InfoPath 2003",
"InfoPath 2007",
"Interix 2.2",
"Internet Explorer 4.0",
"Internet Explorer 4.01",
"Internet Explorer 4.5 for Macintosh",
"Internet Explorer 5",
"Internet Explorer 5.01",
"Internet Explorer 5.01 on Windows 2000 Service Pack 4",
"Internet Explorer 5.1 for Machintosh OS 8 and 9",
"Internet Explorer 5.1 for Macintosh OS X",
"Internet Explorer 5.5",
"Internet Explorer 6 for Windows 2000 Service Pack 4",
"Internet Explorer 6 for Windows Server 2003 for Itanium-based Systems",
"Internet Explorer 6 for Windows Server 2003 x64 Edition",
"Internet Explorer 6 for Windows XP 64-Bit Edition Version 2003",
"Internet Explorer 6 for Windows XP Professional x64 Edition",
"Internet Explorer 6.0",
"Internet Explorer 6.0 for Windows Server 2003",
"Internet Explorer 6.0 for Windows XP Service Pack 2",
"Internet Explorer 6.0 for Windows XP SP1",
"Internet Explorer 6.0 for Windows XP SP3",
"Internet Explorer 7 for Windows Server 2003 for Itanium",
"Internet Explorer 7 for Windows Server 2003 x64 Edition",
"Internet Explorer 7 for Windows XP SP3",
"Internet Explorer 7.0",
"Internet Explorer 7.0 for Windows Server 2003",
"Internet Explorer 7.0 for Windows Server 2008",
"Internet Explorer 7.0 for Windows Server 2008 for Itanium-Based Systems",
"Internet Explorer 7.0 for Windows Server 2008 x64",
"Internet Explorer 7.0 for Windows Vista",
"Internet Explorer 7.0 for Windows Vista x64",
"Internet Explorer 7.0 for Windows XP Professional x64 Edition",
"Internet Explorer 7.0 for Windows XP Service Pack 2",
"Internet Explorer 7.0 for Windows XP Service Pack 3",
"Internet Explorer 8 for Windows Server",
"Internet Explorer 8.0 for Windows",
"Internet Information Server 3.0",
"Internet Information Server 4.0",
"Internet Information Services 5.0",
"Internet Information Services 5.1",
"Internet Information Services 6.0",
"Internet Information Services 7.0",
"Internet Information Services 7.5",
"ISA Server 2000",
"ISA Server 2004 Enterprise Edition",
"ISA Server 2004 Standard Edition",
"ISA Server 2006 Enterprise Edition",
"ISA Server 2006 Standard Edition",
"MDAC 2.1",
"MDAC 2.5",
"MDAC 2.6",
"MDAC 2.7",
"MDAC 2.8",
"Antigen for Exchange",
"Antigen for SMTP Gateway",
"Business Solutions CRM",
"Commercial Internet System 2.0",
"Commercial Internet System 2.5",
"Data Engine (MSDE)",
"Forefront Security for Exchange",
"Forefront Security for Sharepoint",
"Global Input Method Editor for Office 2000 (Japanese)",
"Interactive Training (Step-by-Step)",
"Learning Essentials 1.0, 1.1, and 1.5 for Office",
"Metadirectory Services 2.2",
"Office 2000 Multilanguage Packs",
"Office Compatibility Pack for Word, Excel, and PowerPoint 2007 File Formats",
"Office Converter Pack",
"Office Excel Viewer",
"Office Word Viewer",
"Producer 2003",
"Routing and Remote Access Server for Windows NT 4.0",
"SharePoint Foundation 2010",
"Silverlight 2.0 on Mac",
"Silverlight 2.0 on Windows Client",
"Silverlight 2.0 on Windows Server",
"Silverlight 3.0 on Mac",
"Silverlight 3.0 on Windows Client",
"Silverlight 3.0 on Windows Servers",
"SQL Server 2000 Desktop Engine (MSDE 2000)",
"Terminal Services Advanced Client (TSAC) ActiveX control",
"Virtual Machine (VM)",
"Virtual PC 2004",
"Virtual PC 2007",
"Virtual PC for Mac 6.0",
"Virtual PC for Mac 6.01",
"Virtual PC for Mac 6.02",
"Virtual PC for Mac 6.1",
"Virtual PC for Mac Version 7",
"Virtual Server 2005 Enterprise Edition",
"Virtual Server 2005 R2 Enterprise Edition",
"Virtual Server 2005 R2 Standard Edition",
"Virtual Server 2005 Standard Edition",
"Virtual Server 2005",
"Windows Defender x64 Edition",
"XML Core Services 3.0",
"XML Core Services 4.0",
"XML Core Services 5.0",
"XML Core Services 6.0",
"Money 2000",
"Money 2001",
"MSN Messenger 6",
"MSN Messenger 6.2",
"MSN Messenger 7",
"MSN Messenger 7.0",
"MSN Messenger 7.5",
"NetMeeting",
"Office 2000",
"Office 2001 for Macintosh",
"Office 2003",
"Office 2003 Web Components",
"Office 2004 for Macintosh",
"Office 2008 for Macintosh",
"Office 2010",
"Office 2010 x64",
"Office 2011 for Mac",
"Office 95",
"Office 97",
"Office 98 for Macintosh",
"Office Excel Viewer 2007",
"Office Groove Server 2007",
"Office Groove Server 2010",
"Office SharePoint Designer 2007",
"Office SharePoint Server 2007",
"Office SharePoint Server 2007 x64 Edition",
"Office Small Business Accounting 2006",
"Office System 2007",
"Office v. X for Macintosh",
"Office Visio 2003 Viewer",
"Office Web Applications",
"Office Web Components 2000",
"Office Web Components 2002",
"Office XP",
"OneNote 2003",
"OneNote 2007",
"Open XML File Format Converter for Mac",
"Outlook 2000",
"Outlook 2002",
"Outlook 2003",
"Outlook 2007",
"Outlook 98",
"Outlook Express 4.01",
"Outlook Express 5 for Macintosh",
"Outlook Express 5.01",
"Outlook Express 5.5",
"Outlook Express 5.5 on Windows 2000 sp4",
"Outlook Express 6 for Windows Server 2003 for Itanium-based Systems",
"Outlook Express 6 for Windows XP 64-Bit Edition",
"Outlook Express 6 for Windows XP 64-Bit Edition Version 2003",
"Outlook Express 6 on Windows XP",
"Outlook Express 6 on Windows 2000 sp4",
"Outlook Express 6 on Windows Server 2003",
"Outlook Express 6 on Windows Server 2003 (64 bit edition)",
"Outlook Express 6.0",
"Personal Web Server 4.0",
"Photo Draw 2000 Version 1",
"Photo Draw 2000 Version 2",
"PictureIt 2000",
"Platform SDK Redistributable: GDI+",
"Platform SDK Redistrubutable: CAPICOM",
"PowerPoint 2000",
"PowerPoint 2001 for Macintosh",
"PowerPoint 2002",
"PowerPoint 2003",
"PowerPoint 2003 Viewer",
"PowerPoint 2004 for Mac",
"PowerPoint 2007",
"PowerPoint 2007 Viewer",
"PowerPoint 97",
"PowerPoint 98",
"PowerPoint 98 for Macintosh",
"PowerPoint v. X for Macintosh",
"Project 2000",
"Project 2002",
"Project 2003",
"Project 2007",
"Project 98",
"Project Server 2002",
"Proxy Server 2.0",
"Publisher 2000",
"Publisher 2002",
"Publisher 2003",
"Publisher 2007",
"Publisher 99",
"Report Viewer 2005 Redistributable Package",
"Report Viewer 2008 Redistributable Package",
"Search Server 2008",
"Services for Unix 2.0 (NT)",
"Services for Unix 2.0 (Win2K)",
"Services For Unix 2.1",
"Services For Unix 2.2",
"Services For Unix 3.0",
"Services For Unix 3.5",
"SharePoint Team Services 2002",
"Site Server 3.0",
"Site Server 3.0, Commerce Edition",
"SQL Server 2000",
"SQL Server 2000 Reporting Services",
"SQL Server 2005",
"SQL Server 2005 Express Edition",
"SQL Server 2005 for Itanium Systems",
"SQL Server 2005 x64 Edition",
"SQL Server 7.0",
"Systems Management Server 1.2",
"Systems Management Server 2.0",
"VBA 5.0",
"VBA 6.0",
"VBA 6.2",
"VBA 6.3",
"VBA 6.4",
"Visio 2000",
"Visio 2002",
"Visio 2003",
"Visio 2007",
"Visio Enterprise Architects 2003",
"Visio Viewer 2002",
"Visio Viewer 2007",
"Visual Basic 5.0",
"Visual Basic 6.0",
"Visual FoxPro 6.0",
"Visual FoxPro 8.0",
"Visual FoxPro 9.0",
"Visual Studio .NET 2002",
"Visual Studio .NET 2002 Academic Edition",
"Visual Studio .NET 2002 Enterprise Architext",
"Visual Studio .NET 2002 Enterprise Developer",
"Visual Studio .NET 2002 SP1",
"Visual Studio .NET 2003",
"Visual Studio .NET 2003 Enterprise Architect",
"Visual Studio .NET 2003 Enterprise Developer",
"Visual Studio 2005",
"Visual Studio 2005 Standard Edition",
"Visual Studio 2005 Team Edition for Architects",
"Visual Studio 2005 Team Edition for Developers",
"Visual Studio 2005 Team Edition for Testers",
"Visual Studio 2005 Team Suite",
"Visual Studio 2008",
"Visual Studio 6.0",
"Windows Defender",
"Windows Embedded Standard 7 for  x64-based",
"Windows Live Mail",
"Windows Live Messenger 8.0",
"Windows Live OneCare",
"Windows Mail",
"Windows Mail for Windows Vista",
"Windows Mail for Windows Vista x64 Edition",
"Windows Media Encoder 4.0",
"Windows Media Encoder 4.1",
"Windows Media Encoder 9 Series",
"Windows Media Encoder 9 Series x64 Edition",
"Windows Media Format 7.1 Runtime",
"Windows Format Media Runtime 9",
"Windows Media Format Runtime 9.0",
"Windows Media Format Runtime 9.5",
"Windows Media Format 11 Runtime",
"Windows Media Player 10",
"Windows Media Player 10",
"Windows Media Player 11",
"Windows Media Player 12",
"Windows Media Player 6.4",
"Windows Media Player 6.4 for Windows 2000",
"Windows Media Player 6.4 for Windows NT 4.0",
"Windows Media Player 7.0",
"Windows Media Player 7.1",
"Windows Media Player 9 for Windows Server 2003",
"Windows Media Player 9 for Windows XP",
"Windows Media Player 9.0",
"Windows Media Player for Windows XP",
"Windows Media Rights Manager 1",
"Windows Media Services 2008",
"Windows Media Services 4.0",
"Windows Media Services 4.1",
"Windows Media Services 9",
"Windows Messenger 4.7",
"Windows Messenger 5.x",
"Windows Script 5.1",
"Windows Script 5.5",
"Windows SharePoint Services 3.0",
"Word 2000",
"Word 2001 for Macintosh",
"Word 2002",
"Word 2003",
"Word 2007",
"Word 2010",
"Word 2010 x64",
"Word 97",
"Word 98",
"Word 98 for Macintosh",
"Word v. X for Macintosh",
"Word Viewer 2003",
"Word Web Application",
"Works 2000",
"Works 2001",
"Works 2002",
"Works 2003",
"Works 2004",
"Works 2005",
"Works 2006",
"Works 8",
"Works 8.5",
"Works 9",
]

#
stickyWords = [
"+",
".NET",
"Acceleration",
"Access",
"Accounting",
"ActiveX",
"Administrator",
"Basic",
"Business",
"C++",
"Center",
"Client",
"Collaboration",
"Compatibility",
"Components",
"Converter",
"DHTML",
"DNS",
"Data",
"Database",
"Desktop",
"Digital",
"DirectX",
"DirectX8.1",
"DirectX9.0",
"Edition",
"Encoder",
"Engine",
"Enterprise",
"Excel",
"Exchange",
"Explorer",
"Express",
"Extended",
"File",
"Files",
"Forefront",
"Format",
"Formats",
"Foundation",
"FoxPro",
"Framework",
"GDI",
"GDR",
"Gateway",
"Gpfilt.msp:",
"Gpflt.msp:",
"Host",
"Hyper-V",
"ISA",
"Image",
"InfoPath",
"Integration",
"Internal",
"Internet",
"JScript",
"MAPI",
"Maker",
"Management",
"Media",
"Medium",
"Microsoft",
"Movie",
"Msconv.msp",
"Objects",
"Ocpgpflt.msp",
"Office",
"OneNote",
"Outlook",
"PC",
"Pack",
"pack",
"Package",
"Player",
"PowerPoint",
"Pre-Beta",
"Professional",
"Project",
"Publisher",
"Quartz",
"R2",
"Redistributable",
"Report",
"Reporting",
"Rollup",
"Runtime",
"SP1",
"SP2",
"SP3",
"SP4",
"SQL",
"Search",
"Security",
"Series",
"Server",
"Server2003",
"Service",
"service",
"Services",
"SharePoint",
"Small",
"Snapshot",
"Standard",
"Studio",
"Suite",
"Supportability",
"Systems",
"Threat",
"Viewer",
"Virtual",
"Visio",
"Vista",
"Visual",
"WINS",
"WOW",
"Web",
"Windows",
"Word",
"Works",
"WYukon",
"XP",
"server",
"client",
]

#
x86 = ["x86", "x86-based", "32-bit"]
x64 = ["x64", "x64-based", "64-bit"]
itanium = ["itanium", "ia64", "ia64-based", "ia-based", "IA-64", "IA-64-based", "Itanium-based"]

puncs = [ ",", ";"]

preps = ["for", "in", "of", "on", "with" ]

conjs = ["and", "or"]

#token types

TPROPER = 0
TPROPER_SP = -1
TPROPER_OS = -2
TPROPER_APP = -3
TARCH = 1
TPUNC = 2
TPREP = 3
TCONJ = 4
TNUM = 5
TUNKNOWN = 6

#app/os

os = [
        "Windows 2000", "Windows 2000 Server", "Windows 7", "Windows 95", "Windows 98", "Windows 98 SE", "Windows Me",
        "Windows NT", "Windows Server 2003", "Windows Server 2003 R2", "Windows Server 2008", "Windows Server 2008 R2",
        "Windows Vista", "Windows XP", "Windows XP Professional", "Windows XP Media Center Edition",
        "Windows XP Tablet PC Edition","Windows XP Home Edition",
        "Windows Server 2003 Enterprise Edition", "Windows Server 2003 Standard Edition", "Windows 2003",
        "Windows NT Server 4.0", "Windows NT Server 4.0 Terminal Server Edition",
        "Windows Millennium Edition",
        "Windows 98 Second Edition SE",
        ]

win95 = ["Windows 95"]
win98 = ["Windows 98", "Windows 98 SE", "Windows 98 Second Edition"]
winMe = ["Windows Me", "Windows Millennium Edition"]
winNT = ["Windows NT Server 4.0", "Windows NT Server 4.0 Terminal Server Edition",
         "Windows NT Workstation 4.0"]

win2k = [   "Windows 2000", "Windows 2000 Advanced Server", "Windows 2000 Datacenter Server",
            "Windows 2000 Professional", "Windows 2000 Server", "Windows Server 2000",
            "Windows Small Business Server 2000",
            "Small Business Server 2000",
        ]

winXP = [
"Windows XP",
"Windows XP Home Edition",
"Windows XP Media Center Edition 2002",
"Windows XP Media Center Edition",
"Windows XP Media Center Edition 2005",
"Windows XP Professional",
"Windows XP Tablet PC Edition",
"Windows XP Tablet PC Edition 2005",
        ]

win2k3 = [
"Windows 2003",
"Windows Server 2003",
"Windows Server 2003 R2",
"Windows Server 2003 Datacenter Edition",
"Windows Server 2003 Enterprise Edition",
"Windows Server 2003 for Small Business Server",
"Windows Server 2003 Standard Edition",
"Windows Server 2003 Web Edition",
"Windows Small Business Server 2003",
"Windows Small Business Server 2003 R2",
        ]

vista = ["Windows Vista", "Windows Vista Business", "Windows Vista Enterprise", "Windows Vista Home Basic",
         "Windows Vista Home Premium", "Windows Vista Starter", "Windows Vista Ultimate"
        ]

win7 = [ "Windows 7"
        ]

win2k8 = [ "Windows Server 2008", "Windows Server 2008 R2"
        ]


# a simple lexer for MS bulletin product descriptions
class msLexer:

    #
    def __init__(self, words):
        self.words = words
        self.archs = [string.upper(a) for a in x86] + \
                    [string.upper(a) for a in x64] + \
                    [string.upper(a) for a in itanium]
        return

    #
    def isProper(self, word):
        return word in stickyWords or (word[0].isupper() and word not in ["Additional", "All", "For"])

    #
    def isArch(self, word):
        return string.upper(word) in self.archs

    #
    def isPunc(self, word):
        return word in puncs

    #
    def isPrep(self, word):
        return word in preps

    #
    def isConj(self, word):
        return word in conjs

    #
    def isNum(self, word):
        return re.match("\d+", word) is not None

    # returns a set of tokens, [(TYPE,VAL),..]
    def lex(self):

        toks = []

        #
        for w in self.words:

            cur = None

            #
            if self.isArch(w):
                cur = (TARCH, w)
            elif self.isPunc(w):
                cur = (TPUNC, w)
            elif self.isPrep(w):
                cur = (TPREP, w)
            elif self.isConj(w):
                cur = (TCONJ, w)
            elif self.isNum(w):
                cur = (TNUM, w)
            elif self.isProper(w):
                cur = (TPROPER, w)
            else:
                cur = (TUNKNOWN, w)

            #
            if cur is not None:
                toks.append(cur)

        return toks


#
def printTok(tok):
    tMap = {TPROPER:"PROPER", TARCH:"ARCH", TPUNC:"PUNC", TPREP:"PREP", TCONJ:"CONJ",
            TNUM:"NUM", TUNKNOWN:"UNKNOWN", TPROPER_SP:"TPROPER_SP", TPROPER_APP:"TPROPER_APP",
            TPROPER_OS:"TPROPER_OS"}
    tType = tMap[tok[0]]
    tVal = tok[1]

    #
    if isinstance(tVal, str):
        print "Token [%s, %s]" % (tType, tVal)
    elif isinstance(tVal, list):
        tStr = ""
        for t in tVal:
            tStr += t + " "
        print "Token [%s, %s]" % (tType, tStr)

#
def printToks(toks):
    for tok in toks:
        printTok(tok)

####
class msParser:

    #
    def __init__(self, toks, orig=None, dbg=False):
        self.orig = orig
        self.tokens = toks
        self.osList = win95 + win98 + winMe + winNT + win2k + winXP + win2k3 + vista + win7 + win2k8
        self.doDbg = dbg
        self.a_x86 = [string.upper(a) for a in x86]
        self.a_x64 = [string.upper(a) for a in x64]
        self.a_ia64 = [string.upper(a) for a in itanium]
        return

    #
    def pTok(self, tok):
        printTok(tok)

    #
    def dbg(self, toks, msg, prefix="#"):

        if not self.doDbg:
            return

        print prefix * 20
        print "%s: [%s]" % (msg, self.orig)

        for t in toks:
            self.pTok(t)

    #
    def extractSP(self, tok):
        toks = []
        sp = None
        state = 0

        for t in tok:
            
            #
            tOrig = t
            t = string.upper(t)

            if t == "SERVICE":
                state = 1
            elif state == 1 and (t == "PACK" or t == "SP"):
                state = 2
            elif state == 0 and (re.match("SP\d+", t, re.I)):
                state = 0
                sp = t[2:]
            elif state == 2 and re.match("^\d+$", t):
                sp = t
                state = 0
            elif state == 0 and tOrig != " ":
                toks.append(tOrig)
        
        return (toks, sp)

    #
    def matchOS(self, text):

        match = difflib.get_close_matches(text, self.osList, 1, .9)
        if len(match) > 0:
            return match[0]
        else:
            return None

    #
    def matchApp(self, text):

        match = difflib.get_close_matches(text, msAppList, 1, .7)
        if len(match) > 0:
            return match[0]
        else:
            return None

    #
    def normalizeArch(self, arch):
        if string.upper(arch) in self.a_x86:
            return "x86"
        elif string.upper(arch) in self.a_x64:
            return "x64"
        elif string.upper(arch) in self.a_ia64:
            return "ia64"
        else:
            return "x86"
    
    #
    def parse(self):

        arch = "x86"
        pass1 = []
        pName = []
        
        #pass 1: compact proper tokens/numbers and drop unknowns
        for tok in self.tokens:

            tType, tVal = tok

            #
            if tType == TPROPER or tType == TNUM:
                pName.append(tVal)
            elif tType == TARCH:
                arch = self.normalizeArch(tVal)
            elif tType == TPUNC or tType != TUNKNOWN:
                if pName:
                    pass1.append((TPROPER, pName))
                    pName = []
                pass1.append(tok)
        
        if pName:
            pass1.append((TPROPER, pName))
        
        #
        self.dbg(pass1, "Pass 1")

        #pass 2: extract SP, convert proper tokens into OS/APP
        pass2 = []
        for tok in pass1:

            tType, tVal = tok
            
            if tType == TPROPER:

                app, sp = self.extractSP(tVal)

                #check for app/os
                if app:
                    
                    #try and find OS or app
                    tmp = " ".join(app)

                    match = self.matchOS(tmp)
                    if match:
                        pass2.append((TPROPER_OS, [match]))
                        #pass2.append((TPROPER_OS, tup[0] + ["|", match]))
                    else:
                        match = self.matchApp(tmp)
                        if match:
                            pass2.append((TPROPER_APP, [match]))
                            #pass2.append((TPROPER_APP, tup[0] + ["|", match]))
                        else:
                            pass2.append((TPROPER_APP, app))
                     
                #check for service pack
                if sp is not None:
                    pass2.append((TPROPER_SP, sp))
                
            else:
                pass2.append(tok)

        #
        self.dbg(pass2, "Pass 2", "*")

        #pass 3: connect with app/os:sp
        #this simply skips (does not append) any 'with' in the middle of app/os and SP
        #ie, app/os WITH sp
        pass3 = []
        tLen = len(pass2)
        for i in xrange(0, tLen):

            #
            if (i > 0 and i < tLen - 1) and pass2[i][0] == TPREP and pass2[i][1] == "with":
                if (pass2[i-1][0] == TPROPER_APP or pass2[i-1][0] == TPROPER_OS) and pass2[i+1][0] == TPROPER_SP:
                    continue

            pass3.append(pass2[i])
        
        #
        self.dbg(pass3, "Pass 3", "-")

        #pass 4: final pass, assemble product/sp os/sp lists
        pass4 = []
        tLen = len(pass3)
        for i in xrange(0, tLen):

            #concatenate adjacent app/os - sp pairs into one list
            if pass3[i][0] == TPROPER_APP or pass3[i][0] == TPROPER_OS:
                if i < tLen - 1 and pass3[i+1][0] == TPROPER_SP:
                    pass4.append((pass3[i][0], pass3[i][1] + ["SP" + pass3[i+1][1]]))
                else:
                    pass4.append(pass3[i])

        self.dbg(pass4, "Pass 4", "%")

        #pass 5: unpack any list values into strings
        ret = []
        for t in pass4:

            tType, tVal = t

            #append a string as is, unpack a list of strings into one string
            if isinstance(tVal, str):
                ret.append((tType, tVal))
            elif isinstance(tVal, list):
                tStr = ""
                for t in tVal:
                    tStr += t + " "
                ret.append((tType, tStr))

        if self.doDbg:
            print "** ARCH %s" % arch

        #
        return (arch, ret)



#
def parseProdDesc(sProduct):

        #turn commas/semicolons into word delimiters
        #delete some things we want to ignore
        sProduct = string.strip(sProduct)
        sProduct = re.sub(r"[\[\]()]", "", sProduct)
        sProduct = re.sub(r",", " , ", sProduct)
        sProduct = re.sub(r";", " ; ", sProduct)
        sProduct = re.sub(r"Microsoft", "", sProduct)
        sProduct = re.sub(r"KB\d+", "", sProduct)
        
        #
        words = sProduct.split()

        lex = msLexer(words)
        toks = lex.lex()

        parse = msParser(toks, sProduct)
        return parse.parse()

###############

#

#
if __name__ == "__main__":

    #
    if len(sys.argv) < 2:
        print "Usage: %s [product file]" % sys.argv[0]
        sys.exit(1)

    f = open(sys.argv[1], "r")
    for l in f:

        #turn commas/semicolons into word delimiters
        l = string.strip(l)
        l = re.sub(r"[\[\]()]", "", l)
        l = re.sub(r",", " , ", l)
        l = re.sub(r";", " ; ", l)
        l = re.sub(r"Microsoft", "", l)
        l = re.sub(r"KB\d+", "", l)
        
        #
        words = l.split()

        lex = msLexer(words)
        toks = lex.lex()

        parse = msParser(toks, l, True)
        parse.parse()
