from Engine import *
from argparse import ArgumentParser
from threading import Thread
import os
import sys

def main():
    parser = ArgumentParser(
        prog="Dmap",
        usage="Dmap [-t TARGET -o OUTPUT]"
    )

    parser.add_argument(
        "-t",
        "--target",
        help="Define the target drive.",
        type=str
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Defines the output file/folder that stores the results."
    ) # Output Path

    parser.add_argument(
        "--version",
        help="Prints the version of the software.",
        action='version',
        version='%(prog)s 1.0.0 Prsent by HATZ Community'
    ) # Software Version

    arguments = parser.parse_args()
    if arguments.target:
        drive = arguments.target
        output = arguments.output
        diskImageConverter = DiskImager(DRIVE=drive, OUTPUT=output)
        diskImageConverter.Convert()

if __name__ == '__main__':
    main()