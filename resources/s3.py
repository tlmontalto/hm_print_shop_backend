import models
import boto3
import pandas


def upload_file(file_name, bucket):
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return response

def download_file(file_name, bucket):
    s3 = boto3.resource('s3')
    output = f'downloads/{file_name}'
    s3.Bucket(bucket).download_file(file_name, output)

    return output

def list_files(bucket):
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents