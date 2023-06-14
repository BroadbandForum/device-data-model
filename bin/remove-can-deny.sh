#!/bin/bash

# --include $MYROOT/install/default

export PYTHONPATH=$MYROOT/WT-354/default

for file in tr-181*.xml; do
    echo --- $file ---
    $MYROOT/WT-354/default/bin/report.py \
        --thisonly --loglevel 0 \
        -P $PYTHONPATH/bbfreport/plugins/examples -t candeny \
        -f xml $file -o $file.edited
    /bin/mv -f $file.edited $file
done
