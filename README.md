# MOS images status web application

## Introduction
We have many Jenkins jobs which build MOS images and executed
different automated tests, in the result it is not easy to
see the whole picture oin the one place.

## How It Works
This application contain two components.

The first component is a Python script which use
Jenkins API to collect data about all Jenkins jobs
executions, their results and all downstream jobs results.

The second component is the web application which
shows the all information in one table for each MOS release.

## How To Deploy The Application
To deploy this application on the new environment we
first of all need to install the requirements:

> // in Ubuntu:
> apt-get install -y mongodb python python-pip
> pip install pymongo jenkinsapi

> // in CentOS:
> yum install -y mongodb python python-pip                                  
> pip install pymongo jenkinsapi

After the reqirements installation we can execute script which will
create the database with the information about Jenkins jobs execution
and then start the web application which will show the data from
the data base.
