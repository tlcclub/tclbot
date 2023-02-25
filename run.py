#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram import executor
from bot import dp
from bot.middleware import AlbumMiddleware

if __name__ == '__main__':
    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)
