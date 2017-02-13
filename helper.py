import models
from Crypto.Cipher import DES


def uid_check(uid):
    if models.User.select().where(models.User.username == uid).exists():
        uid = models.User.get(models.User.username == uid).uid
    elif models.User.select().where(models.User.uid == uid).exists():
        pass
    else:
        raise models.DoesNotExist
    return uid

def encrypt(key, iv):
    pass


def decrypt(key, iv):
    pass

# Encryption
encryption_suite = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
cipher_text = encryption_suite.encrypt("A not really secret message. Not for prying eyes.")

# Decryption
decryption_suite = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
plain_text = decryption_suite.decrypt(cipher_text)
