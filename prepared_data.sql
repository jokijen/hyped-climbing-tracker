/* Before using this file to populate your database, create two users using the web app, which will give you users with properly hashed passwords. 
This will make your two first users (ids 1 and 2) admin users and attribute the data here to them */

-- users --
UPDATE users SET administrator = TRUE WHERE id = 1;
UPDATE users SET administrator = TRUE WHERE id = 2;


-- crags --
INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by) VALUES ('Noppavuori', 66.990507, 22.385750, 'Poor quality rock, but great routes', 'Harjasankari', 1);
INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by) VALUES ('Tikankallio', 60.688663, 26.036672, 'An amazing north-east facing crag with excellent routes', 'Saimaan kiipeilijät ry', 1);
INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by) VALUES ('Rotkokallio', 60.714508, 26.270848, 'A small crag with slightly chossy rock, but excellent routes. Bring a clip-stick!', 'J. Koski', 1);
INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by) VALUES ('Siipola', 62.623376, 25.429854, 'An amazing boulder crag with challenging problems. Very close to private property so please keep quiet and do NOT park too close to the house.', 'Pasami', 1);
INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by) VALUES ('Falkberget', 61.749385, 24.428394, 'A majestic cliff that''s very high for Finland. Facing south-west so very hot during the summer. Mostly overhanging or vertical.', 'Team Korppi', 1);


-- climbs --
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Polku', '6B+', 'boulder', 'slab, technical footwork', 1, 'Tomi K.', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Mania', '8b', 'sport', 'technical and continous on small crimps', 2, 'Anna L.', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Onda', '7a', 'sport', 'sharp crimps', 2, 'Jussi L.', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Half century', '8a', 'sport', 'Very powerful start and a hold broke off so it''s more difficult now.', 3, 'J. Koski', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Kiviset ja soraset', '7a+', 'trad', 'Technical along a narrow crack. Sketchy traverse at the start', 2, 'Jussi L.', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Hoptinen illuusio', '6c+', 'sport', 'starts on the boulder, clip anchor', 2, 'Jussi L.', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Matador', '8a', 'sport', 'mega-classic', 5, 'Korppi', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Charlatan', '7c', 'sport', 'many styles in one', 5, 'Korppi', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Renesanssi', '7b+', 'sport', 'technical, hard to onsight', 5, 'Korppi', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Hippa-Heikki', '7b+', 'sport', 'poor rock-quality, pre-clip recommended', 3, 'J. Koski', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Dyno-K', '7b+', 'sport', 'pre-clip recommended', 3, 'J. Koski', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Yatzin orjat', '6c+', 'sport', 'starts on the shelf, continuous', 3, 'J. Koski', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('The Globalist', '8B+', 'boulder', 'burly and powerful', 4, 'Pasami', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Hypergravity', '8B', 'boulder', 'roof, powerful', 4, 'Pasami', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Spider pig', '8A', 'boulder', 'a powerful classic', 4, 'Nalle', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Reitti 2', '7B', 'boulder', 'vertical, delicate with small crimps', 1, 'Minni E.', 1);
INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by) VALUES ('Haastemies', '8A', 'boulder', 'slopers, pumpy', 1, 'Samu E.', 1);


