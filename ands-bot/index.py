from multiprocessing.dummy import Pool as ThreadPool
import elasticsearch, json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from os import listdir
from os.path import isfile, join
import tqdm, time


INDEX_NAME = "reports"
TYPE = "report"
DIR = "./logs/"

def index(id, doc):
    es.index(index=INDEX_NAME, doc_type=TYPE, id=id, body=doc)

def fix(data):
    # fix subtasks duration
    for subtask in data['subtasks']:
        name = subtask['name']
        sec = subtask['data']['benchmark']['duration_seconds']
        data[name + "_duration_seconds"] = sec
    return data

def index_file(file):
    with open(DIR + file) as json_data:
        data = fix(json.load(json_data))
        index(file, data)

if __name__=="__main__":
    start = time.time()

    es = Elasticsearch(hosts=[{"host":"localhost", "port":9200}])
    es.indices.create(index=INDEX_NAME, ignore=400)

    files = [f for f in listdir(DIR) if isfile(join(DIR, f))]

    pool = ThreadPool(8)
    for _ in tqdm.tqdm(pool.imap(index_file, files), total=len(files)):
        pass

    end = time.time()
    print "took: " + str(end-start) + "s"
