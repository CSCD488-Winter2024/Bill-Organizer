The source code is in two directories. 
### backend
The backend code is in the root directory of this github repo and in the "/handlers/" folder. consisting of the files:
- main.py
- cfg.py
- handler.py defines an interface that could be inherited by other handler classes such as wa_leg.py (though it doesnt use it)
- util.py has helper functions used in the backend. Some of these are used by the frontend's "/bill_app/utils.py" file
- create-db.sql
- /handlers/wa_leg.py

### frontend
The frontend code is in "/frontend/billorganizer_frontend/". Most of this code is created by Django.
- "/bill_app/" has most of the relevant frontend code. 
    - /bill_app/utils.py has functions for interfacing with the backend and database
    - /bill_app/views.py has python functions for displaying webpages
    - /bill_app/models.py has classes based on each database table [(see django models)](https://docs.djangoproject.com/en/5.0/topics/db/models/)
    - /bill_app/static/ has css and javascript that is used by the templates in "/billorganizer_frontend/templates/". those templates are then used by /bill_app/views.py to create webpages.
- "/billorganizer_frontend/" has configuration for django, as well as templates for webpages
    - /billorganizer_frontend/templates/ has templates which are imported by */views.py
    - /billorganizer_frontend/urls.py links the functions in */views.py files to website subdirectories.
    - /billorganizer_frontend/settings.py controls django settings.
- /accounts/view.py has code for the signup page.

### building the software
To learn about building the software, see the readme on the main page of this repo.