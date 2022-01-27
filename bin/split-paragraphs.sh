#!/bin/bash

export PYTHONPATH=$MYROOT/WT-354/default

for file in tr-181*.xml; do
    echo --- $file ---
    $MYROOT/WT-354/default/bin/report.py \
        --include $MYROOT/install/default \
        --thisonly -t split -f xml $file -o $file.split
    /bin/mv -f $file.split $file
done
