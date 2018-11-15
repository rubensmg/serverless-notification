#!/usr/bin/python
# -*- coding:utf-8 -*-

from core import DatabaseNotification
from core import QueueNotification
from functools import reduce


def main(event, context):
    try:
        configuration = event['configuration']
        parameters = event['parameters']

        database = DatabaseNotification(**configuration['dynamodb'])
        list_integrations = database.get_topic(
            name=parameters['topic']['name'],
            hash_key=parameters['topic']['hash_key']
        )

        queue = QueueNotification(**configuration['sqs'])

        if not list_integrations:
            raise TypeError(
                'The topic %s dont exists' %
                parameters['topic']['name']
            )

        list_messages_sent = [queue.sent_message(
            {
                'configuration': {
                    'name': integration['name'],
                    'credentials': integration['configuration']
                },
                'message': reduce(lambda acc, cur: acc.replace(f'${cur}', str(parameters['message'][cur])), parameters['message'], integration['model'])
            }
        ) for integration in list_integrations]

        return {
            list_integrations[iterator]['name']: list_messages_sent[iterator]
            for iterator in range(0, len(list_messages_sent))
        }

    except Exception as ex:
        raise Exception(
            f'An error occurs while processing the request (Message: {str(ex)})'
        )