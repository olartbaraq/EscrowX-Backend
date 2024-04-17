import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication  # type: ignore
from rest_framework.exceptions import AuthenticationFailed  # type: ignore
from django.conf import settings  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from datetime import datetime, timedelta

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = self.extract_token(request=request)
        if token is None:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            self.verify_token(payload=payload)

            user_id = payload["id"]
            user = User.objects.get(id=user_id)
            return (user, None)
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid Token")

    def verify_token(self, payload):
        if "exp" not in payload:
            raise InvalidTokenError("no expiration token, Invalid")

        exp_timestamp = payload["exp"]
        current_timestamp = datetime.utcnow().timestamp()

        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token has expired")

    def extract_token(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None

    @staticmethod
    def generate_token(payload):
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload["exp"] = expiration
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return token
