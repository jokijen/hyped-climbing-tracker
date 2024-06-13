/* Before using this file to populate your database, create two users using the web app, which will give you users with properly hashed passwords. 
This will make your two first users (ids 1 and 2) admin users and attribute the data here to them */

-- users --
UPDATE users SET administrator = 't' WHERE id = 1;

UPDATE users SET administrator = 't' WHERE id = 2;


-- crags --
INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by) VALUES ('Noppavuori', 66.990507, 22.385750, 'Poor quality rock, but great routes', 'Harjasankari', 1);

INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by) VALUES ('Tikankallio', 60.688663, 26.036672, 'An amazing north-east facing crag with excellent routes', 'Saimaan kiipeilijät ry', 1);

INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by) VALUES ('Rotkokallio', 60.714508, 26.270848, 'A small crag with slightly chossy rock, but excellent routes. Bring a clip-stick!', 'J. Koski', 1);

INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by) VALUES ('Tikankallio', 62.623376, 27.212458, 'An amazing boulder crag with challenging problems. Very close to private property so please keep quiet and do NOT park too close to the house.', 'Pasami', 1);


-- climbs --
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, manager, created_by) VALUES ('Polku', '6B+', 'boulder', 'slab, technical footwork', 1, 'Harjasankari', 1);

INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, manager, created_by) VALUES ('Mania', '8b', 'sport', 'technical and continous on small crimps', 2, 'Saimaan kiipeilijät ry', 1);

INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, manager, created_by) VALUES ('Onda', '7a', 'sport', 'sharp crimps', 2, 'Saimaan kiipeilijät ry', 1);

INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, manager, created_by) VALUES ('Half century', '8a', 'sport', 'Very powerful start and a hold broke off so it''s more difficult now.', 3, 'J. Koski', 1);

INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, manager, created_by) VALUES ('Kiviset ja soraset', '7a+', 'trad', 'Technical along a narrow crack. Sketchy traverse at the start', 2, 'Saimaan kiipeilijät ry', 1);


-- sends --
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (2, 3, '2023-04-25', 'onsight', 'Excellent crimps.', 1);


-- comments --
INSERT INTO comments (user_id, climb_id, comment) VALUES (2, 3, 'Some birds are nesting on the shelf on the left. It''s better to not climb during their nesting time.');


-- favourite crags --
INSERT INTO favourite_crags (user_id, crag_id) VALUES (1 , 1);

INSERT INTO favourite_crags (user_id, crag_id) VALUES (1 , 3);

INSERT INTO favourite_crags (user_id, crag_id) VALUES (2 , 2);


-- ticklist --
INSERT INTO ticklist (user_id, climb_id) VALUES (1 , 3);

INSERT INTO ticklist (user_id, climb_id) VALUES (2 , 2);

INSERT INTO ticklist (user_id, climb_id) VALUES (2 , 4);
