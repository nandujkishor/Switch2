# Vidyut Switch

Vidyut's web services platform forked from Amblygon Polaris base for [Amblygon Flannel](https://flannel.amblygon.org).

## Installation

This guide provides a walkthrough to getting started with Switch on a local machine. Please keep in mind that the application is being written in Python *3*.

Set-up Virtual Environment in the prefered location. Please ensure you have the latest version of Python 3 installed.
~~~
python3 -m venv venv
~~~
Enter the virtual environment
~~~
. venv/bin/activate
~~~
Install the requirements
~~~
pip install -r requirements.txt
~~~

Please make the environment variable FLASK_APP set to the file *switch.py*

In Linux or UNIX devices, this can be done via

~~~
export FLASK_APP=switch.py
~~~

Flask-Migrate extension is currently in use in the application in order to track the changes made frequently to the database schema. This results in the need to manually migrating the database with each change.

If using a seperate database, please perform the following operations on first use to build the necessary database tables. Please DO NOT perform if using the existing clould instances.

~~~
flask db init
flask db migrate
flask db upgrade
~~~

For each change to the Database model, please enter the following commands to add the new changes and commit to the database. If using existing shared cloud database solutions, please ask the developer managing the migrations.

~~~
flask db migrate
flask db upgrade
~~~

## To run the app

Be inside the switch directory.
~~~
flask run
~~~

To enable debugging during development, set FLASK_ENV environment variable to "development" (without the quotes).

~~~
export FLASK_ENV=development
export FLASK_DEBUG=true
~~~

>>>
Commit and one major / few minor feature(s) at a time. Please remember to put pull requests for major features and properly document new additions.
>>>

*Let's make Vidyut a grand success*

Please find the project deadlines in the telegram group and issues and tasks in Microsoft Planner.
