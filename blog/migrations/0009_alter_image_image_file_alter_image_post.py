# Generated by Django 5.1.4 on 2025-02-07 13:37

import django.db.models.deletion
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=75, scale=None, size=[500, 500], upload_to='post_images/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.post', verbose_name='پست'),
        ),
    ]
