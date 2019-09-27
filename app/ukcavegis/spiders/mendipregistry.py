# -*- coding: utf-8 -*-

from ukcavegis.spiders.mattvoyseyregistry import MattVoyseyRegistry

class MendipRegistry(MattVoyseyRegistry):
    name = 'mendipregistry'
    allowed_domains = ['www.mcra.org.uk']
    start_urls = ['http://www.mcra.org.uk/registry/browse.php']
    registry = 'Mendip'
