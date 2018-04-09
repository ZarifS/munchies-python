queries = {
    'e':
    '''
    SELECT R.type, MI.category, AVG(MI.price) AS average_price FROM Menu_Item MI, Restaurant R 
        WHERE
            MI."restaurantId" IN 
            (SELECT R1."restaurantId" FROM Restaurant R1 WHERE
                R1.type = R.type)
            AND MI."restaurantId" = R."restaurantId"
        GROUP BY R.type, MI.category ORDER BY R.type, MI.category
    ''',

    'f':
    '''SELECT U."userId", R.name, AVG((R8.food+R8.mood+R8.staff+R8.price)/4) AS average , COUNT(R8)
        FROM Rating R8, Restaurant R, Rater U WHERE
        R8."restaurantId" = R."restaurantId" AND R8."userId" = U."userId"
         GROUP BY R.name, U."userId" ORDER BY R.name , average ''',

    'g':
    '''Select R.name, R.type, L.phone_number FROM  Restaurant R,  Location L WHERE 
        NOT EXISTS(SELECT * FROM  Rating R8 WHERE
            date_part('year',R8."postDate") = 2015 AND date_part('month',R8."postDate") = 01
            AND R8."restaurantId" = R."restaurantId")
        AND R."restaurantId" = L."restaurantId" ORDER BY R.name''',

    'h':
    '''SELECT R.name, L.manager_name FROM Restaurant R, Location L WHERE
        R."restaurantId" IN (SELECT R8."restaurantId" FROM Rating R8 WHERE
            R8.staff < ANY(SELECT Rate.staff FROM Rating Rate WHERE
                Rate."userId" = 'Bibo110'))
        AND R."restaurantId" = L."restaurantId"''',

    'i':
    '''SELECT restaurant.name, U.name FROM restaurant, rater U WHERE
        restaurant."restaurantId" IN (SELECT R8."restaurantId" FROM rating R8 WHERE
            R8."restaurantId" IN (SELECT R1."restaurantId" FROM restaurant R1 WHERE
                    R1.type = 'American')
            AND
            R8.food >= All(SELECT Rate.food FROM rating Rate WHERE
                Rate."restaurantId" IN (SELECT R2."restaurantId" FROM restaurant R2 WHERE
                    R2.type = 'American'))
            AND
            R8."userId" = U."userId")''',

    'j':
    '''SELECT ROW_NUMBER() OVER(ORDER BY OverallRating DESC) AS Ranking, OverallRating, Type
        FROM
            (SELECT AVG("overallRating") AS OverallRating, R.type AS Type FROM
                 Restaurant R GROUP BY R.type) AS WhoCares
        WHERE Type = 'Chinese' ''',

    'k':
    '''
    SELECT U.name, U.join_date, U.reputation, R.name, R8."postDate" FROM  Rater U,  Restaurant R,  Rating R8 WHERE 
        U."userId" IN (SELECT U1."userId" FROM  Rater U1 group by U1."userId" HAVING
            (SELECT AVG(Rate.mood  + Rate.food ) FROM  Rating Rate WHERE
                Rate."userId" = U1."userId")
            >= ALL(SELECT AVG(Rate1.mood  + Rate1.food ) FROM  Rating Rate1,  Rater U2 WHERE
                Rate1."userId" = U2."userId" GROUP BY U2."userId"))
        AND R8."userId" = U."userId" AND R8."restaurantId" = R."restaurantId"''',


    'l':
    '''SELECT U.name, U.join_date, U.reputation, R.name, R8."postDate" FROM  Rater U,  Restaurant R,  Rating R8 WHERE
        U."userId" IN (SELECT U1."userId" FROM  Rater U1 WHERE
            (SELECT AVG(mood ) FROM  Rating Rate WHERE Rate."userId" = U1."userId")
                >= ALL(SELECT AVG(mood ) FROM  Rating Rate GROUP BY Rate."userId")
            OR (SELECT AVG(food ) FROM  Rating Rate WHERE Rate."userId" = U1."userId")
                >= ALL(SELECT AVG(food ) FROM  Rating Rate GROUP BY Rate."userId"))
            AND R8."userId" = U."userId" AND R8."restaurantId" = R."restaurantId"''',

    'm':
    '''SELECT U.name, U.reputation, R8.comment FROM  Rating R8,  Rater U WHERE 
        U."userId" IN (SELECT U1."userId" FROM  Rater U1 WHERE
            (SELECT COUNT(*) FROM  Rating Rate WHERE Rate."userId" = U1."userId" AND
                Rate."restaurantId" IN (SELECT R."restaurantId" FROM  Restaurant R WHERE
                    R.name ='Pai'))
            >=  All(SELECT COUNT(*) FROM  Rating Rate1 WHERE 
                Rate1."restaurantId" IN (SELECT R."restaurantId" FROM  Restaurant R WHERE
                    R.name ='Pai') GROUP BY Rate1."userId"))
        AND R8."userId" = U."userId" AND R8."restaurantId" IN (SELECT R."restaurantId" FROM  Restaurant R WHERE
                    R.name ='Pai') ''',

    'n':
    '''SELECT U.name, U.email FROM Rater U WHERE
        U."userId" IN (SELECT R8."userId" FROM Rating R8 WHERE
            (R8.price  + R8.food  + R8.mood  + R8.staff )
            < ANY(SELECT (Rate.price  + Rate.mood  + Rate.food  + Rate.staff ) FROM Rating Rate WHERE
                Rate."userId" IN (SELECT U1."userId" FROM Rater U1 WHERE
                    U1.name = 'John')))''',


    'o':
        '''
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
        '''

}
