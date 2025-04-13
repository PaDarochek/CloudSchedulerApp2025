"""Data structures for scheduling."""

from datetime import datetime


class Task:
    """Task.

    :param id: Task ID
    :param title: Task name
    :param deadline: Deadline for task
    :param created_date: Task date of creation
    :param plan: Planned time for task completion
    :param work: Time already spent on task completion
    """

    id: str
    title: str
    deadline: datetime
    created_date: datetime
    plan: int
    work: int

    def __init__(self, id: int, obj: dict):
        """Create task from ID and parameters dict.

        :param id: Task ID
        :type id: int
        :param obj: Dictionary to create task from
        :type obj: dict
        """
        self.id = id
        self.title = obj["title"]

        self.deadline = datetime.strptime(obj["deadline"], "%d-%m-%Y")
        self.created_date_date = datetime.strptime(obj["created_date"], "%d-%m-%Y")

        self.plan = int(obj["plan"])
        self.work = int(obj["work"])
