#!/bin/bash

export PYTHONPATH=$MYROOT/WT-354/feature2

for file in tr-*.xml; do
    echo "--- $file (fixes - file only) ---"
    $MYROOT/WT-354/default/bin/report.py \
        --include $MYROOT/install/default \
        --thisonly \
        --plugindir ../bin \
        --transform fixes \
        $file
done

for file in tr-181-2-cwmp.xml tr-181-2-usp.xml; do
    echo "--- $file (fixes - complete data model) ---"
    $MYROOT/WT-354/default/bin/report.py \
        --include $MYROOT/install/default \
        --plugindir ../bin \
        --transform fixes \
        $file
done
