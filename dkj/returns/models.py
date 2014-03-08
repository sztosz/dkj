#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.db import models
from django.contrib.auth.models import User

from commodities.models import Commodity


class ReturnCarrier(models.Model):
    name = models.CharField(max_length=50, verbose_name='Przewoźnik')

    def __str__(self):
        return self.name


class Return(models.Model):
    carrier = models.ForeignKey(ReturnCarrier, verbose_name='Przewoźnik')
    carrier_comment = models.CharField(max_length=50, verbose_name='Komentarz do przewoźnika', blank=True)
    driver_name = models.CharField(max_length=50, verbose_name='Nazwisko kierowcy', blank=True)
    car_plates = models.CharField(max_length=10, verbose_name='Nr rejestracyjny', blank=True)
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Czas Rozpoczęcia')
    completed = models.BooleanField(verbose_name='Zakończona', default=False)
    user = models.ForeignKey(User, verbose_name='Użytkownik')

    def __str__(self):
        return str(self.id)

    def return_number(self):
        return 'DKJ {}'.format(str(self.id).zfill(8))


class Waybill(models.Model):
    return_id = models.ForeignKey(Return, verbose_name='Zwrot handlowy')
    number = models.CharField(max_length=10, verbose_name='List Przewozowy')

    def __str__(self):
        return self.number


class Document(models.Model):
    return_id = models.ForeignKey(Return, verbose_name='Zwrot handlowy')
    waybill = models.ForeignKey(Waybill, verbose_name='List przewozowy')
    number = models.CharField(max_length=24, verbose_name='Dokument')

    def __str__(self):
        return self.number


class CommodityInDocument(models.Model):
    return_id = models.ForeignKey(Return, verbose_name='Zwrot handlowy')
    waybill = models.ForeignKey(Waybill, verbose_name='List przewozowy')
    document = models.ForeignKey(Document, verbose_name='Dokument')
    commodity = models.ForeignKey(Commodity, verbose_name='Towar')
    amount = models.IntegerField(verbose_name='Ilość')

    def __str__(self):
        return str(self.id)

    # def document_name(self):
    #     return 'Bezdokumentowy' if self.unknown_origin else self.document
