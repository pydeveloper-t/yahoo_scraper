#!/usr/bin/env bash
sudo docker run -d  --name yahoo_parser  parser:yahoo  -c $1 -o ./

