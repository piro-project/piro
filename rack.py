#!/usr/bin/python3
import board
import busio
import digitalio
import time
import random
from logzero import logger
from adafruit_mcp230xx.mcp23017 import MCP23017
from multiprocessing import Process


class rack:

    def __init__(self, rack_address = 0x20, rack_size = 16, fire_state = False, descriptions = None):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.address = rack_address
        try:
            self.mcp = MCP23017(self.i2c, address=rack_address)
        except ValueError:
            logger.error("Unable to create rack, no device at address.")
            self.mcp = None
        self.rack_size = rack_size                              # How many channels does the rack have? Default = 16
        self.fire_state = fire_state                                 # What state is used to fire the channel?  Use False for active low relays
        self.channels = []                                      # Store the connections to the rack
        self.channels_fired = []                                # Keep track if it's been fired
        self.map = [8, 0, 9, 1, 10, 2, 11, 3, 12, 4, 13, 5, 14, 6, 15, 7]
        self.descriptions = []
        if descriptions:
            for item in descriptions:
                self.descriptions.append(item)
        if self.mcp:
            self.initializeChannels()


    def initializeChannels(self):
        self.channels = []  
        for channel in range(0, self.rack_size):
            logger.debug("Initializing Channel " + str(channel))
            pin = self.mcp.get_pin(channel)
            pin.direction = digitalio.Direction.OUTPUT
            pin.value = not self.fire_state 
            self.channels.append(pin)
            logger.debug("Done!")
            self.channels_fired.append(False)


    def check_rack(self):
        """Return an array of status by channel."""
        return self.channels_fired

    def status(self):
        status = {}
        status['channels'] = [] 
        for i in range(0, self.rack_size):
            mychannel = {}
            mychannel["id"] = i
            mychannel["fired"] = self.channels_fired[i]
            mychannel["description"] = self.descriptions[i]
            status['channels'].append(mychannel)
        # status['channels_fired'] = self.channels_fired
        status['rack_size'] = self.rack_size
        status['address'] = self.address
        status['fire_state'] = self.fire_state
        return status

    def mark_fired(self, channel):
        self.channels_fired[channel] = True

    def all_fired(self):
        """If we don't have any channels that say false, return true."""
        if False in self.channels_fired:
            return False
        else:
            return True
# FIRING

    def fire_channel_thread(self, channel, fire_time = 5):
        p = Process(target=self.fire_channel, args=(channel, fire_time))
        p.daemon = True
        p.start()
        self.mark_fired(channel)
        return channel

    def fire_channel(self, channel, fire_time = 5):
        if not self.channels_fired[channel]:
            if len(self.descriptions) > 0:
                logger.info("Firing {}".format(self.descriptions[channel]))
            else:
                logger.info("Firing channel {}".format(channel))
            self.channels[self.map[channel]].value = self.fire_state
            logger.info("Activating for {} seconds".format(fire_time))
            time.sleep(fire_time)
            self.channels[self.map[channel]].value = not self.fire_state
            # self.channels_fired[channel] = True
            logger.debug("Finished!")
        else:
            logger.warning("Can't fire channel {}, it's already been fired.".format(channel))

    def fire_random(self, fire_time = 5):
        if self.all_fired():
            logger.error("Unable to find an unfired channel")
            return False
        while True:
            channel = random.randrange(self.rack_size)
            if not self.channels_fired[channel]:
                break
        p = Process(target=self.fire_channel, args=(channel, fire_time))
        p.daemon = True
        p.start()
        self.mark_fired(channel)
        return channel
        

# RESETS

    def reset_channel(self, channel):
        """ Reset the fired state of a channel."""
        self.channels_fired[channel] = False

    def reset_all_channels(self):
        """ Reset the fired state of all channels on the rack."""
        for channel in range(0,self.rack_size):
            self.reset_channel(channel)