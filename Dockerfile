FROM python:3.8
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./req.txt ./

RUN pip install --no-cache-dir -r req.txt

COPY . .

EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate

#CMD python manage.py runserver 127.0.0.1:8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]