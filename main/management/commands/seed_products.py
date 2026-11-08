import os
from django.core.management.base import BaseCommand
from main.models import Product

class Command(BaseCommand):
    help = 'Seed the database with sample products'

    def handle(self, *args, **kwargs):
        products_data = [
            {
                'name': 'Casual Denim Jacket',
                'description': 'Premium quality cotton denim jacket suitable for all seasons.',
                'price': 49.99,
                'genre': 'clothing',
                'image': 'products/Screenshot_2024-10-07_042554.png'
            },
            {
                'name': 'Classic Leather Wallet',
                'description': 'Genuine leather bi-fold wallet with multiple card slots and RFID protection.',
                'price': 24.50,
                'genre': 'personal_accessories',
                'image': 'products/Screenshot_2024-11-19_173252.png'
            },
            {
                'name': 'Wireless Noise-Canceling Earbuds',
                'description': 'High-fidelity Bluetooth earbuds with active noise cancellation and 24h battery life.',
                'price': 79.99,
                'genre': 'gadgets',
                'image': 'products/Screenshot_2024-11-19_173530.png'
            },
            {
                'name': 'Silver Elegance Pendant',
                'description': 'Sterling silver crafted necklace with a polished minimalist pendant.',
                'price': 34.00,
                'genre': 'ornamentation',
                'image': 'products/Screenshot_2024-11-19_191021.png'
            },
            {
                'name': 'Hydrating Facial Care Set',
                'description': 'All-natural botanical extracts cleanser, toner, and moisturizer package.',
                'price': 29.99,
                'genre': 'beauty_personal_care',
                'image': 'products/Screenshot_2024-11-19_191237.png'
            },
            {
                'name': 'Ergonomic Pet Harness & Leash',
                'description': 'Reflective and breathable padded harness designed for dogs and cats.',
                'price': 19.99,
                'genre': 'pet_accessories',
                'image': 'products/Screenshot_2024-11-19_191628.png'
            },
            {
                'name': 'Waterproof Travel Backpack',
                'description': 'Durable multi-compartment travel bag ideal for hiking, camping, and flights.',
                'price': 59.90,
                'genre': 'tour_trips',
                'image': 'products/Screenshot_2024-11-19_193945.png'
            },
            {
                'name': 'Floral Summer Dress',
                'description': 'Lightweight and breathable floral patterned dress with elegant waist cut.',
                'price': 39.99,
                'genre': 'women_clothing',
                'image': 'products/Screenshot_2024-11-20_175116.png'
            },
        ]

        count = 0
        for item in products_data:
            obj, created = Product.objects.get_or_create(
                name=item['name'],
                defaults={
                    'description': item['description'],
                    'price': item['price'],
                    'genre': item['genre'],
                    'image': item['image'],
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} sample products!'))

