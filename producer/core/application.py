#!/usr/bin/python
# -*- coding:utf-8 -*-

from boto3 import resource, client
from json import dumps


class DatabaseNotification:

    def __init__(self, **kwargs):
        self.__dynamoDB = resource('dynamodb').Table(kwargs['table_name'])

    def get_topic(self, name: str, hash_key: str) -> list:
        result = self.__dynamoDB.get_item(
            Key={
                'Id': hash_key,
                'Name': name
            },
            AttributesToGet=[
                'Integrations'
            ]
        )

        if 'Item' not in result:
            return

        return result['Item']['Integrations']


class QueueNotification:

    def __init__(self, **kwargs):
        self.__sqs = client('sqs')
        self.__url = kwargs['url']

    def sent_message(self, message: dict) -> bool:
        result = self.__sqs.send_message(
            QueueUrl=self.__url,
            MessageBody=dumps(message)
        )

        return result['MessageId']
