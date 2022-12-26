#!/usr/bin/env python
# coding: utf-8

"""
Module:         auto_utility_dates.py
Description:    library for date processing
Created:        30 Jul 2022

Versions:
20210216    Reorganize utility files
"""
#import config

from datetime import datetime

def getDuration(then, now = datetime.now(), interval = "default"):
    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then # For build-in functions
    duration_in_s = duration.total_seconds()
    
    def years():
        return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
        return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
        return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
        return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
        if seconds != None:
            return divmod(seconds, 1)   
        return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])
        if int(y[0]) > 0: return "{} years, {} days, {} hours, {} minutes and {} seconds".format(int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0]))
        if int(d[0]) > 0: return "{} days, {} hours, {} minutes and {} seconds".format(int(d[0]), int(h[0]), int(m[0]), int(s[0]))
        if int(h[0]) > 0: return "{} hours, {} minutes and {} seconds".format(int(h[0]), int(m[0]), int(s[0]))
        if int(m[0]) > 0: return "{} minutes and {} seconds".format(int(m[0]), int(s[0]))
        return "{} seconds".format(int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]
'''
# Example usage
then = datetime(2022, 9, 30, 0, 22, 15)
now = datetime.now()

print(getDuration(then)) # E.g. Time between dates: 7 years, 208 days, 21 hours, 19 minutes and 15 seconds
print(getDuration(then, now, 'years'))      # Prints duration in years
print(getDuration(then, now, 'days'))       #                    days
print(getDuration(then, now, 'hours'))      #                    hours
print(getDuration(then, now, 'minutes'))    #                    minutes
print(getDuration(then, now, 'seconds'))    #                    seconds
'''
