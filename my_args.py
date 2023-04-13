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
