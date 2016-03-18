import csv
import json
import urllib2
from urllib import urlencode

def read_fieldnames(path):
    with open(path, "r") as path_csv:
        reader = csv.reader(path_csv)
        row = reader.next()
        return row

def get_auth_token(username, password):
    auth_url = 'https://maxcvservices.dnb.com/rest/Authentication'
    req = urllib2.Request(auth_url)
    req.add_header('x-dnb-user', username)
    req.add_header('x-dnb-pwd', password)
    resp = urllib2.urlopen(req)
    auth_token = resp.info().getheader("Authorization")
    return auth_token

def retrieve_content_from_url(auth_token, url):
    req = urllib2.Request(url)
    req.add_header('Authorization', auth_token)
    resp = urllib2.urlopen(req)
    content = resp.read()
    return content

def get_matches(auth_token, confidence_code=5, **kwargs):
    query = {'ConfidenceLowerLevelThresholdValue' : confidence_code,
             'match' : 'true',
             'MatchTypeText' : 'Advanced',
             'CountryISOAlpha2Code' : 'US'}

    if kwargs.get('company_name'):
        query['SubjectName'] = kwargs['company_name']
    if kwargs.get('city'):
        query['PrimaryTownName'] = kwargs['city']
    if kwargs.get('state'):
        query['TerritoryName'] = kwargs['state']
    if kwargs.get('postal_code'):
        query['FullPostalCode'] = kwargs['postal_code']
    if kwargs.get('country'):
        query['CountryISOAlpha2Code'] = kwargs['country']

    if kwargs.get('street1'):
        query['StreetAddressLine-1'] = kwargs['street1']
    if kwargs.get('street2'):
        query['StreetAddressLine-2'] = kwargs['street2']

    query_string = urlencode(query)
    url = 'https://maxcvservices.dnb.com/V5.0/organizations?' + query_string
    print url

    return retrieve_content_from_url(auth_token, url)

token = get_auth_token('P100000D368CF1EE8B74BB5B4322104F', 'WatP1C#!')
fields = read_fieldnames("companies.csv") + ['duns', 'cc']

with open("companies.csv") as in_file:
    reader = csv.DictReader(in_file)
    header_row = reader.next()
    with open("companies-appended.csv", "w") as out_file:
        writer = csv.DictWriter(out_file, fields)
        writer.writeheader()
        for row in reader:
            query = {
                'company_name' : row['name'],
                'street1' : row['address-1'],
                'street2' : row['address-2'],
                'postal_code' : row['zip-code'],
                'state' : row['State'],
                'city' : row['city'],
                'country' : row['country']}

            try:
                response = get_matches(token, **query)
                obj = json.loads(response)
                matches = obj['MatchResponse']['MatchResponseDetail']['MatchCandidate']
                if matches:
                    match = matches[0]
                    print match
                    row['duns'] = match['DUNSNumber']
                    row['cc'] = match['MatchQualityInformation']['ConfidenceCodeValue']
            except:
                print "No match!"

            print row
            writer.writerow(row)
