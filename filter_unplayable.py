#!/usr/bin/env python3

import pandas as pd
from yt_dlp import YoutubeDL

_dataset = pd.read_csv(
    "filtered_data.csv",
    sep=", ",
    on_bad_lines="skip",
    quotechar='"',
    engine="python",
)

dataset = _dataset[_dataset["positive_labels"].str.match(".*/m/04rlf.*")]

with YoutubeDL({"quiet": True}) as ydl:
    for chunk in range(0, len(dataset), 10000):
        playable = []
        for video_id in dataset[chunk : chunk + 10000]["# YTID"]:
            try:
                info = ydl.extract_info(video_id, download=False)
                playable.append(info.get("playable_in_embed"))
            except:
                playable.append(False)
        filtered = dataset[chunk : chunk + 10000][playable]
        filtered.to_csv(f"filtered_{chunk}.csv")
        print(f"{len(playable)} were playable")
