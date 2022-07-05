# s22_team_38
Repository for s22_team_38


## Setup guide 
---

Make sure python, pip, django, and social-auth-app-django packages are installed and on the latest version


```
python -m pip install –-upgrade pip
pip install django 
pip install social-auth-app-django
```

\
Once the packages are installed, navigate to the project directory
```
cd cmuSocialMap
python manage.py makemigrations
python manage.py migrate
```

\
Specifications for config.ini in cmuSocialMap folder
```
[Django]
Secret: ''

[GoogleOAuth2]
Key: ''
Secret: ''
```

\
Running project devserver
```
python manage.py runserver
```