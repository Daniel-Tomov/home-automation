import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("lightnum", type=int)
parser.add_argument("lightval", type=int)

args = parser.parse_args()

#print(args.lightnum)


if args.lightnum == 1:
	if args.lightval == 1:
		os.system('mycroft-say-to lights on')
	elif args.lightval == 0:
		os.system('mycroft-say-to lights off')
