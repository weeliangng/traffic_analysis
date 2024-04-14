from datetime import datetime, timedelta
def get_datetime_intervals(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    minute_intervals = [date_obj + timedelta(minutes=i) for i in range(24*60)]
    minute_intervals_str = [i.strftime("%Y-%m-%dT%H:%M:%S") for i in minute_intervals]
    return minute_intervals_str
