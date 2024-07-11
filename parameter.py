class Parameter:
    def __init__(self) -> None:
        self.link_speed = 100 #Mbps
        self.process_delay = 0.01 #ms
        self.now_time = 0.0
        self.eps = 1e-8
        self.priority_num = 8
        self.time_unit = 1 / 24 # ms, same as the env settings
        self.gate_loop = 8 * 24 # 64 time unit for a cycle, LCM of the TT traffic is 8ms, so the time unit should be 8ms(LCM) / time_unit(1/8ms) = 64
        self.stop_time = 32 # ms
        self.k = 3
        self.verbose = False

param = Parameter()