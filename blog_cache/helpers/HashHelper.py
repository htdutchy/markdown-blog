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
