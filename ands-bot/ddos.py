import lib
from multiprocessing.dummy import Pool as ThreadPool
import string, random, tqdm, urllib2

def hit(id):

    # prefix = "https://demo.ands.org.au/vocabs-registry/api/resource/"
    prefix = "https://vocabs.ands.org.au/registry/api/resource/"

    try:
        url = prefix + "vocabularies/" + str(id)
        print "hitting: " + url
        contents = urllib2.urlopen(url).read()
    except urllib2.HTTPError as err:
        lib.handle_err(err, url)

    try:
        url = prefix + "versions/" + str(id)
        print "hitting: " + url
        contents = urllib2.urlopen(url).read()
    except urllib2.HTTPError as err:
        lib.handle_err(err, url)

def hit_elda(x):
    url = "http://vocabs.ands.org.au/repository/api/lda/rifcs14/concept"
    try:
        print "hitting: " + url
        contents = urllib2.urlopen(url).read()
    except urllib2.HTTPError as err:
        lib.handle_err(err, url)

def hit_iri_resolve(x):
    url = "https://vocabs.ands.org.au/registry/api/services/resolve/lookupIRI?iri=http%3A%2F%2Fvocab.aodn.org.au%2Fdef%2Fgeographicextents%2Fentity%2F46"
    try:
        print "hitting: " + url
        contents = urllib2.urlopen(url).read()
    except urllib2.HTTPError as err:
        lib.handle_err(err, url)

def hit_sissvoc(x):
    url = "http://vocabs.ands.org.au/repository/api/lda/anzsrc-for/resource.json?uri=http://purl.org/au-research/vocabulary/anzsrc-for/2008/" + str(x)
    try:
        print "hitting: " + url
        contents = urllib2.urlopen(url).read()
    except urllib2.HTTPError as err:
        lib.handle_err(err, url)

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

if __name__=="__main__":

    ids = [];
    for x in range(1000):
        # ids.append(randomword(7))
        ids.append(x)
    print ids

    pool = ThreadPool(8)
    for _ in tqdm.tqdm(pool.imap(hit_iri_resolve, ids), total=len(ids)):
        pass

    # end = time.time()
    # print "took: " + str(end-start) + "s"