def split_date_range(start_date_str, end_date_str):
    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%d-%b-%y")
    end_date = datetime.strptime(end_date_str, "%d-%b-%y")

    # Initialize the list to store the year-wise ranges
    year_ranges = []

    # Calculate the remaining year ranges
    current_date = start_date
    while current_date <= end_date:
        year_end = datetime(current_date.year, 12, 31)
        if year_end > end_date:
            year_end = end_date
        year_ranges.append((current_date, year_end))
        current_date = year_end + timedelta(days=1)

    return year_ranges
