# -*- coding: utf-8 -*-

from ukcavegis.spiders.mattvoyseyregistry import MattVoyseyRegistry

class DucRegistry(MattVoyseyRegistry):
    name = 'ducregistry'
    allowed_domains = ['dcuc.org.uk']
    start_urls = ['https://dcuc.org.uk/registry/r/browse.php']
    registry = 'DevonAndCornwall'
