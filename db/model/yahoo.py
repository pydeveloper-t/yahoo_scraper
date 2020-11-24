from db import metadata
from sqlalchemy import func, text, UniqueConstraint
from sqlalchemy import Table, Column, String, TIMESTAMP
from sqlalchemy.dialects.mysql import BIGINT, DATE, DECIMAL, TEXT, VARCHAR

yahoo_historical = Table('yahoo_historical', metadata,
                Column('id', BIGINT(20), primary_key=True, autoincrement=True),
                Column('Date', DATE(),nullable=False, index=True),
                Column('Symbol', String(32), nullable=False, index=True),
                Column('Open', DECIMAL(12, 4), nullable=False),
                Column('High', DECIMAL(12, 4), nullable=False),
                Column('Low', DECIMAL(12, 4), nullable=False),
                Column('Close', DECIMAL(12, 4), nullable=False),
                Column('Adj Close', DECIMAL(12, 4), nullable=False),
                Column('Volume', DECIMAL(12, 4), nullable=False),
                Column('3day_before_change', DECIMAL(12, 4), nullable=False),
                Column('created_at', TIMESTAMP, nullable=False, server_default=func.now()),
                Column('updated_at', TIMESTAMP, nullable=False,
                       server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), index=True),
                UniqueConstraint('Symbol', 'Date', name='symbol_date_uniq')
          )

yahoo_news = Table('yahoo_news', metadata,
                Column('id', BIGINT(20), primary_key=True, autoincrement=True),
                Column('Symbol', String(32), nullable=False, index=True),
                Column('Link', VARCHAR(1024),nullable=False),
                Column('Title', TEXT(), nullable=False),
                Column('created_at', TIMESTAMP, nullable=False, server_default=func.now()),
                Column('updated_at', TIMESTAMP, nullable=False,
                       server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), index=True),
                UniqueConstraint('Link', name='link_uniq')
          )




