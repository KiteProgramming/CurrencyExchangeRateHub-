from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet

cipher_suite = Fernet(settings.ENCRYPTION_KEY)

class EncryptedCharField(models.CharField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return cipher_suite.decrypt(value.encode()).decode()

    def get_prep_value(self, value):
        if value is None:
            return value
        return cipher_suite.encrypt(value.encode()).decode()