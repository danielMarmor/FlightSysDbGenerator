# import time
#
# from dataAccess.fetchApi import FetchApi
# from RequestParams import RequestParams
# from ProduceRequests import ProduceRequests
# from upadateProgressThread import UpdateProgressThread
# from updateProgress import UpdateProgress
# import threading
#
#
# def main():
#     params = RequestParams(
#         0,  # COUNTRIES
#         6,   # ADMINS
#         40,   # AIRLINES
#         400,  # CUSTOMERS
#         6,  # FILGHT PER AIRLINE
#         4,   # TICKETS PER CUST,
#         0  # DB GENERATION
#     )
#     upd_progress = UpdateProgress()
#     upd_progress_thread = UpdateProgressThread(upd_progress, params)
#     thread_progress = threading.Thread(target=upd_progress_thread.run)
#     thread_progress.start()
#     produce_requests = ProduceRequests(params)
#     produce_requests.produce_engine()
#
#
# if __name__ == '__main__':
#     main()
