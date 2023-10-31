import requests
import datetime
import json
import threading
import time
from datetime import datetime as dt
from queue import Queue
import os
from flask_socketio import emit

# Constants
API_ENDPOINTS = {
    "us east": "https://api.logz.io/v1/search",
    "eu central": "https://api-eu-central-1.logz.io/v1/search",
    "canada central": "https://api-ca-central-1.logz.io/v1/search",
    "asia pacific": "https://api-ap-southeast-2.logz.io/v1/search",
    "eu west": "https://api-eu-west-1.logz.io/v1/search",
    "uk south": "https://api-uk-south-1.logz.io/v1/search",
    "west us 2": "https://api-westus2.logz.io/v1/search"
}

TIMEZONES = {
    "idt": "Asia/Jerusalem",
    "ist": "Asia/Kolkata",
    "london": "Europe/London",
    "edt": "US/Eastern",
    "gmt": "Etc/GMT",
    "asia": "Asia/Kolkata",
    "bst": "Europe/London",
    "mdt": "US/Mountain",
    "cdt": "US/Central",
    "cest": "Europe/Paris",
    "utc": "UTC"
}

DELAY_BETWEEN_REQUESTS = 2
MAX_RESULTS_PER_REQUEST = 10000
API_TIMEOUT_SECONDS = 10
MAX_CONCURRENT_REQUESTS = 80
current_date = datetime.datetime.utcnow()  # the user current time in UTC to calculate the DayOffset

# First ser for completed threads for Progress bar cal:
completed_threads_counter = 0

def threaded_fetch_data(api_token, region, lucene_query, start_time, end_time, day_offset, result_queue, accountids_input):
    """Threaded function to fetch data and put results in a queue."""
    results = fetch_data_in_interval(api_token, region, lucene_query, start_time, end_time, day_offset, accountids_input)
    result_queue.put(results)


def fetch_data_in_interval(api_token, region, lucene_query, start_time, end_time, day_offset, accountids_input):
    """Fetch data within a specified time interval."""
    endpoint = API_ENDPOINTS[region.lower()]
    if accountids_input:
        endpoint += f"?{accountids_input}"


    headers = {
        "X-API-TOKEN": api_token,
        "Content-Type": "application/json"
    }
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": lucene_query
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": start_time.isoformat(),
                                "lte": end_time.isoformat(),
                                "format": "strict_date_optional_time"
                            }
                        }
                    }
                ]
            }
        },
        "size": MAX_RESULTS_PER_REQUEST
    }

    for _ in range(3):  # Try up to 3 times
        try:
            response = requests.post(endpoint, headers=headers, json=body, timeout=API_TIMEOUT_SECONDS)
            if response.status_code != 200:
                user_friendly_msg = generate_user_friendly_error(response.status_code, response.text)
                error_message = f"{user_friendly_msg} API Response: {response.text}"
                raise ValueError(error_message)

            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(5)  # Wait for 5 seconds before retrying
    else:
        print(f"Failed to fetch data after 3 attempts for interval {start_time} to {end_time}")
        return []

    if response.status_code != 200:
        print(f"Error fetching data for interval {start_time} to {end_time}. Status code: {response.status_code}")
        return []

    data = response.json()
    return data["hits"]["hits"]


def fetch_data_concurrent(api_token, region, lucene_query, start_time, end_time, day_offset, accountids_input):
    """Fetch data using multiple threads."""

    total_results = []
    current_interval = datetime.timedelta(minutes=2)  # Start with 2 minutes
    threads = []
    result_queue = Queue()
    total_intervals = (end_time - start_time).total_seconds() / current_interval.total_seconds()
    completed_intervals = 0

    while start_time < end_time:
        interval_end = start_time + current_interval
        if interval_end > end_time:
            interval_end = end_time


        # Launch a thread to fetch the data for the current interval
        t = threading.Thread(target=threaded_fetch_data,
                             args=(api_token, region, lucene_query, start_time, interval_end, day_offset, result_queue, accountids_input))
        threads.append(t)
        t.start()
        # Ensure we don't exceed the maximum number of concurrent requests
        while threading.active_count() > MAX_CONCURRENT_REQUESTS:
            time.sleep(0.1)  # Small delay to avoid busy-waiting

        completed_intervals += len([t for t in threads if not t.is_alive()])

        # Clear threads that have completed
        threads = [t for t in threads if t.is_alive()]
        progress_percentage = round(min(100, (completed_intervals / total_intervals) * 100))

        # Emit the progress update to Flask.app
        emit('progress_update', {'progress': progress_percentage}, namespace='/progress', broadcast=True)


        if interval_end == end_time:
            break
        start_time = interval_end

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Collect results from the queue
    while not result_queue.empty():
        total_results.extend(result_queue.get())

    return total_results


def remove_duplicates(total_results):
    """Remove duplicate results based on _id."""
    seen_ids = set()
    unique_results = []
    for result in total_results:
        _id = result.get('_id')
        if _id not in seen_ids:
            seen_ids.add(_id)
            unique_results.append(result)
    return unique_results



def get_file_extension(format):
    return ".csv" if format == "csv" else ".txt"


def process_data(api_token, region, lucene_query, date_time_input, accountids_input, file_format):
    start_date_str, end_date_str, user_timezone_str = [x.strip() for x in date_time_input.split('-')]
    start_date = datetime.datetime.strptime(start_date_str, "%b %d, %Y @ %H:%M:%S.%f")
    end_date = datetime.datetime.strptime(end_date_str, "%b %d, %Y @ %H:%M:%S.%f")
    start_date = datetime.datetime.utcfromtimestamp(start_date.timestamp())
    end_date = datetime.datetime.utcfromtimestamp(end_date.timestamp())
    multi_accountids = [x.strip() for x in accountids_input.split(',')] if accountids_input else None
    accountids_input = '&'.join([f"accountIds={x}" for x in multi_accountids]) if multi_accountids else ''

    day_offset = (current_date - start_date).days + 1

    total_results = fetch_data_concurrent(api_token, region, lucene_query, start_date, end_date, day_offset,
                                          accountids_input)
    unique_results = remove_duplicates(total_results)

    if not unique_results:
        raise ValueError(
            "Sorry, no results were found or the provided credentials are invalid. Please check the terminal for additional details and try again.")

    # Only save to a file if there are results
    if len(unique_results) > 0:

        baseDir = [os.path.dirname(os.path.abspath(__file__))][-1]
        filespath = f"{baseDir}/Downloads/"
        # Get the path to the user's Downloads folder
        # downloads_folder = os.path.expanduser('~') + "/Downloads/"

        file_ext = ".csv" if file_format == "csv" else ".txt"

        # Create the filename with its full path
        filename = filespath + f"Logz.io API Query Tool-{dt.now().strftime('%Y-%m-%d_%H-%M')}-Results-{len(unique_results)}{file_ext}"

        with open(filename, 'w') as file:
            if file_format == "csv":
                import csv
                writer = csv.DictWriter(file, fieldnames=unique_results[0].keys())
                writer.writeheader()
                for result in unique_results:
                    writer.writerow(result)
            else:
                for result in unique_results:
                    file.write(json.dumps(result) + "\n")

        return filename  # Return the full path where the results are saved


def generate_user_friendly_error(status_code, response_text):
    if status_code == 401:
        return "You are not authorized. Please check your credentials."
    elif status_code == 404:
        return "The requested data was not found."
    elif status_code == 500:
        return "There's an issue with the server. Please try again later."
    else:
        return "An unexpected error occurred. Please try again later."

