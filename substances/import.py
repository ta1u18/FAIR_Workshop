""" example code for the substances app"""
import json
import os
import django
import csv
import pubchempy as pcp
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from config.models import *


def opsin(name, getid='stdinchikey'):
    url = 'https://opsin.ch.cam.ac.uk/opsin/' + name
    resp = requests.get(url)
    jsn = resp.content
    data = json.loads(jsn)
    out = None
    if data['status'] == 'SUCCESS':
        out = data[getid]
    return out


with open('../files/substances.csv', newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar='"')
    sms = Substances.objects.values_list('smiles', flat=True).all()
    for row in rows:
        # ignore the first line which is the column names
        if row[0] == 'entrynum':
            continue
        # if substance has already been processed, then skip
        if row[1] in sms:
            continue
        # ignore entrynum field as not needed for substances
        # link between data and susbtances tables using the smiles string
        # search PubChem by using the PubChemPy package
        subs = pcp.get_compounds(row[1], 'smiles')
        for sub in subs:
            print(sub.inchikey)
            # check with OPSIN
            opkey = opsin(row[2])
            if sub.inchikey == opkey:
                # save substance
                s = Substances()
                s.name = row[2]
                s.formula = sub.molecular_formula
                s.molweight = sub.molecular_weight
                s.inchikey = sub.inchikey
                s.smiles = row[1]
                s.iupacname = sub.iupac_name
                s.save()
                print('confirmed substance "' + row[2] + '"')
            else:
                print('substance "' + row[2] + '" not confirmed')
