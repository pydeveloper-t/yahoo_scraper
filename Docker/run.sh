#!/usr/bin/env bash
sudo docker run -d  --name yahoo_parser  --net=host -e DBHOST='localhost' -e DBPORT=3306 -e DATABASE='traxessag' -e DBUSER='admin' -e DBPASSWORD='Qwerty@123' -v /home/android/DataOx:/work parser:yahoo  $1 $2

