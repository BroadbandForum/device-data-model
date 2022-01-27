#!/usr/bin/env python3

"""Edit an XML file header according to
https://issues.broadband-forum.org/browse/BUSPUB-40 decisions.

(Based on edit-manual.py.)
"""

# XXX note that this script can't be run on its output; sorry

import logging
import os
import sys

logging.basicConfig(level=logging.INFO)

# XXX want just the name part; need some utilities / rules / conventions
prog_basename = os.path.basename(sys.argv[0])
(prog_root, _) = os.path.splitext(prog_basename)
logger = logging.getLogger(prog_root)

contact = """
  Comments or questions about this Broadband Forum data model should be
  directed to <info@broadband-forum.org>.
"""


def main(argv=None):
    if argv is None:
        argv = sys.argv

    file = argv[1]

    retain_description_tails = {'-cwmp.xml', '-usp.xml'}
    retain_description = any(file.endswith(tail) for tail in
                             retain_description_tails)

    state = 'initial'
    for line in open(file).readlines():
        ignore = False

        # looking for the last line of the license
        # XXX note that we don't look for the Notice (which indicates DRAFT
        #     status etc.) because we know that it isn't there
        if state == 'initial':
            if line.find('license grant are also deemed granted '
                         'under this license') >= 0:
                state = 'inserting-contact'

        # inserting contact details (this will be the blank line after the
        # license)
        elif state == 'inserting-contact':
            sys.stdout.write(contact)
            state = 'ignore-rest-of-comment'

        # ignoring the rest until the end of the header comment
        elif state == 'ignore-rest-of-comment':
            if line.find('-->') >= 0:
                state = 'continuing-to-end' if retain_description else \
                    'looking-for-description'

        # looking for the top-level description (it's OK if it's not there)
        # XXX note the assumption of exactly two leading spaces
        elif state == 'looking-for-description':
            if line.startswith('  <description>'):
                state = 'ignore-toplevel-description'

        # looking for the end of the top-level description
        elif state == 'ignore-toplevel-description':
            if line.startswith('  </description>'):
                ignore = True
                state = 'continuing-to-end'

        # continuing to the end
        elif state == 'continuing-to-end':
            pass

        else:
            logger.error('invalid state %r' % state)

        if not ignore and not state.startswith('ignore'):
            sys.stdout.write(line)


if __name__ == "__main__":
    sys.exit(main())
