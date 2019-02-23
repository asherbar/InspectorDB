FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /inspectorDB
WORKDIR /inspectorDB
COPY . /inspectorDB/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "sh", "-c", "python manage.py runserver 0.0.0.0:8000" ]
