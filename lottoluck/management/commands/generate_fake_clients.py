from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lottoluck.models import Clientes
from django.core.files import File
import os
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake Clientes data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Clearing existing Clientes data...'))
        
        # Elimina todos los registros de Clientes existentes
        #Clientes.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Generating fake Clientes data...'))

        # Obtén la ruta completa de la imagen por defecto
        default_image_path = 'media/clientes/foto.png'

        # Asegúrate de que la imagen por defecto exista en la ruta especificada
        if os.path.exists(default_image_path):
            default_image = File(open(default_image_path, 'rb'))

            for _ in range(100):  # Cambia 53 por la cantidad de clientes falsos que desees crear
                user = User.objects.create_user(
                    username=fake.user_name(),
                    password=fake.password(),
                    email=fake.email(),
                )

                Clientes.objects.create(
                    user=user,
                    cedula=fake.random_int(min=1000000, max=9999999),
                    nombre=fake.first_name(),
                    apellido=fake.last_name(),
                    gender=fake.random_element(elements=('Male', 'Female')),
                    direccion=fake.address(),
                    email=user.email,
                    telefono=fake.phone_number(),
                    birthdate=fake.date_of_birth(minimum_age=18, maximum_age=80),
                    imagen=default_image,  # Asigna la imagen por defecto
                    tipocliente=fake.random_element(elements=(0, 1, 2)),  # Personaliza tus opciones aquí
                    date_creado=fake.date_time_this_decade(),
                )

                self.stdout.write(self.style.SUCCESS(f'Created Clientes: {user.username}'))

            self.stdout.write(self.style.SUCCESS('Fake Clientes data generation completed.'))
        else:
            self.stdout.write(self.style.ERROR('Default image not found at the specified path.'))
