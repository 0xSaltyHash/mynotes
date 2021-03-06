# Generated by Django 3.2.7 on 2021-11-25 02:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_notes_is_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_date_time', models.DateTimeField(auto_now_add=True)),
                ('favorite_note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.notes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
