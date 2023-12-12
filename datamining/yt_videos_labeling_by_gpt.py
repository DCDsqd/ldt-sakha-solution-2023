import g4f
import sqlite3
import time

# g4f params
g4f.debug.logging = True  # Enable debug logging
g4f.debug.check_version = False  # Disable automatic version checking


# Function to retrieve the first record where 'description' is not NULL and 'gpt_ans' is NULL
def fetch_record(db_file_path, table_name):
    """
    Fetch the first record where 'description' is not NULL and 'gpt_ans' is NULL.

    Parameters:
    db_file_path (str): Path to the SQLite database file.
    table_name (str): Name of the table to query.

    Returns:
    tuple: The first matching record or None if no record is found.
    """
    # Establish a connection to the database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # SQL query to find the required record
    query = f"""SELECT * FROM {table_name}
                WHERE description IS NOT NULL AND gpt_ans IS NULL
                LIMIT 1;"""

    try:
        cursor.execute(query)
        record = cursor.fetchone()
        # Return None if the record is empty (e.g., all values are None)
        return None if record is None or all(x is None for x in record) else record
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


def update_gpt_ans(db_file_path, table_name, record_id, gpt_ans_value):
    """
    Update the 'gpt_ans' field for a record with the given ID.

    Parameters:
    db_file_path (str): Path to the SQLite database file.
    table_name (str): Name of the table to update.
    record_id (int or str): ID of the record to update.
    gpt_ans_value (str): Value to set for the 'gpt_ans' field.

    Returns:
    bool: True if the update was successful, False otherwise.
    """
    # Establish a connection to the database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # SQL query to update the 'gpt_ans' field
    query = f"""UPDATE {table_name}
                SET gpt_ans = ?
                WHERE video_id = ?;"""

    try:
        # Execute the update operation
        cursor.execute(query, (gpt_ans_value, record_id))
        conn.commit()  # Commit the changes
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()


def update_gpt_time(db_file_path, table_name, yt_id, _time):
    # Insert the operation time into the database (assuming there is a column 'operation_time')
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    try:
        cursor.execute(f"""UPDATE {table_name}
                                   SET gpt_time_to_ans = ?
                                   WHERE video_id = ?;""", (_time, yt_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while updating the operation time: {e}")
    finally:
        conn.close()


def ask_gpt(query) -> str:
    # print(g4f.Provider.Bing.params)  # Print supported args for Bing

    # Using automatic a provider for the given model
    # Streamed completion
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": query
        }],
        stream=True,
        provider=g4f.Provider.Yqcloud
    )
    ans = ""
    for message in response:
        ans += message

    return ans


if __name__ == "__main__":

    with open("prompts/yt_gpt_prompt.txt", encoding='utf-8', mode='r') as f:
        prompt = f.read()

    db_path = '../data/large/trending_ru_yt_videos.db'
    table = 'videos'
    record = fetch_record(db_path, table)
    while record is not None:
        query_str = "Заголовок: " + record[2] + "\n"
        query_str += "Описание: " + record[11] + "\n"
        query_str += "Тэги: " + record[6]
        print(query_str)

        start_time = time.time()  # Start time of the operations
        gpt_labels = ask_gpt(prompt + query_str)
        end_time = time.time()
        # Calculate the duration of the operations
        operation_duration = end_time - start_time

        if gpt_labels == "" or gpt_labels is None:
            print("Empty response or no response at all. Terminating script.")
            exit(0)

        print(gpt_labels)

        update_gpt_ans(db_path, table, record[0], gpt_labels)
        update_gpt_time(db_path, table, record[0], operation_duration)

        record = fetch_record(db_path, table)
