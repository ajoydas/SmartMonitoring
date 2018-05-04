# Generated by Django 2.0.3 on 2018-05-04 08:01

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_id', models.IntegerField()),
                ('lat', models.FloatField(null=True)),
                ('lon', models.FloatField(null=True)),
                ('contact_num', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True)),
                ('password', models.CharField(max_length=10, null=True)),
                ('locked', models.BooleanField(default=False)),
                ('tracked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WarningEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=10, null=True)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Position')),
            ],
        ),
        migrations.AddField(
            model_name='position',
            name='tracker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Tracker'),
        ),
    ]
