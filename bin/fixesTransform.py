# XXX should allow transform to consist only of top-level functions, and
#     auto-create a Transform class (or equivalent)

# XXX should support other pandoc-like features, e.g. wrt return values

# XXX plugindirs should automatically include current dir (and others)?

# XXX should relax plugin naming conventions (not require xxxTransform.py)

# XXX should auto-register the Transform, even when class is created manually

from bbfreport.node import Model, Object, Profile
from bbfreport.transform import Transform


class FixesTransform(Transform):
    @staticmethod
    def _visit_Object(node: Object):
        object_version_inherited = node.object_version_inherited
        if not node.version and node.name and object_version_inherited and \
                not node.instance_in_path(('command', 'event')):
            print('%s %s version MUST be set to %s' % (
                node.typename, node.objpath, object_version_inherited))
            #node.version = object_version_inherited

        # only the most specific function is invoked
        # XXX is this the correct behavior?
        FixesTransform._visit__HasDescriptionNameAndBase(node)

    @staticmethod
    def _visit_Profile(node: Profile):
        version_inherited = node.version_inherited
        if not node.version and version_inherited:
            print('%s %s version MUST be set to %s' % (
                node.typename, node.objpath, version_inherited))
            #node.version = version_inherited

    # XXX there should be a better (logical) base class than this
    @staticmethod
    def _visit__HasDescriptionNameAndBase(node):
        # base will only be defined when using --thisonly
        if node.version and node.base:
            # (node.base or node.parent.instance_in_path(('command', 'event')))
            print('%s %s version MUST be removed' % (
                node.typename, node.objpath))
            #node.version = None

        # parent node version, potentially inherited
        parent_version_inherited = node.parent.object_version_inherited if \
            isinstance(node.parent, Object) else node.parent.version_inherited

        # object versions can only be removed if they're command/event args
        is_model_object = isinstance(node, Object) and \
            not node.instance_in_path(('command', 'event'))

        if node.version and node.version == parent_version_inherited and \
                not is_model_object:
            if 0: print('%s %s version MAY be removed' % (
                node.typename, node.objpath))


FixesTransform.register()
