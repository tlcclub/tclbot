#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Messages(object):
    """docstring for Messages"""
    def __init__(self, arg:str = None):
        super(Messages, self).__init__()
        self.arg = arg
    
    def sell(self, user) -> str:
        
        """Returns a message about wind direction and speed"""
        return f'Запускаем мастер настройки породажи, {user.username}'
    
    
