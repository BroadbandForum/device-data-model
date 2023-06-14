#!/bin/bash

for file in tr-*.xml; do
    echo --- $file ---
    sed -e 's/datamodel-1-[0-9]*/datamodel-1-10/g' \
        $file >$file.edited
    /bin/mv -f $file.edited $file
done
