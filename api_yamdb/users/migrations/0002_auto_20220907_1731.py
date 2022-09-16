# Generated by Django 2.2.16 on 2022-09-07 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="confirmation_code",
            field=models.CharField(
                default="XXXX",
                max_length=255,
                null=True,
                verbose_name="confirmation_code",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("user", "user"),
                    ("admin", "admin"),
                    ("moderator", "moderator"),
                ],
                default="user",
                max_length=20,
                verbose_name="role",
            ),
        ),
    ]
