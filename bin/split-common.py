#!/usr/bin/env python3

"""Split tr-181-2-common.xml into separate files.
"""

import argparse
import logging
import os.path
import re
import sys

# XXX want just the name part; need some utilities / rules / conventions
prog_basename = os.path.basename(sys.argv[0])
(prog_root, _) = os.path.splitext(prog_basename)
logger = logging.getLogger(prog_root)

XXX_things_to_improve = """
- InterfaceStackNumberOfEntries goes into the root file but should be in the
  interfacestack file
- Not all component usage can be detected, e.g. the diagnostic test inputs 
  and outputs; need to add as exceptions (c.f. guti and s-nssai)
- Component (and other?) definitions will be output to each file that uses them
"""


class File:
    """Represents tr-181-2-common.xml or a similar file that's to be split
    into multiple files."""

    all_profile_names = set()  # XXX make this be a list like the others?

    # these are keyed by top-level object component name
    component_references = {}

    def __init__(self, filename):
        self._filename = filename
        with open(filename) as fd:
            self._data = self._parse_common_file(fd.readlines())

    def output_toplevel_object(self, object_):
        path, lines = object_
        name = self._get_toplevel_name(path)
        cname = self._get_component_name(path)
        version = '2.14'  # XXX should get this from the input
        filename = self._get_filename(path)
        with open(filename, 'w') as fd:
            # get referenced component names and data types
            component_names = self._component_names(path)
            datatype_names = self._datatype_names(path, component_names)
            profile_names = self._profile_names(path)

            # note component names for later generation of the common file
            self.component_references[cname] = component_names

            # report
            logger.info('%r -> %r' % (path, filename))
            if component_names:
                logger.info('  components %s' % component_names)
            if datatype_names:
                logger.info('  datatypes %s' % datatype_names)
            if profile_names:
                logger.info('  profiles %s' % profile_names)

            # output everything down to just before the (original) model
            self._output_top_lines(fd, path, datatype_names,
                                   component_names, cname=cname)

            # output the top-level object's component definition
            fd.write('  <component name="%s">\n' % cname)
            for path_, lines in self.objcomps:
                name_ = self._get_toplevel_name(path_)
                if name_ == name or name_ in component_names:
                    fd.write(''.join(lines))
            for name_, lines in self.profiles:
                if name_ in profile_names:
                    fd.write(''.join(lines))
            fd.write('  </component>\n')

            # output a model that just references this component
            fd.write('\n')
            fd.write('  <model name="%s:%s">\n' % (name, version))
            if cname != 'Root':
                fd.write('    <component ref="Root"/>\n')
            fd.write('    <component ref="%s"/>\n' % cname)
            fd.write('  </model>\n')

            # output everything after the (original) model
            self._output_bottom_lines(fd, path)

    def output_common(self):
        filename = self._filename.replace('-old.xml', '.xml')  # XXX method?
        assert filename != self._filename
        version = '2.14'  # XXX should get this from the input
        spec_prefix = 'urn:broadband-forum-org:tr-181-2-14-0-'  # XXX ditto
        with open(filename, 'w') as fd:
            # report
            logger.info('%r' % filename)

            # these components weren't written to individual files
            # (because their top-level objects don't exist in the common file)
            # XXX should write them to their own files? shouldn't hard-code
            component_names = ['SelfTestDiagnosticsOutput',
                               'PacketCaptureDiagnosticsInput',
                               'PacketCaptureDiagnosticsOutput']

            # they use these data types
            # XXX shouldn't hard-code this but can't pass here because we
            #     need to add our own imports
            datatype_names = ['URL']

            # output everything down to just before the (original) model
            self._output_top_lines(fd, path=None,
                                   datatype_names=datatype_names,
                                   component_names=None, cname='COMMON')

            # import all the components from the top-level object files
            for toplevel_object in self.toplevel_objects:
                path, _ = toplevel_object
                cname = self._get_component_name(path)

                # get the list of components to import
                # XXX need to distinguish internal and external components
                cnames = [cname] + self.component_references[cname]

                _, file = os.path.split(self._get_filename(path))
                # XXX hack the spec
                spec = spec_prefix + file.replace('tr-181-2-', '').replace(
                        '.xml', '')
                version = '2.14'  # XXX should get this from the input
                fd.write('  <import file="%s" spec="%s">\n' % (file, spec))
                for cname_ in cnames:
                    # XXX some components can be defined in multiple files;
                    #     this is a bug, but work around it by commenting out
                    #     lower-case components, which (a) catches this case,
                    #     and (b) works because they're all internal
                    oc = ''
                    cc = ''
                    if cname_.lower() == cname_:
                        oc = '<!-- '
                        cc = ' -->'
                    fd.write('    %s<component name="%s"/>%s\n' % (oc,
                                                                   cname_, cc))
                fd.write('  </import>\n')
                fd.write('\n')

            fd.write(''.join(self._component_lines(component_names)))

            # output the model, including the _Baseline:n profiles
            fd.write('  <model name="Device:%s">\n' % version)
            for toplevel_object in self.toplevel_objects:
                path, _ = toplevel_object
                cname = self._get_component_name(path)
                fd.write('    <component ref="%s"/>\n' % cname)
            fd.write('\n')
            for profile_name in ['_Baseline:1', '_Baseline:2', '_Baseline:3']:
                lines = [l for n, l in self.profiles if n == profile_name][0]
                fd.write(''.join(lines))
            fd.write('  </model>\n')

            # output everything after the (original) model
            self._output_bottom_lines(fd, path=None)

    @staticmethod
    def _parse_common_file(lines):
        # table of states, regexes and next states
        # XXX this is very specific to the task at hand; it's not general
        # XXX should define regexes separately to ensure consistency
        states = {
            'file-top': (r'\s*<!--', 'comment-top'),
            'comment-top': (r'\s*The undersigned', 'copyrights'),
            'copyrights': (r'\s*$', 'comment-bottom',
                           {'keep-with-this': True}),
            'comment-bottom': (r'\s*-->', 'document-top',
                               {'keep-with-this': True}),
            'document-top': (r'\s*<import\s+file=', 'imports'),
            # note exactly two spaces to distinguish from import/dataType
            'imports': (r'  <dataType\s+name="(\w+)"', 'datatypes'),
            'datatypes': ((r'\s*</dataType>', 'datatypes'),
                          (r'  <dataType\s+name="(\w+)"', 'datatypes'),
                          (r'\s*<template\s+id="(\w+)"', 'templates')),
            'templates': ((r'\s*</template>', 'templates'),
                          (r'\s*<template\s+id="(\w+)"', 'templates'),
                          (r'\s*<component\s+name="([\w-]+)"', 'components')),
            'components': ((r'\s*</component>', 'components'),
                           (r'\s*<component\s+name="([\w-]+)"', 'components'),
                           (r'\s*<model\s+name=', 'model-top')),
            # note that only a single model is supported
            'model-top': ((r'\s*<object\s+name="([\w{}.]+)"', 'objcomps'),
                          (r'\s*<component\s+ref="([\w-]+)"', 'objcomps'),
                          {'define-key': True}),
            'objcomps': ((r'\s*</object>', 'objcomps'),
                         (r'\s*<object\s+name="([\w{}.]+)"', 'objcomps'),
                         (r'\s*<component\s+ref="([\w-]+)"', 'objcomps',
                          {'define-key': True}),
                         (r'\s*<profile\s+name="([\w:]+)"', 'profiles')),
            'profiles': ((r'\s*</profile>', 'profiles'),
                         (r'\s*<profile\s+name="([\w:]+)"', 'profiles'),
                         (r'\s*</model>', 'model-bottom')),
            'model-bottom': (r'\s*</dm:document>', 'document-bottom'),
            'document-bottom': (None, None)
        }

        # initial setup
        data = {}
        current_key = ()
        new_key = ()
        state = 'file-top'

        # process lines
        for line in lines:
            assert state in states

            # there can be one or more condition; they're tested in order
            conditions = states[state]
            if not isinstance(conditions[0], tuple):
                conditions = [conditions]

            # default options to {}
            conditions = tuple(
                    c if len(c) == 3 else tuple(list(c) + [{}]) for c in
                    conditions)

            # break on first match
            match, next_state, keep_with_this = None, None, None
            for regex, next_state, options in conditions:
                next_state = next_state or state  # defaults to current state
                assert not set(options.keys()) - {'keep-with-this',
                                                  'define-key'}
                keep_with_this = options.get('keep-with-this', False)
                define_key = options.get('define-key', False)
                match = re.match(regex, line) if regex else None
                if match:
                    break

            # the data's associated with the current state by default
            data_state = state

            # the key's a (possibly empty) tuple
            if match:
                new_key = match.groups()
                state = next_state
                # when changing state, the data's associated with the new
                # state by default, but 'keep_with_next' overrides this
                if not keep_with_this:
                    data_state = next_state

            # XXX this is a hack really; it defines an entry for a key without
            #     storing the content; it's used for component references
            if new_key and define_key:
                data.setdefault(data_state, {})
                data[data_state].setdefault(new_key, [])
                new_key = None

            if not new_key:
                data.setdefault(data_state, [])
                if isinstance(data[data_state], dict):
                    assert current_key is not None
                    data[data_state][current_key] += [line]
                else:
                    data[data_state] += [line]
            else:
                data.setdefault(data_state, {})
                data[data_state].setdefault(new_key, [])
                data[data_state][new_key] += [line]
                current_key = new_key

        return data

    # the path can refer to a component or an object
    def _get_toplevel_name(self, path):
        # special case: {'Device.', 'Device.Services.'} -> Device
        if path in {'Device.', 'Device.Services.'}:
            return 'Device'

        # Device.InterfaceStack.{i}. -> ['Device', 'InterfaceStack', '{i}', '']
        # Device.IP. -> ['Device', 'IP', '']
        # WiFiAllianceEasyMesh -> ['WiFiAllianceEasyMesh']
        components = path.split('.')
        # 'InterfaceStack', 'IP', 'WiFiAllianceEasyMesh'
        return components[1] if len(components) > 1 else components[0]

    def _get_component_name(self, path):
        name = self._get_toplevel_name(path)
        return 'Root' if name == 'Device' else name

    def _get_filename(self, path):
        name = self._get_toplevel_name(path).lower()
        # special case: 'device' -> 'root'
        if name == 'device':
            name = 'root'
        suffix = self._get_filename_suffix()
        filename = self._filename.replace(suffix, '-%s.xml' % name)
        return filename

    def _get_filename_suffix(self):
        _, filename = os.path.split(self._filename)
        match = re.match(r'.*(-common.*\.xml)$', filename)
        assert match
        return match.group(1)

    def _component_names(self, path):
        # search for components that include objects matching this path
        # XXX this ignores reference in context (which happens) and
        #     <component ref="..." path="..."> (which doesn't?)
        component_names = []
        name = self._get_toplevel_name(path)
        for component_name, lines in self.components:
            for line in lines:
                match = re.match(r'\s*<object\s+name="([\w{}.]+)"', line)
                if match:
                    path_ = match.group(1)
                    if self._get_toplevel_name(path_) == name:
                        if component_name not in component_names:
                            component_names += [component_name]

        # add exceptions because we can't tell where to put components that are
        # referenced in context (not without looking in the cwmp and usp files)
        if path == 'Device.DSL.':
            component_names += ['ADSLLineDiagnosticsInput',
                                'ADSLLineDiagnosticsOutput',
                                'SELTUERDiagnosticsInput',
                                'SELTUERDiagnosticsOutput',
                                'SELTQLNDiagnosticsInput',
                                'SELTQLNDiagnosticsOutput',
                                'SELTPDiagnosticsInput',
                                'SELTPDiagnosticsOutput']
        elif path == 'Device.ATM.':
            component_names += ['ATMF5LoopbackDiagnosticsInput',
                                'ATMF5LoopbackDiagnosticsOutput']
        elif path == 'Device.HPNA.':
            component_names += ['HPNAPHYThroughputDiagnosticsInput',
                                'HPNAPHYThroughputDiagnosticsOutput',
                                'HPNAPerformanceMonitoringDiagnosticsInput',
                                'HPNAPerformanceMonitoringDiagnosticsOutput']
        elif path == 'Device.Ghn.':
            component_names += ['GhnPHYThroughputDiagnosticsInput',
                                'GhnPHYThroughputDiagnosticsOutput',
                                'GhnPerformanceMonitoringDiagnosticsInput',
                                'GhnPerformanceMonitoringDiagnosticsOutput']
        elif path == 'Device.UPA.':
            component_names += ['UPAInterfaceMeasurementDiagnosticsInput',
                                'UPAInterfaceMeasurementDiagnosticsOutput']
        elif path == 'Device.WiFi.':
            component_names += ['WiFiNeighboringWiFiDiagnosticsOutput']
        elif path == 'Device.IP.':
            component_names += ['IPPingDiagnosticsInput',
                                'IPPingDiagnosticsOutput',
                                'IPTraceRouteDiagnosticsInput',
                                'IPTraceRouteDiagnosticsOutput',
                                'IPDownloadDiagnosticsCapabilities',
                                'IPDownloadDiagnosticsInput',
                                'IPDownloadDiagnosticsInput2',
                                'IPDownloadDiagnosticsOutput',
                                'IPUploadDiagnosticsCapabilities',
                                'IPUploadDiagnosticsInput',
                                'IPUploadDiagnosticsInput2',
                                'IPUploadDiagnosticsOutput',
                                'IPUDPEchoDiagnosticsInput',
                                'IPUDPEchoDiagnosticsCapabilities',
                                'IPUDPEchoDiagnosticsInput2',
                                'IPUDPEchoDiagnosticsOutput',
                                'IPLayerCapacityCapabilities',
                                'IPLayerCapacityInput',
                                'IPLayerCapacityOutput',
                                'IPServerSelectionDiagnosticsInput',
                                'IPServerSelectionDiagnosticsOutput']
        elif path == 'Device.DNS.':
            component_names += ['DNSLookupDiagnosticsInput',
                                'DNSLookupDiagnosticsOutput']
        elif path == 'Device.SelfTest.':
            # XXX this object doesn't exist
            component_names += ['SelfTestDiagnosticsOutput']
        elif path == 'Device.Ethernet.':
            component_names += ['SendMagicPacketInput']
        elif path == 'Device.PacketCapture.':
            # XXX this object doesn't exist
            component_names += ['PacketCaptureDiagnosticsInput',
                                'PacketCaptureDiagnosticsOutput']
        elif path == 'Device.PDU.':
            component_names += ['s-nssai']
        elif path == 'Device.WWC.':
            component_names += ['guti', 's-nssai']

        return component_names

    def _datatype_names(self, path, component_names):
        # search for datatypes referenced by objects matching this path
        regex = r'\s*<dataType\s+(?:ref|base)="(\w+)"'
        datatype_names = []
        name = self._get_toplevel_name(path)
        for path_, lines in self.objcomps:
            name_ = self._get_toplevel_name(path_)
            if name_ == name:
                for line in lines:
                    match = re.match(regex, line)
                    if match:
                        datatype_name = match.group(1)
                        if datatype_name not in datatype_names:
                            datatype_names += [datatype_name]

        # also need to search the components
        for component_name in component_names:
            lines = [l for n, l in self.components if n == component_name][0]
            for line in lines:
                match = re.match(regex, line)
                if match:
                    datatype_name = match.group(1)
                    if datatype_name not in datatype_names:
                        datatype_names += [datatype_name]

        return datatype_names

    def _profile_names(self, path):
        # helper for deferring profile inclusion
        # XXX could avoid the need for this by cleverer logic
        def defer(nam, prof):
            return (nam, prof) in (('Ethernet', 'ProviderBridge:1'),
                                   ('Routing', 'QoS:1'),
                                   ('Routing', 'QoS:2'))

        # search for profiles referenced by objects matching this path
        name = self._get_toplevel_name(path)
        profile_names = []
        referenced_profiles = set()
        for profile_name, lines in self.profiles:
            base_profiles = set()
            for line in lines:
                # profile base/extends
                # XXX won't find both base and extends but there aren't any
                match = re.match(r'\s*<profile.+(?:base|extends)="(['
                                 r'\w_:\s]+)"', line)
                if match:
                    base_profiles |= set(match.group(1).split())

                # object reference
                match = re.match(r'\s*<object\s+ref="([\w{}.]+)"', line)
                if match:
                    path_ = match.group(1)
                    name_ = self._get_toplevel_name(path_)
                    if name_ == name:
                        if profile_name not in self.all_profile_names and \
                                not defer(name, profile_name):
                            self.all_profile_names |= {profile_name}
                            profile_names += [profile_name]
                            referenced_profiles |= base_profiles

        # XXX have to hack QoS:2 into QoS (it's not otherwise referenced)
        if path == 'Device.QoS.':
            referenced_profiles |= {'QoS:2'}

        # also have to check referenced profiles
        # XXX this doesn't catch next-level references; are there any?
        if referenced_profiles:
            for referenced_profile in referenced_profiles:
                if referenced_profile not in self.all_profile_names and not \
                        defer(name, referenced_profile):
                    self.all_profile_names |= {referenced_profile}
                    profile_names += [referenced_profile]

        # remove _Baseline:n from the root object
        if path == 'Device.':
            for profile_name in ['_Baseline:1', '_Baseline:2', '_Baseline:3']:
                profile_names.remove(profile_name)

        return profile_names

    def _output_top_lines(self, fd, path, datatype_names, component_names,
                          *, cname=None):
        data = self._data
        lines = []
        lines += data['file-top']
        lines += self._comment_lines(cname=cname, section='top')
        lines += self._copyright_lines(path)
        lines += self._comment_lines(cname=cname, section='bottom')
        lines += self._document_lines(cname=cname)
        lines += self._import_lines(datatype_names, cname=cname)
        lines += self._datatype_lines(datatype_names)
        lines += self._template_lines(path, component_names)
        lines += self._component_lines(component_names)
        fd.write(''.join(lines))

    def _output_bottom_lines(self, fd, path):
        data = self._data
        lines = []
        lines += data['document-bottom']
        fd.write(''.join(lines))

    def _comment_lines(self, *, cname=None, section=None):
        assert section and section in {'top', 'bottom'}
        common = cname and cname.lower() == 'common'
        lines = []
        ignore = False
        for line in self._data['comment-%s' % section]:
            # initial line
            if cname:
                line = line.replace('[COMMON]', '[%s]' % cname)

            # issue history is ignored until next empty line
            # (but only if there's a cname)
            ignore_this = ignore
            if cname and not common and re.search(r'\s*Issue History', line):
                ignore = True
            elif ignore and line.strip() == '':
                ignore = False
                ignore_this = True

            # XXX ignore_this is all about avoiding two consecutive blank lines
            if not ignore and not ignore_this:
                lines += [line]
        return lines

    def _copyright_lines(self, path):
        copyright_paths = {'Device.BulkData.', 'Device.WiFi.'}
        return self._data[
            'copyrights'] if path and path in copyright_paths else []

    def _document_lines(self, *, cname=None):
        common = cname and cname.lower() == 'common'
        suffix = '-%s' % cname.lower() if cname else ''
        lines = []
        ignore = False
        for line in self._data['document-top']:
            # file and spec (don't capture -common or -common-old)
            match = re.match(r'''
                (?P<before>\s*spec=")
                (?P<spec>[^"]+)-common(-old)?
                (?P<between>".*file=")
                (?P<file>[^.]+)-common(-old)?
                (?P<after>.*)
                ''', line, re.VERBOSE)
            if match:
                line = '%s%s%s%s%s%s%s' % (
                    match.group('before'), match.group('spec'), suffix,
                    match.group('between'), match.group('file'), suffix,
                    match.group('after'))

            # description (ignore it and what follows)
            # XXX but retain it in the common file
            # XXX but insert a blank line just because it looks better
            if not common and re.match(r'\s*<description>', line):
                lines += ['\n']
                ignore = True

            if not ignore:
                lines += [line]
        return lines

    def _import_lines(self, datatype_names, *, cname=None):
        datatype_names = datatype_names or []
        lines = []
        for line in self._data['imports']:
            match = re.match(r'\s*<dataType\s+name="(\w+)"', line)
            if not match or match.group(1) in datatype_names:
                lines += [line]

        # add import of Root component (unless this is the root or common file)
        # XXX the common file does import root, but this happens automatically
        if cname and cname.lower() not in {'root', 'common'}:
            lines += ['  <import file="tr-181-2-root.xml" '
                      'spec="urn:broadband-forum-org:tr-181-2-14-root">\n']
            lines += ['    <component name="Root"/>\n']
            lines += ['  </import>\n']
            lines += ['\n']

        return lines

    def _datatype_lines(self, datatype_names):
        datatype_names = datatype_names or []
        return [l for n, v in self.datatypes if n in datatype_names for l in v]

    def _template_lines(self, path, component_names):
        component_names = component_names or []

        # special case: if no path return an empty list
        if not path:
            return []

        # search for templates referenced by objects matching this path
        template_names = []
        name = self._get_toplevel_name(path)

        for path_, lines in self.objcomps:
            name_ = self._get_toplevel_name(path_)
            # if it's a component, need to search the component's lines
            # XXX this wouldn't work for nested components, but there are none?
            if name_ in component_names:
                lines = [l for n, l in self.components if n == name_][0]
            if name_ == name or name_ in component_names:
                for template_name, _ in self.templates:
                    for line in lines:
                        if '{{template|%s}}' % template_name in line:
                            if template_name not in template_names:
                                template_names += [template_name]

        # also need to search the used templates' lines
        for line in [l for n, v in self.templates if n in template_names for
                     l in v]:
            # XXX this won't find multiple template references in a line
            match = re.search(r'{{template\|(\w+)}}', line)
            if match:
                template_name = match.group(1)
                if template_name not in template_names:
                    template_names += [template_name]

        return [l for n, v in self.templates if n in template_names for l in v]

    def _component_lines(self, component_names):
        component_names = component_names or []
        return [l for n, v in self.components if n in component_names for l
            in v]

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def datatypes(self):
        return [(k[0], v) for k, v in self._data.get('datatypes', {}).items()]

    @property
    def templates(self):
        return [(k[0], v) for k, v in self._data.get('templates', {}).items()]

    @property
    def components(self):
        return [(k[0], v) for k, v in self._data.get('components', {}).items()]

    @property
    def objcomps(self):
        return [(k[0], v) for k, v in self._data.get('objcomps', {}).items()]

    @property
    def objects(self):
        return [(n, v) for n, v in self.objcomps if n.endswith('.')]

    @property
    def toplevel_objects(self):
        # special cases for 'Device.', to ignore 'Device.Services.' and to
        # include 'Device.InterfaceStack.{i}.'
        return [(n, o) for n, o in self.objects if n == 'Device.' or (
                len(n.split('.')) == 3 and n != 'Device.Services.') or (
                        len(n.split('.')) == 4 and n.endswith('{i}.'))]

    @property
    def profiles(self):
        return [(k[0], v) for k, v in self._data.get('profiles', {}).items()]

    @property
    def profile_names(self):
        return {n for n, _ in self.profiles}

    def __str__(self):
        return self._filename

    __repr__ = __str__


def main(argv=None):
    if argv is None:
        argv = sys.argv

    default_loglevel = 0

    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(prog=prog_basename, description=__doc__,
                                     fromfile_prefix_chars='@',
                                     formatter_class=formatter_class)

    parser.add_argument("-l", "--loglevel", type=int, default=default_loglevel,
                        help="logging level; default: %r" % default_loglevel)

    args = parser.parse_args(argv[1:])

    # XXX could/should replace these with arguments
    filename = '../device2/tr-181-2-common-old.xml'

    loglevel_map = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}
    logging.basicConfig(level=loglevel_map[args.loglevel])

    # process the file
    file = File(filename)

    # generate a file for each top-level object, e.g. "Device." and
    # "Device.IP."
    # XXX this should be a File method?
    for toplevel_object in file.toplevel_objects:
        file.output_toplevel_object(toplevel_object)

    # generate a version of the input file
    file.output_common()

    # check all profiles have been output
    # XXX should do the same for everything else
    missing_profile_names = File.all_profile_names - set(file.profile_names)
    if missing_profile_names:
        logger.error('not output %r profiles' % sorted(list(
                missing_profile_names)))

if __name__ == '__main__':
    sys.exit(main())
