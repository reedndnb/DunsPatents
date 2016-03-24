import csv

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
  
def company_triples(duns, name, pub_id, relationship):
    t1 = "<http://dnb.com/company/%s>, <http://dnb.com/patents/publication/%s>, <'http://dnb.com/patent/pubid/%s'>" % (duns, relationship, pub_id)
    t2 = "<http://dnb.com/company/%s>, <http://dnb.com/company/name>, '%s'" % (duns, name)
    return [t1, t2]

with open("companies-appended-sample.csv", "r") as companies_in:
    reader = csv.DictReader(companies_in)
    with open("companies-triples.rdf", "w") as companies_out:
        for row in reader:
            pub_id = row['pub-id']
            test = 'http://dnb.com/patent/publication-id/%s' % pub_id
            print "Test: %s" % test
            print(pub_id)
            if not row.get('duns'):
                continue

            for triple in company_triples(row['duns'], row['name'], pub_id, row['relationship']):
                companies_out.write(triple)
                companies_out.write('\n')

    #with open("pub-triples.rdf", "w") as pubs_out:
        #for row in reader:
        #    row['cit-number']