#!/usr/bin/bash
 
. config.sh

query="$1"

# tsv without column names
mysql -u $user -p$password -Nse "$query" $db

