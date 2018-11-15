#!/usr/bin/python
# -*- coding:utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from requests import post

class IntegrationBase(metaclass=ABCMeta):

    @abstractproperty
    def name(self):
        pass

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def __enter__(self):
        pass 

    @abstractmethod
    def send(self, message) -> bool:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass


class IntegrationSlack(IntegrationBase):

    name = 'slack'

    def __init__(self, **kwargs):
        self.__credentials = {
            'url': kwargs['url']
        }

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return

    def send(self, message) -> bool:
        with post(self.__credentials['url'], json={ 'text': message }) as response:
            return response.ok
