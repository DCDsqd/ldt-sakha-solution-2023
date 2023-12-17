from sqlalchemy import Column, String, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class YtTable(Base):
    __tablename__ = 'yt_cache'
    id = Column(String, primary_key=True)
    value = Column(JSON)


class VkTable(Base):
    __tablename__ = 'vk_cache'
    id = Column(Integer, primary_key=True)
    value = Column(JSON)


class TgTable(Base):
    __tablename__ = 'tg_cache'
    id = Column(Integer, primary_key=True)
    value = Column(JSON)
