-- noinspection SqlNoDataSourceInspectionForFile

-- e. For each type of restaurant (e.g. Indian or Irish) and the category of menu item (appetiser, main
-- or desert), list the average prices of menu items for each category.   

--CONFIRMED 

SELECT R.type, MI.category, AVG(MI.price) AS average_price FROM Menu_Item MI, Restaurant R 
	WHERE
		MI."restaurantId" IN 
		(SELECT R1."restaurantId" FROM Restaurant R1 WHERE
			R1.type = R.type)
		AND MI."restaurantId" = R."restaurantId"
	GROUP BY R.type, MI.category ORDER BY R.type, MI.category

--------------------------- Ratings of restaurants ------------------------------------------------

-- f. Find the total number of rating for each restaurant, for each rater. That is, the data should be
-- grouped by the restaurant, the specific raters and the numeric ratings they have received.

--CONFIRMED

SELECT U."userId", R.name, AVG((R8.food+R8.mood+R8.staff+R8.price)/4) AS average , COUNT(R8)
	FROM Rating R8, Restaurant R, Rater U WHERE
	R8."restaurantId" = R."restaurantId" AND R8."userId" = U."userId"
	 GROUP BY R.name, U."userId" ORDER BY R.name , average 

-- g. Display the details of the restaurants that have not been rated in January 2015. That is, you
-- should display the name of the restaurant together with the phone number and the type of
-- food.

--Confirmed

Select R.name, R.type, L.phone_number FROM  Restaurant R,  Location L WHERE 
	NOT EXISTS(SELECT * FROM  Rating R8 WHERE
		date_part('year',R8."postDate") = 2015 AND date_part('month',R8."postDate") = 01
		AND R8."restaurantId" = R."restaurantId")
	AND R."restaurantId" = L."restaurantId" ORDER BY R.name;  

-- h. Find the names and opening dates of the restaurants that obtained Staff rating that is lower
-- than any rating given by rater X. Order your results by the dates of the ratings. (Here, X refers to
-- any rater of your choice.)

SELECT R.name, L.manager_name FROM Restaurant R, Location L WHERE
	R."restaurantId" IN (SELECT R8."restaurantId" FROM Rating R8 WHERE
		R8.staff < ANY(SELECT Rate.staff FROM Rating Rate WHERE
			Rate."userId" = 'Bibo110'))
	AND R."restaurantId" = L."restaurantId";

-- i. List the details of the Type Y restaurants that obtained the highest Food rating. Display the
-- restaurant name together with the name(s) of the rater(s) who gave these ratings. (Here, Type Y
-- refers to any restaurant type of your choice, e.g. Indian or Burger.)  
	
--CONFIRMED (THIS ONE DONE HERE)

SELECT restaurant.name, U.name FROM restaurant, rater U WHERE
	restaurant."restaurantId" IN (SELECT R8."restaurantId" FROM rating R8 WHERE
		R8."restaurantId" IN (SELECT R1."restaurantId" FROM restaurant R1 WHERE
				R1.type = 'American')
		AND
		R8.food >= All(SELECT Rate.food FROM rating Rate WHERE
			Rate."restaurantId" IN (SELECT R2."restaurantId" FROM restaurant R2 WHERE
				R2.type = 'American'))
		AND
		R8."userId" = U."userId");

-- j. Provide a query to determine whether Type Y restaurants are “more popular” than other
-- restaurants.  (Here, Type Y refers to any restaurant type of your choice, e.g. Indian or Burger.)
-- Yes, this query is open to your own interpretation!

--PLAUSIBLE

SELECT ROW_NUMBER() OVER(ORDER BY OverallRating DESC) AS Ranking, OverallRating, Type
 	FROM
		(SELECT AVG("overallRating") AS OverallRating, R.type AS Type FROM
		 	 Restaurant R GROUP BY R.type) AS WhoCares
	WHERE Type = 'Chinese';

---------------------------- Raters and their ratings ----------------------------------------------

-- k. Find the names, join‐date and reputations of the raters that give the highest overall rating, in
-- terms of the Food and the Mood of restaurants. Display this information together with the
-- names of the restaurant and the dates the ratings were done.

--CONFIRMED

SELECT U.name, U.join_date, U.reputation, R.name, R8."postDate" FROM  Rater U,  Restaurant R,  Rating R8 WHERE 
	U."userId" IN (SELECT U1."userId" FROM  Rater U1 group by U1."userId" HAVING
		(SELECT AVG(Rate.mood  + Rate.food ) FROM  Rating Rate WHERE
			Rate."userId" = U1."userId")
		>= ALL(SELECT AVG(Rate1.mood  + Rate1.food ) FROM  Rating Rate1,  Rater U2 WHERE
			Rate1."userId" = U2."userId" GROUP BY U2."userId"))
	AND R8."userId" = U."userId" AND R8."restaurantId" = R."restaurantId"

