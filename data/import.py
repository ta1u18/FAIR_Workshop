""" example code for the references app"""
import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from config.models import *
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat

with open('../files/reliable_pka_data.csv', newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    # create unique field for a data row that can be compared to in the code
    done = Data.objects.\
        annotate(uid=Concat('smiles', V(':'), 'pka_value', V(':'), 'ref', output_field=CharField()))\
        .all().values_list('uid', flat=True)
    for row in rows:
        # ignore the first line which is the column names
        if row[0] == 'entrynum':
            continue
        # check if this data point has been done already
        uid = row[1] + ':' + row[3] + ':' + row[7]
        if uid in done:
            print('data point ' + uid + ' already added')
            continue
        # add to data table, but also add the foreign keys from the other tables
        d = Data()
        d.entrynum = row[0]
        d.smiles = row[1]
        # lookup smiles in substances table and get primary key field
        d.substance_id = Substances.objects.get(smiles=row[1])
        d.pka_type = row[2]
        d.pka_value = row[3]
        if row[4] == '':
            d.temp = None
        else:
            d.temp = row[4]
        d.remarks = row[5]
        d.method = row[6]
        d.ref = row[7]
        # lookup reference code in references table and get primary key field
        d.reference_id = References.objects.get(code=row[7])
        if row[8] == '':
            d.ref_remarks = None
        else:
            d.ref_remarks = row[8]
        if row[9] == '':
            d.entry_remarks = None
        else:
            d.entry_remarks = row[9]
        d.original_iupac_name = row[10]
        if row[11] == '':
            d.original_iupac_nickname = None
        else:
            d.original_iupac_nickname = row[11]
        d.source = row[12]
        d.uniqueid = row[13]
        if row[14] == '':
            d.pressure = None
        else:
            d.pressure = row[14]
        d.acidity_level = row[15]
        d.save()
        # method links in join table can only be added once the data point has been saved
        # lookup set of method codes in methods table and get primary key field -> add to join table
        mtds = row[6].split(', ')
        for mtd in mtds:
            DataMethods.objects.create(data_id=d, method_id=Methods.objects.get(code=mtd.strip()))
        print('data point ' + uid + ' added')
