import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.properties import ObjectProperty
from RequestParams import RequestParams
from ProduceRequests import ProduceRequests
from upadateProgressThread import UpdateProgressThread
from updateProgress import UpdateProgress
import threading


class FormSystemGrid(Widget):
    ADD_TO_DB = 1
    REPLACE_DB = 2
    # DATA
    countries = ObjectProperty(None)
    administrators = ObjectProperty(None)
    airlines = ObjectProperty(None)
    customers = ObjectProperty(None)
    flights = ObjectProperty(None)
    tickets = ObjectProperty(None)
    # STATUS LINE
    status_lbl = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.produce_requests = None

    def submit_add(self):
        try:
            self.generate_data(int(self.ADD_TO_DB))
        except Exception as exc:
            FormSystemGrid.show_popup(str(exc))

    def submit_replace(self):
        try:
            self.generate_data(int(self.REPLACE_DB))
        except Exception as exc:
            FormSystemGrid.show_popup(str(exc))

    def reset_loggings(self):
        self.ids.lbl_log_countries.text = '- 0 countries created'
        self.ids.lbl_log_administrators.text = '- 0 administrators created'
        self.ids.lbl_log_airlines.text = '- 0 airline companies created'
        self.ids.lbl_log_customers.text = '- 0 customers created'
        self.ids.lbl_log_fligths.text = '- creating flights (0/ 0)'
        self.ids.lbl_log_tickets.text = '- creating tickets (0/ 0)'

    def generate_data(self, db_generation_option):
        try:
            countries = self.countries.text
            administrators = self.administrators.text
            airlines = self.airlines.text
            customers = self.customers.text
            flights = self.flights.text
            tickets = self.tickets.text

            params = RequestParams(countries, administrators, airlines,
                               customers, flights, tickets,  db_generation_option)

            progress_bar = self.ids.pbar_main
            progress_bar.opacity = 1
            status_lbl = self.status_lbl
            status_lbl.opacity = 1
            self.ids.lbl_logging.opacity = 1
            self.ids.grd_logging.opacity = 1
            self.reset_loggings()

            logging_lines = {
                'country': self.ids.lbl_log_countries,
                'admin': self.ids.lbl_log_administrators,
                'airline': self.ids.lbl_log_airlines,
                'customer': self.ids.lbl_log_customers,
                'flight': self.ids.lbl_log_fligths,
                'ticket': self.ids.lbl_log_tickets,
            }

            upd_progress = UpdateProgress(progress_bar, status_lbl, logging_lines)
            upd_progress_thread = UpdateProgressThread(upd_progress, params)
            thread_progress = threading.Thread(target=upd_progress_thread.run)
            thread_progress.start()
            self.produce_requests = ProduceRequests(params)
            worker_thread = threading.Thread(target=self.produce_requests.produce_engine)
            worker_thread.start()
        except Exception as exp:
            raise exp

    @staticmethod
    def show_popup(message):
        popup = Popup(title='Message',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 400))
        popup.open()


class FlightSystemFormApp(App):
    form_system_grid = None

    def build(self):
        self.form_system_grid = FormSystemGrid()
        return self.form_system_grid

    def stop_app(self):
        if self.form_system_grid.produce_requests is not None:
            self.form_system_grid.produce_requests.close_connection()


if __name__ == '__main__':
    flight_system_form = FlightSystemFormApp()
    flight_system_form.run()
    flight_system_form.stop_app()
