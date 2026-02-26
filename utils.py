import json
from datetime import datetime
from pathlib import Path


def process(file: Path):
    data = json.loads(file.read_text())

    session_data = json.loads(data["properties"]["sessionData"])

    for key, session in session_data.items():
        if "date" not in session:
            continue

        times = data[f"session{key}"]
        for row in times:
            (state, time_ms), scramble, comment, timestamp = row
            dt = datetime.fromtimestamp(timestamp)
            yield {
                "session_id": key,
                "datetime": dt,
                "state": state,
                "time_ms": time_ms,
            }
