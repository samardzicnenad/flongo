# Flongo
## Description:
Flongo is a "template app" for the Python/Flask - MongoDB environment.  
It also provides a simple user management system that serves the following API endpoints:
- <b>/</b> (it will redirect to /login or /index depending on the existence of the active user session)
- <b>/signup</b>
- <b>/login</b>
and
- <b>/index</b>  

There is also an auxiliary endpoint:  
- <b>/info</b>  

which is not actually a part of the project, but exists in order to provide additional info to the app users.

Once a user signs up and logs in, the session cookie is created and it is valid for 30 minutes

## Usage:
Running
<pre>
$ docker-compose up
</pre>
command will pull images and build, create, start and link the container instances for the services defined in the docker-compose.yml file, resulting in flongo app running on:
<pre>
http://0.0.0.0:80/
</pre>
* docker-compose.yml defines three services that will get started and linked:
  * flongo (python:2.7.12 with the following dependencies: flask, pymongo, libsass)
  * nginx
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

## Notes:
- during the login and signup processes, non ascii characters will be ignored
