FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV SECURE_SSL_REDIRECT 0
RUN mkdir /inspectorDB
WORKDIR /inspectorDB
COPY . /inspectorDB/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "sh", "-c", "python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:8000 project.wsgi:application" ]
