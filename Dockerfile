FROM python:3.11-alpine

WORKDIR /scheduler

COPY requirements.txt /scheduler
RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY scheduler/* /scheduler
WORKDIR /

ENTRYPOINT ["flask"]
CMD ["--app", "scheduler", "run", "--host=0.0.0.0"]
