# import datetime
#
# x = datetime.datetime.now()
# print x
# y =str(x).split(':')
# z = y[0]+":"+y[1]
#
# print y
# print z
import datetime
import pytz # new import

current_time = datetime.datetime.now() #system time

server_timezone = pytz.timezone("US/Eastern")
new_timezone = pytz.timezone("Canada/Central")
print current_time
print server_timezone
print new_timezone
# returns datetime in the new timezone. Profit!
current_time_in_new_timezone = server_timezone.localize(current_time).astimezone(new_timezone)

print current_time_in_new_timezone