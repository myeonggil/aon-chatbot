#!/bin/bash

image=$1

# docker build platform linux/amd64 or linux/arm64
# lima nerdctl build -t $image .

# docker run with mount
lima nerdctl run -v /Users/jumyeonggil/.aws:/root/.aws -v ./:/var/task --network host --name $image -it base
