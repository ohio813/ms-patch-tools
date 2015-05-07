#This page contains a brief overview of the project.

# Introduction #

This project contains a couple of tools to help vulnerability researchers deal with Microsoft patch Tuesdays.

  * msux extracts patch binaries from the .msu format used on Vista/Windows7
  * msPatchInfo extracts file version information from updates

# Details #

The first tool, msux (microsoft update extractor) is quite simple, and is just a shell (cygwin) script used to extract binaries from the Vista/Windows 7 .msu patch installers. It uses the native 'expand' command and a small python script to copy any binaries the patch contains to a directory, naming each binary with it's version number.

The second tool, msPatchInfo, is used to create and maintain a query friendly database of file changes from bulletin to bulletin. Have you ever found yourself asking: "how many versions of mshtml.dll are there for IE8 on XP?"  or "I want to overwrite a function pointer in the ole32 .data segment, how often has it changed?" or "will this xchg esp, ecx in ntdll work for all XP SP3 patch levels?" and so on. This tool is meant to help answer those questions. It works by parsing the file information section in Microsoft bulletins and building a database of changes, which can be queried by a python script. See the [Demo](Demo.md) page for usage.