from app.core.security import hash_password
from app.core.jwt import create_access_token


class AuthService:

    def register(self, user):

        hashed = hash_password(user.password)

        return {
            "username": user.username,
            "email": user.email,
            "password": hashed
        }

    def login(self, email):

        token = create_access_token(
            {
                "sub": email
            }
        )

        return token