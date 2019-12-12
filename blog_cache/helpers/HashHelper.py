import hashlib


def md5_file(filepath):
    try:
        md5 = hashlib.md5()
        file = open(filepath, "rb")
        with file as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        file.close()
    except IOError:
        return False

    return md5.hexdigest()


def sha256_file(filepath):
    try:
        sha256 = hashlib.sha256()
        file = open(filepath, "rb")
        with file as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        file.close()
    except IOError:
        return False

    return sha256.hexdigest()


def sha512_file(filepath):
    try:
        sha512 = hashlib.sha512()
        file = open(filepath, "rb")
        with file as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha512.update(chunk)
        file.close()
    except IOError:
        return False

    return sha512.hexdigest()


def md5_string(string):
    md5 = hashlib.md5()
    md5.update(string)
    return md5.hexdigest()


def sha256_string(string):
    sha256 = hashlib.sha256()
    sha256.update(string)
    return sha256.hexdigest()


def sha512_string(string):
    sha512 = hashlib.sha512()
    sha512.update(string)
    return sha512.hexdigest()
