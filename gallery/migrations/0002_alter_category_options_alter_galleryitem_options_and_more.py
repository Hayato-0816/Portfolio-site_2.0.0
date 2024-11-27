# Generated by Django 4.2.16 on 2024-11-13 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='galleryitem',
            options={'ordering': ['-created_at'], 'verbose_name': 'Gallery Item', 'verbose_name_plural': 'Gallery Item'},
        ),
        migrations.AlterField(
            model_name='galleryitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='gallery.category', verbose_name='Category'),
        ),
    ]
