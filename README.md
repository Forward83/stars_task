# stars_task
### Installing
To install application follow the following steps:  
1. Clone this repository to local machine
2. Install packages from requirements.txt
3. Make and execute migrations
4. Create superuser (to have access to admin)
5. Load initial data from fixture
6. Run local server
```
git clone https://github.com/Forward83/stars_task
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py loaddata initial_data.json
python3 manage.py runserver
```
