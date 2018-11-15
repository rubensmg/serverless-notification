#!/usr/bin/python
# -*- coding:utf-8 -*-

from integrations.integration import IntegrationBase

def factory(name, **kwargs):
    list_integrations = [integration for integration in IntegrationBase.__subclasses__() if name == integration.name]

    if len(list_integrations) != 1:
        raise TypeError(f'The integration ${name} does not exists')
    
    return list_integrations[0](**kwargs)
