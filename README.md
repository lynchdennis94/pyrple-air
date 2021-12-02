# pyrple-air
An unofficial python library to interface with the PurpleAir API

# About
pyrpleair is an unofficial library used to interface with the PurpleAir API, as defined at https://api.purpleair.com .
The library is intended to provide an easy interface for the official API without having to re-implement basic features 
(such as parsing optional API arguments, defining the endpoints, handling RESTful calls, etc...). 

# Requirements
The following libraries are imported, and must be present for the pyrpleair library to function as expected:
* requests

# How to use
After importing the pyrpleair library into your project, create an instance of the PyrpleAir class and define the read 
and write keys for your project (these keys are provided via Purple Air, and are required to interface with the API - 
the library will not work without these keys).

An example snippet, which can be used to validate your keys through the library, would be:
```buildoutcfg
from pyrpleair import PyrpleAir

read_key = "ABC12345"
write_key = "DEF12345"
pyrpleair_instance = PyrpleAir(read_key=read_key, write_key=write_key)
pyrpleair_instance.check_api_key(pyrpleair_instance.read_key) #Validates the read key
pyrpleair_instance.check_api_key(pyrpleair_instance.write_key) #Validates the write key
```

# Supported Endpoints
* validate api keys using `check_api_key`
* get data for a specific sensor using `get_sensor_data`
* get data for a group of sensors using `get_sensors_data`
* create and delete groups and members
* get group and member data and lists