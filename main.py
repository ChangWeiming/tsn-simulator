from scenario import *
import argparse

parser = argparse.ArgumentParser(description='tsn simulator main loop')
parser.add_argument('--config', type=str, default='./data/config.json', help='config path')
args = parser.parse_args()

s = Scenario(config.Config(args.config))
print(s.main())