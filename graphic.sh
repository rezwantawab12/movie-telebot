#!/bin/bash

word=$1
word2=$2
con=$(echo "$word" | tr " " "-")
before=$(echo "$con" | cut -d "|" -f1 )



curl -s "https://starkmovie.af/movie/$before/" | grep -o -E  "2160p|1080p|720p"   | sort | uniq  >  $word2


