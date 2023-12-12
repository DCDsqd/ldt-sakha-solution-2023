import pandas as pd
import sqlite3
import argparse


# Usage:
# python csv_to_db.py path_to_csv_file.csv path_to_database.db table_name
# python csv_to_db.py ../large/trending_ru_yt_videos.csv ../large/trending_ru_yt_videos.db trending_videos


def csv_to_sqlite(csv_file_path, db_file_path, table_name):
    """
    Convert a CSV file to a SQLite database table.

    Parameters:
    csv_file_path (str): Path to the CSV file.
    db_file_path (str): Path to the SQLite database file.
    table_name (str): Name of the table to create in the SQLite database.
    """
    encodings = ['utf-8', 'windows-1251', 'cp1252', 'cp1251', 'utf-16']  # List of encodings to try
    df = None

    used_enc = None
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_file_path, encoding=encoding)
            used_enc = encoding
            break  # Stop trying if successful
        except UnicodeDecodeError:
            continue  # Try the next encoding if current one fails

    if df is None:
        print("Failed to read the CSV file with the tried encodings.")
        return

    try:
        # Create a SQLite database connection
        conn = sqlite3.connect(db_file_path)

        # Write the DataFrame to the database
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        # Close the database connection
        conn.close()

        print(f"CSV data from '{csv_file_path}' successfully imported to '{table_name}' table in '{db_file_path}' "
              f"database using encoding {used_enc}.")
    except Exception as e:
        print(f"An error occurred while writing to the database: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert a CSV file to a SQLite database table.")
    parser.add_argument('csv_file_path', type=str, help='Path to the CSV file.')
    parser.add_argument('db_file_path', type=str, help='Path to the SQLite database file.')
    parser.add_argument('table_name', type=str, help='Name of the table to create in the SQLite database.')

    args = parser.parse_args()
    csv_to_sqlite(args.csv_file_path, args.db_file_path, args.table_name)


if __name__ == '__main__':
    main()
