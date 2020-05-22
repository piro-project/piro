#!/usr/bin/python3
import board
import busio
import digitalio
import time
import random
from logzero import logger
from adafruit_mcp230xx.mcp23017 import MCP23017

class rack:

    def __init__(self, rack_address = 0x20, rack_size = 16, fire_state = False):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.mcp = MCP23017(self.i2c, address=rack_address)
        self.rack_size = rack_size                              # How many channels does the rack have? Default = 16
        self.fire_state = False                                 # What state is used to fire the channel?  Use False for active low relays
        self.channels = []                                      # Store the connections to the rack
        self.channels_fired = []                                # Keep track if it's been fired
        

        for channel in range(0, self.rack_size):
            logger.debug("Initializing Channel " + str(channel))
            pin = self.mcp.get_pin(channel)
            pin.direction = digitalio.Direction.OUTPUT
            pin.value = True
            self.channels.append(pin)
            logger.debug("Done!")
            self.channels_fired.append(False)

    def check_rack(self):
        """Return an array of status by channel."""
        # status = []
        # for channel in range(0, self.rack_size):
        #     status.append({ 'channel_name': 'channel ' + str(channel),
        #                     'channel_number': channel,
        #                     'channel_status': self.channels[channel].value
        #     })
        # return status
        return self.channels_fired

# FIRING

    def fire_channel(self, channel, fire_time = 5):
        if not self.channels_fired[channel]:
            logger.debug("Firing channel {}".format(channel))
            self.channels[channel] = self.fire_state
            logger.debug("Activating for {} seconds".format(fire_time))
            time.sleep(fire_time)
            self.channels[channel] = not self.fire_state
            self.channels_fired[channel] = True
            logger.debug("Finished!")
        else:
            logger.warning("Can't fire channel {}, it's already been fired.".format(channel))

    def fire_random(self, fire_time = 5):
        while True:
            channel = random.randrange(self.rack_size)
            if not self.channels_fired[channel]:
                break
        self.fire_channel(channel)
        

# RESETS

    def reset_channel(self, channel):
        """ Reset the fired state of a channel."""
        self.channels_fired[channel] = False

    def reset_all_channels(self):
        """ Reset the fired state of all channels on the rack."""
        for channel in range(0,self.rack_size):
            self.reset_channel(channel)