import argparse

from expense_processing.config import DATA_FOLDER
from expense_processing.ingestion import ingest_folder
from expense_processing.logging_config import setup_logging


def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        prog="expense-processing",
        description="Load expense CSV files into PostgreSQL and run analytics.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser(
        "ingest", help="Load CSV files from a folder into the database"
    )
    ingest_parser.add_argument(
        "--folder", default=DATA_FOLDER, help="Folder containing CSV files"
    )

    args = parser.parse_args()

    if args.command == "ingest":
        ingest_folder(args.folder)


if __name__ == "__main__":
    main()