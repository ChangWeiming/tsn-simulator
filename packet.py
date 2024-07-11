from parameter import *
class Packet:
    def __init__(self, _start_time, _size, _dest_id, _route, _priority, _id, _app_id = 0) -> None:
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
        if param.verbose:
            print(f"packet route: {self.route}")
    def get_next_route(self):
        return self.route[self.hop + 1]