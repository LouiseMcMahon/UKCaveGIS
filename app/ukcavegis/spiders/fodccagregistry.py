# -*- coding: utf-8 -*-

from ukcavegis.spiders.mattvoyseyregistry import MattVoyseyRegistry

class FodccagRegistry(MattVoyseyRegistry):
    name = 'fodccagregistry'
    allowed_domains = ['fodccag.org.uk']
    start_urls = ['http://www.fodccag.org.uk/registry/browse.php']
    registry = 'GloucestershireAndWye'
