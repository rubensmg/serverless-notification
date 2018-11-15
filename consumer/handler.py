#!/usr/bin/python
# -*- coding:utf-8 -*-

from integrations import factory
from json import loads

def main(event, context):

    try:
        message = loads(event['Records'][0]['body'])
        with factory(message['configuration']['name'], **message['configuration']['credentials']) as instance:
            message_delivered = instance.send(message['message'])
            if not message_delivered:
                raise IOError(f'Error to delivery message')
            return "Message delivered"
    except Exception as ex:
        raise Exception(f'An error occurs while processing the request (Message: {str(ex)})')
