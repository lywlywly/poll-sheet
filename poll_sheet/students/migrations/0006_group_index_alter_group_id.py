# Generated by Django 4.2.2 on 2024-01-12 07:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0005_alter_poll_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="index",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="group",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
