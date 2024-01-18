#!/usr/bin/env python3

"""Edit an XML file to use the Alias component.

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
import_regex = re.compile(r'(\s*)(<dataType\s+name="Alias"'
                          r'(?:\s+ref="_AliasCommon")?/>)(.+)', re.S)

object_open_regex = re.compile(r'(\s*<object\s+name\s*=\s*")([^"]+)(".+)',
                               re.S)
object_version_regex = re.compile(r'(.*version\s*=\s*")([^"]+)(".+)', re.S)
object_close_regex = re.compile(r'(.*)(>)(\s+)', re.S)

alias_open_regex = re.compile(r'(\s*)(<parameter\s+name="Alias"\s+access=")'
                              r'(\w+)(".+)', re.S)
alias_version_regex = re.compile(r'(.*version\s*=\s*")([^"]+)(".+)', re.S)
alias_descr_regex = re.compile(r'(\s*)({{datatype\|expand}}.+)', re.S)
alias_close_regex = re.compile(r'(\s*)(</parameter>)(.+)', re.S)

alias_prof_regex = re.compile(r'(\s*<parameter\s+ref="Alias"\s+'
                              r'requirement=")(readWrite)("/>.+)', re.S)
model_regex = re.compile(r'(\s*<model\s+name="[^:]+:2\.)(\d+)(">.+)', re.S)

# these could be command-line arguments
copyright_year = '2023'
amend = '17'
amend_corr = '%s-0' % amend
import_comp = '<component name="Alias-2-0"/>'
ref_comp = '<component ref="Alias-2-0"%s/>'  # version is substituted
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
    do_nothing = not any(import_regex.match(line) for line in lines)
    if do_nothing:
        logger.info('%s: no Alias import; nothing to be done' % base)

    state = 'outer'
    seen_alias_descr = False
    object_name = None
    object_version = None
    alias_version = None
    for line in lines:
        ignore = False

        if do_nothing:
            pass

        elif state == 'outer':
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

            # replace the Alias data type import with the Alias-2-0
            # component import
            if match := import_regex.match(line):
                prefix, entity, suffix = match.groups()
                if entity != import_comp:
                    line = '%s%s%s' % (prefix, import_comp, suffix)
                    logger.info('%s: import %s -> %s' % (base, entity,
                                                         import_comp))

            # note object names and versions
            if match := object_open_regex.match(line):
                version, closed = None, None
                _, name, _ = match.groups()
                if name:
                    object_name = name
                if match := object_version_regex.match(line):
                    _, version, _ = match.groups()
                if match := object_close_regex.match(line):
                    _, closed, _ = match.groups()
                if version:
                    object_version = version
                if not closed:
                    state = 'object'

            # look for Alias parameter definition
            if match := alias_open_regex.match(line):
                indent, prefix, access, suffix = match.groups()
                if access != param_access:
                    logger.warning('%s: Alias access is unexpected %s' %
                                   (base, access))
                else:
                    ignore = True
                    state = 'alias'
                    alias_version = None
                    seen_alias_descr = False

            # replace Alias profile readWrite requirements with
            # writeOnceReadOnly
            if match := alias_prof_regex.match(line):
                prefix, req, suffix = match.groups()
                if req != prof_req:
                    line = '%s%s%s' % (prefix, prof_req, suffix)
                    logger.info('%s: req %s -> %s' % (base, req, prof_req))

            # update the local model version
            if match := model_regex.match(line):
                prefix, version, suffix = match.groups()
                if version != amend:
                    line = '%s%s%s' % (prefix, amend, suffix)
                    logger.info('%s: model %s -> %s' % (base, version, amend))

        # capture object version (if not on the <object line)
        elif state == 'object':
            if match := object_version_regex.match(line):
                _, version, _ = match.groups()
                if version:
                    object_version = version
            if match := object_close_regex.match(line):
                _, closed, _ = match.groups()
                state = 'outer'

        # replace Alias parameter definition with Alias-2-0 component reference
        elif state == 'alias':
            ignore = True

            if alias_descr_regex.match(line):
                seen_alias_descr = True

            if match := alias_version_regex.match(line):
                alias_version = match.group(2)

            if match := alias_close_regex.match(line):
                if seen_alias_descr:
                    ignore = False
                    state = 'outer'
                    prefix, _, suffix = match.groups()
                    version = alias_version or object_version or ''
                    if version:
                        version = ' version="%s"' % version
                    line = '%s%s%s' % (prefix, ref_comp % version, suffix)
                    logger.info('%s: %s Alias -> %s' % (
                        base, object_name, ref_comp % version))

        else:
            logger.error('invalid state %r' % state)

        if loglevel != logging.INFO and not ignore:
            sys.stdout.write(line)


if __name__ == "__main__":
    sys.exit(main())
