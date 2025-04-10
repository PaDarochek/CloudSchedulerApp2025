"""Data structures for YouGile entities."""

from datetime import datetime


# @dataclass
# class Project:
#     """YouGile project.

#     :param id: Project ID
#     :param title: Project name
#     """

#     id: str
#     title: str


# @dataclass
# class Board:
#     """YouGile board.

#     :param id: Board ID
#     :param title: Board name
#     """

#     id: str
#     title: str


# @dataclass
# class Deadline:
#     """Deadline for the task.

#     :param deadline: Due date
#     :param start_date: Start date
#     """

#     deadline: datetime
#     start_date: Optional[datetime] = None


# @dataclass
# class TimeTracking:
#     """Time tracking for the task.

#     :param plan: Planned amount of hours for task
#     :param work: Completed amount of hours for task
#     """

#     plan: int
#     work: int


class Task:
    """YouGile task.

    :param id: Task ID
    :param title: Task name
    :param description: Task description
    :param archived: Flag for archived task
    :param completed: Flag for completed task
    :param deadline: Deadline for task
    :param time_tracking: Time tracking for task
    """

    id: str
    title: str
    # description: str
    # archived: bool
    # completed: bool
    start_date: datetime
    deadline: datetime
    plan: int
    work: int

    def __init__(self, id: int, obj: dict):
        """Create task from dict with YouGile parameters.

        :param obj: Dictionary to create task from
        :type obj: dict
        """
        self.id = id
        self.title = obj["title"]

        self.deadline = datetime.strptime(obj["deadline"], "%d-%m-%Y")
        self.start_date = datetime.strptime(obj["start_date"], "%d-%m-%Y")

        self.plan = int(obj["plan"])
        self.work = int(obj["work"])
