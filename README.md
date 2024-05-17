# Hyped - An outdoors climbing tracker

Hyped is a web application that allows users to track routes they have climbed outdoors, rate them, add crags to favourites, and manage a tick-list (a “to-climb” list) for future adventures.

Every user is either a regular user, editor, or administrator.

The web app is built using Python and Flask. It uses a PostgreSQL database, with HTML and CSS for the frontend.

## Table of contents
1. [Application functionality and features](#application-functionality-and-features)

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
