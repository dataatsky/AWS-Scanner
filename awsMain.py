
import argparse
import testS3 as s3aws
import os.path

parser = argparse.ArgumentParser(description='Aws Scanner')

parser.add_argument('-l', '--list', required=False, dest='list', action='store_true',
                    help='Name of text file containing buckets to check')
parser.add_argument('-s' '--save', required=False, dest='save')
parser.add_argument('buckets', help='Name of the bucket')

args = parser.parse_args()


#Read a text file
if os.path.isfile(args.buckets):
    with open(args.buckets, 'r') as f:
        for line in f:
            line = line.rstrip()
            s3aws.check_bucket(line,args.list,args.save)
else:
    s3aws.check_bucket(args.buckets,args.list,args.save)
