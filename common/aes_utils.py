import hashlib


def md5_encrypt(password):
    return hashlib.new('md5', bytes(password, encoding='utf-8')).hexdigest()
