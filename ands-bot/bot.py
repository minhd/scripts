from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import json
import tqdm, time

api_url = 'https://test.ands.org.au/api/registry/records/'

def sync(id):
    url = api_url+str(id)+'/sync'
    try:
        contents = urllib2.urlopen(url).read()
        with open('./logs/'+str(id)+'.json', 'w') as f:
            f.write(contents)
    except urllib2.HTTPError as err:
        print "err: " + url + " : " + str(err.code)

def graph(id):
    url = api_url+str(id)+'/graph'
    try:
        urllib2.urlopen(url).read()
    except urllib2.HTTPError as err:
        print "err: " + url + " : " + str(err.code)

def crawl(url, offset = 0, pp = 1000):
    global ids
    data = True
    while (data != []):
        data = fetch_json(url+'?limit='+str(pp)+'&offset='+str(offset))
        for i in data:
            ids.append(i['registry_object_id'])
        offset += pp

def fetch_json(url):
    print url
    contents = urllib2.urlopen(url).read()
    data = json.loads(contents)
    return data

if __name__ == "__main__":
    start = time.time()

    print "fetching"
    crawl(api_url, 0, 10000)

    print "syncing "+str(len(ids)) +" records"

    pool = ThreadPool(8)
    for _ in tqdm.tqdm(pool.imap(sync, ids), total=len(ids)):
        pass

    end = time.time()
    print "took: " + str(end-start) + "s"