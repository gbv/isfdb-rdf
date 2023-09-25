#!/usr/bin/bash
 
user="isfdb"
password="isfdb"
db=isfdb


dump="$1"

 if [ $# == 0 ]; then
  echo "usage: $0 backup-mysql-file.zip"
  exit
elif [ ! -f "$dump" ]; then
  echo >&2 "missing dump file $dump"
  exit 1
fi

tables=$(mysql -u $user -p$password -Nse 'SHOW TABLES' $db)
 
count() { echo $#; }

if [ ! -z "$tables" ]; then
  echo -n Dropping $(count "$tables") tables from "$db" ...
  for table in $tables; do
    mysql -u $user -p$password -e "DROP TABLE $table" $db
  done
fi
echo done
 
echo -n "Importing $dump ..."

zcat "$dump" | mysql -u $user -p$password $db
echo done
