<p><b>UPD</b>: проект завернут в docker container (работал вчера над этой задачей после отпhавки на проверку, в cвоих личных учебных целях)</p> 
<p>Запуск проекта с docker-compose:
  docker-compose up --build (первичный запуск, или запуск после любых изменений в коде)
  docker-compose up (последующие запуски без изменения в коде проекта)</p>





<b>Запуск без докер:</b>
<p>
1 - установить все зависимости: pip install -r req.txt <br>
2 - сделать миграции : python manage.py makemigrations <br>
3 - применить миграции : python manage.py migrate <br>
4 - установить свой SECRET_KEY (на прямую в settings.py или в .env c именем 'KEY') <br>
5 - запуск проекта - python manage.py runserver</p> <br>

<strong>Урлы:<strong><br>
  документация:<br>
    http://127.0.0.1:8000/api/swagger/<br>
    http://127.0.0.1:8000/api/redoc/<br>
    
  <b>эндпоинт для обработки файла <b>bills.xlsx:<br>
    http://127.0.0.1:8000/api/parse/<br>
  
  <b>эндпоинт со списком счетов с возможностью фильтровать по организации, клиенту:<b><br>
    http://127.0.0.1:8000/api/pills/<br>
    

