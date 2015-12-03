# coding=utf-8

from tornado.gen import coroutine


@coroutine
def init_db():

    from models import User, Role

    role_admin = yield Role.objects.get(key='admin')
    if not role_admin:
        role_admin = yield Role(key='admin', name="管理员").save()

    role_salesmanager = yield Role.objects.get(key='salesmanager')
    if not role_salesmanager:
        Role(key='salesmanager', name="销售人员").save()

    role_warehousekeeper = yield Role.objects.get(key='warehousekeeper')
    if not role_warehousekeeper:
        Role(key='warehousekeeper', name="仓库管理员").save()

    user_admin = yield User.objects.get(
        name='admin', role_id=str(role_admin._id))
    if not user_admin:
        User(
            name="admin",
            password=User.encode_raw_password('jingan'),
            role_id=str(role_admin._id),
            status='ACTIVE'
        ).save()
