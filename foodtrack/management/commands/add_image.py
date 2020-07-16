from django.core.management.base import BaseCommand
from django.conf import settings
from requests import get
from core.models import ProductorProfile,UserProfile,  MyImage, Address, Product, ProductCategory
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.files import File
import shutil
import time
from random import randint, random
import lorem
import csv


class Command(BaseCommand):
    help = 'A description of your command'

    def handle(self, *args, **options):

        print("adding  profile picture..")
        for index, user_profile in enumerate(UserProfile.objects.all()):
            print(index)
            url = f'https://i.pravatar.cc/300/{index}'
            response = get(url)
            filename = f'media/profile-picture-{user_profile.user.username}.jpg'
            with open(filename, "wb") as f:
                f.write(response.content)

            reopen = open(filename, "rb")
            picture = File(reopen)
            user_profile.picture=picture
            user_profile.save()
            time.sleep(1)
