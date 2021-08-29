### TODO
- [ ] set-up a query system to retrieve all results from ES: https://stackoverflow.com/questions/53729753/how-to-get-all-results-from-elasticsearch-in-python
- [ ] hardcode fix for vm_max_map_count: https://github.com/docker/for-win/issues/5202, currently need to run `sudo sysctl -w vm.max_map_count=262144 ` everytime the server (in this case, the desktop) is restarted
- [ ] push prelim code to github (get subset_en_tweets in there as well?)
- [x] turn notebook for bulk insertion into a python script
- [ ] backup index?
- [x] read mapping in from json
- [ ] remove duplicates, '08-03' may have duplicates inserted (remove based on status_id?)

```
mkdir esdatadir
chmod g+rwx esdatadir
chgrp 0 esdatadir'
```