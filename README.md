# MMO-Fans

Another Django project. A resource for role-playing game fans to share characters with each other and write reviews about them. Registration is also either through a Yandex account, or with confirmation via email (using the django-allauth package). Models and connections in the database architecture have been designed. Signals have been described. Authors and administrators can delete/create/edit publications. The average user cannot. The template is based on Bootstrap.

What to do to make it work:

Dependencies need to be installed (pip install -r requirements.txt)

Run the command python manage.py runserver

Follow the link http://127.0.0.1:8000/articles/

Posts and responses can be created directly through the application. It is enough to create a superuser, or simply register
