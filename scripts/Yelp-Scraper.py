# importing the requests library
import requests
import json
import functools

# api-endpoint
URL = "https://api.yelp.com/v3/businesses/search"

# location given here
location = "Manhattan"
radius = 40000
limit = 50
categories = ["japanese", "chinese", "indian", "african", "american"]

businesses_format = []

HEADERS = {
    'Authorization': 'Bearer UKZ_LEnLwGA-LzpGApvSRmhLT4raUykkdTPUUE4pGZRUnQZfpmmrp_y7eagg0w6L8f6UYUlh_kQuAbvzvZtYzqeBaasGybuw8XI8fB3B3Eszom4lSZoMTrlFvEWCX3Yx'
}


def scrape():
    for category in categories:
        i = 0
        while i < 1000:

            # defining a params dict for the parameters to be sent to the API
            PARAMS = {
                'location': location,
                'radius': radius,
                'categories': category+', All',
                'limit': limit,
                'offset': i
            }

            # sending get request and saving the response as response object
            r = requests.get(url=URL, params=PARAMS, headers=HEADERS)

            # extracting data in json format
            data = r.json()
            print(PARAMS)

            if 'businesses' in data:
                for business in data['businesses']:
                    id = business['id']
                    name = business['name']
                    address = business['location']['address1']
                    coordinates = business['coordinates']
                    # cuisine = functools.reduce(lambda y, x: x['title'] + ", " + y['title'], business['categories'])
                    cuisine = category
                    number_of_reviews = business['review_count']
                    rating = business['rating']
                    categories_restaurant = business['categories']
                    zip_code = business['location']['zip_code']
                    businesses_format.append({
                        'id': id,
                        'name': name,
                        'address': address,
                        'coordinates': coordinates,
                        'cuisine': cuisine,
                        'rating': rating,
                        'number_of_reviews': number_of_reviews,
                        'zip_code': zip_code,
                        'categories': categories_restaurant
                    })
               

            i += 50

        print("Length", len(businesses_format))

    with open('yelp-restaurants.json', 'w') as outfile:
        print('dumping')
        json.dump({'yelp-restaurants': businesses_format}, outfile)
