from parameter import *
class Packet:
    def __init__(self, _start_time, _size, _dest_id, _route, _priority, _id, _app_id = 0) -> None:
        self.enable_cb = param.enable_cb
        self.cb_id = 0
        self.start_time = _start_time
        self.size = _size
        self.destination_id = _dest_id
        self.route = _route
        self.timestamp = [_start_time]
        self.priority = _priority
        self.hop = 0
        self.next_destination = -1
        self.id = _id
        self.app_id = _app_id
        # self.next_hop_id = -1
        if param.verbose:
            print(f"packet route: {self.route}")
    def get_next_route(self):
        if self.enable_cb and type(self.route[0]) == list :
            hop_list = [None if self.hop + 1 >= len(self.route[i]) else self.route[i][self.hop + 1] for i in range(len(self.route))]
            return hop_list

        assert type(self.route[0] == int)
        return [self.route[self.hop + 1]]
    def cb_len(self):
        if self.enable_cb:
            return len(self.get_next_route())
        return 1
    def incr_cb_id(self):
        if self.enable_cb:
            self.cb_id += 1

    def next_hop(self):
        # print(self.get_next_route(), self.cb_id)
        return self.get_next_route()[self.cb_id]

    def qch_priority_change(self):
        if param.enable_qch:
            if self.priority == 7:
                self.priority = 6
            elif self.priority == 6:
                self.priority = 7