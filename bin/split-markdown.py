#!/usr/bin/env python3

"""Split index.md into separate files (intended for the WT-181 specification
but should more-or-less work for any spec).
"""

import argparse
import logging
import os.path
import re
import sys

from typing import IO, Optional

# XXX want just the name part; need some utilities / rules / conventions
prog_basename = os.path.basename(sys.argv[0])
(prog_root, _) = os.path.splitext(prog_basename)
logger = logging.getLogger(prog_root)


def parse_heading(heading: str, *, context: dict) -> \
        tuple[Optional[str], Optional[str]]:
    """Parse a level-1 heading, returning the corresponding output directory
    and filename."""
    # split into '# title {attributes}
    match = re.match(r'#\s+(.*?)\s*(?:{(.*?)})?\s*$', heading)
    if not match:
        logger.error("level-1 heading %r didn't match pattern; ignored" %
                     heading)
        return None, None
    title = match.group(1)
    attributes = match.group(2) or ''

    # derive the directory name from the attributes
    # XXX could/should check that once have seen an annex everything is
    #     an annex or appendix, and once have seen an appendix everything is
    #     an appendix
    out_dir = 'annexes' if '.annex' in attributes else 'appendices' if \
        '.appendix' in attributes else 'main'

    # clean up the title (to use for the file name)
    # XXX we currently assume that two digits are sufficient
    title_clean = re.sub(r'\W+', '-', title).lower()
    # ensure there are no leading or trailing hyphens
    # XXX could probably use a cleverer pattern to avoid the need for this
    title_clean = re.sub(r'^-|-$', '', title_clean)

    # XXX hack out-dir for 'appendices'
    out_dir = 'appendices' if title_clean == 'appendices' else out_dir

    # update the context (it keeps track of file numbers)
    context.setdefault(out_dir, -1)
    context[out_dir] += 1
    file_number = context[out_dir]

    # XXX number the annexes starting at 1 rather than 0 (cosmetic)
    if out_dir == 'annexes':
        file_number += 1

    # XXX hack file number 99 for 'back-matter'
    if title_clean == 'back-matter':
        file_number = 99

    # form the file name
    out_file = '%02d-%s.md' % (file_number, title_clean)
    logger.info('%r -> %s %s' % (heading, out_dir, out_file))
    return out_dir, out_file

# XXX temporarily open files with mode 'r'; should use 'x'
def open_file(directory: str, filename: str, mode: str = 'w') -> IO:
    """Open a file in the specified directory, creating the directory if need
    be. By default, the file must not already exist."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    fd = open(path, mode)
    logger.info('opened %s' % fd)
    return fd


def main(argv=None):
    if argv is None:
        argv = sys.argv

    default_filename = ['index.md']
    default_loglevel = 0

    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog=prog_basename, description=__doc__,
                                     fromfile_prefix_chars='@',
                                     formatter_class=formatter_class)

    parser.add_argument('filename', type=str, nargs='*',
                        default=default_filename,
                        help='file name(s); default: %r' % default_filename)
    parser.add_argument('-l', '--loglevel', type=int, default=default_loglevel,
                        help='logging level; default: %r' % default_loglevel)

    args = parser.parse_args(argv[1:])

    loglevel_map = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}
    logging.basicConfig(level=loglevel_map[args.loglevel])

    # read the input file(s), writing each line to the appropriate
    # output file (switching to a new file for each level-1 heading)
    context = {}
    out_dir, out_file = parse_heading('# front matter', context=context)
    assert out_dir and out_file
    out_fd = open_file(out_dir, out_file)
    in_metadata = False
    for filename in args.filename:
        for line in open(filename).read().splitlines():

            # we need to know whether we're in a metadata block because '#'
            # is a comment (not a heading) within metadata
            if line == '---':
                in_metadata = True
            elif in_metadata and (line == '...' or line == '---'):
                in_metadata = False

            # is this a new level-1 heading?
            elif not in_metadata and line.startswith('# '):
                out_dir, out_file = parse_heading(line, context=context)
                assert out_dir and out_file
                out_fd = open_file(out_dir, out_file)

            # is this the 'back matter' line?
            # XXX this is an honorary appendix; this wouldn't be ideal if
            #     there weren't any appendices
            elif not in_metadata and re.match(
                    r'!include\s+back-matter\.md\s*$', line):
                out_dir, out_file = parse_heading('# back matter {.appendix}',
                                                  context=context)
                assert out_dir and out_file
                out_fd = open_file(out_dir, out_file)

            # write the line to the appropriate file
            # XXX could potentially fix up image references?
            out_fd.write('%s\n' % line)
    out_fd.close()


if __name__ == '__main__':
    sys.exit(main())
