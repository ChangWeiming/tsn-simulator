from app import *
from queue import Queue
import statistics_pkt
import copy

class Device:
    def __init__(self, _id, _forward_table = [], _link = []) -> None:
        self.app = []
        self.id = _id
        self.forward_table = _forward_table
        self.send_queue = Queue() 
        self.link = _link
        self.stat = dict()
        self.unique_pkt_map = set()

    def set_forward_table(self, forward_table, link):
        self.forward_table = forward_table
        self.link = link

    def add_app(self, a: App):
        self.app.append(a)
    def get_next_event_time(self, links):
        event_time = 1e10
        #app
        for a in self.app:
            event_time = min(a.get_next_event_time(), event_time)

        #link 
        if not self.send_queue.empty():
            port_id = self.get_port_id(self.send_queue.queue[0].next_hop())
            event_time = min(event_time, links[self.link[port_id]].get_next_available_time())
        
        return event_time

    def get_port_id(self, device_id):
        for i in range(len(self.forward_table)):
            if self.forward_table[i] == device_id:
                return i
        
        print(device_id, self.id, self.forward_table)
        raise RuntimeError("error routing")

    def do(self, links):
        for a in self.app:
            if a.can_send():
                pkt = a.prepare_packet()
                statistics_pkt.g_stat.add_pkt_cnt(pkt)
                self.send_queue.put(pkt)
                for i in range(1, pkt.cb_len()):
                    pkt = copy.deepcopy(pkt)
                    pkt.incr_cb_id()
                    self.send_queue.put(pkt)

        while not self.send_queue.empty():
            pkt = self.send_queue.queue[0]
            if param.verbose:
                print(f"next_hop: {pkt.next_hop()}, cb_id:{pkt.cb_id}")

            port_id = self.get_port_id(pkt.next_hop())
            if param.verbose:
                print(f"Device {self.id}: is sending with link:{self.link[port_id]}, link info: {links[self.link[port_id]].is_available()}")

            if links[self.link[port_id]].is_available():
                if param.verbose:
                    print(f"Device {self.id}: is sending with port_id:{port_id}")
                self.send_queue.get()
                links[self.link[port_id]].transmit_packet(pkt)
            else:
                break
        

    def receive_packet(self, pkt: Packet):
        pkt.timestamp.append(param.now_time)
        if pkt.destination_id != self.id:
            raise RuntimeError("wrong routing to destination")
        
        if param.enable_cb:
            if (pkt.id, pkt.app_id) in self.unique_pkt_map:
                return
            self.unique_pkt_map.add((pkt.id, pkt.app_id))

        statistics_pkt.g_stat.collect_pkt(pkt)
        if pkt.app_id in self.stat:
            self.stat[pkt.app_id].append(param.now_time - pkt.start_time)
        else:
            self.stat[pkt.app_id] = [param.now_time - pkt.start_time]
        # print(param.now_time - pkt.start_time, pkt.timestamp, pkt.app_id, (sum(self.stat[pkt.app_id]) / (pkt.id + 1)), pkt.route)
