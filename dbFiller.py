# Written by Filip Slatinac to populate DB tables with some data from
# zomato and some dummy rating data
import urllib3
from requests import HTTPError
import json
import random
import datetime
from models import Rater, Restaurant, Location, Rating, MenuItem, RatingItem
import time

def populateRestaurantTable(db):
    start = 0
    while start < 100:
        url = "https://developers.zomato.com/api/v2.1/search?start="+str(start)+"&lat=40.748&lon=-73.985"
        start += 20
        jsonResponse = {}
        try:
            request = urllib3.PoolManager().request('GET', url,
                                                    headers={"user-key": "21524a1242003830e7d41d90a2918c3e"})
            jsonResponse = json.loads(request.data.decode('UTF-8'))
        except HTTPError:
            print("Error")

        restaurants = jsonResponse['restaurants']

        for restaurantObject in restaurants:
            restaurant = restaurantObject['restaurant']
            name = restaurant['name']
            pic_url = restaurant['featured_image']
            if not pic_url:
                pic_url = ""
            url = restaurant['url']
            rating = restaurant['user_rating']
            overallRating = rating['aggregate_rating']
            overallRating = float(overallRating)
            print(name)

            restaurantObject = Restaurant.query.filter_by(name=name).first()

            cuisines = restaurant['cuisines'].strip().split(',')

            if not restaurantObject:
                new_restaurant = Restaurant(name=name, type=cuisines[0], url=url, overallrating=overallRating,
                                            pic_url=pic_url)
                restaurantObject = new_restaurant
                db.session.add(restaurantObject)
                db.session.commit()
                db.session.refresh(restaurantObject)
            locationObject = Location.query.filter_by(restaurantId=restaurantObject.restaurantId,
                                                      street_address=restaurant['location']['address']).first()

            if not locationObject:
                firstName = ['Joe', 'Bob', 'Jason', 'Paul', 'John', 'Steve', 'Bill', 'Carl', 'Chase', 'Derek', 'Dennis',
                             'Matthew',
                             'Jacob', 'Raymond', 'Bond', 'Rami', 'Bibo', 'Filip', 'Zarif', 'Pasoon', 'Praiyon',
                             'Anthony']
                lastName = ['Matthews', 'Johnson', 'Smith', 'Jacobson', 'Mac', 'Taleb', 'Cen', 'Adi', 'Azimi',
                            'Slatinac', 'Yan', 'Nader']
                num1 = random.randint(0, len(firstName) - 1)
                num2 = random.randint(0, len(lastName) - 1)
                num3 = random.randint(100, 999)
                num4 = random.randint(1000, 9999)

                address = restaurant['location']['address']
                managerName = firstName[num1] + " " + lastName[num2]
                phoneNumber = "613 " + str(num3) + " " + str(num4)
                openTime = "09:00:00"
                closeTime = "24:00:00"

                new_location = Location(restaurantId=restaurantObject.restaurantId, street_address=address,
                                        phone_number=phoneNumber, manager_name=managerName, open=openTime,
                                        close=closeTime)
                db.session.add(new_location)
                db.session.commit()
        time.sleep(5)


