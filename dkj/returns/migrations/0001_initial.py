# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('commodities', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnCarrier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='Przewoźnik', help_text='Przewoźnik', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('carrier', models.ForeignKey(to_field='id', verbose_name='Przewoźnik', help_text='Przewoźnik', to='returns.ReturnCarrier')),
                ('comment', models.CharField(verbose_name='Komentarz', blank=True, help_text='Komentarz do przewoźnika lub do zwrotu', max_length=50)),
                ('driver_name', models.CharField(verbose_name='Kierowca', help_text='Jan Kowalski', max_length=50)),
                ('car_plates', models.CharField(verbose_name='Rejestracja', blank=True, help_text='np. WR 00000', max_length=10)),
                ('start_date', models.DateTimeField(verbose_name='Czas Rozpoczęcia', help_text='2014-01-01', auto_now_add=True)),
                ('completed', models.BooleanField(verbose_name='Zakończona', help_text='Zakończona', default=False)),
                ('user', models.ForeignKey(to_field='id', verbose_name='Użytkownik', help_text='Użytkownik', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Waybill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('return_id', models.ForeignKey(to_field='id', verbose_name='Zwrot handlowy', help_text='ID zwrotu handlowego', to='returns.Return')),
                ('number', models.CharField(verbose_name='List Przewozowy', help_text='Podaj 10 cyfr', max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('return_id', models.ForeignKey(to_field='id', verbose_name='Zwrot handlowy', help_text='ID zwrotu handlowego', to='returns.Return')),
                ('waybill', models.ForeignKey(to_field='id', verbose_name='List przewozowy', help_text='ID Listu przwozowego', to='returns.Waybill')),
                ('number', models.CharField(verbose_name='Dokument', help_text='MMW-01S/12345678/2014', max_length=24)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommodityInDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('return_id', models.ForeignKey(to_field='id', verbose_name='Zwrot handlowy', help_text='ID zwrotu handlowego', to='returns.Return')),
                ('waybill', models.ForeignKey(to_field='id', verbose_name='List przewozowy', help_text='ID Listu przwozowego', to='returns.Waybill')),
                ('document', models.ForeignKey(to_field='id', null=True, verbose_name='Dokument', help_text='ID Dokumentu', to='returns.Document')),
                ('commodity', models.ForeignKey(to_field='id', verbose_name='Towar', help_text='Towar', to='commodities.Commodity')),
                ('amount', models.IntegerField(verbose_name='Ilość', help_text='Ilość')),
                ('serial', models.CharField(verbose_name='S/N', help_text='Towar', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
