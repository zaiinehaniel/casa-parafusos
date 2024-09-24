import jwt
from datetime import datetime, timedelta

# Secret key for encoding/decoding the JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


def create_jwt_token(data: dict):
    """
    Creates a JWT token with an expiration time.
    :param data: Payload data to encode in the token
    :return: JWT token as a string
    """
    to_encode = data.copy()
    # Set the token to expire in 30 minutes
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})

    # Encode the token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
