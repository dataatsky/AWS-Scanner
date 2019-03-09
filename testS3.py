import boto3, botocore,requests,subprocess

client = boto3.client('s3')


def exceptions(e,bucketname):

    error_code = e.response['Error']['Message']
    if error_code == 'AccessDenied':
        print('Access Denied')
    if error_code == 'All access to this object has been disabled':
        print('All access to this object has been disabled:')
    if error_code == 'The specified bucket does not exist':
        print('The specified bucket does not exist',bucketname)


def permissions_bucket(bucketname):
    """
    This function checks the permissions of a bucket and gives information about the bucket' permissions.
    """

    try:
        list_bucket_response = client.get_bucket_acl(Bucket=bucketname)  # args.buckets
        for grant in list_bucket_response['Grants']:
            if grant is not None:
                save_results_file(grant)



    except botocore.exceptions.ClientError as e:
        exceptions(e,bucketname)


def check_bucket_files(bucketname,argssave):
    """
    This functions gives you information about the contents of S3 buckets if these are set to public.
    """
    try:
        results = client.list_objects(Bucket=bucketname)
        for obj in results.get('Contents', []):
            if obj is not None:
                save_results_file(obj)


    except botocore.exceptions.ClientError as e:
        exceptions(e,bucketname)


def check_bucket_name(bucketname):

    if (len(bucketname) < 3) or (len(bucketname) >63):
        return False

    for char in bucketname:
        if char.lower() not in "abcdefghijklmnopqrstuvwxyz0123456789.-":
            return False
    return True


def check_bucket(bucket,argslist,argssave):
    awscred_configured()  # Checks if the aws credentials are set up.

    if ".amazonaws.com" in bucket:
        buckets = bucket[:bucket.rfind(".s3")]
    elif ":" in bucket:
        buckets = bucket.split[0]
    else:
        buckets = bucket

    valid_bucket = check_bucket_name(bucket)

    if not valid_bucket:
        message = "{0:>11} : {1}".format("[invalid bucket name]", bucket)
        print(message)
        return

    else:
        check_bucket_name(buckets)
        permissions_bucket(buckets)
        check_bucket_files(buckets,argssave)


def awscred_configured():

    p = subprocess.Popen(['aws', 'sts', 'get-caller-identity', '--output', 'text', '--query', 'Account'],stdout=subprocess.PIPE)
    response, error = p.communicate()

    if error is not None:
        print("Your AWS creds are not setup. Please set them up to make this program work correctly")
    else:
        pass


def save_results_file(info):
    f = open('results.txt','a')
    f.write(str(info) + '\n')
    f.close()

