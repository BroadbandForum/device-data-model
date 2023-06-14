#!/bin/bash

for file in tr-*.xml; do
    echo --- $file ---

    # this adds missing command async="false"
    # XXX it's not clever enough to handle multi-line elements
    sed -e '/command name=.*async=/b' \
        -e '/command name=.*>/s/()"/& async="false"/' \
        $file >$file.edited
    /bin/mv -f $file.edited $file

    # this adds missing uniqueKey functional="true"
    # XXX it's not clever enough to handle multi-line elements
    sed -e '/<uniqueKey>/s/>/ functional="true">/' \
        $file >$file.edited
    /bin/mv -f $file.edited $file
done
