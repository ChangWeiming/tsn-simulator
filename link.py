from packet import *
from parameter import param

class Link:
    def __init__(self) -> None:
        self.next_available_time = 0
        self.pkt = None
    
    def get_next_available_time(self):
        if abs(self.next_available_time) < param.eps:
            return param.now_time
        return self.next_available_time
    
    def is_available(self):
        return self.pkt == None

    def transmit_packet(self, pkt:Packet):
        self.pkt = pkt
        self.next_available_time = param.now_time + pkt.size * 8 / (param.link_speed * 1024 * 1024) * 1000
    
    def get_next_event_time(self):
        if abs(self.next_available_time) < param.eps:
            return 1e10
        return self.next_available_time

    def do(self, devices):
        devices[self.pkt.get_next_route()].receive_packet(self.pkt)
        self.pkt = None
        self.next_available_time = 0