#!/bin/bash

cd "${dirname "$0"}"
source env/bin/activate
python3 -m uvicron main:app --host=0.0.0.0 --workers=4