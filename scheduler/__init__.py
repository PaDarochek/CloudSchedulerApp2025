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
    TextField("$.created_date", as_name="created_date"),
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


@app.post("/task")
def add_task():
    task_params = dict()
    title = request.args.get("title")
    deadline = request.args.get("deadline")
    created_date = request.args.get("created_date")
    plan = request.args.get("plan")
    work = request.args.get("work")

    if (
        title is None
        or deadline is None
        or created_date is None
        or plan is None
        or work is None
        or not plan.isnumeric()
        or not work.isnumeric()
    ):
        raise Exception("Invalid request args")

    task_params["title"] = title
    task_params["deadline"] = deadline
    task_params["created_date"] = created_date
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

    sorted_tasks = [
        task.__dict__
        for task in algorithms.sort_tasks(tasks, start_date, end_date)
    ]
    return sorted_tasks
