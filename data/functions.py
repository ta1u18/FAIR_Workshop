from config.models import *
from scidatalib.scidata import SciData


def getscidata(subid, refid):
    data = Data.objects.filter(substance_id=subid, reference_id=refid)
    sub = Substances.objects.get(id=subid)
    ref = References.objects.get(id=refid)

    # create scidata file
    uid = 'iupac_dc_' + data[0].uniqueid
    url = "https://scidata.unf.edu/tranche/" + uid.replace('_', '/') + "/"
    dcjld = SciData(uid)
    dcjld.discipline('w3i:Chemistry')
    dcjld.subdiscipline('w3i:PhysicalChemistry')
    dcjld.version('1')
    dcjld.title("IUPAC Dissociation Constant for " + sub.name)
    dcjld.author([{"name": "Stuart Chalk", "orcid": "https://orcid.org/0000-0002-0703-7776"}])
    dcjld.description("SciData representation of acid/base dissociation constant data")
    dcjld.publisher("Chalk Research Laboratory, University of North Florida")
    dcjld.base(url)
    dcjld.permalink(url)
    dcjld.graph_uid(uid)
    dcjld.namespaces({'cheminf': 'https://semanticchemistry.github.io/semanticchemistry/ontology/cheminf.owl#'})
    dcjld.context(['https://stuchalk.github.io/scidata/contexts/scidata.jsonld',
                   'https://stuchalk.github.io/scidata/contexts/iupac_dc.jsonld'])

    # add the chemical substance
    s = {'@id': "substance"}
    s.update({'name': sub.iupacname})
    s.update({'formula': sub.formula})
    s.update({'molweight': sub.molweight})
    s.update({'inchikey': sub.inchikey})
    dcjld.facets([s])

    # add the dissciation data
    dpnts = []
    for datum in data:
        dpnt = ({"@id": "datapoint"})
        dpnt.update({'dctype': datum.pka_type})
        if 'pKA' in datum.pka_type:
            dpnt.update({'dctype#': "cheminf:CHEMINF_000194"})
        dpnt.update({'value': datum.pka_value})
        dpnts.append(dpnt)
    dcjld.datapoint(dpnts)

    # add the sources
    srcs = []
    # original paper
    src1 = {'citation': ref.citation, 'type': 'journal article'}
    if ref.url:
        src1.update({'url': ref.url})
    srcs.append(src1)
    # CSD entry
    src2 = {'citation': 'IUPAC Digitized pKa Dataset',
            'type': 'dataset', 'doi': 'https://doi.org/10.5281/zenodo.7236453'}
    srcs.append(src2)
    dcjld.sources(srcs)

    # add the rights
    dcjld.rights("The International Union of Pure and Applied Chemistry",
                 "CC BY-NC 4.0 https://creativecommons.org/licenses/by-nc/4.0/")

    # output the jsonld
    return dcjld.output
