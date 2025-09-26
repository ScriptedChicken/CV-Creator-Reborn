#!/bin/bash

cd "$(dirname "$0")"
source .venv/bin/activate
python3 cover_letter_creator/app.py