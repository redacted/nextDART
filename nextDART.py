#!/usr/bin/env python

# Global data

# dict for dart station rss IDs
stations = {
    'pearse'           : 'PERSE',
    'blackrock'        : 'BROCK',
    'grand canal dock' : 'GCDK',
    'tara'             : 'TARA',
    'tara street'      : 'TARA',
}   


def dart_arrival_time(dart, now):
    """
    returns time to DART in minutes (int). 
    dart = RSS item 
    now = (hours, minutes) tuple
    """

    dart_ = dart.split()
    # get the hours and minutes of the dart arrival, convert to minutes
    hours_eta, mins_eta = dart_[0].split(':')
    delta_min = 60*int(hours_eta) + int(mins_eta)

    # do the same with the current time
    now_min = 60*int(now[0]) + int(now[1])

    return int(delta_min - now_min)

def set_args():
    """
    Set up options
    """

    import sys
    from optparse import OptionParser

    # set up arguments, take any immediate action required
    parser = OptionParser()

    parser.add_option("-s", "--station", dest="start_station", help="starting station")

    parser.add_option("-d", "--direction", dest="direction", help="direction of travel" )

    parser.add_option("-l", "--list", action="store_true", dest="list_stations", help="list available stations" )

    (options, args) = parser.parse_args()   

    if options.list_stations:
        print "Possible options for starting station:"
        print "\n".join(stations.keys())  
        sys.exit()
    
    # assign arguments as required
    try:
        start_station = options.start_station.lower()
        direction = options.direction.lower()
    except Exception, e:
        parser.error("Problem with arguments, see -h --help for help")
        print e                 

    return (start_station, direction)

def main():
    import sys

    try:
        import feedparser
    except Exception, e:
        print("Requires feedparser module")
        print e

    # handle options
    start_station, direction = set_args()

    feed = feedparser.parse('http://www.irishrail.ie/realtime/publicinfo.asp?strLocation=' + stations[start_station])
    # check that feed returned correctly
    good_responses = [200,]
    try:
        if feed.status not in good_responses:
            print("Feed download failed (status %d)" % (feed.status) )
            sys.exit()
    except Exception, e:
        print("Error: no connection made")
        sys.exit()

    print feed.feed.title

    # terminating stations
    if direction == 'south':
        targets = ['Bray', 'Greystones']
    elif direction == 'north':
        targets = ['Howth', 'Malahide']

    # initialise current time
    feed_time = feed.feed.title.split()[-1]
    # time is HH:MMam so we split on':' then remove the am or pm
    now_hour, now_min = feed_time.split(':')[0], feed_time.split(':')[1]
    now_min = now_min[0:-2]
    now = (now_hour, now_min)

    # now find the right darts
    #for item in feed['items']:
    for entry in feed.entries:
        dart = entry.title
        # destination is last word in each item
        if dart.split()[-1] in targets:
            print("[ arriving in %3d minutes ]  %s" % (dart_arrival_time(dart, now), dart))     

if __name__ == '__main__':
    main()
