import random
from packet import *
from parameter import *

class App:
    def __init__(self, interval_func, interval_args, src, dest, size, route, priority, start_time, deadline = 0, probs = 1.0, app_id = 0) -> None:
        self.interval_func = interval_func
        self.interval_args = interval_args
        self.dest = dest
        self.src = src
        self.size = size
        self.route = route
        self.priority = priority
        self.next_event_time= 0.0
        self.start_time = start_time
        self.app_id = app_id
        self.pkt_id = -1 #to make it zero index
        self.deadline = deadline
        self.probs = probs
    
    def get_interval_and_set_next_event_time(self) -> float:
        interval = self.interval_func(*self.interval_args)

        if param.verbose:
            print( f'probs: {self.probs} before interval:{interval}')
        while random.random() > self.probs:
            interval += self.interval_func(*self.interval_args)
        if param.verbose:
            print(f'probs: {self.probs} after interval:{interval}')

        self.next_event_time = param.now_time + interval
        if param.verbose:
            print(f"interval:{interval} next_event_time:{self.next_event_time}")
        return interval

    def prepare_packet(self) -> Packet:
        self.get_interval_and_set_next_event_time()
        self.pkt_id += 1
        return Packet(param.now_time, self.size, self.dest, self.route, self.priority, self.pkt_id, self.app_id)

    def get_next_event_time(self):
        return max(self.start_time, self.next_event_time)

    def can_send(self) -> bool:
        return param.now_time >= self.get_next_event_time()
