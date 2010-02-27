"""Channel model."""

from cement.core.log import get_logger
from cement.core.namespace import get_config

log = get_logger(__name__)
config = get_config()

class Channel(object):
    def __init__(self):
        self.id = None
        self.label = None
        self.name = None
        self.arch_name = None
        self.summary = None
        self.description = None
        self.maintainer_name = None
        self.maintainer_email = None
        self.maintainer_phone = None
        self.support_policy = None
        self.gpg_key_url = None
        self.gpg_key_id = None
        self.gpg_key_fp = None
        self.end_of_life = None
        self.parent_channel_label = None