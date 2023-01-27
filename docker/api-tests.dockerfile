# This docker image runs the set of api smoke-tests to check if the api service
# is up and responding.
# 
# These tests do not write anything and should be safe to repeatedly run.

FROM python:3.10-slim

# TODO in reality, this should ONLY need the requests depencency
RUN pip install requests flask mysql-connector-python

COPY ws_login_client/ ws_login_client
COPY ws_login_domain/  ws_login_domain
# TODO remove this one
COPY ws_login_flaskr/  ws_login_flaskr
COPY tests/ tests

CMD ["python", "-m", "unittest", "tests.integration.test_api"]
