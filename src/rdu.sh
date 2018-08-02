#!/bin/bash

find . -type f -print0 | xargs -0 du -h | sort -h #| tail -n $1 

