import random
import json
import os
import statistics_pkt
import config
from device import *
from switch import *
from parameter import *
from link import *
from app import *

current_directory = os.path.dirname(os.path.abspath(__file__))
def fixed_interval(a):
    return a

class Scenario:

    def __init__(self, conf: config.Config, gate = None, apps = []) -> None:
        configs = conf.get_config_map()

        self.configs = configs
        # load from config.json
        self.topo_map_path = 'data/topo.map' if len(configs['topo_map_path']) == 0 else configs['topo_map_path']
        self.app_path= 'data/app.json' if len(configs['app_path']) == 0 else configs['app_path']
        self.device_num = configs['device_num']
        self.switch_num = configs['switch_num']
        param.stop_time = conf.get_value_with_default("simulation_time_ms", 32) 
        param.link_speed = conf.get_value_with_default("bandwidth_mb", 100) 

        if configs["core_mode"]:
            self.n = self.switch_num * 2
        else:
            self.n = self.switch_num + self.device_num
        self.devices = []
        self.links = []
        self.graph = []
        self.apps = apps
        self.gate = gate

        for x in range(self.n):
            self.graph.append([-1] * self.n)

        if configs["core_mode"]:
            for i in range(self.switch_num):
                self.add_edge(i, i + self.switch_num)

    def add_edge(self, f, t):
        if self.graph[f][t] != -1:
            return
        self.links.append(Link())
        self.graph[f][t] = len(self.links) - 1
        self.links.append(Link())
        self.graph[t][f] = len(self.links) - 1


    def load_network(self, path):
        f = open(os.path.join(current_directory, path))
        for line in f.readlines():
            x, y = map(int, line.split(' '))
            self.add_edge(x, y)
        f.close()

    def load_apps(self, path):
        app_info = []
        ret_list = []
        if len(self.apps) == 0:
            f = open(os.path.join(current_directory, path))
            s = f.read()
            app_info = json.loads(s)
            f.close()
        else:
            app_info = self.apps

        
        for x in app_info:
            param = tuple()
            func = fixed_interval
            f = x['interval_func']
            if f == 'fixed':
                func = fixed_interval
                param = (x['interval'],)
            elif f == 'uniform':
                func = random.uniform
                param = (x['interval'] - x['interval_var'], x['interval'] + x['interval_var'])
            ret_list.append(App(interval_func=func, interval_args=param, 
                                src=x['src'], dest=x['dest'], size=x['size'], route=x['route'], priority=x['priority'], start_time=x['start_time'], 
                                deadline=x['deadline'] , probs=x['prob'], app_id=x['app_id']))

        return ret_list

    def prepare(self):
        param.gate_loop = 2
        param.guard_band_unit = 0
        param.now_time = 0.0
        param.enable_qbv = False
        param.enable_qch = True
        param.enable_cb = False

        for i in range(self.switch_num):
            self.devices.append(Switch(_id=i))
        for i in range(self.switch_num, self.n):
            self.devices.append(Device(_id=i))
        
        self.load_network(self.topo_map_path)
        
        # set forward table and corresponding links
        for i in range(self.n):
            forward_table = []
            links = []
            for to in range(self.n):
                if self.graph[i][to] != -1:
                    forward_table.append(to)
                    links.append(self.graph[i][to])
            self.devices[i].set_forward_table(forward_table, links)
        
        # set gate
        
        if self.gate == None:
            gate = []
            for i in range(param.priority_num):
                gate.append([])
                for j in range(param.gate_loop):
                    gate[i].append(1)
            
            if param.enable_qch:
                for i in range(param.gate_loop):
                    gate[7][i] = 1 - i
                    gate[6][i] = i
                #print(gate)
            for i in range(0, self.switch_num):
                self.devices[i].set_gate(gate)
        else:
            for i in range(0, self.switch_num):
                self.devices[i].set_gate(self.gate[i])

        # set app
        apps = self.load_apps(self.app_path)
        for a in apps:
            self.devices[a.src].add_app(a)
            g_stat.register_app(a)

    def main(self):
        statistics_pkt.g_stat.clear()
        self.prepare()

        callback_func = []
        callback_args = []
        while param.now_time < param.stop_time:
            event_time = 1e10

            verbose_log = []
            for i in range(len(self.links)):
                t_i = self.links[i].get_next_event_time()
                verbose_log.append((i, t_i,))

                if t_i < event_time:
                    callback_func = [self.links[i].do]
                    callback_args = [(self.devices, )]
                    event_time = t_i
                elif abs(t_i - event_time) < param.eps:
                    callback_func.append(self.links[i].do)
                    callback_args.append( (self.devices,) )

        
            if param.verbose:
                print(f"link next event time is (id, time):{verbose_log}")

            verbose_log = []
            for i in range(self.n):
                t_i = self.devices[i].get_next_event_time(self.links)

                if t_i < event_time:
                    callback_func = [self.devices[i].do]
                    callback_args = [(self.links,)]
                    event_time = t_i
                elif abs(t_i - event_time) < param.eps:
                    callback_func.append(self.devices[i].do)
                    callback_args.append((self.links,))
                verbose_log.append((i, t_i,))
            
            if param.verbose:
                print(f"device next event time is (id, time):{verbose_log}")
            
            param.now_time = event_time
            if param.now_time > param.stop_time:
                break

            if param.verbose:
                print(f"action time is:{param.now_time}, callback_func is:{callback_func}")

            for i in range(len(callback_func)):
                callback_func[i](*callback_args[i])
            callback_func = []
            callback_args = []
        # return [statistics_pkt.g_stat.app_latency_average(), statistics_pkt.g_stat.app_lost_rate()]
        return statistics_pkt.g_stat.get_stat()
