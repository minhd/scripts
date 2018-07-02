from multiprocessing.dummy import Pool as ThreadPool
import os, pickle, argparse, tqdm, time, json, urllib2
import lib, config


def graph(id):
    url = config.api_url+str(id)+'/graph'
    try:
        urllib2.urlopen(url).read()
    except urllib2.HTTPError as err:
        lib.handle_err(err)

if __name__ == "__main__":
    start = time.time()

    print "fetching"
    ids = lib.crawl(config.api_url, 0, 10000)

    parser = argparse.ArgumentParser()
    parser.add_argument('--threads', help='threads count', default=config.threads_count)
    parser.add_argument('-y', help="yes all", default=False, action='store_true')
    args = parser.parse_args()

    threads_count = int(args.threads)

    print "wamring graph cache for {num} records threads: {threads_count}".format(
        num=len(ids),
        threads_count = threads_count
        )

    proceed = args.y
    if not proceed:
        proceed = lib.ask()

    if proceed:
        pool = ThreadPool(threads_count)
        for _ in tqdm.tqdm(pool.imap(graph, ids), total=len(ids)):
            pass

    end = time.time()
    print "Finished. Took: " + str(end-start) + "s"