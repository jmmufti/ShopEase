# Generated by Django 5.0.6 on 2024-11-19 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='genre',
            field=models.CharField(choices=[('clothing', 'Clothing'), ('personal_accessories', 'Personal Accessories'), ('ornamentation', 'Ornamentation')], default='clothing', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='F:\\ShopEase\\shopease\templates', upload_to='products/'),
        ),
    ]
