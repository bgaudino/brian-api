# Generated by Django 4.0.6 on 2022-09-04 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_item_iteminstance_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iteminstance',
            name='name',
        ),
    ]