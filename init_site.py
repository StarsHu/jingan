# coding=utf-8


def init_db():

    from models import database
    from models import User, Group

    Group.create_table(True)
    admin_group, created = Group.get_or_create(name="管理员")
    salesmanager_group, created = Group.get_or_create(name="销售人员")
    warehousekeeper_group, created = Group.get_or_create(name="仓库管理员")

    User.create_table(True)
    User.get_or_create(
        name="cula",
        defaults={
            'password': User.encode_raw_password('123456'),
            'group_id': admin_group.id
        }
    )

    database.close()
