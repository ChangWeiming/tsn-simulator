import random

tt_flows = 10
sporadic_flows = 5

def topo_flow_gen():
    # 100Mbps for 17 flows
    app_info = []
    app_id = 0
    for i in range(50): 
        # topo
        app = {
            'src': 4,
            'dest': 6,
            'size': random.randint(1,200),
            'interval_func': 'fixed',
            'interval': 1,
            'app_id': app_id,
            'deadline': 1,
            'prob': 1,
        }
        app_id += 1
        app_info.append(app)

        app = {
            'src': 5,
            'dest': 7,
            'size': random.randint(1,200),
            'interval_func': 'fixed',
            'interval': 1,
            'app_id': app_id,
            'deadline': 1,
            'prob': 1,
        }

        app_id += 1
        app_info.append(app)

    for i in range(100): 

        app = {
            'src': 4,
            'dest': 6,
            'size': random.randint(1,200),
            'interval_func': 'fixed',
            'interval': 1,
            'app_id': app_id,
            'deadline': 1,
            'prob': 0.5,
        }
        app_id += 1
        app_info.append(app)

        app = {
            'src': 5,
            'dest': 7,
            'size': random.randint(1,200),
            'interval_func': 'fixed',
            'interval': 1,
            'app_id': app_id,
            'deadline': 1,
            'prob': 0.5,
        }
        app_id += 1
        app_info.append(app)


    # load app from config file
    # f = open('data/original_app.json', 'w')
    # f.write(json.dumps(app_info))
    # f.close()
    return app_info
def A380_flow_gen(flow_num = 120):
    '''
    9 switches 0 - 8
    8 devices in A380 9 - 16
    '''
    tt_flows = flow_num // 3 * 2
    sporadic_flows = flow_num // 3
    assert tt_flows + sporadic_flows == flow_num

    intervals = [1,2,4,8]
    probs = [0.2, 0.35, 0.5, 0.65, 0.8]
    deadline = 3
    app_info = []
    app_id = 0
    for i in range(tt_flows): 
        # A380
        src = -1
        dest = -1
        while src == dest:
            src = random.randint(9, 12)
            dest = random.randint(13, 16)
        app = {
            'src': src,
            'dest': dest,
            'size': random.randint(1, 1500),
            'interval_func': 'fixed',
            'interval': intervals[random.randint(0, len(intervals) - 1)],
            'app_id': app_id,
            'deadline': deadline,
            'prob': 1,
        }
        app_id += 1
        app_info.append(app)

    for i in range(sporadic_flows): 
        # A380
        src = -1
        dest = -1
        while src == dest:
            src = random.randint(9, 12)
            dest = random.randint(13, 16)
        app = {
            'src': src,
            'dest': dest,
            'size': random.randint(1,1500),
            'interval_func': 'fixed',
            'interval': intervals[random.randint(0, len(intervals) - 1)],
            'app_id': app_id,
            'deadline': deadline,
            'prob': probs[random.randint(0, len(probs) - 1)],
        }
        app_id += 1
        app_info.append(app)
    # for i in range(3):
    #     # A380
    #     src = -1
    #     dest = -1
    #     while src == dest:
    #         src = random.randint(9, 12)
    #         dest = random.randint(13, 16)
    #     app = {
    #         'src': src,
    #         'dest': dest,
    #         'size': 0,
    #         'interval_func': 'fixed',
    #         'interval': 1000,
    #         'app_id': app_id,
    #         'deadline': deadline,
    #         'prob': 0,
    #     }
    #     app_id += 1
    #     app_info.append(app)
    return app_info


def ladder_flow_gen():
    '''
    9 switches 0 - 7
    8 devices in A380 8 - 15
    '''
    intervals = [1,2,4,8]
    probs = [0.2, 0.35, 0.5, 0.65, 0.8]
    deadline = 3
    app_info = []
    app_id = 0
    for i in range(tt_flows): 
        # A380
        src = -1
        dest = -1
        while src == dest:
            src = random.randint(8, 11)
            dest = random.randint(12, 15)
        app = {
            'src': src,
            'dest': dest,
            'size': random.randint(1, 1500),
            'interval_func': 'fixed',
            'interval': intervals[random.randint(0, len(intervals) - 1)],
            'app_id': app_id,
            'deadline': deadline,
            'prob': 1,
        }
        app_id += 1
        app_info.append(app)

    for i in range(sporadic_flows): 
        # A380
        src = -1
        dest = -1
        while src == dest:
            src = random.randint(8, 11)
            dest = random.randint(12, 15)
        app = {
            'src': src,
            'dest': dest,
            'size': random.randint(1,1500),
            'interval_func': 'fixed',
            'interval': intervals[random.randint(0, len(intervals) - 1)],
            'app_id': app_id,
            'deadline': deadline,
            'prob': probs[random.randint(0, len(probs) - 1)],
        }
        app_id += 1
        app_info.append(app)
    # for i in range(3):
    #     # A380
    #     src = -1
    #     dest = -1
    #     while src == dest:
    #         src = random.randint(8, 11)
    #         dest = random.randint(12, 15)
    #     app = {
    #         'src': src,
    #         'dest': dest,
    #         'size': 0,
    #         'interval_func': 'fixed',
    #         'interval': 1000,
    #         'app_id': app_id,
    #         'deadline': deadline,
    #         'prob': 0,
    #     }
    #     app_id += 1
    #     app_info.append(app)
    return app_info
def ERG_flow_gen(flow_num = 120):
    '''
    9 switches 0 - 7
    8 devices in A380 8 - 15
    '''
    tt_flows = flow_num // 3 * 2
    sporadic_flows = flow_num // 3
    assert tt_flows + sporadic_flows == flow_num
    tt_flows = 80
    sporadic_flows = 40
    intervals = [1,2,4,8]
    probs = [0.2, 0.35, 0.5, 0.65, 0.8]
    deadline = 3
    app_info = []
    app_id = 0
    for i in range(tt_flows): 
        # A380
        src = -1
        dest = -1
        while src == dest:
            src = random.randint(8, 11)
            dest = random.randint(12, 15)
        app = {
            'src': src,
            'dest': dest,
            'size': random.randint(1, 1500),
            'interval_func': 'fixed',
            'interval': intervals[random.randint(0, len(intervals) - 1)],
            'app_id': app_id,
            'deadline': deadline,
            'prob': 1,
        }
        app_id += 1
        app_info.append(app)

    for i in range(sporadic_flows): 
        # A380
        src = -1
        dest = -1
        while src == dest:
            src = random.randint(8, 11)
            dest = random.randint(12, 15)
        app = {
            'src': src,
            'dest': dest,
            'size': random.randint(1,1500),
            'interval_func': 'fixed',
            'interval': intervals[random.randint(0, len(intervals) - 1)],
            'app_id': app_id,
            'deadline': deadline,
            'prob': probs[random.randint(0, len(probs) - 1)],
        }
        app_id += 1
        app_info.append(app)
    for i in range(3):
        # A380
        src = -1
        dest = -1
        while src == dest:
            src = random.randint(8, 11)
            dest = random.randint(12, 15)
        app = {
            'src': src,
            'dest': dest,
            'size': 0,
            'interval_func': 'fixed',
            'interval': 1000,
            'app_id': app_id,
            'deadline': deadline,
            'prob': 0,
        }
        app_id += 1
        app_info.append(app)
    return app_info
