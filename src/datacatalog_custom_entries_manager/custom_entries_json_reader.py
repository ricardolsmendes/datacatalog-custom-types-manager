import json
import logging
from typing import Dict, List

from . import constant


class CustomEntriesJSONReader:

    @classmethod
    def read_file(cls, file_path: str) -> List[Dict[str, object]]:
        """
        Read Custom Entries from a JSON file.

        :param file_path: The JSON file path.
        :return: A list with the Custom Entries assembled by their parent Groups.
        """
        logging.info('')
        logging.info('>> Reading the JSON file: %s...', file_path)

        with open(file_path) as json_file:
            json_data = json.load(json_file)

        return cls.__make_entry_groups_from_system_indexed_data(json_data)

    @classmethod
    def __make_entry_groups_from_system_indexed_data(cls, json_object: Dict[str, object]) \
            -> List[Dict[str, object]]:

        systems_json = json_object.get(constant.ENTRIES_JSON_USER_SPECIFIED_SYSTEMS_FIELD_NAME)

        entry_groups = []
        for system_json in systems_json:
            entry_groups.extend(cls.__make_entry_groups_from_system(system_json))
        return entry_groups

    @classmethod
    def __make_entry_groups_from_system(cls, json_object: Dict[str, object]) \
            -> List[Dict[str, object]]:

        system_name = json_object.get(constant.ENTRIES_JSON_USER_SPECIFIED_SYSTEM_FIELD_NAME)
        groups_json = json_object.get(constant.ENTRIES_JSON_ENTRY_GROUPS_FIELD_NAME)
        return [cls.__make_entry_group(group_json, system_name) for group_json in groups_json]

    @classmethod
    def __make_entry_group(cls, json_object: Dict[str, object], system_name: str) \
            -> Dict[str, object]:

        entries_json = json_object.get(constant.ENTRIES_JSON_ENTRIES_FIELD_NAME)
        return {
            'id': json_object.get(constant.ENTRIES_JSON_ENTRY_GROUP_ID_FIELD_NAME),
            'name': json_object.get(constant.ENTRIES_JSON_ENTRY_GROUP_NAME_FIELD_NAME),
            'entries': cls.__make_entries(entries_json, system_name)
        }

    @classmethod
    def __make_entries(cls, json_array: List[Dict[str, str]], system_name: str) \
            -> List[Dict[str, str]]:

        return [cls.__make_entry(json_object, system_name) for json_object in json_array]

    @classmethod
    def __make_entry(cls, json_object: Dict[str, str], system_name: str) -> Dict[str, str]:
        return {
            'linked_resource': json_object.get(constant.ENTRIES_JSON_LINKED_RESOURCE_FIELD_NAME),
            'display_name': json_object.get(constant.ENTRIES_JSON_DISPLAY_NAME_FIELD_NAME),
            'description': json_object.get(constant.ENTRIES_JSON_DESCRIPTION_FIELD_NAME, ''),
            'user_specified_type': json_object.get(
                constant.ENTRIES_JSON_USER_SPECIFIED_TYPE_FIELD_NAME),
            'user_specified_system': system_name,
            'created_at': json_object.get(constant.ENTRIES_JSON_CREATED_AT_FIELD_NAME),
            'updated_at': json_object.get(constant.ENTRIES_JSON_UPDATED_AT_FIELD_NAME),
        }
