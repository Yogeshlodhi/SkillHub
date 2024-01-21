pip install virtualenv
virtualenv myenv
cd myenv
source bin/activate
cd ..
pip install django
django-admin startproject project_name
cd project_name
python3 manage.py runserver
(move myenv to project_name folder)
python3 manage.py startapp base
'base.apps.BaseConfig', # Add this line to the list of installed apps in main folder
In urls.py of main folder, we can add routes of the app
For better practice, we will create urls.py file in base directory