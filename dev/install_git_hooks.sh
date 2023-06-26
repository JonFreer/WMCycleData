#!/bin/bash

BASE=$(dirname $0)

ln -s $BASE/check.sh $BASE/../.git/hooks/pre-commit