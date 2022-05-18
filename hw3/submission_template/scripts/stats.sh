#!/bin/bash

#define variable
tweetfile=$1

if [ $# = 1 ]; then # check if user has input the correct # of arguments
    if [ -f "$tweetfile" ]; # if file exists
    then
        if [ `wc -l < $tweetfile` -ge 10000 ]; then
            wc -l < $tweetfile | xargs # total num of lines
            sed -n '1p' $tweetfile # print first line
            tail -n 10000 $tweetfile | grep -c "potus" # get num of lines that contain "potus" in the last 10000 lines
            sed -n '100,200p' $tweetfile | grep -c "fake" # get num of lines between line 100-200 that contains "fake"
        else
            echo "There are less than 5 lines in this file."
        fi

    else
        echo "$tweetfile does not exist."
    fi

else
    echo "Invalid number of arguments. Please enter a single tweet file."
fi





