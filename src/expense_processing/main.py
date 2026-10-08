import argparse

from expense_processing.config import DATA_FOLDER
from expense_processing.ingestion import ingest_folder
from expense_processing.logging_config import setup_logging
from expense_processing.analytics import REPORTS, run_report

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
   
    analytics_parser = subparsers.add_parser(
        "analytics", help="Run an analytics report on the stored expenses"
    )
    analytics_parser.add_argument(
        "--report",
        choices=list(REPORTS),
        required=True,
        help="Which report to run",
    )

    args = parser.parse_args()

    if args.command == "ingest":
        ingest_folder(args.folder)

    elif args.command == "analytics":
        run_report(args.report)

if __name__ == "__main__":
    main()