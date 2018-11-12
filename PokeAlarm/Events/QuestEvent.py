# Standard Library Imports
import datetime
# 3rd Party Imports
# Local Imports
from PokeAlarm import Unknown
from . import BaseEvent
from PokeAlarm.Utils import get_gmaps_link, get_applemaps_link, \
    get_waze_link, get_dist_as_str, get_base_types


class QuestEvent(BaseEvent):
    """ Event representing the discovery of a PokeStop. """

    def __init__(self, data):
        """ Creates a new Quest Event based on the given dict. """
        super(QuestEvent, self).__init__('quests')
        check_for_none = BaseEvent.check_for_none

        # Identification
        self.stop_id = data['pokestop_id']
        self.stop_name = check_for_none(
            str, data.get('pokestop_name') or data.get('name'),
            Unknown.REGULAR)
        self.stop_image = check_for_none(
            str, data.get('pokestop_url') or data.get('url'), Unknown.REGULAR)

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
	
        # Quest Details
        self.quest = data['type']

		# Amount Details
        self.target = data.get('target')
		
		# Conditions
        self.conditions = data.get('conditions')
        self.rewardstring = check_for_none(
            str, data.get('rewards'), Unknown.REGULAR).strip()
        print(self.rewardstring)
        self.condition_type = None
        self.throw_type_id = None
        self.hit = None
        self.raid_levels = None
        self.pokemon_type_ids = None
        self.pokemon_ids = None
		
		# Rewards
        self.rewards = None
		
		# Items
        self.item_id = None
        self.amount = None
        self.stardust = None
		
		# Pokemon
        self.pokemon_id = None
        self.gender_id = None
        self.costume_id = None
        self.shiny = None
        self.form_id = None
		
        print(data)
		
        for condition in data['conditions']:
            self.infos = condition.get('info')
            self.condition_type = condition.get('type')
            if self.infos:
                self.hit = condition.get('info').get('hit')
                self.throw_type_id = condition.get('info').get('throw_type_id')
                self.raid_levels = condition.get('info').get('raid_levels')
                #self.pokemon_type_ids = condition.get('info').get('pokemon_type_ids')
                #self.pokemon_ids = condition.get('info').get('pokemon_ids')
                #if condition.get('info').get('throw_type_id'):
                #    for ids in condition.get('info').get('throw_type_id'):
                #        self.throw_type_id = ids			
                #if condition.get('info').get('raid_levels'):
                #    for ids in condition.get('info').get('raid_levels'):
                #        self.raid_levels = ids		
                if condition.get('info').get('pokemon_type_ids'):
                    for ids in condition.get('info').get('pokemon_type_ids'):
                        self.pokemon_type_ids = ids	
                if condition.get('info').get('pokemon_ids'):
                    for ids in condition.get('info').get('pokemon_ids'):
                        self.pokemon_ids = ids
				
        for reward in data['rewards']:
            self.rinfos = reward.get('info')
            self.rewards = reward.get('type')
            if self.rinfos:
                self.item_id = reward.get('info').get('item_id')
                self.amount = reward.get('info').get('amount')
                self.pokemon_id = reward.get('info').get('pokemon_id')
                self.gender_id = reward.get('info').get('gender_id')
                self.costume_id = reward.get('info').get('costume_id')
                self.shiny = reward.get('info').get('shiny')
                self.form_id = reward.get('info').get('form_id')			
            if self.rewards == 3:
                self.stardust = 1
		
        self.expiry = datetime.datetime.now().strftime("%d/%m/%Y 23:59")
        self.quest_type = check_for_none(int, data.get('type'), 0)
        self.condition_type = check_for_none(int, self.condition_type, 0)
        self.throw_type = check_for_none(int, self.throw_type_id, 0)
        self.pokemon_type = check_for_none(int, self.pokemon_type_ids, 0)
        self.name2 = check_for_none(int, self.pokemon_ids, 0)
        self.reward_type = check_for_none(int, self.rewards, 0)
        self.item_type = check_for_none(int, self.item_id, 0)
        self.name = check_for_none(int, self.pokemon_id, 0)

    def generate_dts(self, locale, timezone, units):
        """ Return a dict with all the DTS for this event. """
        quest_name = locale.get_quest_type_name(self.quest_type)
        condition_name = locale.get_condition_type_name(self.condition_type)
        throw_name = locale.get_throw_type_name(self.throw_type)
        type_name = locale.get_pokemon_type_name(self.pokemon_type)
        name2 = locale.get_pokemon_name(self.name2)
        reward_name = locale.get_reward_type_name(self.reward_type)
        item_name = locale.get_item_type_name(self.item_type)
        name = locale.get_pokemon_name(self.name)

        if self.hit is not None:
            self.hit = 'In a Row'
        else:
            self.hit = ''

        if self.raid_levels is not None:
            self.raid_levels = self.raid_levels
        else:
            self.raid_levels = ''

        if self.amount is not None:
            self.amount = self.amount
        else:
            self.amount = ''
			
        if self.pokemon_id is not None:
            self.pokemon_id = self.pokemon_id
        else:
            self.pokemon_id = ''
			
        stop_sprite = ''
        if self.pokemon_id:
            stop_sprite = 'http://skoodat.ca:200/sprites/{}.png'.format(self.pokemon_id)
        if self.item_id:
            stop_sprite = 'http://skoodat.ca:200/sprites/regular/quest/{}.png'.format(self.item_id)
        if self.stardust:
            stop_sprite = 'http://skoodat.ca:200/sprites/regular/quest/-{}.png'.format(self.stardust)
            item_name = 'Stardust'

        stop_img = ''
        if self.stop_image is not "unknown":
            stop_img = self.stop_image
        else:
            stop_img = 'http://skoodat.ca:200/sprites/regular/quest/Pokestop.png'
			
        dts = self.custom_dts.copy()
        dts.update({
            # Identification
            'stop_id': self.stop_id,
            'stop_name': self.stop_name,
            'stop_image': stop_img,
			'stop_sprite': stop_sprite,
			# Quest
            'quest_id': self.quest_type,
            'reward_id': self.reward_type,
            'quest_type': quest_name,
            'reward_type': reward_name,
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
            'geofence': self.geofence,
            # Quest Details
            'quest': self.quest,
			'target': self.target,
            'conditions_id': self.condition_type,
			'conditions_name': condition_name,
            'raid_levels': self.raid_levels,
			'throw_name': throw_name,
			'hit': self.hit,
            'type_name': type_name,
			'mon_name2': name2,
            'item_id': self.item_id,
			'item_name': item_name,
            'amount': self.amount,
            'mon_name': name,
			'pokemon_id': self.pokemon_id,
            'gender_id': self.gender_id,
            'costume_id': self.costume_id,
            'shiny': self.shiny,
            'form_id': self.form_id,
            'expiry': self.expiry,
            'rewardstring': self.rewardstring
        })
        return dts