-- l. Find the names and reputations of the raters that give the highest overall rating, in terms of the
-- Food or the Mood of restaurants. Display this information together with the names of the
-- restaurant and the dates the ratings were done.

--CONFIRMED

SELECT U.name, U.join_date, U.reputation, R.name, R8."postDate" FROM  Rater U,  Restaurant R,  Rating R8 WHERE
	U."userId" IN (SELECT U1."userId" FROM  Rater U1 WHERE
		(SELECT AVG(mood ) FROM  Rating Rate WHERE Rate."userId" = U1."userId")
			>= ALL(SELECT AVG(mood ) FROM  Rating Rate GROUP BY Rate."userId")
		OR (SELECT AVG(food ) FROM  Rating Rate WHERE Rate."userId" = U1."userId")
			>= ALL(SELECT AVG(food ) FROM  Rating Rate GROUP BY Rate."userId"))
		AND R8."userId" = U."userId" AND R8."restaurantId" = R."restaurantId";

-- m. Find the names and reputations of the raters that rated a specific restaurant (say Restaurant Z)
-- the most frequently. Display this information together with their comments and the names and
-- prices of the menu items they discuss. (Here Restaurant Z refers to a restaurant of your own
-- choice, e.g. Ma Cuisine).

-- do one ot the the or or both

--CONFIRMED

SELECT U.name, U.reputation, R8.comment FROM  Rating R8,  Rater U WHERE 
	U."userId" IN (SELECT U1."userId" FROM  Rater U1 WHERE
		(SELECT COUNT(*) FROM  Rating Rate WHERE Rate."userId" = U1."userId" AND
			Rate."restaurantId" IN (SELECT R."restaurantId" FROM  Restaurant R WHERE
				R.name ='Pai'))
		>=  All(SELECT COUNT(*) FROM  Rating Rate1 WHERE 
			Rate1."restaurantId" IN (SELECT R."restaurantId" FROM  Restaurant R WHERE
				R.name ='Pai') GROUP BY Rate1."userId"))
	AND R8."userId" = U."userId" AND R8."restaurantId" IN (SELECT R."restaurantId" FROM  Restaurant R WHERE
				R.name ='Pai') 

-- n. Find the names and emails of all raters who gave ratings that are lower than that of a rater with
-- a name called John, in terms of the combined rating of Price, Food, Mood and Staff. (Note that
-- there may be more than one rater with this name).

-- CONFIRMED

SELECT U.name, U.email FROM Rater U WHERE
	U."userId" IN (SELECT R8."userId" FROM Rating R8 WHERE
		(R8.price  + R8.food  + R8.mood  + R8.staff )
		< ANY(SELECT (Rate.price  + Rate.mood  + Rate.food  + Rate.staff ) FROM Rating Rate WHERE
			Rate."userId" IN (SELECT U1."userId" FROM Rater U1 WHERE
				U1.name = 'John')));

-- o. Find the names, types and emails of the raters that provide the most diverse ratings. Display this
-- information together with the restaurants names and the ratings. For example, Jane Doe may
-- have rated the Food at the Imperial Palace restaurant as a 1 on 1 January 2015, as a 5 on 15
-- January 2015, and a 3 on 4 February 2015.  Clearly, she changes her mind quite often.

-- use standard deviaton

SELECT U.name, U.type, U.email, R.name, R8.food , R8.price , 
	R8.mood , R8.staff , R8.comment FROM  Rater U,  Rating R8,  Restaurant R WHERE
		U."userId" IN (SELECT U1."userId" FROM  Rater U1 GROUP BY U1."userId" HAVING
			(SELECT max(stddev) FROM(SELECT stddev(Rate.mood  + Rate.staff  + Rate.price  +Rate.food ) as stddev 
				FROM  Rating Rate WHERE Rate."userId" = U1."userId" GROUP BY Rate."restaurantId") as whoCares)
			>= ALL((SELECT max(stddev) FROM (SELECT stddev(Rate1.mood  + Rate1.staff  + Rate1.price  +Rate1.food ) FROM  Rating Rate1 GROUP BY Rate1."userId", Rate1."restaurantId") as whoCares)))
		AND R8."userId" = U."userId" AND R8."restaurantId" = R."restaurantId" AND
			R."restaurantId" IN (SELECT R2."restaurantId" FROM   restaurant R2 GROUP BY R2."restaurantId" HAVING
			(SELECT max(stddev) FROM(SELECT stddev(Rate2.mood  + Rate2.staff  + Rate2.price  +Rate2.food ) as stddev 
				FROM  Rating Rate2 WHERE Rate2."restaurantId" = R2."restaurantId" GROUP BY Rate2."restaurantId", Rate2."userId") as whoCares)
			>= ALL((SELECT max(stddev) FROM (SELECT stddev(Rate3.mood  + Rate3.staff  + Rate3.price  +Rate3.food ) FROM  Rating Rate3 GROUP BY Rate3."userId", Rate3."restaurantId") as whoCares)))



