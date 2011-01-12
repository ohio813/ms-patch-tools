#!/bin/bash
#

cabExtract="/cygdrive/c/WINDOWS/system32/expand.exe"
tmpDir="output.tmp"
tmpDir2="output2.tmp"
outputDir="patch-files"
patchCab=""
dName=`dirname $0`

fName=$1
ext=${fName#*.}

#
if [ $# -ne 1 ]
then
    echo "Usage: `basename $0` [.msu file]"
    exit 1
fi

echo "Extracting file $fName..."
rm -rf $tmpDir $tmpDir2 $outputDir

#create the first output directory
mkdir $tmpDir
mkdir $outputDir

#extract the patch
$cabExtract -F:* $fName $tmpDir >/dev/null

#find the patch CAB
for i in $tmpDir/*.[cC][aA][bB]
do
	if ! [[ "`basename $i`" =~ "WSUS" ]]
	then
		patchCab=$i
		break
	fi
done

#extract patch
echo "Patch cab is $patchCab"

mkdir $tmpDir2
$cabExtract -F:* $patchCab $tmpDir2 > /dev/null

#find all DLLS
for i in `find $tmpDir2`
do
    if [ -f $i ]
    then

        #test if it's a PE file
        file "$i" | grep PE > /dev/null

        if [ $? -eq 0 ]
        then
            #it's a PEfile, get the version # and create the output file
            fName=`basename $i`
            fVers="`$dName/dllVers.py $i`"
            echo "Creating $outputDir/$fName.$fVers"
            cp $i "$outputDir/$fName.$fVers"
        fi
    fi
done

#clean up
rm -rf $tmpDir $tmpDir2
