from pytz import all_timezones

print len(all_timezones)
for zone in all_timezones:
    if 'India' in zone:
        print zone