import models


def uid_check(uid):
    if models.User.select().where(models.User.username == uid).exists():
        uid = models.User.get(models.User.username == uid).uid
    elif models.User.select().where(models.User.uid == uid).exists():
        pass
    else:
        raise models.DoesNotExist
    return uid
