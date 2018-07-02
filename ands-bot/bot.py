from multiprocessing.dummy import Pool as ThreadPool
import os, pickle, argparse, tqdm, time, json, urllib2


api_url = 'https://test.ands.org.au/api/registry/records/'
id_cache = 'ids.txt'
threads_count = 8

def sync(id):
    url = api_url+str(id)+'/sync'
    try:
        contents = urllib2.urlopen(url).read()
        with open('./logs/'+str(id)+'.json', 'w') as f:
            f.write(contents)
    except urllib2.HTTPError as err:
        print "err: " + url + " : " + str(err.code) + " reason: " + str(err.reason)

def graph(id):
    url = api_url+str(id)+'/graph'
    try:
        urllib2.urlopen(url).read()
    except urllib2.HTTPError as err:
        print "err: " + url + " : " + str(err.code) + " reason: " + str(err.reason)

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

if __name__ == "__main__":
    start = time.time()

    print "fetching"
    ids = crawl(api_url, 0, 10000)

    parser = argparse.ArgumentParser()
    parser.add_argument('--workflow', help='workflow', default='SyncWorkflow')
    parser.add_argument('--threads', help='threads count', default=threads_count)
    args = parser.parse_args()

    threads_count = int(args.threads)

    print "syncing {num} records with workflow: {workflow}, threads: {threads_count}".format(
        num=len(ids),
        workflow=args.workflow,
        threads_count = threads_count
        )
    proceed = ask()
    if proceed:
        pool = ThreadPool(threads_count)
        for _ in tqdm.tqdm(pool.imap(sync, ids), total=len(ids)):
            pass

    end = time.time()
    print "Finished. Took: " + str(end-start) + "s"