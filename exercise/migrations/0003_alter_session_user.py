# Generated by Django 4.0 on 2021-12-25 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('exercise', '0002_remove_session_end_date_session_finish_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='user.user'),
            preserve_default=False,
        ),
    ]