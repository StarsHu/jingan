# coding=utf-8


def init_db():

    from models import database
    from models import User, Group

    Group.create_table(True)
    admin_group, created = Group.get_or_create(name="admin")

    User.create_table(True)
    User.get_or_create(
        name="cula",
        defaults={
            'password': '123456',
            'group_id': admin_group.id
        }
    )

    database.close()
