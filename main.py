#!/usr/bin/env python3
"""\
routine (& program) idea -- the N commandments of <user>

the routine and program may run for the remainder of your life; as long as you desire

every month (day 1), pick 1-3 new goals to accept for the remainder of your life
- the one month is the trial period, where you will attempt to achieve a 100% success rate for the entire month
- if you fail the goal, you must subdivide the goal into a smaller/more narrow goal and re-add it to the list of potential goals
- if you succeed, you must live to the goal for the remainder of life
- if you fail after the month completes, re-add it to the list of potential goals without subdivision (you can even increase scope if desired)

some hard rules:
- new goal setting & program reports happen only at the beginning of each month (day 1, sometime before midnight) - there are no check-ins
- even if you fail your goal on day 1 of the month, you must continue to attempt 100% for the rest of the month
- you are to define a precise failure criteria for each goal at the time of goal-setting
    - by nature of the program's assumption of trust after the month, you must be honest with yourself in capability demonstration
- the failure criteria is labelled loosely as 'around 100%' but you should aim for ~ >=95% or <=1/30 daily chore failures
- there are no rewards for accomplishing a goal; the goal in and of itself should be of valuable reward

goals should be specific and realistic.
- the ultimate aim of the program is to train you to be a better version of yourself
- subdivision and limiting of scope are considered good practice (e.g. "only do X without Y")
"""

import dataclasses
from datetime import datetime, timedelta

import json

STATE_FILE = "state.json"


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


@dataclasses.dataclass
class SuccessCriteria:
    num_checkpoints: int
    permitted_failures: int


@dataclasses.dataclass
class Goal:
    name: str
    success_criteria: SuccessCriteria
    starts_at: datetime
    ends_at: datetime


@dataclasses.dataclass
class State:
    goals: list[Goal]


def main() -> int:
    if datetime.today().day != 1:
        print("This program only runs on the first day of the month.")
        return 1

    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    except json.decoder.JSONDecodeError:
        print("Error: state file is corrupted.")
        print("Please delete the state file and restart the program.")
        return 1
    except FileNotFoundError:
        state = State(goals=[])
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, cls=EnhancedJSONEncoder)

    print("Welcome to the N Commandments program.")
    print("Please enter your goals for the month.")
    print("Enter 'q' to finish.")

    while True:
        goal_name = input("Goal name: ")
        if goal_name == "q":
            break

        num_checkpoints = int(input("Number of checkpoints: "))
        permitted_failures = int(input("Permitted failures: "))

        success_criteria = SuccessCriteria(num_checkpoints, permitted_failures)
        goal = Goal(
            name=goal_name,
            success_criteria=success_criteria,
            starts_at=datetime.today(),
            ends_at=datetime.today() + timedelta(days=30),
        )
        state.goals.append(goal)

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, cls=EnhancedJSONEncoder)

    print("Goals saved successfully.")
    print("Good luck!")

    return 0


if __name__ == "__main__":
    exit(main())
