from queue import Queue
from parameter import param
from packet import *
from statistics_pkt import *
import copy

class Switch:
    def __init__(self, _id = 0,_link = [], _gate = [],  _forward_table = []) -> None:
        self.id = _id
        self.forward_table = _forward_table
        self.packet_queue = [Queue() for _ in range(param.priority_num)]
        self.link = _link 
        self.gate = _gate 
        self.process_packets = Queue()
        self.unique_pkt_map = set()

    def set_forward_table(self, _forward_table, _link):
        self.forward_table = _forward_table
        self.packet_queue = [Queue() for _ in range(param.priority_num)]
        self.link = _link 
    
    def set_gate(self, gate):
        if len(gate) != param.priority_num or len(gate[0]) != param.gate_loop:
            raise ValueError("gate length not consistent with param")
        self.gate = gate

    def get_next_event_time(self, links) -> float:
        event_time = 1e10
        #process delay
        if not self.process_packets.empty():
            pkt = self.process_packets.queue[0]
            event_time = min(event_time, pkt.timestamp[-1] + param.process_delay)
        
        #queue delay
        for j in range(param.priority_num): 
            if not self.packet_queue[j].empty():
                port = self.get_port_id(self.packet_queue[j].queue[0].next_hop())
                transmit_start_time = max(links[self.link[port]].get_next_available_time(), self.time_to_open(j))
                event_time = min(event_time, transmit_start_time)
        return event_time

    def get_port_id(self, device_id):
        for i in range(len(self.forward_table)):
            if self.forward_table[i] == device_id:
                return i
        if param.verbose:
            print(f"next hop id:{device_id} forward_table:{self.forward_table}, now id:{self.id}")
        raise RuntimeError("error routing")
        
        
    def time_to_open(self, priority) -> float:
        '''
        accept the priority of the queue and returns when the priority opens
        '''
        now_gate_id = int(param.now_time / param.time_unit) % param.gate_loop
        guard_band_id = int((param.now_time + param.guard_band_unit) / param.time_unit) % param.gate_loop

        # not in the guard band time
        if self.gate[priority][now_gate_id] == 1 and now_gate_id == guard_band_id:
            return param.now_time

        for i in range(1, param.gate_loop):
            if self.gate[priority][(now_gate_id + i) % param.gate_loop] == 1:
                return int((param.now_time + i  * param.time_unit) / param.time_unit) * param.time_unit + param.eps
        raise ProcessLookupError # no gate open

    def is_gate_open_now(self, priority) -> bool:
        now_gate_id = int(param.now_time / param.time_unit) % param.gate_loop
        guard_band_id = int((param.now_time + param.guard_band_unit) / param.time_unit) % param.gate_loop
        if param.verbose:
            print(f'switch_id: {self.id}, now_gate_id: {now_gate_id}, guard_band_id: {guard_band_id}')
        if now_gate_id != guard_band_id:
            return False
        return self.gate[priority][now_gate_id] == 1
    
    def do(self, links):
        #process delay
        if not self.process_packets.empty():
            pkt = self.process_packets.queue[0]
            if param.now_time  <= pkt.timestamp[-1] + param.process_delay + param.eps: #eliminate double possile error, maybe
                self.process_packets.get()
                self.packet_queue[pkt.priority].put(pkt)

        #queue delay
        for j in range(param.priority_num - 1, -1, -1): 
            while not self.packet_queue[j].empty():
                p = self.get_port_id(self.packet_queue[j].queue[0].next_hop())
                if param.verbose:
                    print(f'In switch {self.id}, transmitting packet at port {p}, is available:{links[self.link[p]].is_available()} and gate status:{self.is_gate_open_now(j)}, time_to_open {self.time_to_open(j)}')
                if links[self.link[p]].is_available() and self.is_gate_open_now(j):
                    pkt = self.packet_queue[j].get()
                    links[self.link[p]].transmit_packet(pkt)
                else:
                    break

    def get_buffer_size(self):
        tot_size = 0
        for i in range(len(self.packet_queue)):
            tot_size += self.packet_queue[i].qsize()
        return tot_size + self.process_packets.qsize()

    def print_queue(self):
        print('now_time:', param.now_time)
        pkts = []
        for i in range(len(self.packet_queue)):
            print('queue i:', i,  end='->')
            for j in range(self.packet_queue[i].qsize()):
                print(self.packet_queue[i].queue[j].app_id, end=' ')
                pkts.append(self.packet_queue[i].queue[j])
            print('')
        
        print('process_packets:', end=' ')
        for i in range(self.process_packets.qsize()):
            print(self.process_packets.queue[i].app_id, end = ' ')
        print('')
        
        for i in range(len(pkts)):
            print(pkts[i].app_id, pkts[i].route)

    def receive_packet(self, pkt:Packet):
        if self.get_buffer_size() <= param.switch_buffer_size:

            # if param.enable_cb:
            #     if (pkt.id, pkt.app_id) in self.unique_pkt_map:
            #         return
            #     self.unique_pkt_map.add((pkt.id, pkt.app_id))

            pkt.qch_priority_change()
            self.process_packets.put(pkt)
            pkt.timestamp.append(param.now_time)
            pkt.hop += 1
        else:

            if pkt.app_id == 286:
                print('pkt:', pkt.route, ' switch_id:', self.id, ' app_id:', pkt.app_id)
                print(pkt.timestamp)
                self.print_queue()

            g_stat.add_pkt_lost(pkt)