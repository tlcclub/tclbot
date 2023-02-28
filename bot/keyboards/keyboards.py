#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BTN_PLACE_SELL = InlineKeyboardButton('Продать', callback_data='sell')
BTN_PLACE_BUY = InlineKeyboardButton('Купить', callback_data='buy')
BTN_DONE = InlineKeyboardButton('Закончить', callback_data='done')

SELL = InlineKeyboardMarkup().add(BTN_PLACE_SELL)
BUY = InlineKeyboardMarkup().add(BTN_PLACE_BUY)
HELP = InlineKeyboardMarkup().add(BTN_PLACE_SELL) # .add(BTN_PLACE_BUY)

DONE = InlineKeyboardMarkup().add(BTN_DONE)
