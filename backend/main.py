import asyncio
import argparse
import logging
import sys

from server import ServerOptions, Server 

parser = argparse.ArgumentParser(
    prog="MusicBox",
)
parser.add_argument("--logfile", default="musicbox.log")
parser.add_argument("--host", default="localhost")
parser.add_argument("--port", default=8080)
parser.add_argument("--file", default="filtered.csv")
parser.add_argument("--debug", action="store_true", default=False)
parser.add_argument("--ssl", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--key", action="store_true", default="privkey1.pem")
parser.add_argument("--cert", action="store_true", default="fullchain1.pem")


def setup_logging(args):
    logger = logging.getLogger("server")
    logger.propagate = False

    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    logger.setLevel(loglevel)

    fh = logging.FileHandler(filename=args.logfile)
    ch = logging.StreamHandler(stream=sys.stdout)

    formatter = logging.Formatter(
        fmt="{name:>20} {filename:>15}:{lineno:<3} {levelname:>8} {message}",
        style="{"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger



if __name__ == "__main__":
    args = parser.parse_args()
    opts = ServerOptions()

    opts.host = args.host
    opts.port = args.port
    opts.file = args.file
    opts.debug = args.debug
    opts.ssl = args.ssl
    opts.ssl_cert = args.cert
    opts.ssl_key = args.key

    logger = setup_logging(args)

    server = Server(opts=opts)
    asyncio.run(server.start())
