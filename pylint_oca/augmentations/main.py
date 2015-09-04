
import os

from pylint_plugin_utils import suppress_message
from pylint.checkers.base import BasicChecker
from .. import settings


def is_manifest_file(node):
    filename = os.path.basename(node.root().file)
    is_manifest = filename in settings.MANIFEST_FILES
    return is_manifest


def apply_augmentations(linter):
    """Apply suppression rules."""

    # W0104 - pointless-statement
    # manifest file have a valid pointless-statement dict
    suppress_message(linter, BasicChecker.visit_discard,
                     'W0104', is_manifest_file)