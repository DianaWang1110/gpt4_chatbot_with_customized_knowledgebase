import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_s3(file_name, bucket, s3_file_path):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param s3_file_path: S3 object name. If not specified then the file_name is used
    :return: True if file was uploaded, else False
    """
    s3 = boto3.client('s3')

    try:
        s3.upload_file(file_name, bucket, s3_file_path)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False