def populateMenuTable(db):
    menus = [
        {'name': 'chicken burger', 'description': 'chicken burger served with fries', 'category': 'main'},
        {'name': 'beef burger', 'description': 'beef burger served with fries', 'category': 'main'},
        {'name': 'mac and cheese', 'description': 'mac and cheese served with cheese bread', 'category': 'main'},
        {'name': 'lobster', 'description': 'lobster served with rice or brocolie', 'category': 'main'},
        {'name': 'crab', 'description': 'crab served with rice or brocolie', 'category': 'main'},
        {'name': 'oysters', 'description': 'oyster served with rice or brocolie', 'category': 'main'},
        {'name': 'lamb', 'description': 'lamb served with rice or brocolie', 'category': 'main'},
        {'name': 'chicken shawarma', 'description': 'chicken shawarma served with patatos', 'category': 'main'},
        {'name': 'beef shawarma', 'description': 'beef shawarma served with patatos', 'category': 'main'},
        {'name': 'ravioli', 'description': 'ravioli served with bread', 'category': 'main'},
        {'name': 'donuts', 'description': 'delicious donuts served with chocolate milk', 'category': 'dessert'},
        {'name': 'cream cookies', 'description': 'delicious cookies served with chocolate milk', 'category': 'dessert'},
        {'name': 'roast beef sandwich', 'description': 'delicious roast beef sandwich with fries or rice',
         'category': 'dessert'},
        {'name': 'club sandwich', 'description': 'club sandwich served fries', 'category': 'main'},
        {'name': 'chicken sandwich', 'description': 'chicken sandwich served fries', 'category': 'main'},
        {'name': 'chicken panini', 'description': 'chicken panini served fries', 'category': 'main'},
        {'name': 'beef panini', 'description': 'beef panini served fries', 'category': 'main'},
        {'name': 'mushroom soup', 'description': 'mushroom soup served with bread and crackers', 'category': 'starter'},
        {'name': 'chicken soup', 'description': 'chicken soup served with bread and crackers', 'category': 'starter'},
        {'name': 'lamb soup', 'description': 'lamb soup served with bread and crackers', 'category': 'starter'},
        {'name': 'tomato soup', 'description': 'tomato soup served with bread and crackers', 'category': 'starter'},
        {'name': 'ceasar soup', 'description': 'delicious salad served with a glass of flavoured water',
         'category': 'starter'},
        {'name': 'garden salad', 'description': 'delicious salad served with a glass of flavoured water',
         'category': 'starter'},
        {'name': 'chicken nuggets', 'description': 'chicken nuggets served with fries', 'category': 'main'},
        {'name': 'chicken tenders', 'description': 'chicken tenders served with fries', 'category': 'main'},
        {'name': 'grilled cheese', 'description': 'grilled cheese served with fries', 'category': 'main'},
        {'name': 'peperoni pizza', 'description': 'delicious pizza served with your choice of pop', 'category': 'main'},
        {'name': 'greek pizza', 'description': 'delicious pizza served with your choice of pop', 'category': 'main'},
        {'name': 'vegeterian pizza', 'description': 'delicious pizza served with your choice of pop',
         'category': 'main'},
        {'name': 'cheese pizza', 'description': 'delicious pizza served with your choice of pop', 'category': 'main'},
        {'name': 'bmt bagel', 'description': 'delicious bagel served with chips', 'category': 'main'},
        {'name': 'cream cheese bagel', 'description': 'delicious bagel served with chips', 'category': 'main'},
        {'name': 'steak', 'description': 'good cut steak served with mashed patatos', 'category': 'main'},
        {'name': 'tuna', 'description': 'best tuna in town', 'category': 'main'},
        {'name': 'filet mignon', 'description': 'best filet mignon served with a glass of wine or water',
         'category': 'main'},
        {'name': 'milkshake', 'description': 'banana, chocolate, vanila or cookies and cream', 'category': 'dessert'},
        {'name': 'rice and chicken', 'description': 'very basic meal for the ones in a hurry', 'category': 'main'},
        {'name': 'chicken noodles', 'description': 'chicken noodles served in a large bowl', 'category': 'main'},
        {'name': 'beef noodles', 'description': 'beef noodles served in a large bowl', 'category': 'main'}
    ]

    itemTypes = ['Swedish', 'Indian', 'Greek', 'Chinese', 'Japanese', 'American', 'Mexican', 'Spanish', 'Canadian',
                 'Lebanese', 'Egyptian', 'Tanzanian', 'Pakistani', 'Afghani', 'Bengali', 'Iraqi', 'French',
                 'Austrailian']

    for i in range(len(menus)):
        menus[i]['price'] = random.randint(5, 40)
        num = random.randint(0, len(itemTypes) - 1)
        menus[i]['type'] = itemTypes[num]

    restaurants = Restaurant.query.all()

    for restaurant in restaurants:
        print(restaurant.restaurantId)
        restaurantId = restaurant.restaurantId

        randomAmount = random.randint(3, len(menus))
        randomItems = []

        for i in range(randomAmount):
            index = random.randint(0, len(menus) - 1)
            randomItems.append(menus[index])

        for item in randomItems:
            menuItem = MenuItem.query.filter_by(restaurantId=restaurantId, name=item['name']).first()
            if not menuItem:
                menuItemObject = MenuItem(name=item['name'], price=item['price'], restaurantId=restaurantId,
                                          description=item['description'], foodtype=item['type'],
                                          category=item['category'])
                db.session.add(menuItemObject)
                db.session.commit()


