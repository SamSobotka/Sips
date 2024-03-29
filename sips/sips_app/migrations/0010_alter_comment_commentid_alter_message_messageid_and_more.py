# Generated by Django 4.2.7 on 2023-12-13 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sips_app', '0009_alter_user_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentid',
            field=models.BigAutoField(db_column='commentID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='messageid',
            field=models.BigAutoField(db_column='messageID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='postid',
            field=models.BigAutoField(db_column='postID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transactionid',
            field=models.BigAutoField(db_column='transactionID', primary_key=True, serialize=False),
        ),
    ]
