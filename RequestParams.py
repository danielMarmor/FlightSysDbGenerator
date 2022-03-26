class RequestParams:
    NUM_COUNTRIES = 100
    
    def __init__(self,
                 countries,
                 adminitrators,
                 airlines,
                 customers,
                 flights_per_airline,
                 tickets_per_customer,
                 db_generation_option
                 ):
        RequestParams.validate_params(countries,
                                      adminitrators,
                                      airlines,
                                      customers,
                                      flights_per_airline,
                                      tickets_per_customer)

        self.num_adminitrators = int(adminitrators)
        self.num_airlines = int(airlines)
        self.num_customers = int(customers)
        self.num_flights_per_airline = int(flights_per_airline)
        self.num_tickets_per_customer = int(tickets_per_customer)
        self.db_generation_option = db_generation_option

        # COUNTERS
        self.requested_counters = {
            'country': RequestParams.NUM_COUNTRIES,
            'admin': self.num_adminitrators,
            'airline': self.num_airlines,
            'customer': self.num_customers,
            'flight':  self.num_airlines * self.num_flights_per_airline,
            'ticket': self.num_customers * self.num_tickets_per_customer
        }
        self.completed_counters = {
            'country': 0,
            'admin': 0,
            'airline': 0,
            'customer': 0,
            'flight': 0,
            'ticket': 0
        }

        self.error_counters = {
            'country': 0,
            'admin': 0,
            'airline': 0,
            'customer': 0,
            'flight': 0,
            'ticket': 0
        }

    @staticmethod
    def validate_params(countries: str,
                        administrators: str,
                        airlines: str,
                        customers: str,
                        flights: str,
                        tickets: str):

        if not countries.isdigit():
            raise Exception('Countries must be valid numbers')
        if not administrators.isdigit():
            raise Exception('Administrators must be valid numbers')
        if not airlines.isdigit():
            raise Exception('Airline Companies must be valid numbers')
        if not customers.isdigit():
            raise Exception('Customers must be valid numbers')
        if not flights.isdigit():
            raise Exception('Flights must be valid numbers')
        if not tickets.isdigit():
            raise Exception('Tickets must be valid numbers')

    def get_requested_count(self):
        req_count = RequestParams.NUM_COUNTRIES + \
                    self.num_adminitrators + \
                    self.num_airlines +\
                    self.num_customers + \
                    (self.num_airlines * self.num_flights_per_airline) + \
                    (self.num_customers * self.num_tickets_per_customer)
        return req_count