-- sends --
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (2, 3, '2023-04-25', 'onsight', 'A nice climb! Loved the moves.', 0);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (1, 2, '2023-05-10', 'send', 'Excellent crimps and a fantastic continuous climb.', 3);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (1, 4, '2023-06-01', 'send', 'Tough route, but managed it after five sessions.', 1);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (1, 5, '2023-06-15', 'send', 'Finally sent it! Very satisfying.', 1);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (1, 6, '2023-06-20', 'onsight', 'Enjoyable climbing from start to finish.', 1);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (1, 7, '2023-07-05', 'flash', 'Intense climb, great holds.', 2);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (1, 1, '2023-06-12', 'flash', 'A nice slab.', 0);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (2, 2, '2023-07-03', 'send', 'I struggled with the small crimps, but overall the route is fantastic.', 3);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (1, 3, '2023-09-11', 'onsight', 'Great climb, the sharp crimps are tricky.', 2);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (2, 4, '2023-09-15', 'send', 'Powerful start indeed. I had to stack a few rocks just to reach the new starting hold', 2);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (2, 5, '2023-10-21', 'send', 'Narrow crack was a challenge.', 1);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (2, 6, '2023-11-05', 'flash', 'Like an indoor route, but outdoors.', 1);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (2, 7, '2023-10-02', 'send', 'Mega-classic indeed!', 3);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (2, 8, '2022-04-10', 'flash', 'Variety of styles, loved it.', 2);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (1, 9, '2023-04-14', 'onsight', 'Hard to onsight but managed. Almost fell close to the top.', 1);
INSERT INTO sends (user_id, climb_id, send_date, send_type, review, rating) VALUES (2, 10, '2024-03-19', 'flash', 'Pre-clip recommended for sure.', 2);


-- comments --
INSERT INTO comments (user_id, climb_id, content) VALUES (2, 3, 'Some birds are nesting on the shelf on the left. It''s better to not climb during their nesting time.');
INSERT INTO comments (user_id, climb_id, content) VALUES (1, 1, 'Great climb, but very crowded on weekends.');
INSERT INTO comments (user_id, climb_id, content) VALUES (1, 2, 'Watch out for loose rocks near the top.');
INSERT INTO comments (user_id, climb_id, content) VALUES (2, 5, 'Perfect for a sunny day. Gets good shade in the afternoon.');
INSERT INTO comments (user_id, climb_id, content) VALUES (1, 6, 'Pretty technical route. Definitely worth trying.');
INSERT INTO comments (user_id, climb_id, content) VALUES (1, 7, 'Very challenging! Need to improve my footwork.');
INSERT INTO comments (user_id, climb_id, content) VALUES (2, 1, 'The slab section is quite smooth.');
INSERT INTO comments (user_id, climb_id, content) VALUES (2, 2, 'Crimps are really small and challenging.');
INSERT INTO comments (user_id, climb_id, content) VALUES (1, 3, 'Sharp holds, take care with your fingers.');
INSERT INTO comments (user_id, climb_id, content) VALUES (2, 4, 'Powerful moves at the start, great climb.');
INSERT INTO comments (user_id, climb_id, content) VALUES (1, 5, 'Narrow crack makes it a bit tricky. Needs really small cams.');
INSERT INTO comments (user_id, climb_id, content) VALUES (2, 6, 'Anchor placement may be a challenge for shorter climbers.');
INSERT INTO comments (user_id, climb_id, content) VALUES (2, 7, 'Lives up to the hype, great route.');
INSERT INTO comments (user_id, climb_id, content) VALUES (2, 14, 'Someone left a brush and a mini-hangboard close to this line. I put them under the roof to keep them safe from rain :)');
INSERT INTO comments (user_id, climb_id, content) VALUES (1, 9, 'Difficult to onsight, very technical, but such a cool one.');
INSERT INTO comments (user_id, climb_id, content) VALUES (2, 10, 'Rock quality is a bit poor, be cautious.');


-- favourite crags --
INSERT INTO favourite_crags (user_id, crag_id) VALUES (1, 1);
INSERT INTO favourite_crags (user_id, crag_id) VALUES (1, 3);
INSERT INTO favourite_crags (user_id, crag_id) VALUES (1, 5);
INSERT INTO favourite_crags (user_id, crag_id) VALUES (2, 4);
INSERT INTO favourite_crags (user_id, crag_id) VALUES (2, 2);


-- ticklist --
INSERT INTO ticklist (user_id, climb_id) VALUES (1, 13);
INSERT INTO ticklist (user_id, climb_id) VALUES (2, 12);
INSERT INTO ticklist (user_id, climb_id) VALUES (2, 14);
INSERT INTO ticklist (user_id, climb_id) VALUES (1, 16);
INSERT INTO ticklist (user_id, climb_id) VALUES (2, 17);