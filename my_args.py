from os import getenv


def host_arguments(parser):
    parser.add_argument('name', nargs="?", type=str,
                        help="Pass bucket name.", default=None)

    parser.add_argument(
        "-src",
        "--source",
        type=str,
        help="pass source file/folder",
        default=None    )


def quote_arguments(parser):
  parser.add_argument(
        'bucket_name',
        type=str,
        help="Pass bucket name.",
        default=None)
  
  parser.add_argument(
        "-i",
        "--inspire",
        type=str,
        help="Pass author name",
        default = None)