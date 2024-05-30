import sqlalchemy as sa
from orm.db import Users
from schema.user import User
from datetime import datetime

def insert(session, data:User):
    sql = sa.insert(Users).values(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        avatar=data.avatar,
        created_at=datetime.now()
    )
    insert_user=session.execute(sql)
    session.commit()
    return insert_user

def get_all(session):
    sql = sa.select(Users)
    select_all_user = session.execute(sql)
    return select_all_user

def get_by_id(session,id):
    sql = sa.select(Users).where(Users.c.id==id)
    select_user = session.execute(sql)
    return select_user

def update(session, id, data:User, updated_at):
    sql = sa.update(
        Users
    ).where(
        Users.c.id==id
    ).values(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        avatar=data.avatar,
        updated_at=updated_at
    )
    update_user = session.execute(sql)
    session.commit()
    return update_user

def delete(session, id):
    sql = sa.delete(
        Users
    ).where(
        Users.c.id==id
    )
    deleted_user = session.execute(sql)
    session.commit()
    return deleted_user