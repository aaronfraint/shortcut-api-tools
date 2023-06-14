import json
import subprocess
import pandas as pd
from dataclasses import dataclass
from datetime import datetime, timedelta


from .env_vars import SHORTCUT_TOKEN, OWNER_ID


@dataclass
class Story:
    id: int
    app_url: str
    name: str
    updated_at: str
    completed: bool
    archived: bool

    @property
    def _last_updated_on(self) -> datetime:
        return datetime.strptime(self.updated_at, "%Y-%m-%dT%H:%M:%SZ")

    def _was_updated(self, days: int) -> bool:
        time_offset = datetime.now() - timedelta(days=days)
        return self._last_updated_on > time_offset

    @property
    def was_updated_this_week(self):
        return self._was_updated(days=7)

    @property
    def was_updated_in_past_two_weeks(self):
        return self._was_updated(days=14)


CMD_GET_ALL_STORIES_FOR_USER = [
    "curl",
    "-X",
    "POST",
    "-H",
    "Content-Type: application/json",
    "-H",
    f"Shortcut-Token: {SHORTCUT_TOKEN}",
    "-d",
    '{ "owner_ids": ["OWNER_ID"] }'.replace("OWNER_ID", OWNER_ID),
    "-L",
    "https://api.app.shortcut.com/api/v3/stories/search",
]


def get_stories_for_user():
    process = subprocess.Popen(
        CMD_GET_ALL_STORIES_FOR_USER,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, err = process.communicate()
    json_output = json.loads(output)

    all_story_data = []

    for story in json_output:
        data = dict(
            (k, story[k])
            for k in ("name", "app_url", "id", "completed", "archived", "updated_at")
        )
        if not data["completed"] and not data["archived"]:
            all_story_data.append(data)

    df = pd.DataFrame.from_records(all_story_data).sort_values(
        by=["updated_at"], ascending=False
    )

    return df


def print_stories_to_update(df):
    counter = 0
    for idx, row in df.iterrows():
        story = Story(**row)

        if not story.was_updated_in_past_two_weeks:
            counter += 1
            print(f"#{counter} ---------")
            print("\t", story.name)
            print("\t", story.app_url)
