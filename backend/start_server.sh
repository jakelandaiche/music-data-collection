#!/usr/bin/env bash

eval "$(micromamba shell hook --shell bash)"
micromamba activate /home/jake/micromamba/envs/sen
python /home/jake/music-data-collection/backend/main.py --host 167.71.241.60 --port 8080
