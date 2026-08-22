import bcrypt


def hash(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
