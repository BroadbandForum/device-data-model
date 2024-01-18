#!/bin/bash

for file in tr-181*.xml; do
  echo --- $file ---
  ../bin/use-alias-component.py $file >$file.edited
  /bin/mv -f $file.edited $file
done
