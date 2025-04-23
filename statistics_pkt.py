from packet import *
from app import *

class Statistics:
    def __init__(self) -> None:
        self.app_timestamp = {} #[app_id][pkt_id][route_id]
        self.lost_packet = {} # [app_id][tot_packet, drop_packet]
        self.apps = {} #[app_id] -> app
    
    def register_app(self, a:App):
        self.apps[a.app_id] = a

    def collect_pkt(self, pkt:Packet):
        if pkt.app_id not in self.app_timestamp:
            self.app_timestamp[pkt.app_id] = [pkt.timestamp]
        else:
            self.app_timestamp[pkt.app_id].append(pkt.timestamp)
    
    def add_pkt_cnt(self, pkt:Packet):
        if pkt.app_id not in self.app_timestamp:
            self.app_timestamp[pkt.app_id] = []

        if pkt.app_id not in self.lost_packet:
            self.lost_packet[pkt.app_id] = [1, 0]
        else:
            self.lost_packet[pkt.app_id][0] += 1
    def add_pkt_lost(self, pkt:Packet):
        self.lost_packet[pkt.app_id][1] += 1

    def clear(self):
        self.app_timestamp = {} #[app_id][pkt_id][route_id]
        self.lost_packet= {} #[app_id][pkt_id][route_id]
        self.apps = {} #[app_id] -> App

    def app_latency_average(self):
        avg_latency = {}
        for app in self.app_timestamp:
            s = 0
            for pkt in self.app_timestamp[app]:
                latency = pkt[-1] - pkt[0]
                s += latency
            # loss rate = 1
            if(len(self.app_timestamp[app]) == 0):
                avg_latency[app] = None
            else:
                avg_latency[app] = (s / len(self.app_timestamp[app])) 
        return avg_latency
    
    def app_lost_rate(self):
        loss_rate = {}
        for app in self.lost_packet:
            loss_rate[app] = self.lost_packet[app][1] / self.lost_packet[app][0]
        return loss_rate 
    def app_deadline_satisfication(self):
        #deadline satisfication & lost_rate
        ddl = {}
        for app in self.app_timestamp:
            s = 0
            for pkt in self.app_timestamp[app]:
                latency = pkt[-1] - pkt[0]
                if latency > self.apps[app].deadline:
                    s += 1
            
            # loss rate = 1
            if(len(self.app_timestamp[app]) == 0):
                ddl[app] = 0
            else:
                ddl[app] = (s / self.lost_packet[app][0]) 
        return ddl 
    def get_stat(self) -> dict:
        '''
        returns a dict including:
        'lost' -> lost packets / all packts 
        'ddl' -> ddl not satisfied / all packets
        'qoe' -> packet not reached / all packets
        'avg' -> average latency of all recieved packets
        '''

        ret = {}
        ret['lost'] = self.app_lost_rate()
        ret['ddl'] = self.app_deadline_satisfication()
        ret['qoe'] = {}
        for app in ret['lost']:
            ret['qoe'][app] = ret['lost'][app] + ret['ddl'][app]
        ret['avg'] = self.app_latency_average()
        return ret

    def get_random_packet_timestamp(self):
        for app in self.app_timestamp:
            for pkt in self.app_timestamp[app]:
                latency = pkt[-1] - pkt[0]
                if latency > 10:
                    print(app, pkt)
                    break

g_stat = Statistics()