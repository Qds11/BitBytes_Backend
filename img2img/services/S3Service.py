import boto3, uuid ,sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).absolute().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from botocore.exceptions import ClientError
from utils.APIError import InvalidAPIUsage

class S3BucketWrapper:
    """ Encapsulates S3 bucket actions.
        Reference: https://docs.aws.amazon.com/code-library/latest/ug/python_3_s3_code_examples.html
    """

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')
    
    def put(self, file, prefix="public/", object_name=None, contentType='image/png'):
        """
        Uploads a file to an S3 bucket and returns the URL of the uploaded file.

        Args:
            file (file-like object): The file to be uploaded.
            prefix (str, optional): The S3 bucket prefix where the file will be stored. Default is "public/".
            object_name (str, optional): The name of the object in the S3 bucket. If None, a UUID will be generated. Default is None.
            contentType (str, optional): The MIME type of the file. Default is 'image/png'.

        Returns:
            str: The URL of the uploaded file.

        Raises:
            InvalidAPIUsage: If there is an error during the file upload process.

        Example usage:
            url = put(file, prefix="images/", contentType='image/jpeg')
        """
        if object_name is None:
            object_name = str(uuid.uuid4())
        try:
            response = self.s3.upload_fileobj(file, self.bucket_name, prefix + object_name, ExtraArgs={'ContentType': contentType})
            url = f"https://{self.bucket_name}.s3.ap-southeast-1.amazonaws.com/{prefix}{object_name}"
        except ClientError as e:
            InvalidAPIUsage(e, 500)

        return url

def hello_s3(file):
    s3Bucket = S3BucketWrapper("bitbytebucket")
    return s3Bucket.put(file)
        
    