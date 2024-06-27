#!/bin/sh

export PATH="/usr/local/go/bin:$PATH"
cd $(dirname $0)

python3 ./main.py ./build.json