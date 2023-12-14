# Generated by Django 4.2.7 on 2023-12-08 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sips_app', '0007_item_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commentid',
            field=models.BigAutoField(db_column='commentID', default=3000000000, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='messageid',
            field=models.BigAutoField(db_column='messageID', default=5000000000, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='postid',
            field=models.BigAutoField(db_column='postID', default=2000000000, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transactionid',
            field=models.BigAutoField(db_column='transactionID', default=4000000000, primary_key=True, serialize=False),
        ),
    ]
