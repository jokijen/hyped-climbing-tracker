# Hyped - An outdoors climbing tracker

Hyped is a web application that allows users to track routes they have climbed outdoors, rate them, add crags to favourites, and manage a tick-list (a “to-climb” list) for future adventures.

Every user is either a regular user or administrator.

The web app is built using Python and Flask. It uses a PostgreSQL database, with HTML and CSS for the frontend.

## Table of contents
- [Motivation](#Motivation)
- [Application functionality and features](#application-functionality-and-features)
- [Current state of the application](#current-state-of-the-application)
- [Testing the application in production](#testing-the-application-in-production)
- [Credits](#Credits)


## Motivation

This project has been created for learning purposes and the course "Tietokannat ja web-ohjelmointi" (University of Helsinki).


## Application functionality and features

- The home page (after login) has links to the user's favourite crags, tick-list, logbook, all crags, all climbs, and a top 10 list of popular/logged climbs for all users.
- Users can sign up for a new account, and log in or out.
- Users can log routes they have climbed (and review them). They can also add a public comment.
- Users can manage a tick-list of routes they want to climb in the future. (Once climbed, routes can be moved from the tick-list to the logbook.)
- Users can add a crag to favourites, and view favourites as a list.
- Users can search for crags and climbs with a specific word in the name, difficulty, type, or description.
- Administrators can also add, edit, and delete crags.
- Administrators can also add, edit, and delete routes.
- Administrators can additionally remove user comments on routes.

### Crags

- Common to users.
- Crags have a name, location, count of routes, and count of times favourited by users.

### Climbs

- Common to users.
- Climbs have a name, difficulty/grade (font-grade), and type (boulder, sport, trad, DWS).
- Each route also has a rating (0–3) calculated from user ratings, count of logged sends, and public user comments.

### Logbook and tick-list

- Personal to users.
- Logbook and tick-list consist of individual routes added by the user. 
- Once a user logs a climb, it will vanish from the tick-list if it was there. 

### Favourite crags

- Personal to users.
- Favourite crags consist of crags added to favourites by the user.


## Current state of the application

The development of the Hyped application is progressing well with the main stucture in place. There has been some development in what functionality seems necessary and important for the application. 

- Usability and features: Users can register and log in/out. Users can view their profile and change their password. Sessions are managed. Users can search for crags/climbs and mark climbs as sent. Users can view crag/climb information, including comments and sends logged by users. Admin users can add crags and climbs. Users can add crags to favourites. Users can add climbs to tick-lists. Users can write and delete their comments. Front page shows latest sends and a search.
- Backend / Python, Flask: There are files for routes, users, crags, climbs, ticklist, sends, and comments to manage different aspects of the app. 
- Database: A database schema has been created and updated from the intial version. There is also a data-dump file for testing purposes. 
- Front / HTML: The login and registration pages are complete. The home page visible after login has a structure in place, but it's not finalised yet. The favourite crags, tick-list, and logged sends of users, as well as crag and climb pages are almost finished. There is a profile page for the user (with the possibility to change the password). Flash messaging has been introduced to most forms to give the user feeback. 
- Formatting: A style.css file has been created for formatting, and a logo has been designed in both black and white. The style of the website is not yet finalized. 
- Next up: Users can edit/delete their sends. 
 
Overall, the project has made decent progress with most key elements in place or nearly completed. All feedback is very welcome. Development will continue on from here.


## Testing the application in production

You can test the application by taking the following steps: 
1. Clone the repository and go to its root directory
2. Create a file .env and add "DATABASE_URL=" with path to database and "SECRET_KEY=" with a secret key
3. Create a virtual environment with $ python3 -m venv venv
4. Activate the virtual environment with $ source venv/bin/activate
5. Install all the necessary packages using pip with $ pip install -r requirements.txt
6. Start up PostgreSQL with $ start-pg.sh (you can use it in terminal with the command psql) - PostgreSQL was installed using a custom installation script that can be found here: https://github.com/hy-tsoha/local-pg
7. Set up the database schema, run (in the app directory) $ psql < schema.sql
8. If you want to populate your database, create two users by running the app and registering new users, and then run the commands in the prepared data file. Run the following command (in the app directory) run $ psql < prepared_data.sql
8. Start the application with $ flask run


## Credits

- Logo font: Befolk (free commercial license) by Hendra Dirtyline at Dirtyline Studio
https://dirtylinestudio.com/product/befolk-script/
- Climbing thesaurus: Produced by ChatGPT-4o, when given a prompt with terms to be included as well as asking for some similar ones to be added. Small edits to the content made manually.  
- Prepared data: ChatGPT-4o has been very helpful in creating test input data for the database. Nevertheless, most crags and climbs are existing ones. 
