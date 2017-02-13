import models
from Crypto.Cipher import AES


def uid_check(uid):
    if models.User.select().where(models.User.username == uid).exists():
        uid = models.User.get(models.User.username == uid).uid
    elif models.User.select().where(models.User.uid == uid).exists():
        pass
    else:
        raise models.DoesNotExist
    return uid


def encrypt(key, iv, text):
    # Encryption
    encryption_suite = AES.new(key, AES.MODE_CFB, iv)
    text = encryption_suite.encrypt("A not really secret message. Not for prying eyes.")
    return text


def decrypt(key, iv, text):
    # Decryption
    decryption_suite = AES.new(key, AES.MODE_CFB, iv)
    text = decryption_suite.decrypt(text)
    return text
