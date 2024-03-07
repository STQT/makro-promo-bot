# Generated by Django 4.2.9 on 2024-03-04 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promotions", "0006_promotion_conditions_ru_promotion_conditions_uz"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="", verbose_name="Загружаемый отчет")),
                (
                    "report_file",
                    models.FileField(blank=True, null=True, upload_to="", verbose_name="Отчетность ответа"),
                ),
            ],
        ),
    ]
