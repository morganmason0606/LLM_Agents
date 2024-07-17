#! /usr/bin/bash
#run ./get_html.sh arg1 arg2
#arg1 = name of output file (no suffix)
#arg 2 = url to website
curl -o ./text/$1.html $2
