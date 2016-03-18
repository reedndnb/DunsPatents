import csv
import sys

def write_publication(f, pub):
    print("<http://dnb.com/patents/publication/%s>, <http://dnb.com/patents/publication/kind>, '%s'" % (pub['pub-number'], pub['pub-kind']))
    print("<http://dnb.com/patents/publication/%s>, <http://dnb.com/patents/publication/country>, '%s'" % (pub['pub-number'], pub['pub-country']))
    print("<http://dnb.com/patents/publication/%s>, <http://dnb.com/patents/publication/title/EN>, '%s'" % (pub['pub-number'], pub['invention-title_EN']))
    print("<http://dnb.com/patents/publication/%s>, <http://dnb.com/patents/publication/title/FR>, '%s'" % (pub['pub-number'], pub['invention-title_FR']))
    print("<http://dnb.com/patents/publication/%s>, <http://dnb.com/patents/publication/title/DE>, '%s'" % (pub['pub-number'], pub['invention-title_DE']))

def write_citations(f, pub_id, citations):
    # Link publication to citation
    # and output the citation properties as triples

    pub_uri = 'http://dnb.com/patents/publication/%s' % pub_id
    for i, citation in enumerate(citations):
        citation_uri = pub_uri + '/citation/' + i
        print("<%s>, <http://dnb.com/patents/publication/citation>, <%s>" % (pub_uri, citation_uri))
        print("<%s>, <http://dnb.com/patents/publication/citation/number>, '%s'" % (citation_uri, citation['cit-number']))
        print("<%s>, <http://dnb.com/patents/publication/citation/kind>, '%s'" % (citation_uri, citation['kind']))
        print("<%s>, <http://dnb.com/patents/publication/citation/country>, '%s'" % (citation_uri, citation['country']))


def generate_objects(f, indexes, row):
    publication = {}
    publication['pub-number'] = row[indexes['pub-number'][0]] # unique id
    publication['pub-country'] = row[indexes['pub-country'][0]]
    publication['pub-kind'] = row[indexes['pub-kind'][0]]
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

    #for column in d.keys():
    #    indexes = d[column]
    #    object_type = extract_object_type(column)
    #    for i in indexes:


fields_of_interest = ['cit-number', 'pub-country', 'pub-number', 'pub-kind', 'pub-date', 'pri-country', 'pri-number', 'pri-date',
                      'cit-country', 'cit-kind', 'non-pat-cit', 'invention-title_EN', 'invention-title_DE',
                      'invention-title_FR']

with open("output_sample.tsv") as pubs_in:
    reader = csv.reader(pubs_in, delimiter='\t')
    header = reader.next()

    # Extract indexes
    indexes = {}
    for i, col in enumerate(header):
        if col in fields_of_interest:
            #print("%s index: %d" % (col, i))
            index_list = indexes.get(col)
            if not index_list:
                index_list = []
                indexes[col] = index_list
            index_list.append(i)

    for row in reader:
        with open("pubs.rdf", "w") as pubs_out:
            values = generate_objects(sys.stdout, indexes, row)


