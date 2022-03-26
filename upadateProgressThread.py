import threading
from updateProgressConsumer import UpdateProgressConsumer


class UpdateProgressThread:
    DECIMAL_HOP = 0.001

    def __init__(self, update_progress, request_params):
        self.update_progress = update_progress
        self.request_params = request_params
        self.comsumer = UpdateProgressConsumer(self)
        self.requested_count = self.request_params.get_requested_count()
        self.complete_count = 0
        self.exceptions_count = 0
        self.exceptions = []
        self.next_decimal_value = 0

    def register_completed(self):
        percentage = 1
        message = 'Data Generation Completed!'
        self.update_progress.update(percentage, message, 'SEND')
        self.update_progress.completed()
        self.print_summation()
        self.print_exceptions()

    def register_ok(self, object_type):
        self.complete_count += 1
        self.request_params.completed_counters[object_type] += 1
        percentage = self.complete_count / self.requested_count
        counter_entry = self.request_params.completed_counters[object_type]
        reuqsted_entry = self.request_params.requested_counters[object_type]
        self.update_progress.update(percentage, None, 'SEND')
        self.update_progress.log_line(object_type, counter_entry, reuqsted_entry)

    def register_error(self, object_type, error_desc):
        self.exceptions_count += 1
        self.exceptions.append(f'Type: {object_type} -Reject Description: {error_desc}')
        self.complete_count += 1
        percentage = self.complete_count / self.requested_count
        message = f'{object_type}s error -{error_desc}'
        self.update_progress.update(percentage, message, 'SEND')

    def print_summation(self):
        for key, value in self.request_params.completed_counters.items():
            print(f'{value} {key}s created')
        print('********')

    def print_exceptions(self):
        for exc in self.exceptions:
            print(exc)
        print('********')

    def run(self) -> None:
        self.update_progress.update(0, 'Initializing...', 'LOAD')
        self.comsumer.consume_update_progress()

