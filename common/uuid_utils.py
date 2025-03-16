import uuid


def get_uuid_str():
    return str(uuid.uuid4()).replace("-", "")


def get_default_id():
    return "00000000000000000000000000000000"


if __name__ == '__main__':
    print(get_uuid_str())

