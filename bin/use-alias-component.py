#!/usr/bin/env python3

"""Edit an XML file to use the Alias component.

** UPDATED APRIL 2024 to use replace Alias-1-0 and Alias-2-0 with Alias **

(Based on edit-file-headers.py.)

The changes are illustrated by the tr-181-2-atm.xml diffs shown below:

    * Update the copyright year
    * Update the spec and file attributes
    * Replace the Alias data type import with the Alias-2-0 component import
    * Replace Alias parameter definitions with Alias-2-0 component references
    * Replace Alias profile readWrite requirements with writeOnceReadOnly
    * Update the local model version

It should be safe to run this script on its output.

% git diff origin/develop tr-181-2-atm.xml
diff --git a/device2/tr-181-2-atm.xml b/device2/tr-181-2-atm.xml
index b2631e9..2240aa0 100644
--- a/device2/tr-181-2-atm.xml
+++ b/device2/tr-181-2-atm.xml
@@ -2,7 +2,7 @@
 <!--
   Device:2 Root Data Model: Common Object definitions [ATM]

-  Copyright (c) 2010-2020, Broadband Forum
+  Copyright (c) 2010-2023, Broadband Forum

   Redistribution and use in source and binary forms, with or
   without modification, are permitted provided that the following
@@ -55,13 +55,13 @@
         https://www.broadband-forum.org/cwmp/cwmp-datamodel-1-10.xsd
       urn:broadband-forum-org:cwmp:datamodel-report-1-0
         https://www.broadband-forum.org/cwmp/cwmp-datamodel-report-1-0.xsd"
-    spec="urn:broadband-forum-org:tr-181-2-16-0-atm"
-    file="tr-181-2-16-0-atm.xml">
+    spec="urn:broadband-forum-org:tr-181-2-17-0-atm"
+    file="tr-181-2-17-0-atm.xml">

   <import file="tr-069-biblio.xml" spec="urn:broadband-forum-org:tr-069"/>

   <import file="tr-106-types.xml" spec="urn:broadband-forum-org:tr-106">
-    <dataType name="Alias" ref="_AliasCommon"/>
+    <component name="Alias-2-0"/>
   </import>

   <import file="tr-181-2-root.xml"
@@ -273,14 +273,7 @@
         </syntax>
       </parameter>

-      <parameter name="Alias" access="readWrite">
-        <description>
-          {{datatype|expand}}
-        </description>
-        <syntax>
-          <dataType ref="Alias"/>
-        </syntax>
-      </parameter>
+      <component ref="Alias-2-0"/>

       <parameter name="Name" access="readOnly">
         <description>
@@ -736,7 +729,7 @@
       <object ref="Device.ATM.Link.{i}." requirement="createDelete">
         <parameter ref="Enable" requirement="readWrite"/>
         <parameter ref="Status" requirement="readOnly"/>
-        <parameter ref="Alias" requirement="readWrite"/>
+        <parameter ref="Alias" requirement="writeOnceReadOnly"/>
         <parameter ref="Name" requirement="readOnly"/>
         <parameter ref="LastChange" requirement="readOnly"/>
         <parameter ref="LowerLayers" requirement="readWrite"/>
@@ -771,7 +764,7 @@
     </profile>
   </component>

-  <model name="ATM:2.16">
+  <model name="ATM:2.17">
     <component ref="Root"/>
     <component ref="ATM"/>
   </model>
"""

import logging
import os
import re
import sys

# XXX want just the name part; need some utilities / rules / conventions
prog_basename = os.path.basename(sys.argv[0])
(prog_root, _) = os.path.splitext(prog_basename)
logger = logging.getLogger(prog_root)

# regexes
copyright_regex = re.compile(r'(\s*Copyright\s+\(c\)\s+[\d, -]+)(\d{4})('
                             r'.+Broadband Forum.+)', re.S)
spec_regex = re.compile(r'(.*spec\s*=\s*"urn:[^:]+:tr-181-2-)(\d+-\d+)(.+)',
                        re.S)
file_regex = re.compile(r'(.*file\s*=\s*"tr-181-2-)(\d+-\d+)(.+)', re.S)

import_regex = re.compile(r'(\s*)(<component\s+name="Alias[^"]*"/>)(.+)', re.S)
ref_regex = re.compile(r'(\s*)(<component\s+ref=")(Alias[^"]*)(".+)',
                       re.S)

model_regex = re.compile(r'(\s*<model\s+name="[^:]+:2\.)(\d+)(">.+)', re.S)

# these could be command-line arguments
copyright_year = '2024'
amend = '18'
amend_corr = '%s-0' % amend
import_comp = '<component name="Alias"/>'
ref_comp = '<component ref="Alias"/>'
param_access = 'readWrite'
prof_req = 'writeOnceReadOnly'


def main(argv=None):
    if argv is None:
        argv = sys.argv

    file = argv[1]
    base, _ = os.path.splitext(file)

    loglevel = logging.INFO if len(argv) > 2 else logging.WARNING
    logging.basicConfig(level=loglevel)

    lines = open(file).readlines()

    # if nothing matches the Alias import regex there's nothing to be done
    not_imported = not any(import_regex.match(line) for line in lines)
    if not_imported:
        logger.info('%s: no Alias import; nothing to be done' % base)

    # check whether the import is used
    not_referenced = not any(ref_regex.match(line) for line in lines)
    if not not_imported and not_referenced:
        logger.warning('%s: no Alias references; should remove the import' %
                       base)

    for line in lines:
        ignore = False

        if not_imported:
            pass

        else:
            # update the copyright year
            if match := copyright_regex.match(line):
                prefix, year, suffix = match.groups()
                if year != copyright_year:
                    line = '%s%s%s' % (prefix, copyright_year, suffix)
                    logger.info('%s: copyright year %s -> %s' % (
                        base, year, copyright_year))

            # update the spec attribute
            # (a change is reported as a warning because any referencing files
            # have to be updated)
            if match := spec_regex.match(line):
                prefix, version, suffix = match.groups()
                if version != amend_corr:
                    line = '%s%s%s' % (prefix, amend_corr, suffix)
                    logger.warning('%s: spec %s -> %s' % (base, version,
                                                          amend_corr))

            # update the file attribute
            if match := file_regex.match(line):
                prefix, version, suffix = match.groups()
                if version != amend_corr:
                    line = '%s%s%s' % (prefix, amend_corr, suffix)
                    logger.info('%s: file %s -> %s' % (base, version,
                                                       amend_corr))

            # replace the Alias-2-0 component import with Alias
            if match := import_regex.match(line):
                prefix, entity, suffix = match.groups()
                if entity != import_comp:
                    line = '%s%s%s' % (prefix, import_comp, suffix)
                    logger.info('%s: import %s -> %s' % (base, entity,
                                                         import_comp))

            # replace the Alias-2-0 component reference with Alias
            # (discard any attributes)
            if match := ref_regex.match(line):
                indent, prefix, name, suffix = match.groups()
                if name == 'Alias-2-0':
                    line = '%s%sAlias"/>\n' % (indent, prefix)
                    logger.info('%s: reference Alias-2-0 -> Alias' % base)

            # update the local model version
            if match := model_regex.match(line):
                prefix, version, suffix = match.groups()
                if version != amend:
                    line = '%s%s%s' % (prefix, amend, suffix)
                    logger.info('%s: model %s -> %s' % (base, version, amend))

        if loglevel != logging.INFO and not ignore:
            sys.stdout.write(line)


if __name__ == "__main__":
    sys.exit(main())
