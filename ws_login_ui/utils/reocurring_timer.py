import threading

class ReocurringTimer:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback;

    def start(self):
        self.cancel_event = threading.Event()
        def in_thread():
            self.callback()
            while not self.cancel_event.wait(self.interval):
                self.callback()
        self.thread = threading.Thread(target=in_thread, daemon=True)
        print("Refresh Thread Started")
        self.thread.start()

    def cancel(self):
        self.cancel_event.set()
        self.thread.join()
        print("Refresh Thread Canceled")
