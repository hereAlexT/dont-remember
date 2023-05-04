FROM python:3.10

COPY . .

RUN pip3 install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

CMD ["gunicorn", "app:wsgi_app", "-b", "0.0.0.0:8888", "--workers", "1", "--threads", "1",  "--log-level", "debug"]

