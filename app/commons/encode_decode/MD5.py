from hashlib import blake2b

from app.commons.setting import HASH_KEY


def hash_value(string, size=10):
    hl = blake2b(digest_size=size, key=HASH_KEY.encode())
    string = string.encode()  # must be bytes
    hl.update(string)
    return hl.hexdigest()  # str


if __name__ == "__main__":
    print(hash_value('18'))
