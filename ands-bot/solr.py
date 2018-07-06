import lib

solr_url = "http://researchdata.ands.org.au:8983/solr/"

def crawl(q):

    ids = lib.load_ids()
    if ids:
        return ids
    ids = []
    start = 0
    rows = 10000

    url = solr_url + "portal/select?fl=id&indent=on&q="+q+"&&wt=json"

    # get numFound
    data = lib.fetch_json(url)
    numFound = data['response']['numFound']
    print "Found " + str(numFound)

    url = solr_url + "portal/select?fl=id&indent=on&q="+q+"&start=0&rows="+str(numFound)+"&wt=json"
    data = lib.fetch_json(url)

    for doc in data['response']['docs']:
        ids.append(doc['id'])

    print "Saving %s records", len(str)
    lib.save_ids(ids)

    return ids

if __name__ == "__main__":
    q = "license_class:unknown"
    ids = crawl(q)

