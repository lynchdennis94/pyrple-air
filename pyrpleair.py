"""
Main entry point to the pyrpleair library. The official API definitions can be found at https://api.purpleair.com.
"""

import requests

class PyrpleAir:
    __api_base = "https://api.purpleair.com/"
    __api_version = "v1"    
    __api_endpoint = {
        "keys": __api_base + __api_version + "/keys", 
        "sensors": __api_base + __api_version + "/sensors",
        "sensor": __api_base + __api_version + "/sensors/{sensor_index}",
        "groups": __api_base + __api_version + "/groups",
        "group":  __api_base + __api_version + "/groups/{group_id}",
        "groups_members": __api_base + __api_version + "/groups/{group_id}/members",
        "group_member": __api_base + __api_version + "/groups/{group_id}/members/{member_id}"        
    }
    
    def __init__(self, read_key=None, write_key=None):
        """
        Sets up a hook to interface with the Purple Air api

        :param read_key: the read key provided by PurpleAir
        :param write_key: the write key provided by PurpleAir
        """
        
        if not (read_key or write_key):
            raise ValueError(
                "You need to specify at least one API key. " + 
                "You can email contact@purpleair.com to obtain one."
            )
        
        self.read_key = read_key
        self.write_key = write_key

    def check_api_key(self, key):
        """
        Validates an input key and returns the key type

        :param key: the key to validate
        :return: the api response tuple (status_code, response_content)
        """
        header = {'X-API-Key': key}
        response = requests.get(self.__api_endpoint["keys"], headers=header)
        return response.status_code, response.json()

    def get_sensor_data(self, sensor_index, read_key=None, fields=None, cf=None):
        """
        Returns sensor data for an individual sensor based on the input sensor index

        :param sensor_index: the id of the specific sensor being queried
        :param read_key: a sensor-specific api key for private devices
        :param fields: a comma-delimited list of specific fields to return in the response
        :param cf: a float override used when using the pm2.5_alt field
        :return: the api response tuple (status_code, response_content)
        """

        header = {'X-API-Key': self.read_key}
        parameters = {}
        self.__add_optional_args_to_payload(parameters, locals(), ['sensor_index'])

        response = requests.get(self.__api_endpoint["sensor"].format(sensor_index=sensor_index), headers=header, params=parameters)
        return response.status_code, response.json()

    def get_sensors_data(self, fields, cf=None, location_type=None, read_keys=None, show_only=None, modified_since=None,
                         max_age=None, nwlng=None, nwlat=None, selng=None, selat=None):
        """
        Returns sensor data for a list of sensors, based on the input arguments that filter out specific sensors

        :param fields: a comma-delimited list of specific fields to return in teh response
        :param cf: a float override used when using the pm2.5_alt field
        :param location_type: the location type for sensors (0=Outside, 1=Inside)
        :param read_keys: distinct read keys used for private devices - can be comma-delimited if multiple keys are used
        :param show_only: A comma-separated list of sensor_index values, limiting results to the specified sensors
        :param modified_since: Excludes results for sensors which were last modified BEFORE the specificed modified since timestamp
        :param max_age: filters results to only include sensors updated within the last number of seconds (default of 604800)
        :param nwlng: A northwest longitude coordinate for providing a bounding box to geographically bound sensors
        :param nwlat: A northwest latitude coordinate for providing a bounding box to geographically bound sensors
        :param selng: A southeast longitude coordinate for providing a bounding box to geographically bound sensors
        :param selat: A southeast latitude coordinate for providing a bounding box to geographically bound sensors
        :return: the API response tuple (status code, response_content)
        """
        header = {'X-API-Key': self.read_key}
        parameters = {'fields': fields}

        self.__add_optional_args_to_payload(parameters, locals(), ['fields'])

        response = requests.get(self.__api_endpoint["sensors"], headers=header, params=parameters)
        return response.status_code, response.json()
    
    def create_group(self, name):
        """
        Create a new group which is a collection of individual sensor members.
        
        :param name: name of the group to create (can contain spaces)
        :return: the API response tuple (status code, response_content)        
        """
        header = {'X-API-Key': self.write_key}        
        parameters = {'name': name}
        
        response = requests.post(self.__api_endpoint["groups"], headers=header, params=parameters)
        return response.status_code, response.json()
                
    def delete_group(self, group_id):
        """
        Deletes the group specified by `group_id`
        
        :param group_id: The group_id of the requested group. This group must be owned by `self.read_key`
        :return: the API response tuple (status code, response_content) - returns 204 on success"""
        
        header = {'X-API-Key': self.write_key}     
        parameters = {"group_id": group_id}   
        
        response = requests.delete(self.__api_endpoint["group"].format(group_id=group_id), headers=header)
        return response.status_code, response.text
        
    def add_group_member(self, group_id, sensor_id=None, sensor_index=None, owner_email=None, location_type=None):
        """
        Adds a certain sensor to a group by creating a new group member
        
        :param group_id: The group_id of the requested group. This group must be owned by `self.read_key`
        :param sensor_id: The `sensor_id` of the new member sensor from the device label
        :param sensor_index: The `sensor_index` from the web UI or `get_sensors_data()`
        :param owner_email: Address that matches the owner email set during device registration
        :param location_type: 0 = outside, 1 = inside 
        
        Public sensors can be added by either sensor_id or sensor_index
        Private sensors must be added by specifying sensor_id, owner_email, and optionally location_type (if present during registration).        
        """
        header = {'X-API-Key': self.write_key}
        parameters = {'group_id': group_id}

        self.__add_optional_args_to_payload(parameters, locals(), ['group_id'])

        response = requests.post(self.__api_endpoint["groups_members"].format(group_id=group_id), headers=header, params=parameters)
        return response.status_code, response.json()
        
    def delete_group_member(self, group_id, member_id):
        """
        Removes a member (sensor) from a group 
        
        :param group_id: The group_id of the requested group. This group must be owned by `self.read_key`
        :param member_id: The member_id of the sensor in the group - unique per group and not the sensor ID
        :return: the API response tuple (status code, response_content) - returns 204 on success        
        """            
        header = {'X-API-Key': self.write_key}     
        parameters = {"group_id": group_id, "member_id": member_id}   
        
        response = requests.delete(self.__api_endpoint["group_member"].format(group_id=group_id, member_id=member_id), headers=header)
        return response.status_code, response.text
     
    def get_group_info(self, group_id):
        """
        Returns a list of all members contained in `group_id`
        
        :param group_id The group_id of the requested group. This group must be owned by `self.read_key`
        :return: the API response tuple (status code, response_content)        
        """
        header = {'X-API-Key': self.read_key}
        response = requests.get(self.__api_endpoint["group"].format(group_id=group_id), headers=header)
        return response.status_code, response.json()
    
    def get_owned_groups(self):
        """
        Returns a list of all the groups owned by `self.read_key`
        
        :return: the API response tuple (status code, response_content)        
        """
        header = {'X-API-Key': self.read_key}
        response = requests.get(self.__api_endpoint["groups"], headers=header)
        return response.status_code, response.json()
        
        
    def get_group_sensors_data(self, group_id, fields, cf=None, location_type=None, read_keys=None, show_only=None, modified_since=None,
                         max_age=None, nwlng=None, nwlat=None, selng=None, selat=None):

        """
        Returns sensor data for a predetermined list of sensors contained by a specific `group_id`. Returned data is 
        similar to `get_sensors_data()`

        :param group_id The group_id of the requested group
        :param fields: a comma-delimited list of specific fields to return in the response
        :param cf: a float override used when using the pm2.5_alt field
        :param location_type: the location type for sensors (0=Outside, 1=Inside)
        :param read_keys: distinct read keys used for private devices - can be comma-delimited if multiple keys are used
        :param show_only: A comma-separated list of sensor_index values, limiting results to the specified sensors
        :param modified_since: Excludes results for sensors which were last modified BEFORE the specificed modified since timestamp
        :param max_age: filters results to only include sensors updated within the last number of seconds (default of 604800)
        :param nwlng: A northwest longitude coordinate for providing a bounding box to geographically bound sensors
        :param nwlat: A northwest latitude coordinate for providing a bounding box to geographically bound sensors
        :param selng: A southeast longitude coordinate for providing a bounding box to geographically bound sensors
        :param selat: A southeast latitude coordinate for providing a bounding box to geographically bound sensors
        :return: the API response tuple (status code, response_content)
        """
        header = {'X-API-Key': self.read_key}
        parameters = {'fields': fields}

        self.__add_optional_args_to_payload(parameters, locals(), ['fields'])

        response = requests.get(self.__api_endpoint["groups_members"].format(group_id=group_id), headers=header, params=parameters)
        return response.status_code, response.json()


    @staticmethod
    def __add_optional_args_to_payload(parameters, input_args, args_to_skip):
        """
        Takes in the parameter payload (a dict), the input args to a function, and the name of args to skip, and adds all
        input args to the parameters payload if they aren't intentionally skipped and were defined with a 'non-None' value

        :param parameters: the parameters payload
        :param input_args: the list of all input args to any given function
        :param args_to_skip: a list of args to skip adding to the payload
        """
        args_to_skip.extend(['self', 'header', 'parameters']) # May be present in inputs, but should never be added
        if input_args is not None and len(input_args) > 0:
            for input_arg_name in input_args:
                if input_arg_name not in args_to_skip:
                    input_arg_value = input_args[input_arg_name]
                    if input_arg_value is not None:
                        parameters[input_arg_name] = input_arg_value