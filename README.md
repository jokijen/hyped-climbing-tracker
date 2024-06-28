# Hyped - An outdoors climbing tracker

Hyped is a web application that allows users to track routes they have climbed outdoors, rate them, add crags to favourites, and manage a tick-list (essentially a “to-climb” list) for future adventures.

Every user is either a regular user or administrator.

The web app is built using Python and Flask. It uses a PostgreSQL database, with HTML and CSS for frontend.

## Table of contents
- [Motivation](#Motivation)
- [Application functionality and features](#application-functionality-and-features)
- [Current state of the application](#current-state-of-the-application)
- [Testing the application](#testing-the-application)
- [Using the app](#using-the-app)
- [Credits](#Credits)


## Motivation

This project has been created for learning purposes and the course "Tietokannat ja web-ohjelmointi", 2024 (University of Helsinki).


## Application functionality and features

- Users can sign up for a new account, and log in or out.
- The home page (after login) dislplays a list of the 5 latest sends that users have added to the app. The navigation sidebar has links to the user's favourite crags, tick-list, logbook, all crags, all climbs, random crag and climb, thesaurus, and profile.
- Users can search for crags and climbs with a specific word in the name, difficulty, type, or description.
- Users can add a crag to favourites, or remove it, and view their favourites as a list.
- Users can add climbs that they want to climb in the future to a tick-list, as well as remove them.
- Users can log (incl. review) routes they have climbed. They can also add public comments under the climbs.
- Administrators can also add crags and climbs. 
- Administrators can remove user comments on routes.

### Crags

- Common to users.
- Crags have a name, location, count of routes, difficulty range of climbs at the crag, and count of times favourited by users.

### Climbs

- Common to users.
- Climbs have a name, difficulty/grade (font-grade), and type (boulder, sport, trad, DWS).
- Each route also has a rating (0–3) calculated from user ratings, count of logged sends, and public user comments.
- A user can see the tick and send count of climbs.

### Logbook and tick-list

- Personal to users.
- Logbook and tick-list consist of individual climbs marked sent by the user. 
- Once a user logs a climb, it will vanish from the tick-list if it was there. 

### Favourite crags

- Personal to users.
- Favourite crags consist of crags added to favourites by the user.


## Current state of the application

The Hyped application is fully functional and development is complete.

### Completed features

Features have been completed as per [Application functionality and features](#application-functionality-and-features) and the application is ready for use.

For the purposes of the course, this scope seemed reasonable and some changes were made to the intial plan. The primary objectives were learning diverse features and development techniques, as opposed to implementing numerous features that are technically very similar to one-another. For this reason some initial feature ideas were removed and new ones added. In order to focus on finding ways to implement all features using HTML and CSS, JavaScript was exclueded from the project.

### Development overview

- Backend / Python, Flask: There are separate files for routes, climbs, comments, crags, favourites, sends, ticklist, and users to manage different aspects of the app. 
- Database: The database schema.sql file provides the schema for the database and the prepared_data.sql file can be used to populate the database when testing. 
- Front / HTML: File layout.html holds the structure of the page including the navigation sidebar. Separate html files for each page have the main content for that page. 
- Formatting: File style.css handles formatting. A white logo with no background is placed on top of the navigation sidebar. 

### Potential further development

- Social features: Allowing users to build up their profile, as well as follow and message each other.
- Statistics: Features to display various statistics for the user.
- Admin tools: Providing a wider selection of tools and features for admins.


## Testing the application

You can test the application by taking the following steps: 
1. Clone the repository and go to its root directory
2. Create a file .env and add "DATABASE_URL=" with path to database and "SECRET_KEY=" with a secret key
3. Create a virtual environment with $ python3 -m venv venv
4. Activate the virtual environment with $ source venv/bin/activate
5. Install all the necessary packages using pip with $ pip install -r requirements.txt
6. Start up PostgreSQL with $ start-pg.sh (you can use it in terminal with the command psql) - PostgreSQL was installed using a custom installation script that can be found here: https://github.com/hy-tsoha/local-pg
7. Set up the database schema, run $ psql < schema.sql
8. If you want to populate your database, create two users by using the app and registering two new users. Then run the commands in the prepared data file by running the following command (in the app directory) run $ psql < prepared_data.sql
8. Start the application with $ flask run


## Using the app

1. Register a new user
2. Log in to access the features
3. Browse crags and climbs, add crags to favourites, tick climbs or mark them sent, and comment on climbs. Admin users may add new crags and climbs.
4. Log out


## Credits

- Logo font: Befolk (free commercial license) by Hendra Dirtyline at Dirtyline Studio
https://dirtylinestudio.com/product/befolk-script/
- Climbing thesaurus: Produced by ChatGPT-4o, when given a prompt with terms to be included as well as asking for some similar ones to be added. Small edits to the content made manually.  
- Prepared data: ChatGPT-4o has been very helpful in creating test input data for the database. Nevertheless, most crags and climbs are existing ones. 
