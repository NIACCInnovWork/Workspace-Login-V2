FROM python:slim
EXPOSE 8000/tcp

RUN useradd -ms /bin/bash login-web-server
USER login-web-server
WORKDIR /home/login-web-server

# DATABASE configuration
ENV DB_HOST     "localhost"
ENV DB_USER     "root"
ENV DB_PASSWORD "foobar"

# Install requirements first
COPY requirements*.txt ./
RUN pip install -r requirements.txt
RUN pip install -r requirements-prod.txt

# Copy in application source
# This needs to be refactored in order to reduce the layer count.
COPY config.py .
COPY controller/ controller/
COPY database/ database/
COPY main.py .
COPY report_cli.py .
COPY reports reports/
COPY resources resources/
COPY templates templates/
COPY user_interface user_interface/
COPY flaskr flaskr/

# Launch the login application within gunicorn
ENTRYPOINT [".local/bin/gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "--access-logfile=-", "flaskr:create_app()"]
