from multiprocessing.dummy import Pool as ThreadPool
import os, pickle, argparse, tqdm, time, json, urllib2
import lib,config

def sync(id):
    url = config.api_url+str(id)+'/sync/?workflow='+str(workflow)
    try:
        contents = urllib2.urlopen(url).read()
        with open('./logs/'+str(id)+'.json', 'w') as f:
            f.write(contents)
    except urllib2.HTTPError as err:
        lib.handle_err(err, url)

if __name__ == "__main__":
    start = time.time()

    print "fetching"
    ids = lib.crawl(config.api_url, 0, 10000)

    parser = argparse.ArgumentParser()
    parser.add_argument('--workflow', help='workflow', default=config.workflow)
    parser.add_argument('--threads', help='threads count', default=config.threads_count)
    parser.add_argument('-y', help="yes all", default=False, action='store_true')
    args = parser.parse_args()

    threads_count = int(args.threads)
    workflow = args.workflow

    print "syncing {num} records with workflow: {workflow}, threads: {threads_count}".format(
        num=len(ids),
        workflow=workflow,
        threads_count = threads_count
        )

    if lib.ask(args.y):
        pool = ThreadPool(threads_count)
        for _ in tqdm.tqdm(pool.imap(sync, ids), total=len(ids)):
            pass

    print "Finished. Took: " + str(time.time()-start) + "s"