# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY req.txt /code/
RUN pip install -r req.txt
COPY . /code/
#EXPOSE 8000
RUN python manage.py makemigrations


#CMD python manage.py runserver 127.0.0.1:8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]