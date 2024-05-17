from orm.db_setup import metadata
from sqlalchemy import (Table, Column, Integer, Text, JSON, String, Enum, ForeignKey, Time, DateTime)

Users = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(255), nullable=True),
    Column('first_name', String(255), nullable=True),
    Column('last_name', String(255), nullable=True),
    Column('avatar', String(255), nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
    Column('deleted_at', DateTime, nullable=True),
)