from django.core.management.base import BaseCommand
from django.conf import settings
from requests import get
from core.models import ProductorProfile, MyImage, Address, Product, ProductCategory
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
        addresses = []
        print("extracting address")
        with open('list_address.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            
            for row in readCSV:
                address = {}
                address['street'] = row[0]
                address['street_cp'] = "NA"
                address['city'] = row[2]
                address['province'] = row[2]
                address['postal_code'] = row[1]
                address['country'] = row[3]
                addresses.append(address)

        print("creating profile..")
        for i in range(20):
            productor_name = f'productor{i}'
            print(".." + productor_name)
            user= User.objects.create_user(email=f'bot{i}@bot.com', username=f'bot{i}', password="bot123456789", is_productor=True)
            user.mail_confirmed = True
            address_data = addresses[i % len(addresses)]
            address = Address.objects.create(**address_data)

            productor_profile_data= {
                "rating": i % 6,
                "name": productor_name,
                "bio": lorem.paragraph(),
                "address": address
            }
            productor_profile = ProductorProfile.objects.create(user=user, **productor_profile_data)
            user.productor_profile = productor_profile
            user.save()
            for i in range(3):
                nb = randint(0,50)
                url = f'https://picsum.photos/1024/480/?image={nb}'
                response = get(url)
                filename = f'media/profile-{productor_name}-{nb}.jpg'
                with open(filename, "wb") as f:
                    f.write(response.content)

                reopen = open(filename, "rb")
                picture = MyImage(file=File(reopen), name=filename)
                picture.save()
                productor_profile.pictures.add(picture)
                time.sleep(1)
            time.sleep(1.0)

        
        print("creating article for ... ")
        for productor in ProductorProfile.objects.all():
            print("..." + productor.name)
            nb_articles = randint(1,4)
            
            for i in range(nb_articles):

                nb = randint(50, 200)
                url = f'https://picsum.photos/600/400/?image={nb}'
                response = get(url)
                filename = f'media/{productor_name}-{i}.jpg'
                with open(filename, "wb") as f:
                    f.write(response.content)
                
                reopen = open(filename, "rb")
                picture = File(reopen)
                
                is_deliverable =  randint(0,1) == 1
                is_pickup =  randint(0,1) == 1
                product  = Product(name=f'article-{i}-{productor.name}', product_code=f'{i}:{productor.name}', price=randint(1,100), quantity=randint(1,10), rating = random()*6.0, category=ProductCategory.choices()[randint(0,3)][0], description=lorem.sentence(), is_deliverable=is_deliverable, delivery_time_days=randint(7,14), creator=productor)
                product.picture = picture
                product.save()
                
                time.sleep(1)