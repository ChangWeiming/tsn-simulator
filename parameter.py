class Parameter:
    def __init__(self) -> None:
        self.link_speed = 100 #Mbps
        self.process_delay = 0.001 #ms
        self.cycle_time = 8
        self.now_time = 0.0
        self.eps = 1e-8
        self.priority_num = 8
        self.time_unit = 0.5 # ms, same as the env settings
        self.time_unit_int = 5
        self.guard_band_unit = 1 / (self.time_unit_int * 6)
        self.gate_loop = self.cycle_time * self.time_unit_int # 64 time unit for a cycle, LCM of the TT traffic is 8ms, so the time unit should be 8ms(LCM) / time_unit(1/8ms) = 64
        self.stop_time = 32 # ms
        self.k = 3
        self.switch_buffer_size = 128000000
        self.enable_qbv = True
        self.enable_qch = False
        self.enable_cb = True
        # self.verbose = True
        self.verbose = False


    def from_config():
        pass

param = Parameter()