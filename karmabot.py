import json
import os.path

class Karma(object):
    def __init__(self, file_name):
        self.file_name = file_name
        
        # If there are no such file then make a new one.
        if not os.path.isfile(self.file_name):
            f = open(self.file_name, "w")
            f.write("{}")
            f.close()

        # Open for read mode.
        self.file = open(self.file_name, "r+")
        self.karma_dict = json.load(self.file)

        # Alias: in the format of {"OG" : ["alias_1", "alias_2"], ...}
        self.alias_dict = {}

    def create_new_entry(self, entry):
        """ Create a new karma entry. If it already exists, do nothing. """
        if entry not in self.karma_dict:
            self.karma_dict[entry] = 0
            # Create a new alias entry for it.
            self.alias_dict[entry] = []
            
    def increment(self, entry):
        """ Increment the karma of the given entry value
            entry: string
        """
        entry = entry.lower()
        if entry in self.karma_dict:
            self.karma_dict[entry] += 1
        else:
            self.create_new_entry(entry)
            self.karma_dict[entry] = 1

    def decrement(self, entry):
        """ Same as increment, except decrement. """
        entry = entry.lower()
        if entry in self.karma_dict:
            self.karma_dict[entry] -= 1
        else:
            self.create_new_entry(entry)
            self.karma_dict[entry] = -1

    def read(self, entry):
        """ Return karma value of the specified entry as an int. """
        entry = entry.lower()
        if entry in self.karma_dict:
            return self.karma_dict[entry]
        else:
            return 0

    def dump(self):
        """ Write the dictionary into a json file. """
        self.file.seek(0)
        self.file.truncate()
        json.dump(self.karma_dict, self.file)

    def close(self):
        """ Close the file """
        self.dump()
        self.file.close()

    def removeEntry(self, entry):
        """ Remove an entry from the dictionary"""
        if entry in self.karma_dict:
            del self.karma_dict[entry]

##    def add_alias(self, new, to_original):
##        """ Add a new alias to the given original. If the original is an alias,
##                add it its original.
##            Return False if alias exist but points to an entirely different original.
##        """
##        # Used for checking if alias already have an original
##        check_original = get_original(new)  
##        
##        # Alias doesn't exist yet.
##        if check_original == False:
##            # The original alias doesn't exist either.
##            if get_original(to_original) == False:
##                self.alias_dict[to_original] = [new]
##            # The original alias exists.
##            self.alias_dict[get_original(to_original)].append(new)
##        # Alias already exists
##        else:
##            # If the alias is already in a completely different alias branch.
##            if check_original != get_original(to_original):
##                return False
##            
##        return True

    def get_original(self, entry):
        """ Check if the given entry exists and return the original if it is an alias
                or itself if it is an original.
            Return false if no alias exists.
        """
        entry = entry.lower()
        # Entry is an original.
        if entry in self.alias_dict:
            return entry
        # Entry exists as an alias.
        for key, value in self.alias_dict.iteritems():
            if entry in value:
                return key
        # If entry doesn't exist.
        return False
        

karma = Karma("karma.json")
