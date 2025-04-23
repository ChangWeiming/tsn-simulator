from scenario import *
import statistics_pkt
import time
import argparse

parser = argparse.ArgumentParser(description='tsn simulator main loop')
parser.add_argument('--config', type=str, default='./data/config.json', help='config path')
args = parser.parse_args()

s = Scenario(config.Config(args.config))
start = time.time()
x = s.main()
end = time.time()
# print("{}".format(end - start))

flag = 0
ans = 0
s = 0
# print(x)
# statistics_pkt.g_stat.get_random_packet_timestamp()
for k,v in x['qoe'].items():
    # s += 1
    if v > 1e-8:
        flag = 1
        break
    # ans += v
    
print (flag)

