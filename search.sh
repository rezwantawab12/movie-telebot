#!/bin/bash
word=$1
word2=$2



curl -s "https://starkmovie.af/?s=$word" | grep -o '<h2 class="Title[^>]*>[^<]*' | sed 's/<h2 class="Title[^>]*>//' > $word2
