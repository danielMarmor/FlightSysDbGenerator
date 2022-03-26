from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label


class UpdateProgress:
    def __init__(self, progress_bar: ProgressBar, status_label: Label, logging_lines: dict):
        self.progress_bar = progress_bar
        self.status_label = status_label
        self.progress_bar.value = 0
        self.status_label.text = ''
        self.logging_lines = logging_lines

    def update(self, complete_percent, current_message, state):
        self.progress_bar.value = complete_percent
        if state == 'LOAD':
            self.status_label.text = current_message
        else:
            self.status_label.text = f'{str(round(complete_percent * 100, 2))}% Completed'

    def completed(self):
        self.status_label.text = 'Completed Succesfuly!'

    def log_line(self, object_type, current_count, max_count):
        line = self.logging_lines[object_type]
        if object_type in ['flight', 'ticket']:
            line.text = f'- creating {object_type}s ({str(current_count)}/ {str(max_count)})'
        else:
            line.text = f'- {current_count} {object_type}s created'
