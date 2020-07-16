from django.db import models

# Create your models here.

class MailingList(models.Model):
    email = models.EmailField(db_index=True, unique=True)