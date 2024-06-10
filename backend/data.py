import logging
import pandas as pd

logger = logging.getLogger(__name__)

def get_videos(N=10, dataset="musicCaps1.csv") -> list[dict]:
    logger.info(f"Getting {N} videos from {dataset}")
    dataset = pd.read_csv(
        dataset,
        on_bad_lines="skip",
        quotechar='"',
        engine="python",
    )

    videos = []
    for _, row in dataset.sample(N).iterrows():
        videos.append({"id": row["# YTID"], "start_time": row["start_seconds"]})
    return videos
