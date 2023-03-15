""" Django models for FAIR Workshop database """
from django.db import models
import requests


class Substances(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=1024, blank=True, null=True)
    formula = models.CharField(max_length=256, blank=True, null=True)
    molweight = models.FloatField(blank=True, null=True)
    inchikey = models.CharField(max_length=27, blank=True, null=True)
    smiles = models.CharField(max_length=128, blank=True, null=True)
    iupacname = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'substances'
        app_label = 'substances'


class Methods(models.Model):
    id = models.SmallAutoField(primary_key=True)
    code = models.CharField(max_length=8, blank=True, null=True)
    perrin = models.CharField(max_length=256, blank=True, null=True)
    perrinsupp = models.CharField(max_length=256, blank=True, null=True)
    serjeant = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'methods'
        app_label = 'methods'


class References(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=8, blank=True, null=True)
    citation = models.CharField(max_length=256, blank=True, null=True)
    journal = models.CharField(max_length=128, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    abbrev = models.CharField(max_length=128, blank=True, null=True)
    authors = models.CharField(max_length=2048, blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    volume = models.CharField(max_length=6, blank=True, null=True)
    issue = models.CharField(max_length=16, blank=True, null=True)
    startpage = models.CharField(max_length=6, blank=True, null=True)
    endpage = models.CharField(max_length=6, blank=True, null=True)
    url = models.CharField(max_length=256, blank=True, null=True)
    doi = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(max_length=32, blank=True, null=True)
    caref = models.CharField(max_length=16, blank=True, null=True)
    other = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'references'
        app_label = 'references'


class Data(models.Model):
    id = models.BigAutoField(primary_key=True)
    entrynum = models.CharField(max_length=8, blank=True, null=True)
    smiles = models.CharField(max_length=128, blank=True, null=True)
    substance_id = models.ForeignKey(Substances, models.DO_NOTHING, db_column="substance_id", blank=True, null=True)
    pka_type = models.CharField(max_length=512, blank=True, null=True)
    pka_value = models.CharField(max_length=16, blank=True, null=True)
    temp = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=128, blank=True, null=True)
    method = models.CharField(max_length=8, blank=True, null=True)
    ref = models.CharField(max_length=8, blank=True, null=True)
    reference_id = models.ForeignKey(References, models.DO_NOTHING, db_column="reference_id", blank=True, null=True)
    ref_remarks = models.CharField(max_length=128, blank=True, null=True)
    entry_remarks = models.CharField(max_length=128, blank=True, null=True)
    original_iupac_name = models.CharField(max_length=128, blank=True, null=True)
    original_iupac_nickname = models.CharField(max_length=128, blank=True, null=True)
    source = models.CharField(max_length=128, blank=True, null=True)
    uniqueid = models.CharField(max_length=16, blank=True, null=True)
    pressure = models.CharField(max_length=16, blank=True, null=True)
    acidity_level = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'data'
        app_label = 'data'


class DataMethods(models.Model):
    """ class for the compilations/sources join table """
    id = models.BigAutoField(primary_key=True)
    data_id = models.ForeignKey(Data, models.DO_NOTHING, blank=True, null=True, db_column='data_id')
    method_id = models.ForeignKey(Methods, models.DO_NOTHING, blank=True, null=True, db_column='method_id')

    class Meta:
        managed = True
        db_table = 'data_methods'
        unique_together = (('data_id', 'method_id'),)
