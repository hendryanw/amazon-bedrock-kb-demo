import boto3

# Split S3 URI into bucket name and object key
def split_s3_uri(s3_uri):
    s3_uri_parts = s3_uri.replace("s3://","").split("/")
    bucket_name = s3_uri_parts.pop(0)
    object_key = "/".join(s3_uri_parts)
    return bucket_name, object_key

# Generate S3 presigned URL to allow user to directly access the document stored in S3
def generate_presigned_url(s3_uri, expiration_time=3600):
    bucket_name, object_key = split_s3_uri(s3_uri)
    
    s3_client = boto3.client('s3', region_name = "us-east-1")
    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expiration_time
    )
    return presigned_url, bucket_name, object_key