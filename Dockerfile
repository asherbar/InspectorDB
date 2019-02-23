FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /inspectorDB
WORKDIR /inspectorDB
COPY . /inspectorDB/
RUN pip install -r requirements.txt
CMD [ "python", "./manage.py collectstatic --noinput && gunicorn project.wsgi:application" ]
