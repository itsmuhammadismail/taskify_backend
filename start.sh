#!/bin/bash

source env/bin/activate
python3 -m uvicorn main:app --host=0.0.0.0 --workers=4