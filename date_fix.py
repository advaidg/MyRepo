import concurrent.futures
from datetime import datetime, timedelta

def run_sql(start_date, end_date):
    # Format dates as "dd--mm--yy" before using in SQL
    formatted_start_date = start_date.strftime("%d--%m--%y")
    formatted_end_date = end_date.strftime("%d--%m--%y")
    
    # Replace this with your actual SQL Plus command execution logic
    # For demonstration purposes, returning 0 or 1 to simulate success or failure
    return 0  # Replace with actual logic

def split_date_range(start_date, end_date, num_threads):
    date_range = end_date - start_date
    delta = date_range // num_threads
    
    date_ranges = []
    current_date = start_date
    
    for _ in range(num_threads):
        next_date = current_date + delta
        date_ranges.append((current_date, next_date))
        current_date = next_date

    return date_ranges

def run_threads(num_threads, start_date, end_date):
    date_ranges = split_date_range(start_date, end_date, num_threads)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(run_sql, start, end) for start, end in date_ranges]

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            result = future.result()
            formatted_start_date = date_ranges[i][0].strftime("%d--%m--%y")
            formatted_end_date = date_ranges[i][1].strftime("%d--%m--%y")

            if result == 0:
                print(f"Thread {i+1}: SQL execution succeeded for {formatted_start_date} to {formatted_end_date}")
            else:
                print(f"Thread {i+1}: SQL execution failed for {formatted_start_date} to {formatted_end_date}")

if __name__ == "__main__":
    start_date_str = "01-01-20"
    end_date_str = "01-01-25"
    date_format = "%d-%m-%y"

    start_date = datetime.strptime(start_date_str, date_format)
    end_date = datetime.strptime(end_date_str, date_format)
    
    num_threads = 40

    run_threads(num_threads, start_date, end_date)
