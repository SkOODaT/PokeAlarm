# Standard Library Imports
from datetime import datetime
# 3rd Party Imports
# Local Imports
from PokeAlarm import Unknown
from . import BaseEvent
from PokeAlarm.Utils import get_gmaps_link, get_applemaps_link, \
    get_waze_link, get_time_as_str, get_seconds_remaining, get_dist_as_str, get_grunt_type


class StopEvent(BaseEvent):
    """ Event representing the discovery of a PokeStop. """

    def __init__(self, data):
        """ Creates a new Stop Event based on the given dict. """
        super(StopEvent, self).__init__('stop')
        check_for_none = BaseEvent.check_for_none

        # Identification
        self.stop_id = data['pokestop_id']
        self.stop_name = check_for_none(
            str, data.get('pokestop_name') or data.get('name'),
            Unknown.REGULAR)
        self.stop_image = check_for_none(
            str, data.get('pokestop_url') or data.get('url'), Unknown.REGULAR)

        # Time left
        self.expiration = data['lure_expiration']
        self.time_left = None
        if self.expiration is not None:
            self.expiration = datetime.utcfromtimestamp(self.expiration)
            self.time_left = get_seconds_remaining(self.expiration)

        # Time left
        self.incidentexpiration = data['incident_expire_timestamp']
        self.itime_left = None
        if self.incidentexpiration is not None:
            self.incidentexpiration = datetime.utcfromtimestamp(self.incidentexpiration)
            self.itime_left = get_seconds_remaining(self.incidentexpiration)
		
        self.pokestopdisplay = data['pokestop_display']
		
        self.gruntType = data['grunt_type']
		
        # Location
        self.lat = float(data['latitude'])
        self.lng = float(data['longitude'])

        # Completed by Manager
        self.distance = Unknown.SMALL
        self.direction = Unknown.TINY

        # Used to reject
        self.name = self.stop_id
        self.geofence = Unknown.REGULAR
        self.custom_dts = {}

    def generate_dts(self, locale, timezone, units):
        """ Return a dict with all the DTS for this event. """
        time = get_time_as_str(self.expiration, timezone)
        itime = get_time_as_str(self.incidentexpiration, timezone)
        dts = self.custom_dts.copy()
        stop_img = ''
        if self.stop_image is not "unknown":
            stop_img = self.stop_image
        dts.update({
            # Identification
            'stop_id': self.stop_id,
            'stop_name': self.stop_name,
            'stop_image': stop_img,

            # Time left
            'time_left': time[0],
            '12h_time': time[1],
            '24h_time': time[2],

            # Incidend Time left
            'itime_left': itime[0],
            'i12h_time': itime[1],
            'i24h_time': itime[2],
			
			# Pokestop Display
            'pokestopdisplay': self.pokestopdisplay,
            'gruntType': locale.get_grunt_name(self.gruntType),
			
            # Location
            'lat': self.lat,
            'lng': self.lng,
            'lat_5': "{:.5f}".format(self.lat),
            'lng_5': "{:.5f}".format(self.lat),
            'distance': (
                get_dist_as_str(self.distance, units)
                if Unknown.is_not(self.distance) else Unknown.SMALL),
            'direction': self.direction,
            'gmaps': get_gmaps_link(self.lat, self.lng),
            'applemaps': get_applemaps_link(self.lat, self.lng),
            'waze': get_waze_link(self.lat, self.lng),
            'geofence': self.geofence
        })
        return dts
