import json
import requests


class Base(object):
    def __init__(self):
        self.api_url = ''
        self.api_method = 'GET'
        self.headers = {}
        self.name = ''

    def get_request_data(self, **kwargs):
        pass

    def get_content(self):
        resp = requests.request(method=self.api_method,
                                url=self.api_url,
                                data=self.get_request_data(),
                                headers=self.headers,
                                )
        content = json.loads(resp.content.decode('utf-8'))
        return content

    def get_restaurants_list(self):
        raise NotImplementedError()

    def parse_restaurant_data(self, restaurant):
        raise NotImplementedError()

    def get_datas(self):
        data = []
        for restaurant in self.get_restaurants_list():
            address, latitude, longitude = self.parse_restaurant_data(restaurant)
            data.append((self.name, address, latitude, longitude))
        return data


class BurgerKing(Base):
    def __init__(self):
        super().__init__()
        self.api_url = 'https://burgerking.ru/middleware/bridge/cache/api/v1/restaurants'
        self.name = 'Burger King'

    def get_restaurants_list(self):
        return self.get_content()['response']

    def parse_restaurant_data(self, restaurant):
        address = restaurant.get('address', '') or restaurant.get('name')
        latitude = restaurant.get('latitude')
        longitude = restaurant.get('longitude')
        return address, float(latitude), float(longitude)


class McDonalds(Base):
    def __init__(self):
        super().__init__()
        self.api_url = 'https://mcdonalds.ru/api/restaurants'
        self.name = 'McDonald’s'

    def get_restaurants_list(self):
        return self.get_content()['restaurants']

    def parse_restaurant_data(self, restaurant):
        address = restaurant.get('location', {}).get('name', '')
        latitude = restaurant.get('latitude')
        longitude = restaurant.get('longitude')
        return address, float(latitude), float(longitude)


class KFC(Base):
    def __init__(self):
        super().__init__()
        self.api_url = 'https://api.kfc.com/api/store/v2/store.geo_search'
        self.api_method = 'POST'
        self.headers = {'Content-Type': 'application/json',
                        }
        self.name = 'KFC'

    def get_request_data(self):
        # KFC Добавляем параметры поиска, рандомные координаты и радиус поиска 100 тыс.км.
        # чтобы нашлось определенно ВСЕ
        return json.dumps({'coordinates': [68, 33],
                           'radiusMeters': 100000000,
                           'channel': "website",
                           })

    def get_restaurants_list(self):
        return self.get_content()['searchResults']

    def parse_restaurant_data(self, restaurant):
        store = restaurant.get('store', {})
        if not store:
            raise ValueError('No store data')
        city = store['contacts']['city']['ru']
        latitude, longitude = store['contacts']['coordinates']['geometry']['coordinates']
        return city, latitude, longitude


def get_all_datas():
    data = []
    classes = [KFC,
               BurgerKing,
               McDonalds,
               ]
    for c in classes:
        restaurant = c()
        data += restaurant.get_datas()
    return data
