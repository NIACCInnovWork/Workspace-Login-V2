FROM python:3.10-slim
EXPOSE 8000

# Create user and install directory
RUN useradd --system login-api && \
  mkdir /opt/login-api-server && \
  chown login-api:login-api /opt/login-api-server

# Install Requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt && pip install gunicorn

USER login-api
WORKDIR /opt/login-api-server

COPY ws_login_domain ws_login_domain
COPY ws_login_flaskr ws_login_flaskr

CMD ["gunicorn", "--bind=0.0.0.0", "--access-logfile=-", "ws_login_flaskr:create_app()"]
