#brief demos of tools

# msux #

This is pretty self-explanatory:

./msux.sh<br />
Usage: msux.sh `[`.msu file`]`<br />
./msux.sh Windows6.0-KB979559-x86.msu<br />
Extracting file Windows6.0-KB979559-x86.msu...<br />
Patch cab is output.tmp/Windows6.0-KB979559-x86.cab<br />
Creating patch-files/win32k.sys.6.0.6001.18468<br />
Creating patch-files/win32k.sys.6.0.6001.22682<br />
Creating patch-files/win32k.sys.6.0.6002.18253<br />
Creating patch-files/win32k.sys.6.0.6002.22396<br />
ll patch-files/<br />
total 7976<br />
-rwxr-xr-x 1 user None 2036224 Jan 11 23:01 win32k.sys.6.0.6001.18468<br />
-rwxr-xr-x 1 user None 2036736 Jan 11 23:01 win32k.sys.6.0.6001.22682<br />
-rwxr-xr-x 1 user None 2037248 Jan 11 23:01 win32k.sys.6.0.6002.18253<br />
-rwxr-xr-x 1 user None 2045440 Jan 11 23:02 win32k.sys.6.0.6002.22396<br />


# msPatchInfo #

This consists of several python scripts used to build, update, and query the database of file version information. The database itself is simply a python 'shelve' file. We'll start with the query interface, and then discuss the other scripts after.

**queryMSDB.py** - is what you think it is. It works like this:

Usage ./queryMSDB.py `[`-d bulletin db `]` `[` -f binary `]` < -v version regex > < -s service pack regex >
> < -p product regex > < -b branch regex (GDR/QFE/LDR) > < -a x86/x64/ia64 (default x86) > <br />
> < -u sort by bulletin id instead of dll version > < -y verbose >
<pre>
./queryMSDB.py -f mshtml.dll -v "8\.0" -u -p "XP"<br>
-{Querying db patch-info.db...<br>
<br>
+<br>
+<br>
+++ MS08-078 +++<br>
+<br>
|--[MSHTML.DLL 8.0.6001.18247 (x86/x86)<br>
+<br>
+<br>
+++ MS09-002 +++<br>
+<br>
|--[MSHTML.DLL 8.0.6001.18259 (x86/x86)<br>
+<br>
+<br>
+++ MS09-019 +++<br>
+<br>
|--[MSHTML.DLL 8.0.6001.18783 (x86/x86)<br>
....snip....<br>
+<br>
+<br>
+++ MS10-071 +++<br>
+<br>
|--[MSHTML.DLL 8.0.6001.18975 (x86/x86)<br>
+<br>
+<br>
+++ MS10-090 +++<br>
+<br>
|--[MSHTML.DLL 8.0.6001.18999 (x86/x86)<br>
----<br>
./queryMSDB.py -f mso.dll -v "12\.0"<br>
-{Querying db patch-info.db...<br>
<br>
+<br>
+<br>
+++ MS07-025 +++<br>
+<br>
|--[MSO.DLL 12.00.6017.5000 (x86/x86)<br>
+<br>
+<br>
+++ MS08-055 +++<br>
+<br>
|--[MSO.DLL 12.0.6320.5000 (x86/x86)<br>
+<br>
+<br>
+++ MS10-036 +++<br>
+<br>
|--[MSO.DLL 12.0.6535.5002 (x86/x86)<br>
+<br>
+<br>
+++ MS10-087 +++<br>
+<br>
|--[MSO.DLL 12.0.6545.5004 (x86/x86)<br>
</pre>

---

Currently, the database contains file version information for all bulletins from 2005-2011(January). Unfortunately though, it does **NOT** contain service pack information for any applications or operating systems. Since it works by parsing KB articles derived from bulletins, this information is not available.

**For reasons explained below, when you want to find binaries that belong to a certain version of a product you are better off using the '-v' option and specifying a regex that uses the major version of the application. For Office 2007: "-v 12\.0". The '-p' switch works well for operating systems, but not so well for applications.**

## How it works ##

Several files are used to parse bulletins and generate the database.

**msPatchInfo.py**

Usage: ./msPatchInfo.py < year > < bulletin num  >

Retrieves and parses a single bulletin, outputting it to stdout in text based format. It's typically used like this to retrieve a bunch of bulletins for further parsing:

for i in `````seq 1 74`````; do ./msPatchInfo.py 9 $i >> 2009; done

**genMsFileInfoDb.py**

Usage: ./genMsFileInfoDb.py `[` -g generate `[`bulletin file`]` `]` `[` -u update `[`bulletin file`]` `]`
> < -d database file (default patch-info.db) >

This takes the output of msPatchInfo.py and uses it to generate or update the database file. For example:

./genMsFileInfoDb.py -g 2009

will create a new database, while

./genMsFileInfoDb.py -u 2009

will update the current database (patch-info.db, or -d argument).

These three scripts are all that you should need to use, but there is another script used by genMsFileInfoDb.py that deserves a few words.

**appParse.py**

A library used to perform fuzzy string matching on product/os strings parsed from the bulletin file information. Microsoft is terribly inconsistent with their naming scheme in the file version tables, and there are often misspellings and formatting errors that make matching up application/os tags really ugly. The approach I took was a list of operating systems and applications gathered from Microsoft's bulletin search page combined with a list of my own. The matching uses python's difflib, with varying degrees of success. Unfortunately, it's far from perfect for applications. However, for operating systems it works quite well. From a practical standpoint, this means that when you use the '-p' tag to search for a specific product you're gambling a bit. For this reason, I prefer to use '-v' to specify a regex for the DLL/EXE version. So, for IE8/mshtml.dll, '-v 8\.0'. This will work 99% of the time, while searching for "Internet Explorer 8" is liable to miss or match incorrectly. Unfortunately the data set is pretty terrible (and apparently largely generated by hand).

## Building and updating the DB ##

### building ###
You can use the patch-info.db file provided in the release, or you can build your own database. Assuming you want to start from scratch:

./getAllBulletins.sh

./genMsFileInfoDb.py -g all-years

./queryMSDB.py [bla](bla.md)

### updating ###
Assuming you have to add the patches for January 2011, updating can be done as follows.

./msPatchInfo.py 11 1 > log

./msPatchInfo.py 11 2 >> log

./genMsFileInfoDb.py -u log

## TODO ##

Service packs for popular applications and for operating systems need to be added.

appParse.py needs to perform better