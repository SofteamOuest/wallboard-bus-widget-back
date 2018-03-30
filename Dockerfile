FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 5000
CMD [ "gunicorn", "--workers", "4", "--worker-class", "gthread", "--threads", "4", "--bind", "0.0.0.0:5000", "run:app" ]