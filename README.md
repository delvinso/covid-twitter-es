
# Set-up

This is a hobby project that attempts to put to use the covid19 related tweets I've gathered since the start of the pandemic (roughly Jan 2020).

1. Tweets gathered nightly via cronjob scheduler, dumped as a csv and RDS courtesy of rtweet.
2. Scripts generate nlp-related statistics (https://github.com/delvinso/covid19_unique_tweets) and/or subsetting english only tweets
- `/mnt/e/twitter/covid19/output` -> github repo
- `/mnt/e/twitter/clean_en` -> elasticsearch for downstream analyses

1. Start the elasticsearch instance: `docker-compose up --build`
2. Create the index and bulk upload: `python3 bulk_insert.py`. Note this uses the mapping contained in `mappings.json`
3. Sanity check, up to 2021-09-01:

```
curl -X GET "localhost:9200/_cat/indices?v"
health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   twitter                         tIXz38I4SjKU7PpqowI66g   5   1  283844291          827    251.8gb        251.8gb
```

#### TODO/Misc/Learning Notes
- [x] ~~hardcode fix for vm_max_map_count: https://github.com/docker/for-win/issues/5202, currently need to run `sudo sysctl -w vm.max_map_count=262144 ` everytime the server (in this case, the desktop) is restarted~~ Not needed since moved to WSL
- [ ] backup index?
- [x] 3hrs for 'mask' query - incrased min and max heap size to 2gb but not sure if registered. moving the docker set up into Ubuntu vs. window's mount has increased query speeds from 3-4hours for ~3 million results to tens of minutes
- [x] testing if 4 slices (half of previous 8) will speed-up queries. this seems - breaks ssh connection b/c oom
- [x] scrap parallel processing and storing the results in memory, instead try chunking the scroll api/iterable 
- [ ] possibly add sentiment scores to index - what benefit is there for pre-computing these? seems like a pain especially for 250+ million documents
- [ ] wildcard type seems to be smaller in size and efficient for partial string matching - see related links (https://stackoverflow.com/questions/66809617/elastic-search-ngram-tokenizer-performance-for-uuid)

