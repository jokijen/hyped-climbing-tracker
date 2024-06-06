# Hyped - An outdoors climbing tracker

Hyped is a web application that allows users to track routes they have climbed outdoors, rate them, add crags to favourites, and manage a tick-list (a “to-climb” list) for future adventures.

Every user is either a regular user, editor, or administrator.

The web app is built using Python and Flask. It uses a PostgreSQL database, with HTML and CSS for the frontend.

## Table of contents
1. [Application functionality and features](#application-functionality-and-features)
2. [Current state of the application]
(#current-state-of-the-application)
3. [Testing the application in production]
(#testing-the-application-in-production)

## Application functionality and features

- The front page (after login) has links to the logbook, tick-list, favourite crags, all crags, and a top 10 list of popular/logged climbs for all users.
- Users can sign up for a new account, and log in or out.
- Users can log routes they have climbed (including dates). They can add a personal note and/or a public comment.
- Users can manage a tick-list of routes they want to climb in the future. (Once climbed, routes can be moved from the tick-list to the logbook.)
- Users can add a crag to favourites, and view favourites as a list.
- Users can search for crags with a specific word in the name, description, or location.
- Users can search for routes with a specific word in the name, description, or difficulty.
- Editors can also add, edit, and delete crags.
- Editors can also add, edit, and delete routes.
- Administrators can additionally remove user comments on routes.

### Crags

- Common to users.
- Crags have a name, location, count of routes, and count of times favourited by users.

### Routes

- Common to users.
- Routes have a name, difficulty/grade (font-grade), and type (boulder, sport, trad, DWS).
- Each route also has a rating (stars: 0–3) calculated from user ratings, count of logged climbs, and public user comments.

### Logbook and tick-list

- Personal to users.
- Logbook and tick-list consist of individual routes added by the user.

### Favourite crags

- Personal to users.
- Favourite crags consist of crags added to favourites by the user.


## Current state of the application

The development of the Hyped application is progressing with early versions of many key components either initiated or done:
 
- Backend (Python, Flask): The routes.py file has been started. Additionally, there are various Python files including climbs.py, crags.py, and users.py to manage different aspects of the app.
- Database: An initial schema.sql file has been created to define the database, but otherwise the database side of the development is in very early stages.
- HTML: The login and registration pages are fairly complete. The home page visible after login has a structure in place.
- Formatting: An initial style.css file has been created for formatting, and a logo has been designed in both black and white. The style of the website is not yet finalized, which is why there may be variation on different pages.
 
Overall, the project has made fairly decent progress with some base elements in place or initiated. All feedback is very welcome. Development will continue on from here.


## Testing the application in production

You can test the application by taking the following steps: 
1. Clone the repository and go to its root directory
2. Create a directory .env and add "DATABASE_URL=" with path to database and "SECRET_KEY=" with a secret key
3. Create a virtual environment with $ python3 -m venv venv
4. Activate the virtual environment with $ source venv/bin/activate
5. Install all the necessary packages using pip with $ pip install -r requirements.txt
6. Start up PostgreSQL with $ start-pg.sh (you can use it in terminal with the command psql) - PostgreSQL was installed using a custom installation script that can be found here: https://github.com/hy-tsoha/local-pg
7. Set up the database schema with $ psql < schema.sql
8. Start the application with $ flask run