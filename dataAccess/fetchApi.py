import requests


class FetchApi:
    @staticmethod
    def get_countries(countries_api):
        response = requests.get(countries_api)
        countries_json = response.json()
        countries_data = countries_json['data']
        countries_names = [value['country'] for (item, value) in countries_data.items()]
        return countries_names

    @staticmethod
    def get_airline_companies(airline_companies_api, requested_number):
        request_url = f'{airline_companies_api}?size={requested_number}'
        response = requests.get(request_url)
        airlines_data = response.json()
        airlines_names = [data['business_name'] for data in airlines_data]
        return airlines_names

    @staticmethod
    def get_users(users_api, requested_number):
        request_url = f'{users_api}?size={requested_number}'
        response = requests.get(request_url)
        users_data = response.json()
        users = [{
            'username': data['username'],
            'password': data['password'],
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'address': f'{data["address"]["city"]} {data["address"]["street_name"]} '
                       f'{data["address"]["street_address"]}',
            'phone_number': data['phone_number'],
            'credit_card_number': data['credit_card']['cc_number']
        } for data in users_data]
        return users








