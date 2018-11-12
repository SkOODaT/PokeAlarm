# Standard Library Imports
import operator
# 3rd Party Imports
# Local Imports
from . import BaseFilter
from PokeAlarm.Utilities import GymUtils as GymUtils, QuestUtils
from PokeAlarm.Utilities import MonUtils as MonUtils


class QuestFilter(BaseFilter):
    """ Filter class for limiting which quests trigger a notification. """

    def __init__(self, mgr, name, data):
        """ Initializes base parameters for a filter. """
        super(QuestFilter, self).__init__(mgr, 'quest', name)

        # Monster ID - f.monster_ids contains m.monster_id
        self.monster_ids = self.evaluate_attribute(  #
            event_attribute='monster_id', eval_func=operator.contains,
            limit=BaseFilter.parse_as_set(
                MonUtils.get_monster_id, 'monsters', data))

        # Exclude Monsters - f.monster_ids not contains m.ex_mon_id
        self.exclude_monster_ids = self.evaluate_attribute(  #
            event_attribute='monster_id',
            eval_func=lambda d, v: not operator.contains(d, v),
            limit=BaseFilter.parse_as_set(
                MonUtils.get_monster_id, 'monsters_exclude', data))

        # Distance
        self.min_dist = self.evaluate_attribute(  # f.min_dist <= m.distance
            event_attribute='distance', eval_func=operator.le,
            limit=BaseFilter.parse_as_type(float, 'min_dist', data))
        self.max_dist = self.evaluate_attribute(  # f.max_dist <= m.distance
            event_attribute='distance', eval_func=operator.ge,
            limit=BaseFilter.parse_as_type(float, 'max_dist', data))

        # Quest Description
        self.quest_contains = self.evaluate_attribute(  # f.gn matches e.gn
            event_attribute='quest', eval_func=GymUtils.match_regex_dict,
            limit=BaseFilter.parse_as_set(
                GymUtils.create_regex, 'quest_contains', data))
        self.quest_excludes = self.evaluate_attribute(  # f.gn no-match e.gn
            event_attribute='quest',
            eval_func=GymUtils.not_match_regex_dict,
            limit=BaseFilter.parse_as_set(
                GymUtils.create_regex, 'quest_excludes', data))

        # Reward Description
        self.reward_contains = self.evaluate_attribute(  # f.gn matches e.gn
            event_attribute='rewardstring', eval_func=GymUtils.match_regex_dict,
            limit=BaseFilter.parse_as_set(
                GymUtils.create_regex, 'reward_contains', data))
        self.reward_excludes = self.evaluate_attribute(  # f.gn no-match e.gn
            event_attribute='rewardstring',
            eval_func=GymUtils.not_match_regex_dict,
            limit=BaseFilter.parse_as_set(
                GymUtils.create_regex, 'reward_excludes', data))

        self.quest_types = self.evaluate_attribute(
            event_attribute='quest_type', eval_func=operator.contains,
            limit=BaseFilter.parse_as_set(QuestUtils.get_quest_type, 'quest_types', data)
        )
		
        self.reward_types = self.evaluate_attribute(
            event_attribute='reward_type', eval_func=operator.contains,
            limit=BaseFilter.parse_as_set(QuestUtils.get_reward_type, 'reward_types', data)
        )

        self.item_types = self.evaluate_attribute(
            event_attribute='item_type', eval_func=operator.contains,
            limit=BaseFilter.parse_as_set(QuestUtils.get_item_type, 'item_types', data)
        )
		
        self.condition_types = self.evaluate_attribute(
            event_attribute='condition_type', eval_func=operator.contains,
            limit=BaseFilter.parse_as_set(QuestUtils.get_condition_type, 'condition_types', data)
        )
		
        self.throw_types = self.evaluate_attribute(
            event_attribute='throw_type', eval_func=operator.contains,
            limit=BaseFilter.parse_as_set(QuestUtils.get_throw_type, 'throw_types', data)
        )
		
        self.pokemon_types = self.evaluate_attribute(
            event_attribute='pokemon_type', eval_func=operator.contains,
            limit=BaseFilter.parse_as_set(QuestUtils.get_pokemon_type, 'pokemon_types', data)
        )

        # Geofences
        self.geofences = BaseFilter.parse_as_list(str, 'geofences', data)

        # Custom DTS
        self.custom_dts = BaseFilter.parse_as_dict(
            str, str, 'custom_dts', data)

        # Missing Info
        self.is_missing_info = BaseFilter.parse_as_type(
            bool, 'is_missing_info', data)

        # Reject leftover parameters
        for key in data:
            raise ValueError("'{}' is not a recognized parameter for"
                             " Quest filters".format(key))

    def to_dict(self):
        """ Create a dict representation of this Filter. """
        settings = {}

        if self.monster_ids is not None:
            settings['pokemon_ids'] = self.monster_ids 
			
        # Distance
        if self.min_dist is not None:
            settings['min_dist'] = self.min_dist
        if self.max_dist is not None:
            settings['max_dist'] = self.max_dist

        # Geofences
        if self.geofences is not None:
            settings['geofences'] = self.geofences
			
        # Geofences
        if self.item_types is not None:
            settings['item_types'] = self.item_types

        # Missing Info
        if self.is_missing_info is not None:
            settings['missing_info'] = self.is_missing_info

        return settings
