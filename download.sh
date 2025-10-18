#!/bin/bash

word=$1
word2=$2
word3=$3
word4=$4
word5=$5

con=$(echo "$word" | tr " " "-")
before=$(echo "$con" | cut -d "|" -f1 )

mkdir download
curl -s "https://starkmovie.af/movie/$before/" | grep download  > "download/$word2.txt"
sleep 10
grep -oP "https://.*?\.(mkv|mp4)" "./download/$word2.txt" > "./download/$word3"
sleep 5

cat "./download/$word3" | grep $word4 > "./download/$word5"
sleep 5
wget -i "./download/$word5" -P "./uploads"
