#!/bin/bash

export PYTHONPATH=$MYROOT/WT-354/default

# create mappings
update=""
for file in tr-181-1.xml tr-181-2-cwmp.xml tr-181-2-usp.xml; do
    echo "--- $file (create/update mappings) ---"
    $MYROOT/WT-354/default/bin/report.py \
        --include $MYROOT/install/default \
        -t relref $update \
        --relref-mappings-file=relref-mappings-script.json \
        $file
    update="--relref-update-mappings"
done

# apply mappings
for file in tr-181-*.xml; do
    echo "--- $file (apply mappings) ---"
    $MYROOT/WT-354/default/bin/report.py \
        --include $MYROOT/install/default \
        --thisonly \
        -t relref \
        --relref-apply-mappings \
        --relref-mappings-file=relref-mappings-script.json \
        -f xml \
        $file \
        -o $file.relref
    /bin/mv -f $file.relref $file
done

/bin/rm -f relref-mappings-script.json
