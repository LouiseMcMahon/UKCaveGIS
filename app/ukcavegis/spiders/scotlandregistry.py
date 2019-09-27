# -*- coding: utf-8 -*-

from ukcavegis.spiders.mattvoyseyregistry import MattVoyseyRegistry

class ScotlandRegistry(MattVoyseyRegistry):
    name = 'scotlandregistry'
    allowed_domains = ['registry.gsg.org.uk']
    start_urls = ['http://registry.gsg.org.uk/sr/browse.php']
    registry = 'Scotland'
