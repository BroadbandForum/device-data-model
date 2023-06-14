#!/usr/bin/env python3

"""Check for files that have been edited since the last release but whose
spec (and file) attributes haven't been updated."""

import argparse
import logging
import os.path
import re
import subprocess
import sys

from typing import Dict, List, Tuple

from pyutil import git

# XXX want just the name part; need some utilities / rules / conventions
prog_basename = os.path.basename(sys.argv[0])
(prog_root, _) = os.path.splitext(prog_basename)
logger = logging.getLogger(prog_root)


def parse_tag(tag: str) -> List[Tuple[int, int, int]]:
    # v2.15.1-rel -> ('2', '15', '1')
    match = re.match(r'^v(\d+)\.(\d+)\.(\d+)', tag)
    assert match is not None, 'invalid tag %s' % tag
    i, a, c = match.groups()
    ii, ia, ic = int(i), int(a), int(c)
    return [(ii + 1, 0, 0), (ii, ia + 1, 0), (ii, ia, ic + 1)]


def parse_file(name: str) -> Tuple[str, int, int, int, str]:
    # XXX this is quite a tight pattern; will relax it if necessary
    match = re.match(r'^(tr-\d+)-(\d+)(?:-(\d+))?(?:-(\d+))?-([\w-]+)\.xml$',
                     name)
    assert match is not None, 'invalid file attribute %s' % name
    doc, i, a, c, label = match.groups('0')
    return doc, int(i), int(a), int(c), label


def added_attributes(line: str, *, prefix: str = '') -> Dict[str, str]:
    attrs = {}
    blocks = re.findall(r'(\[-|{\+)(.*?)(-]|\+})', line)
    for start, text, stop in blocks:
        removed = start == '[-' and stop == '-]'
        added = start == '{+' and stop == '+}'
        assert removed or added
        text = text.strip()
        logger.debug('%s%s %r' % (prefix, start[1], text))

        if added and (matches := re.findall(r'(\w+)\s*=\s*"([^"]*)"', text)):
            for name, value in matches:
                assert name not in attrs
                attrs[name] = value
    return attrs


# XXX this is quite limited
def file_updated(path: str, file: str,
                 next_versions: List[Tuple[int, int, int]]) -> bool:
    path_comps = parse_file(path)
    file_comps = parse_file(file)
    return path_comps[0] == file_comps[0] and \
        (file_comps[1], file_comps[2], file_comps[3]) in next_versions and \
        path_comps[4] == file_comps[4]


def main(argv=None):
    if argv is None:
        argv = sys.argv

    default_loglevel = 0

    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog=prog_basename, description=__doc__,
                                     fromfile_prefix_chars='@',
                                     formatter_class=formatter_class)

    default_tag = 'v2.15.1-rel'
    default_subdir = 'device2'
    default_file = []

    parser.add_argument('-s', '--subdir', default=default_subdir,
                        help='root subdirectory to use; default: %s'
                             % default_subdir)
    parser.add_argument('-t', '--tag', type=str, default=default_tag,
                        help='git tag (or tag1..tag2) for most recent '
                             'release; default: %r' % default_tag)
    parser.add_argument('-f', '--file', type=str, nargs='*',
                        default=default_file,
                        help='files to process (used for debugging); '
                             'default: %r' % default_file)
    parser.add_argument('-l', '--loglevel', type=int, default=default_loglevel,
                        help='logging level; default: %r' % default_loglevel)

    args = parser.parse_args(argv[1:])

    loglevel_map = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}
    logging.basicConfig(level=loglevel_map[args.loglevel])

    # this assumes that the program is run from within a git checkout
    gitdir = git.find_gitdir('.')
    # XXX args.subdir is an abuse of the original intent, but it works OK here
    repo = git.Repository(gitdir, args.subdir, quiet=True)

    # XXX this is a bit hacky
    tags = repo.get_tags(quiet=True)
    for tag in args.tag.split('..'):
        if tag != 'HEAD' and tag not in tags:
            logger.error('non-existent tag %s' % tag)
            return 1

    next_versions = parse_tag(args.tag)

    paths = repo.list_files(quiet=True)
    paths_to_update = []
    for path in paths:
        # we're only interested in XML files
        if not path.endswith('.xml'):
            continue

        # are we only interested in a single file?
        if args.file and not any(f.lower() in path.lower() for f in args.file):
            continue

        # get a list of commits since the specified tag
        try:
            commit_details = repo.query_log(since=args.tag, pretty='%h %ad',
                                            date='short', paths=path)
        except subprocess.CalledProcessError as e:
            logger.error(e)
            if e.stderr:
                for line in e.stderr.splitlines():
                    logger.error(line)
            continue

        # we're only interested if there are any commits
        if not commit_details:
            continue

        # check for added attributes
        seen_file = False
        for commit_detail in commit_details:
            commit, date = commit_detail.split(maxsplit=1)
            prefix = '%s %s: ' % (path, commit_detail)
            try:
                diffs = repo.show_object(commit, word_diff='plain', paths=path)
                logger.info('%s%d diffs' % (prefix, len(diffs)))
                for diff in diffs:
                    if attrs := added_attributes(diff, prefix=prefix):
                        if 'file' in attrs:
                            logger.info('%s%s' % (prefix, attrs))

                        # note whether the file attribute was added
                        if 'file' in attrs and attrs['file'] not in {
                            'tr-069-biblio.xml', 'tr-106-types.xml'} and \
                            file_updated(path, attrs['file'], next_versions):
                            seen_file = True

                        # note whether the local model name attribute was added
                        # XXX this logic is incomplete (careful not to get
                        #     confused by profiles)
                        if False and 'name' in attrs and ':' in attrs['name']:
                            logger.warning('%scheck local model name %s' % (
                                prefix, attrs['name']))
            except AssertionError as e:
                logger.error('%s%s' % (prefix, e))
                continue
            except subprocess.CalledProcessError as e:
                logger.error('%s%s' % (prefix, e))
                if e.stderr:
                    for line in e.stderr.splitlines():
                        logger.error('%s%s' % (prefix, line))
                continue

        # if there are commits then the file attribute should have been updated
        if commit_details and not seen_file:
            logger.warning("%s has %d commits since %s but its file "
                           "attribute hasn't been updated" % (
                            path, len(commit_details), args.tag))
            paths_to_update.append(path)

    if paths_to_update:
        logger.warning('%d files need to be updated' % len(paths_to_update))


if __name__ == '__main__':
    sys.exit(main())
