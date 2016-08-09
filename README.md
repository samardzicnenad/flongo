# Flongo
## Description:
Flongo is a "template app" for the Flask - MongoDB environment.  
It also provides a simple user management system that serves the following API endpoints:
- <b>/</b> (it will redirect to /login or /index depending on the existence of the active user session)
- <b>/signup</b>
- <b>/login</b>
and
- <b>/index</b>  

There is also an auxiliary endpoint:  
- <b>/info</b>  

which is not actually a part of the project, but exists in order to provide additional info to the app users.

## Usage:
Running
<pre>
$ docker-compose up
</pre>
command will build, create, start and link the container instances for the services defined in the docker-compose.yml file, resulting in web app running on:
<pre>
http://0.0.0.0:5000/
</pre>
* docker-compose.yml defines two services that will get started and linked:
  * web (python:2.7.12 with the following dependencies: flask, pymongo, libsass)
  * mongo (mongo:3.3.10)
  
## Data model specifics:
The app stores data in three tables:
- users
  - usernames and email addresses are unique
- sessions
  - the list of the most recent user sessions
- past_sessions
  - the list of the past user sessions

## Templates and styling:
The app uses:
- jinja2 - templating system and
- libsass - flask extension for building css from sass or scss
