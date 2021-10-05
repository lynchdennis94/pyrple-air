"""
Main entry point to the pyrpleair library. The official API definitions can be found at https://api.purpleair.com.
"""

import requests

class PyrpleAir:
    __check_api_endpoint = "https://api.purpleair.com/v1/keys"
    __get_sensor_data_endpoint = "https://api.purpleair.com/v1/sensors/{}"
    __get_sensors_data_endpoint = "https://api.purpleair.com/v1/sensors"

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
        response = requests.get(self.__check_api_endpoint, headers=header)
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

        response = requests.get(self.__get_sensor_data_endpoint.format(sensor_index), headers=header, params=parameters)
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

        response = requests.get(self.__get_sensors_data_endpoint, headers=header, params=parameters)
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


