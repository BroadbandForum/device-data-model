#!/usr/bin/env python3

"""Manually apply edits that could use the misc transform for, but do it
this way so there are no line-break or whitespace changes.

OBSOLETE
"""

# XXX maybe

import logging
import os
import re
import sys

logging.basicConfig(level=logging.INFO)

# XXX want just the name part; need some utilities / rules / conventions
prog_basename = os.path.basename(sys.argv[0])
(prog_root, _) = os.path.splitext(prog_basename)
logger = logging.getLogger(prog_root)

retain = {'tr-181-2-bulkdata.xml', 'tr-181-2-usp.xml''tr-181-2-wifi.xml'}

trigger = 'The undersigned members have elected to grant the copyright to'

import_ = """
  <import file="tr-181-2-root.xml" spec="urn:broadband-forum-org:tr-181-2-14-root">
    <component name="Root"/>
  </import>

"""[1:]

component_ = """
    <component ref="Root"/>
"""[1:]

def main(argv=None):
    if argv is None:
        argv = sys.argv

    file = argv[1]

    state = 'initial'
    need_import = True
    for line in open(file).readlines():
        ignore = False

        if state == 'initial':
            if line.find('<!--') >= 0:
                state = 'comment'

            elif line.find('<import file="tr-181-2-root.xml"') >= 0:
                need_import = False

            elif re.match('  <(component|dataType|template)', line) and \
                    need_import:
                sys.stdout.write(import_)
                logger.info('added import')
                need_import = False

            elif line.find('<model') >= 0:
                state = 'model'

        elif state == 'comment':
            if line.find(trigger) >= 0:
                if file in retain:
                    logger.info('retained copyright')
                else:
                    logger.info('removed copyright')
                    state = 'ignore'
            elif line.find('-->') >= 0:
                state = 'initial'

        elif state == 'ignore':
            if line.strip() == '':
                ignore = True
                state = 'initial'

        elif state == 'model':
            if line.find('<component') < 0:
                ignore = True
            else:
                if line.find('Root') < 0:
                    sys.stdout.write(component_)
                    logger.info('updated model')
                state = 'final'

        elif state == 'final':
            pass

        else:
            logger.error('invalid state %r' % state)

        if state != 'ignore' and not ignore:
            sys.stdout.write(line)


if __name__ == "__main__":
    sys.exit(main())
