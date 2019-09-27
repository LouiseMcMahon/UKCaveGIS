# -*- coding: utf-8 -*-

from ukcavegis.spiders.mattvoyseyregistry import MattVoyseyRegistry

class DcaRegistry(MattVoyseyRegistry):
    name = 'dcaregistry'
    allowed_domains = ['registry.thedca.org.uk']
    start_urls = ['https://registry.thedca.org.uk/registry/browse.php']
    registry = 'Derbyshire'
