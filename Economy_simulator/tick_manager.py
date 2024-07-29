import time
from society import Society

class TickManager:
    def __init__(self,society : Society) -> None:
        self.society = society
        self.stop = False

        self.start()

    def start(self):
        while not self.stop:
            time.sleep(1)
            print('time passes')