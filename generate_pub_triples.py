import csv
import sys

COMPANY_URI = 'http://dnb.com/duns/%s'
PUB_URI = 'http://dnb.com/patents/publication/%s'

def triple_object(subject, predicate, object):
    return "<%s> <%s> <%s> ." % (subject, predicate, object)

def print_triple_object(subject, predicate, object):
    triple = triple_object(subject, predicate, object)
    if triple:
        print(triple)

def triple_literal(subject, predicate, value):
    if not value:
        return
    return "<%s> <%s> \"%s\" ." % (subject, predicate, value.strip())

def print_triple_literal(subject, predicate, value):
    triple = triple_literal(subject, predicate, value)
    if triple:
        print(triple)

def set_company_uri(key, val, context):
    context['company_uri'] = COMPANY_URI % val

def write_publication(f, pub):
    pub_uri = PUB_URI % pub['pub-number']
    print_triple_literal(pub_uri, 'http://dnb.com/patents/publication/kind', pub['pub-number'])
    print_triple_literal(pub_uri, 'http://dnb.com/patents/publication/country', pub['pub-country'])
    print_triple_literal(pub_uri, 'http://dnb.com/patents/publication/title/EN', pub['invention-title_EN'])
    print_triple_literal(pub_uri, 'http://dnb.com/patents/publication/title/FR', pub['invention-title_FR'])
    print_triple_literal(pub_uri, 'http://dnb.com/patents/publication/title/DE', pub['invention-title_DE'])

    ipcr_codes = pub['IPCR'].split('|')
    for ipcr_code in ipcr_codes:
        print_triple_literal(pub_uri, 'http://dnb.com/patents/publication/IPCR', ipcr_code)

    cpc_codes = pub['CPC'].split('|')
    for cpc_code in cpc_codes:
        print_triple_literal(pub_uri, 'http://dnb.com/patents/publication/CPC', cpc_code)


def write_citations(f, pub_id, citations):
    # Link publication to citation
    # and output the citation properties as triples

    pub_uri = PUB_URI % pub_id
    for i, citation in enumerate(citations):
        citation_uri = pub_uri + '/citation/' + i
        print_triple_object(pub_uri, "http://dnb.com/patents/publication/citation", citation_uri)
        print_triple_literal(citation_uri, "http://dnb.com/patents/publication/citation/number", citation['cit-number'])
        print_triple_literal(citation_uri, "http://dnb.com/patents/publication/citation/kind>", citation['kind'])
        print_triple_literal(citation_uri, "http://dnb.com/patents/publication/citation/country", citation['country'])

def write_non_patent_citation(npc):
    # TODO: Implement once we have some data to output
    pass

def generate_objects(f, indexes, row):
    publication = {}
    publication['pub-number'] = row[indexes['pub-number'][0]] # unique id
    publication['pub-country'] = row[indexes['pub-country'][0]]
    publication['pub-kind'] = row[indexes['pub-kind'][0]]
    publication['IPCR'] = row[indexes['IPCR'][0]]
    publication['CPC'] = row[indexes['CPC'][0]]
    publication['invention-title_EN'] = row[indexes['invention-title_EN'][0]]
    publication['invention-title_FR'] = row[indexes['invention-title_FR'][0]]
    publication['invention-title_DE'] = row[indexes['invention-title_DE'][0]]
    write_publication(f, publication)

    # Find all citations in row
    cit_indexes = indexes['cit-kind']
    num_citations = len(cit_indexes)
    citations = []
    for i in range(num_citations):
        kind = row[indexes['cit-kind'][i]]
        country = row[indexes['cit-country'][i]]
        number = row[indexes['cit-number'][i]]
        if number:
            citation = {'cit-number' : number,
                        'kind' : kind,
                        'country' : country,
                        'pub-number' : row['pub-number']}
            citations.append(citation)
    if citations:
        write_citations(f, citation)

    # Find all non-patent citations in row
    # There should only be one entry, which has pipe-delimited values
    non_patent_citations = row[indexes['non-pat-cit'][0]].split('|')

    for npc in non_patent_citations:
        write_non_patent_citation(npc)


fields_of_interest = ['cit-number', 'pub-country', 'pub-number', 'pub-kind', 'pub-date', 'pri-country', 'pri-number', 'pri-date',
                      'cit-country', 'cit-kind', 'non-pat-cit', 'invention-title_EN', 'invention-title_DE',
                      'invention-title_FR', 'IPCR', 'CPC']

with open("output_sample.tsv") as pubs_in:
    reader = csv.reader(pubs_in, delimiter='\t')
    header = reader.next()

    # Extract indexes
    indexes = {}
    for i, col in enumerate(header):
        if col in fields_of_interest:
            index_list = indexes.get(col)
            if not index_list:
                index_list = []
                indexes[col] = index_list
            index_list.append(i)

    for row in reader:
        with open("pubs.rdf", "w") as pubs_out:
            generate_objects(sys.stdout, indexes, row)


