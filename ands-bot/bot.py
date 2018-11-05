import argparse
import time
import tqdm
import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import config
import lib
import db


def write_result(ro_id, contents):
    with open('./logs/'+str(ro_id)+'.json', 'w') as f:
        f.write(contents)


def sync(ro_id):
    url = config.api_url+str(ro_id)+'/sync/?workflow='+str(workflow)
    print url
    try:
        start = time.time()
        contents = urllib2.urlopen(url).read()
        db.touch(ro_id, time.time() - start)
        write_result(ro_id, contents)
    except urllib2.HTTPError as err:
        lib.handle_err(err, url)


def fetch():
    not_done = db.not_done()
    if len(not_done) > 0:
        return not_done
    lib.crawl(config.api_url, 0, 10000)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workflow', help='workflow', default=config.workflow)
    parser.add_argument('--threads', help='threads count', default=config.threads_count)
    parser.add_argument('-y', help="yes all", default=False, action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    """
    usage: python bot.py --threads=2 --workflow=SyncWorkflow
    """
    start = time.time()

    ids = fetch()
    args = parse_args()

    threads_count = int(args.threads)
    workflow = args.workflow

    print "syncing {num} records with workflow: {workflow}, threads: {threads_count}".format(
        num=len(ids),
        workflow=workflow,
        threads_count=threads_count
    )

    if lib.ask(args.y):
        pool = ThreadPool(threads_count)
        for _ in tqdm.tqdm(pool.imap(sync, ids), total=len(ids)):
            pass

    print "Finished. Took: " + str(time.time()-start) + "s"
