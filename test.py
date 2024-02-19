from datetime import datetime

date_string = "2024-02-06 15:03:33"
datetime_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

print(datetime.utcnow() > datetime_object)