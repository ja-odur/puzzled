import json
import os
from decouple import config

from backend.lib import first

# A local configuration file name
LOCAL_CONFIG_FILE_NAME = '.config.json'


class JsonConfigParseError(Exception):
    pass


class SettingsVector(dict):
    @classmethod
    def make_vector(cls, **kwargs):
        """
        This method returns a vector with all nested dicts converted to vectors too. This creates
        a vector which contains other vectors containing vectors ad-nauseum down into the
        depths of hell.
        """
        output = dict(**kwargs)
        for k, v in kwargs.items():
            if isinstance(v, dict):
                output[k] = cls.make_vector(**v)

        return cls(**output)

    def get_by_path(self, path, default_value=None, return_type=None):
        """
        This method returns a path from the vector assuming that this vector
        contains other vectors containing vectors ad-nauseum down into the
        depths of hell.

        For example, to get the value found at vector['key1']['key2']['key3']
        you would use the path key1.key2.key3 to locate the value.

        If the path does not exist or reaches a value in the path that is not a
        vector, it returns the default_value as the return.

        :param path: The path to the value you want.  Each item should be
                     separated by a '.'.

        :param default_value: The default value you want returned if your path
                              leads to nothing. Defaults to None.

        :param return_type: The built-in value type to return.  Useful when you need
                            a boolean, integer, or long.  Defaults to whatever the JSON
                            parser found.

        :return: The value found at the path or the default value.
        """
        output = default_value

        if path is None:
            return output

        # Split the path by '.' so that we can follow it
        path_items = path.split('.')

        # Take the first item and remove it, we'll use the remaining items
        # late
        path_item = path_items.pop(0)

        # Get the value from ourselves of the first item.  We're not asking for
        # the default_value back as the default of this call because logic
        # would go wonky if someone gave a default_value that was a vector,
        # honestly.
        value = self.get(path_item, None)

        if value is None:
            # We got nothing back, so we're just returning the default value.
            return default_value

        if len(path_items) == 0:
            # We arrived at the end of the path.  We either got a value or the
            # default value from the previous call, so we'll just live go with
            # it.
            return value

        # Ok, we have items left in the path.  We can only continue if we
        # have another vector.
        if not isinstance(value, SettingsVector):
            # We traversed part of the path but hit a non-vector where we
            # would have expected one.  We'll just return the default
            # value.
            return default_value

        # If we got here, we have path items left AND we have a vector we
        # can recurse down with the rest of the path items.
        output = value.get_by_path('.'.join(path_items), default_value)
        #
        # if output and return_type and not isinstance(output, return_type):
        #     # We definitely need to do a type conversion.  The question is, how is the best
        #     # way to go about this?
        #     output = convert_value(output, return_type)

        return output


def load_json_settings():
    """
    This method is responsible for finding a JSON-based settings file and
    loading it into a nice Mash that we can then use to get values from. This
    method is critical to the new settings.py logic an the configuration of our
    application.

    The logic decides on the best configuration file to use by looking for it
    in the following locations:

        1. Path specified by OS environment variable called
           'DYNAMIC_CONFIGURATION_FILE'
        2. The root of the project in a file called .config.json

    Once a file is found it is loaded and returned.
    :return: dict
    """
    potential_locations = [
        config('DYNAMIC_CONFIGURATION_FILE', None),
        os.path.join(os.getcwd(), LOCAL_CONFIG_FILE_NAME),
    ]

    # Weed out any None values, if they exist.  No reason to even check, nor
    # show it in error messages later.
    potential_locations = [pl for pl in potential_locations if pl is not None]

    # Use a clever little bit of lambda logic to find the first one we like.
    file_location = first(potential_locations, key=lambda x: os.path.exists(x))

    # Print out an error that we can't find the file anywhere.  We aren't going
    # to throw an exception, because we hope that the default settings are
    # enough.
    if file_location is None:
        print('Unable to find a JSON settings file.')
        print('Please set DYNAMIC_CONFIGURATION_FILE to a valid path or place '
              'the configuration file at one of the following locations:')
        for location in potential_locations:
            print(' * {}'.format(location))
        print('This error is most likely popping up because you don\'t have a local config file.')

        # create an empty vector and exit out.
        return SettingsVector()

    # Ok, we have a file location, lets see if we can load it and parse it.
    try:
        with open(file_location) as file_handle:
            output = json.load(file_handle)

    except Exception as e:
        # Just re-raise this so that we have intelligent error information for
        # the developer that screwed up somewhere.
        raise JsonConfigParseError('Unable to load and parse file at {}: {}'.format(file_location, e.message))

    return SettingsVector.make_vector(**output)


settings_vector = load_json_settings()
