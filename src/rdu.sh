#!/usr/bin/env bash

# find files recursively, 
# sort them by human readable size 
find . -type f -print0 | xargs -0 du -h | sort -h
