# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('returns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodityindocument',
            name='serial',
            field=models.CharField(help_text='Towar', blank=True, verbose_name='S/N', max_length=50),
        ),
    ]