def populateRaterTable(db):
    firstName = ['John', 'Bob', 'Chase', 'Derek', 'Dennis', 'Matthew', 'Jacob', 'Raymond', 'Bond', 'Rami', 'Bibo',
                 'Filip', 'Zarif', 'Pasoon', 'Praiyon', 'Anthony']
    num = 100
    rater_type = ['blog', 'online', 'food critic']
    joinDate = str(datetime.date.today())[:10]

    usernames = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    emails = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    raters = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    for i in range(0, 15):
        usernames[i] = firstName[i] + str(num)
        num += 1
        emails[i] = usernames[i] + '@gmail.com'
        raters[i] = Rater(userId=usernames[i], email=emails[i], name=firstName[i], join_date=joinDate,
                          reputation=random.randint(1, 5), raterType=rater_type[random.randint(0, 2)])
        db.session.add(raters[i])
        db.session.commit()


def populateRatingTable(db):
    restaurants = Restaurant.query.all()
    users = Rater.query.all()
    comments = [
        'This restaurant was absolutely great, the food, staff, mood and price were fantastic',
        'The restaurant had great food and mood, but not so much of a staff and the prices were a bit too high',
        'This restaurant had great food but the mood and staff were not as good as we thought it would be, it does not help that the prices were quite high',
        'This restaurant was okay, the food was decent',
        'This restaurant was not good at all'
    ]

    prices = [
        5,
        4,
        3,
        2,
        1
    ]

    moods = [
        5,
        4,
        3,
        2,
        1
    ]

    staffs = [
        5,
        4,
        3,
        2,
        1
    ]

    foods = [
        5,
        4,
        3,
        2,
        1
    ]

    for restaurant in restaurants:
        restaurantId = restaurant.restaurantId
        user = users[random.randint(0, len(users) - 1)]
        userId = user.userId

        commentLevel = random.randint(0, 4)
        comment = comments[commentLevel]
        price = prices[commentLevel]
        mood = moods[commentLevel]
        staff = staffs[commentLevel]
        food = foods[commentLevel]
        date = str(datetime.date.today())[:10]

        RatingObject = Rating(comment=comment, priceRating=price, restaurantId=restaurantId, userId=userId,
                              moodRating=mood,
                              staffRating=staff, foodRating=food, postDate=date)
        db.session.add(RatingObject)
        db.session.commit()


def populateMenuItemRatingTable(db):
    users = Rater.query.all()
    items = MenuItem.query.all()
    comments = ['I enjoyed this item very much! Will recommend to all my friends!',
                'The item was pretty good. I would come again.',
                'The item was okay. Might try again sometime.',
                'The item was not very good. Will avoid next time.',
                'The item was absolutely garbage. Will never come here again!']

    for item in items:
        itemID = item.itemId
        randUser = users[random.randint(0, len(users) - 1)]
        user = randUser.userId
        num = random.randint(0, 4)
        comment = comments[num]
        date = str(datetime.date.today())[:10]
        ratingNum = num + 1
        ItemRatingObject = RatingItem(userId=user, itemId=itemID, postDate=date, rating=ratingNum, comment=comment)
        db.session.add(ItemRatingObject)
        db.session.commit()
