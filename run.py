#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram import executor
from bot import dp

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
