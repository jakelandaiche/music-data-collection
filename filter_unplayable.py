#!/usr/bin/env python3

import pandas as pd
from yt_dlp import YoutubeDL

_dataset = pd.read_csv(
  "eval_segments.csv",
  sep=", ",
  on_bad_lines="skip",
  skiprows=2,
  quotechar='"',
  engine="python"
)

dataset = _dataset[_dataset["positive_labels"].str.match(".*/m/04rlf.*")]

playable = []
with YoutubeDL({ "quiet": True }) as ydl: 
  for video_id in dataset['# YTID']:
    URL = f'https://www.youtube.com/watch?v={video_id}'
    try:
      info = ydl.extract_info(video_id, download=False)
      playable.append(info.get('playable_in_embed'))
    except:
      playable.append(False)
      
filtered = dataset[playable]
filtered.to_csv('filtered.csv')