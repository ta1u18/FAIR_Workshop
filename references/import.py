""" example code for the references app"""
import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from config.models import *
from crossref.restful import Works

with open('../files/references.csv', newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    codes = References.objects.values_list('code', flat=True).all()
    for row in rows:
        # ignore the first line which is the column names
        if row[0] == 'code':
            continue
        # if reference has already been processed, then skip
        if row[0] in codes:
            continue
        vcode = row[0]
        vcite = row[1]
        vcabs = row[2]
        vothr = row[3]
        # go out to crossref and get DOI
        works = Works()
        refs = works.query(bibliographic=vcite)
        print(vcite)
        doi = None
        for ref in refs:
            # check the 'match' score for the first ref to see if its over 50%
            if ref['score'] > 50:
                doi = ref['DOI']
            break
        m = References(code=vcode, citation=vcite, caref=vcabs, other=vothr, doi=doi)
        m.save()
        print('row ' + vcode + ' ingested')
