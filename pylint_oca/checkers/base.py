
'''
Inherit core checkers to change function.
'''

import os

from pylint.checkers import utils
from pylint.checkers.base import BasicChecker
from pylint.interfaces import IAstroidChecker

from .. import settings

OCA_MSGS = {
    'W%d01' % settings.BASE_CORE_ID: (
        # Disabled in manifest files
        'Statement seems to have no effect. Core msg-id W0104',
        'oca-pointless-statement',
        'Used when a statement doesn\'t have (or at least seems to) '
        'any effect.'
    ),
}


class CustomBasicChecker(BasicChecker):
    __implements__ = IAstroidChecker

    def __init__(self, *args, **kwargs):
        super(CustomBasicChecker, self).__init__(*args, **kwargs)
        self.msgs = OCA_MSGS
        self.options = ()
        self.reports = ()

    def open(self):
        super(CustomBasicChecker, self).open()
        # Enable stats for other check different to enabled here
        kwargs = {
            'pointless_statement': 0,
        }
        self.stats = self.linter.add_stats(**kwargs)

    @utils.check_messages('oca-pointless-statement')
    def visit_discard(self, node):
        '''Check pointless-statement in all py files except manifest files
        A manifest file have a dict pointless.
        '''
        if os.path.basename(self.linter.current_file) not in \
                settings.MANIFEST_FILES:
            self.linter.enable('pointless-statement')
            res = super(CustomBasicChecker, self).visit_discard(node)
            self.linter.disable('pointless-statement')
            return res