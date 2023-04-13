import io
import logging
from botocore.exceptions import ClientError
from auth import init_client
from bucket.policy import assign_policy
from host_static.host_web_configuration import set_bucket_website_policy
from host_static.host_web_page_files import static_web_page_file
from my_args import host_arguments, quote_arguments
import argparse
import json
from urllib.request import urlopen, Request
from random import choice

from object.crud import upload_local_file


headers = {
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

parser = argparse.ArgumentParser(
    description="CLI program that uploads your static website to aws s3 bucket.",
    prog='main.py'
)

subparsers = parser.add_subparsers(dest='command')

host = host_arguments(subparsers.add_parser(
    "host", help="work with static website hosting"))
quotes = quote_arguments(subparsers.add_parser(
    "quote", help="work with random string quotes"))


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

                # upload and print website url
                print(static_web_page_file(s3_client, args.name, args.source))

        case "quote":
            if args.bucket_name and args.inspire:
                json_result = []
                with urlopen(Request("https://type.fit/api/quotes", data=None,headers=headers)) as response:
                    json_result = json.loads(response.read().decode())
                
                quote_list = []                    
                for i in json_result:
                    if(i['author'] == args.inspire):
                        quote_list.append(i)
                        
                    
                # random_quote = json.dumps(choice(quote_list))
                random_quote = choice(quote_list)
                file_name = f'static/{dict(random_quote)["author"]}.json'
                with open(file_name, 'w') as f:
                    f.write(json.dumps(random_quote))
                
                print(upload_local_file(s3_client, args.bucket_name, file_name, True, "upload_file"))



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
