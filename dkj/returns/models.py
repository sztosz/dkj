#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com

from django.db import models
from django.contrib.auth.models import User

from commodities.models import Commodity


class ReturnCarrier(models.Model):
    name = models.CharField(max_length=50, verbose_name='Przewoźnik', help_text='Przewoźnik')

    def __str__(self):
        return self.name


class Return(models.Model):
    carrier = models.ForeignKey(ReturnCarrier, verbose_name='Przewoźnik', help_text='Przewoźnik')
    comment = models.CharField(max_length=50, verbose_name='Komentarz', blank=True,
                               help_text='Komentarz do przewoźnika lub do zwrotu')
    driver_name = models.CharField(max_length=50, verbose_name='Kierowca',
                                   help_text='Jan Kowalski')
    car_plates = models.CharField(max_length=10, verbose_name='Rejestracja', blank=True,
                                  help_text='np. WR 00000')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Czas Rozpoczęcia', help_text='2014-01-01')
    completed = models.BooleanField(verbose_name='Zakończona', default=False, help_text='Zakończona')
    user = models.ForeignKey(User, verbose_name='Użytkownik', help_text='Użytkownik')

    def __str__(self):
        return str(self.id)

    def return_number(self):
        return 'DKJ {}'.format(str(self.id).zfill(8))


class Waybill(models.Model):
    return_id = models.ForeignKey(Return, verbose_name='Zwrot handlowy', help_text='ID zwrotu handlowego')
    number = models.CharField(max_length=10, verbose_name='List Przewozowy', help_text='Podaj 10 cyfr')

    def __str__(self):
        return self.number


class Document(models.Model):
    return_id = models.ForeignKey(Return, verbose_name='Zwrot handlowy', help_text='ID zwrotu handlowego')
    waybill = models.ForeignKey(Waybill, verbose_name='List przewozowy', help_text='ID Listu przwozowego')
    number = models.CharField(max_length=24, verbose_name='Dokument', help_text='MMW-01S/12345678/2014')

    def __str__(self):
        return self.number


class CommodityInDocument(models.Model):
    return_id = models.ForeignKey(Return, verbose_name='Zwrot handlowy', help_text='ID zwrotu handlowego')
    waybill = models.ForeignKey(Waybill, verbose_name='List przewozowy', help_text='ID Listu przwozowego')
    document = models.ForeignKey(Document, verbose_name='Dokument', help_text='ID Dokumentu', null=True)
    commodity = models.ForeignKey(Commodity, verbose_name='Towar', help_text='Towar')
    amount = models.IntegerField(verbose_name='Ilość', help_text='Ilość')
    serial = models.CharField(max_length=50, verbose_name='S/N', help_text='Towar' )

    def __str__(self):
        return str(self.commodity)

    # def document_name(self):
    #     return 'Bezdokumentowy' if self.unknown_origin else self.document
