
import argparse
import testS3 as s3aws
import sys
import os.path
import boto3

parser = argparse.ArgumentParser()
parser.add_argument('buckets',help='file text with bucket names')
parser.add_argument('-l', '--list', required=False, dest='list', action='store_true',
                    help='Save bucket file listing to local file: ./list-buckets/${bucket}.txt')
client = boto3.client('s3')
args = parser.parse_args()

if os.path.isfile(args.buckets):
    with open(args.buckets, 'r') as f:
        for line in f:
            line = line.rstrip()
            s3aws.check_bucket(line,args.list)
else:
    s3aws.check_bucket(args.buckets,args.list)
