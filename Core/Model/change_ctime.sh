#!/bin/sh

# a root script to manually change the ctime of a file in a linux operating system environment
#
# USAGE:
# change_ctime.sh <new_datetime> <filename>
#
# time format: three letters of the day - three letters of the month - DD hh:mm:ss timezone YYYY
# CET: Central European Time
# CEST: Central European Summer Time
#
# #disabled script parts from stackoverflow
# https://stackoverflow.com/questions/16126992/setting-changing-the-ctime-or-change-time-attribute-on-a-file/17066309#17066309

# now="Sun May 12 11:20:40 CET 2021"
# echo $now
now = $1
#sudo date --set="Sat May 11 06:00:00 CET 2013"
chmod 777 $2
sudo date --set="$now"