Mothership Dispatcher.
=====================

(0) create a virtual environment.  Populate the VE by running pip install -r requirements.txt

(1) The project consists of two processes: the django web application launched in the usual
way, either by manage.py runserver or by launching using uwsgi. The other 
process is a lightweight dispatcher.  In a production environment, one would
use Celery or a similar utility to run periodic requests. 

(2) The project requires a PostgreSQL/PostGIS datbase in order to run.  In my submission, I will
include a link to an LXD container including the django web server and a correctly configured 
database. If not using the dehydrated container, create a database called maship, user maship 
has all rights on db maship and has password maship.  as user maship, psql maship to get into the
psql console.  Create the geospatial tables by running CREATE EXTENSION POSTGIS.  Now create the 
db tables by running >python manage.py migrate.  Finally, an ETL routine has been provided 
to populate the database - to run the ETL routine,
in a terminal window with an activated virtual environment, cd to the etl directory and invoke 
>python import_data.py.  This will create three tables: shipment, driver and dispatch. It will 
populate shipment and driver with the data included in the problem.  NOTE that it may be necessary
to play with the PYTHONPATH environment variable in order for python to find the various application
modules.  In my environment, PYTNONPATH is set to the directory containing the project.

(3) Start the web server.

(4) Start the dispatch in another terminal.  Be sure that the virtual environment is activated.
To invoke the dispatcher cd maship/task and then python dispatcher.py.  The dispatcher will cycle
until all shipments have been dispatched and then stop.




