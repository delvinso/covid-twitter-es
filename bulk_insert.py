import csv
import gzip
from elasticsearch import Elasticsearch, helpers
import json
import os
import shutil
from glob import glob
import time


# using dictreader
# fixed bug where verified and protected true/false not being cast correctly
def document_stream(file_to_index, index_name):
    with gzip.open(file_to_index, "rt", newline="") as csvfile:
        
        for row in csv.DictReader(csvfile):

            for fld in ['verified', 'protected']:
                row[fld] = (row[fld] == 'TRUE') # these are both either 'True' or 'False'
                                                                
            for fld in ['favorite_count', 'favourites_count', 'followers_count', 'quote_count', 'reply_count', 'reply_to_status_id', 'reply_to_user_id', 'retweet_count', 'status_id', 'user_id']:
                row[fld] = try_int(row[fld])
            
            for k in row:
                if row[k] == 'NA': 
                    row[k] = None
            
            status_id = row['status_id']
            # delete status_id k:v so it doesn't persist in the output of the generator
            del row['status_id']
                                                                

            yield {"_index": index_name,
                    #"_type": type_name,
                    "_id" : status_id,
                    "_source": json.dumps(row),
                    }
            
            
def try_int(s):
    try: 
        int(s)
        return int(s)
    except ValueError:
        return s
                
if __name__ == "__main__":

    es = Elasticsearch([{"host": "localhost", "port": 9200}])
    index_name = "twitter"
    json_file_path = "./mappings.json"
    dir_to_insert = "/mnt/e/twitter/clean_en/*csv.gz"

    with open(json_file_path, "r") as j:
        mapping = json.loads(j.read())

    # es.indices.delete(index=index_name, ignore=[400, 404])
    es.indices.create(
        index=index_name, body=mapping, ignore=400  # ignore 400 already exists code
    )

    start_time = time.time()
    for f in glob(dir_to_insert):
        print(f)

        for success, info in helpers.parallel_bulk(
            es,
            actions=document_stream(os.path.join(dir_to_insert, f), index_name),
            chunk_size=1000, 
            thread_count=6, 
            # queue_size=8,
            request_timeout=60,

        ):
            if not success:
                print("A document failed:", info)

        shutil.move(
            f, os.path.join("/mnt/e/twitter/clean_en/inserted", os.path.basename(f))
        )
        print(
            "Done moving {} to {}".format(
                f, os.path.join("/mnt/e/twitter/clean_en/inserted", os.path.basename(f))
            )
        )

    end_time = time.time()
    print("Done in {}s".format((end_time - start_time) / 60))
