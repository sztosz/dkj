#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# @author: Bartosz Nowak sztosz@gmail.com


import csv
import time  # TODO Remove DEBUG
from io import TextIOWrapper

from django.core.urlresolvers import reverse
from django.views.generic import FormView, CreateView

from dkj.common import LoggedInMixin, EanValidator
from . import models, forms


class ImportSingle(LoggedInMixin, CreateView):

    template_name = 'commodities/import_single.html'
    form_class = forms.CommodityImportSingleForm

    def get_success_url(self):
        return reverse('index')


class ImportBatch(LoggedInMixin, FormView):

    template_name = 'commodities/import_batch.html'
    form_class = forms.CommodityImportBatchForm

    def form_valid(self, form):
        file = TextIOWrapper(self.request.FILES['file'].file, encoding=self.request.encoding)
        parser = CommodityParser(file)
        parser.parse()
        parser.sync_with_database()
        return super(ImportBatch, self).form_valid(form)

    def get_success_url(self):
        return reverse('index')

    # TODO Add single commodity EAN verification


class CommodityParser():
    def __init__(self, file, newline='', delimiter=';', quotechar='"'):
        self.file = file
        self.newline = newline
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.warnings = []
        self.errors = []
        self.parsed_data = []

    def parse(self):
        # TODO Remove DEBUG
        start_time = time.time()
        reader = csv.reader(self.file, delimiter=self.delimiter, quotechar=self.quotechar)
        validator = EanValidator()
        counter_valid = 0
        counter_invalid = 0
        print('READER : ', reader)
        for row in reader:
            ean = row[0]
            if not validator.ean_valid(ean):
                counter_invalid += 1
                continue
            sku = row[1]
            name = row[2]
            self.parsed_data.append({'ean': ean, 'sku': sku, 'name': name})
            counter_valid += 1
        # TODO Remove DEBUG
        print('Valid : ', counter_valid)
        print('Invalid : ', counter_invalid)
        print('Parsing : ', time.time() - start_time, "seconds")

    def sync_with_database(self):
        # TODO Remove DEBUG
        start_time = time.time()
        counter_created = 0
        counter_updated = 0
        for commodity in self.parsed_data:
            obj, created = models.Commodity.objects.update_or_create(
                ean=commodity['ean'], defaults={'sku': commodity['sku'], 'name': commodity['name']})
            if created:
                counter_created += 1
            else:
                counter_updated += 1
        # TODO Remove DEBUG
        print('Created : ', counter_created)
        print('Updated : ', counter_updated)
        print('Adding to DB : ', time.time() - start_time, "seconds")


