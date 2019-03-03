import boto3, botocore, argparse, sys, os, requests

parser = argparse.ArgumentParser()
parser.add_argument('buckets',help='file text with bucket names')
client = boto3.client('s3')
args = parser.parse_args()


def check_bucket_exists():
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.head_bucket(Bucket=args.buckets)
        print("Bucket Exists!")
        return True
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            print('Private bucket')
            return True
        elif error_code == 404:
            print("Bucket does not exist")
            return False

def permissions_bucket():
    """
    This function checks the permissions of a bucket and gives information about the bucket' permissions.
    """

    try:
        list_bucket_response = client.get_bucket_acl(Bucket=args.buckets)  # args.buckets
        for grant in list_bucket_response['Grants']:
            print(grant)

    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Message']
        if error_code == 'AccessDenied':
            print('Access Denied')
        if error_code == 'All access to this object has been disabled':
            print('All access to this object has been disabled')
        if error_code == 'The specified bucket does not exist':
            print('The specified bucket does not exist')


def check_bucket_files():
    """
    This functions gives you information about the contents of S3 buckets if these are set to public.
    """

    results = client.list_objects(Bucket=args.buckets)
    for obj in results.get('Contents', []):
        print(obj)


def check_bucket(bucket,argsList):

    if ".amazonaws.com" in bucket:
        buckets = bucket[:bucket.rfind(".s3")]
    elif ":" in bucket:
        buckets = bucket.split[0]
    else:
        buckets = bucket

    valid_bucket = check_bucket_name(bucket)

    if not valid_bucket:
        message = "{0:>11} : {1}".format("[invalid]", bucket)
        slog.error(message)
        return





def check_bucket_name(bucketname):

    if (len(bucketname) < 3) or (len(bucketname) >63):
        return False

    for char in bucketname:
        if char.lower() not in "abcdefghijklmnopqrstuvwxyz0123456789.-":
            return False
    return True


def check_bucket_without_creds(bucketname, triesleft=3):

    if triesleft == 0:
        return False

    bucketurl = 'http://' + bucketname + '.s3.amazonaws.com'

    r = requests.head(bucketurl)

    if r.status_code == 200:
        return True
    elif r.status_code == 403:
        return True
    elif r.status_code == 404:
        return False
    elif r.status_code == 503:
        return check_bucket_without_creds(bucketname, triesleft -1)
    else:
        raise ValueError("Unhandled status code: " + str(r.status_code) + " for bucket: " + bucketname)


def awsCred_Configured(bucket):

    pass










#check_bucket_exists()
permissions_bucket()
