from datetime import datetime, timedelta

target_datetime = None # Global variable to store the target date and time

def validate_time(time_str):
    """ Validate if the time_str is in the correct format '%H:%M'. """
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def validate_date(date_str):
    """ Validate if the date_str is in the correct format '%d/%m/%Y'. """
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def update_countdown():
    """ Calculate and return the remaining time as a formatted string. """
    now = datetime.now()
    
    if target_datetime is None:
        return 'No Target Time Set'
    
    remaining_time = target_datetime - now
    
    if remaining_time <= timedelta(0):
        return 'Countdown Ended'
    
    # Break down remaining time into days, hours, minutes, seconds, and milliseconds
    days, remainder = divmod(remaining_time.total_seconds(), 86400)  # 86400 seconds in a day
    hours, remainder = divmod(remainder, 3600)  # 3600 seconds in an hour
    minutes, remainder = divmod(remainder, 60)  # 60 seconds in a minute
    seconds, milliseconds = divmod(remainder, 1)  # 1 second is 1000 milliseconds
    milliseconds = int(milliseconds * 1000)  # Convert fraction of second to milliseconds
    
    # Format the countdown string
    time_str = f"{int(days)} Day(s) " if days > 0 else ""
    time_str += f"{int(hours):02}:" if days > 0 or hours > 0 else ""
    time_str += f"{int(minutes):02}:" if days > 0 or hours > 0 or minutes > 0 else ""
    time_str += f"{int(seconds):02}"
    
    return time_str.strip()

def countdown_xd(day, month, year, hour, minute, second=0):
    """
    Set the target date and time, then return the formatted countdown string.
    """
    global target_datetime
    target_datetime = datetime(year, month, day, hour, minute, second)
    
    return update_countdown()
