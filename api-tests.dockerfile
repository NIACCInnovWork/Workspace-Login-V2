# This docker image runs the set of api smoke-tests to check if the api service
# is up and responding.
# 
# These tests do not write anything and should be safe to repeatedly run.

FROM python:3.10-slim

# TODO in reality, this should ONLY need the requests depencency
RUN pip install requests flask mysql-connector-python

COPY client/ client
COPY database/ database
COPY flaskr/ flaskr
COPY test_api.py test_api.py

CMD ["python", "-m", "unittest", "test_api"]
