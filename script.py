import json
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from pathlib import Path


class State(IntEnum):
    DNF = -1
    OK = 0
    PENALTY = 2000


@dataclass
class Solve:
    state: int
    time_ms: int
    scramble: str
    comment: str
    timestamp: datetime

    @classmethod
    def from_row(cls, row):
        (state, time_ms), scramble, comment, timestamp = row
        return cls(
            State(state), time_ms, scramble, comment, datetime.fromtimestamp(timestamp)
        )


@dataclass
class Session:
    id: int
    name: str
    opt: dict
    rank: int
    stat: list
    start_time: datetime
    end_time: datetime
    solves: list[Solve]

    @classmethod
    def from_sessiondata(cls, id, data, solves):
        return cls(
            id,
            data["name"],
            data["opt"],
            data["rank"],
            data["stat"],
            datetime.fromtimestamp(data["date"][0]),
            datetime.fromtimestamp(data["date"][1]),
            solves,
        )

    def stats(self):
        """Should return perhaps
        1. number of solves (total)
        2. number of DNFs
        3. mean time
        """


@dataclass
class CubingData:
    sessions: list[Session]
    current_session_id: int
    tools: bool

    @classmethod
    def from_export(cls, file: Path):
        data = json.loads(file.read_text(encoding="utf-8"))
        sessiondata = json.loads(data["properties"]["sessionData"])

        current_session_id = data["properties"]["sessionN"]
        tools = data["properties"]["tools"]

        sessions = []
        for k, v in sessiondata.items():
            solve_rows = data[f"session{k}"]
            solves = [Solve.from_row(row) for row in solve_rows]
            session = Session.from_sessiondata(k, v, solves)

            sessions.append(session)

        return cls(sessions, current_session_id, tools)


files = Path("data").glob("*.txt")
most_recent = sorted(files)[-1]

data = CubingData.from_export(most_recent)


for session in data.sessions:
    if session.start_time != min(s.timestamp for s in session.solves):
        print(session)

    if session.end_time != max(s.timestamp for s in session.solves):
        print(session)
