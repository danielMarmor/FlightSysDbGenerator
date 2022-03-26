import pika
import json
from RequestParams import RequestParams
from dataAccess.fetchApi import FetchApi


class ProduceRequests:
    QUEUE_NAME = 'FlightSystemData'
    DATA_BUFFER = 100

    def __init__(self, request_params: RequestParams):
        self.request_params = request_params
        self.connection = None
        self.channel = None
        self.init_connection()

    def init_connection(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.QUEUE_NAME)

    def close_connection(self):
        self.channel.queue_delete(self.QUEUE_NAME)
        self.connection.close()

    def produce_engine(self):
        try:
            # COUNTRIES
            countries_api = 'https://api.first.org/data/v1/countries'
            countries_names = FetchApi.get_countries(countries_api)

            # AIRLINES NAMES
            airline_companies_api = 'https://random-data-api.com/api/company/random_company'
            airline_companies_names = FetchApi.get_airline_companies(airline_companies_api, self.request_params.num_airlines)

            # ADMINISTRATORS
            admin_users_api = 'https://random-data-api.com/api/users/random_user'
            admin_users = FetchApi.get_users(admin_users_api, self.request_params.num_adminitrators)

            # AIRLINES
            airlines_users_api = 'https://random-data-api.com/api/users/random_user'
            airlines_users = FetchApi.get_users(airlines_users_api, self.request_params.num_airlines)

            # CUSTOMERS
            customers_users_api = 'https://random-data-api.com/api/users/random_user'
            # START
            start_request = json.dumps({'type': 'START', 'payload':
                {'db_generation_option':  self.request_params.db_generation_option}})
            self.channel.basic_publish(exchange='', routing_key=self.QUEUE_NAME, body=start_request)

            # PRODUCE COUNTRIES
            for country in countries_names:
                country_request = json.dumps({'type': 'country', 'payload': country})
                self.channel.basic_publish(exchange='', routing_key=self.QUEUE_NAME, body=country_request)

            # PRODUCE AIRLINES NAMES BANK
            for airline_name in airline_companies_names:
                airline_name_request = json.dumps({'type': 'airline_name', 'payload': airline_name})
                self.channel.basic_publish(exchange='', routing_key=self.QUEUE_NAME, body=airline_name_request)

            # PRODUCE ADMINISTRATORS
            for admin in admin_users:
                admin_request = json.dumps({'type': 'admin', 'payload': admin})
                self.channel.basic_publish(exchange='', routing_key=self.QUEUE_NAME, body=admin_request)

            # PRODUCE AIRLINES
            for airline in airlines_users:
                airline['flights_per_airline'] = self.request_params.num_flights_per_airline
                airline_request = json.dumps({'type': 'airline', 'payload': airline})
                self.channel.basic_publish(exchange='', routing_key=self.QUEUE_NAME, body=airline_request)

            # # BEFORE_CUSTOMERS
            # before_cust_request = json.dumps({'type': 'BEFORE_CUST', 'payload': {}})
            # self.channel.basic_publish(exchange='', routing_key=self.QUEUE_NAME, body=before_cust_request)

            # CUSTOMERS
            trips_to_source = (self.request_params.num_customers // self.DATA_BUFFER) + 1
            for i in range(1, trips_to_source + 1):
                is_partial_amount = (i * self.DATA_BUFFER) > self.request_params.num_customers
                data_size = (self.request_params.num_customers % self.DATA_BUFFER) if is_partial_amount else self.DATA_BUFFER
                customer_users = FetchApi.get_users(customers_users_api, data_size)
                for cust in customer_users:
                    cust['tickets_per_customer'] = self.request_params.num_tickets_per_customer
                    customer_request = json.dumps({'type': 'customer', 'payload': cust})
                    self.channel.basic_publish(exchange='', routing_key=self.QUEUE_NAME, body=customer_request)

            # COMPLETED
            completed_request = json.dumps({'type': 'COMPLETED', 'payload': {}})
            self.channel.basic_publish(exchange='', routing_key=self.QUEUE_NAME, body=completed_request)
        except KeyboardInterrupt:
            self.close_connection()
        except Exception as exp:
            self.close_connection()
            raise exp



