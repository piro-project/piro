import rack
import yaml
import random
from logzero import logger

class rackset:

    def __init__(self):
        self.rack_array = [] #create an empty set of racks

    def add_rack(self, rack_address = 0x20, rack_size = 16, fire_state = False):
        """Add a new rack to the rackset."""
        self.rack_array.append(rack.rack(rack_address, rack_size, fire_state))

    def add_rack_from_config(self,config):
        # Setup rack address
        if 'rack_address' in config:
            rack_address = config['rack_address']
        else:
            rack_address = False

        # Setup rack size
        if 'rack_size' in config:
            rack_size = config['rack_size']
        elif 'descriptions' in config:
            rack_size = len(config['descriptions'])
        else:
            rack_size = 16

        # Setup fire state
        if 'fire_state' in config:
            fire_state = config['fire_state']
        else:
            fire_state = False
        
        # Setup channels
        if 'descriptions' in config:
            channels = config['descriptions']
        else:
            channels = False

        self.rack_array.append(rack.rack(rack_address, rack_size, fire_state, channels))

    def load_racks_from_file(self, filename):
        a_yaml_file = open(filename)
        config = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
        for rack in config['racks']:
            self.add_rack_from_config(rack)

    def status(self):
        status = []
        for i in range(0,self.size()):
            status.append(self.rack_array[i].status())
        return status

    def fire_list(self):
        mylist = []
        mylist.append("http://piro:5000/rackset/fire/random" )
        for i in range(0,self.size()):
            for j in range(0, self.rack_array[i].rack_size):
                mylist.append("http://piro:5000/rackset/fire/" + str(i) + "/" + str(j) )
        return mylist

    def size(self):
        return len(self.rack_array)

    def all_fired(self):
        status = True
        for rack in range(0,self.size()):
            if not self.rack_array[rack].all_fired():
                status = False
                return status
        return status


    def fire_channel(self, rack, channel, fire_time = 5):
        return self.rack_array[rack].fire_channel_thread(channel, fire_time)
    
    def fire_random(self, fire_channel = 5):
        if self.all_fired():
            logger.error("Can't fire, no unfired channels available")
            return False
        while True:
            rack = random.randrange(self.size())
            if not self.rack_array[rack].all_fired():
                break
        fired_channel = self.rack_array[rack].fire_random(fire_channel)
        return rack, fired_channel
        
    def reset(self):
        for rack in range(0,self.size()):
            self.rack_array[rack].reset_all_channels()
