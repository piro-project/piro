import rack
import logging
import logzero
from logzero import logger

# logzero.loglevel(logging.INFO)
rack1 = rack.rack(0x21)

logger.info(rack1.check_rack())
rack1.fire_channel(2,0.5)
logger.info(rack1.check_rack())
rack1.fire_channel(2)
rack1.reset_all_channels()
rack1.fire_channel(2,0.5)
rack1.fire_random()
rack1.fire_random()
rack1.fire_random()
rack1.fire_random()
rack1.fire_random()
logger.info(rack1.check_rack())