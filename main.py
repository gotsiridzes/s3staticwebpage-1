import logging
from botocore.exceptions import ClientError
from auth import init_client
from bucket.policy import assign_policy
from host_static.host_web_configuration import set_bucket_website_policy
from host_static.host_web_page_files import static_web_page_file
from my_args import host_arguments
import argparse

parser = argparse.ArgumentParser(
    description="CLI program that uploads your static website to aws s3 bucket.",
    prog='main.py'
)

subparsers = parser.add_subparsers(dest='command')

host = host_arguments(subparsers.add_parser(
    "host", help="work with static website hosting"))


def main():
    s3_client = init_client()
    args = parser.parse_args()

    match args.command:
        case "host":
            if args.name:
                # enable public read policy
                assign_policy(s3_client, "public_read_policy", args.name)

                # configure website policy
                set_bucket_website_policy(s3_client, args.name, True)

                #upload and print website url
                print(static_web_page_file(s3_client, args.name, args.source))


if __name__ == "__main__":
    try:
        main()
    except ClientError as error:
        if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            logging.warning("Bucket already exists! Using it.")
        else:
            logging.error(error)
    except ValueError as error:
        logging.error(error)
