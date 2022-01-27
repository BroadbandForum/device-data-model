#!/bin/bash

export PYTHONPATH=$MYROOT/WT-354/default

for file in tr-181*.xml; do
    echo --- $file ---
    $MYROOT/WT-354/default/bin/report.py \
        --include $MYROOT/install/default \
        --thisonly -t version -f xml $file -o $file.version
    /bin/mv -f $file.version $file
done
