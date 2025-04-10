#!/usr/bin/env python3
"""Launcher."""

from scheduler import algorithms, data_structures

import datetime

import json

import os

from flask import Flask, request

from redis import Redis
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import TextField, NumericField
from redis.commands.json.path import Path


host = os.getenv("REDIS_SERVICE_HOST")
port = int(os.getenv("REDIS_SERVICE_PORT"))
r = Redis(host=host, port=port, decode_responses=True)

schema = (
    TextField("$.title", as_name="title"),
    TextField("$.deadline", as_name="deadline"),
    TextField("$.start_date", as_name="start_date"),
    NumericField("$.plan", as_name="plan"),
    NumericField("$.work", as_name="work"),
)

index = r.ft("idx:task")
try:
    index.info()
except Exception:
    index.create_index(
        schema,
        definition=IndexDefinition(
            prefix=["task:"], index_type=IndexType.JSON
        ),
    )

if r.get("next_id") is None:
    r.set("next_id", 0)

app = Flask(__name__)

### TEST

# x = {
#     "title": "cook",
#     "deadline": "12-03-2025",
#     "start_date": "09-03-2025",
#     "plan": 3,
#     "work": 0,
# }
# r.json().set(f"task:{next_id}", Path.root_path(), x)
# print(r.ft("idx:task").search("*").docs[0]["json"])

###


@app.post("/task")
def add_task():
    task_params = dict()
    title = request.args.get("title")
    deadline = request.args.get("deadline")
    start_date = request.args.get("start_date")
    plan = request.args.get("plan")
    work = request.args.get("work")

    if (
        title is None
        or deadline is None
        or start_date is None
        or plan is None
        or work is None
        or not plan.isnumeric()
        or not work.isnumeric()
    ):
        raise Exception("Invalid request args")

    task_params["title"] = title
    task_params["deadline"] = deadline
    task_params["start_date"] = start_date
    task_params["plan"] = int(plan)
    task_params["work"] = int(work)

    next_id = int(r.get("next_id"))
    r.json().set(f"task:{next_id}", Path.root_path(), task_params)
    next_id += 1
    r.set("next_id", next_id)
    return {}, 200


@app.route("/list")
def get_task_list():
    tasks = [json.loads(d["json"]) for d in r.ft("idx:task").search("*").docs]
    return tasks


@app.route("/sort")
def get_sorted_task_list():
    try:
        start_date = datetime.datetime.strptime(
            request.args.get("start_date"), "%d-%m-%Y"
        )
        end_date = datetime.datetime.strptime(
            request.args.get("end_date"), "%d-%m-%Y"
        )
    except Exception:
        raise "Invalid request args"

    tasks = [
        data_structures.Task(
            int(d["id"].split(":")[-1]), json.loads(d["json"])
        )
        for d in r.ft("idx:task").search("*").docs
    ]

    relevant_tasks = algorithms.get_relevant_tasks(tasks, start_date, end_date)
    sorted_tasks = [
        task.__dict__
        for task in algorithms.sort_tasks(relevant_tasks, start_date, end_date)
    ]
    return sorted_tasks


# class App(controllers.IApp):
#     """App.

#     :param controllers: App controllers
#     """

#     def __init__(self):
#         super().__init__()
#         self.title("Smart Scheduler")
#         set_appearance_mode("dark")
#         self.minsize(512, 512)

#         self.frame: CTkFrame | None = None
#         self.model = models.AppLogicModel()
#         self.views = {}
#         self.controllers = {}

#         self.views["login"] = views.LoginView
#         self.controllers["login"] = controllers.LoginController(self)

#         self.views["boards"] = views.BoardView
#         self.controllers["boards"] = controllers.BoardController(self)

#         self.views["tasks"] = views.TasksView
#         self.controllers["tasks"] = controllers.TasksController(self)

#         self.show_view("login")

#     def get_model(self) -> models.AppLogicModel:
#         """Get app logic model.

#         :return: App logic model
#         :rtype: models.AppLogicModel
#         """
#         return self.model

#     def show_view(self, id: str):
#         """Show view by ID.

#         :param id: View ID
#         :type id: str
#         """
#         view_cls = self.views[id]
#         controller = self.controllers[id]
#         if self.frame:
#             self.frame.pack_forget()
#             self.frame.destroy()
#         self.frame = view_cls(self, controller)
#         self.frame.pack(fill="both", expand=True)


# def main():
#     """Launch app."""
#     app = App()
#     app.mainloop()
