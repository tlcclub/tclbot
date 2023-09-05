#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import os
import pathlib
import sys
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Bot:
    token: str
    trade_chat_id: int
    admin_id: int


@dataclass
class DatabaseConfig:
    host: str
    port: int
    dbname: str
    username: str
    password: str
    driver: str


@dataclass
class Config:
    bot: Bot
    db: DatabaseConfig = None


def init_config() -> Config:
    config = Config
    try:
        if path := os.getenv("TLC_BOT_CONFIG", None) is None:
            raise ValueError
        path = pathlib.Path(path)
        cfg = configparser.ConfigParser()
        cfg.read(path)
        config.bot = Bot(**cfg.get("bot"))
        if cfg.get("database"):
            config.db = DatabaseConfig(**cfg.get("db"))
    except ValueError:
        config = load_envs(config)
    return config


mapping = dict(
    db=DatabaseConfig,
    bot=Bot
)


def load_envs(config: Config) -> Config:
    load_dotenv()

    envs = dict([
      (k, v) for k, v in os.environ.items() if k.lower().startswith("tlc")])
    print(61, envs)
    try:
        if len(envs) == 0:
            raise KeyError
    except KeyError:
        sys.exit("Error while setting config")

    if 'TLC_DATABASE' in envs.keys():
        db = dict([
          ("_".join(k.lower().split('_')[2:]), v)
          for k, v in envs.items() if k.lower().startswith('tlc_database')])
        setattr(config, 'db', mapping.get('db')(**db))
    bot = dict([
      ("_".join(k.lower().split('_')[2:]), v)
      for k, v in envs.items() if k.lower().startswith('tlc_bot')])
    print(bot)

    setattr(config, 'bot', mapping.get('bot')(**bot))

    return config
