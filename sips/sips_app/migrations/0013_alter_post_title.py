# Generated by Django 4.2.7 on 2023-12-17 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sips_app', '0012_remove_comment_likes_remove_post_likes_comment_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]