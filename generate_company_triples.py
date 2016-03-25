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

def write_company_triples(company):
    company_uri = COMPANY_URI % company['duns']
    pub_uri = PUB_URI % company['pub_id']
    print_triple_object(company_uri,
                        'http://dnb.com/patents/publication/' + company['relationship'],
                        pub_uri)
    print_triple_literal(company_uri,
                         'http://dnb.com/company/name',
                         company['name'])

with open("companies-appended-sample.csv", "r") as companies_in:
    reader = csv.DictReader(companies_in)
    for row in reader:
        #print "---- ROW: %s ------" % str(row)
        pub_id = row['pub-id']
        test = 'http://dnb.com/patent/publication-id/%s' % pub_id
        if not row.get('duns'):
            #print "No Duns -- skipping..."
            continue
        #print '--- %s, %s ---- ' % (row.get('duns'), row.get('name'))

        company = {'duns' : row['duns'],
                   'name' : row['name'],
                   'relationship' : row['relationship'],
                   'pub_id' : pub_id}

        write_company_triples(company)
