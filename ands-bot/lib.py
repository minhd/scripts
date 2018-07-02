import os, pickle
import config

id_cache = config.id_cache

def crawl(url, offset = 0, pp = 1000):
    if os.path.isfile(id_cache):
        with open(id_cache) as f:
            ids = pickle.load(f)
            print "ids loaded from ids.txt "+str(len(ids))+" records"
            return ids
    ids = []
    data = True
    while (data != []):
        data = fetch_json(url+'?limit='+str(pp)+'&offset='+str(offset))
        for i in data:
            ids.append(i['registry_object_id'])
        offset += pp
    # write ids to file
    with open(id_cache, 'w') as f:
        pickle.dump(ids, f)
        print "ids written to " + id_cache

    return ids

def fetch_json(url):
    print url
    contents = urllib2.urlopen(url).read()
    data = json.loads(contents)
    return data

def ask():
    print "proceed? [Y/n]:"
    choice = raw_input().lower()
    if choice in {'yes','y', 'ye', ''}:
       return True
    elif choice in {'no','n'}:
       return False
    else:
       sys.stdout.write("Please respond with 'yes' or 'no'")

def handle_err(err):
    print "err: " + url + " : " + str(err.code) + " reason: " + str(err.reason)