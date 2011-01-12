#!/bin/bash

#
baseYear=5
declare -a maxBulletinIDs=(55 78 69 78 74 106)

#
curYear=$baseYear
for maxID in ${maxBulletinIDs[@]}
do
    let outFile=$curYear+2000
    rm -f $outFile

    echo "Getting bulletins for $outFile 1 - $maxID..."
    for id in `seq 1 $maxID`
    do
        ./msPatchInfo.py $curYear $id >>$outFile
    done
    let curYear=$curYear+1
done

#create the file with all years bulletins
cat 20* > all-years

echo "All bulletins stored in all-years file"
echo "Now run ./genMsFileInfoDb.py all-years"

####
## max bulletin ids by year. in 2005 the format changed substantially from before
## in 2008 it changed again
#2010: 1 - 106
#2009: 1 - 74
#2008: 1 - 78
#2007: 1 - 69
#2006: 1 - 78
#2005: 1 - 55
#***
#2004: 1 - 45
#2003: 1 - 51
#2002: 1 - 72
#2001: 1 - 60
#2000: 1 - 100
