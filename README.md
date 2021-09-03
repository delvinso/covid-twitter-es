### TODO
- [x] set-up a query system to retrieve all results from ES: https://stackoverflow.com/questions/53729753/how-to-get-all-results-from-elasticsearch-in-python
- [x] ~~hardcode fix for vm_max_map_count: https://github.com/docker/for-win/issues/5202, currently need to run `sudo sysctl -w vm.max_map_count=262144 ` everytime the server (in this case, the desktop) is restarted~~ Not needed since moved to WSL
- [ ] push prelim code to github (get subset_en_tweets in there as well?)
- [x] turn notebook for bulk insertion into a python script
- [ ] backup index?
- [x] read mapping in from json
- [x] remove duplicates, '08-03' may have duplicates inserted (remove based on status_id?)

- [x] 3hrs for 'mask' query - incrased min and max heap size to 2gb but not sure if registered.  moved to WSL
- [x] testing if 4 slices (half of previous 8) will speed-up queries. this seems - breaks ssh connection
