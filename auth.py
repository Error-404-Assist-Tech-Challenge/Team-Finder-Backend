import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    access_secret = 'SECRET'
    refresh_secret = 'REFRESH'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id, secret, expires_delta):
        payload = {
            'exp': datetime.utcnow() + expires_delta,
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            secret,
            algorithm='HS256'
        )

    def decode_token(self, token, secret):
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials, self.access_secret)

    def refresh_token(self, refresh_token):
        user_id = self.decode_token(refresh_token, self.refresh_secret)
        access_token, _ = self.generate_tokens(user_id)
        return access_token, user_id

    def generate_tokens(self, user_id):
        access_token = self.encode_token(user_id, self.access_secret, timedelta(hours=1))
        refresh_token = self.encode_token(user_id, self.refresh_secret, timedelta(days=1))
        return access_token, refresh_token
