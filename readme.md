# Piro
## What is it?
Piro is an open source raspberry pi fireworks controller.  I created Piro primarily because I like allowing my kids to (safely) set the fireworks off.  

Initially Piro is based around using the i2c bus to connect to MCP23017 chips to expand the GPIO and provide 5V TTL for the relay board.  Using the Pi's native GPIO would require logic level shifting for the cheap 5v relay boards you can get from ebay/aliexpress.

## Config file
### Maps
The Map allows you to set which pin is activated for which logical channel.  You could accomplish the same thing by connecting your pins in a different order, but this allows for flat ribbon cables to be used and is easier to change later.

The MCP23017's pins are laid out in this order:
| Row 1 | Row 2 |
| ----- | ----- |
| 0     | 8     |
| 1     | 9     |
| 2     | 10    |
| 3     | 11    |
| 4     | 12    |
| 5     | 13    |
| 6     | 14    |
| 7     | 15    |

But the 16 channel relay's pins are laid out like this:
| Row 1 | Row 2 |
| ----- | ----- |
| 0     | 1     |
| 2     | 3     |
| 4     | 5     |
| 6     | 7     |
| 8     | 9     |
| 10    | 11    |
| 12    | 13    |
| 14    | 15    |

#### Example maps
These are all specific to the hardware I used, your milage may vary:
In Relay board order: [8, 0, 9, 1, 10, 2, 11, 3, 12, 4, 13, 5, 14, 6, 15, 7]
Reverse second half : [8, 0, 9, 1, 10, 2, 11, 3,  7, 15, 6, 14, 5, 13, 4, 12]
Twelve tubes + 4 misc on bottom: [8, 0, 9, 1, 10, 2, 7, 15, 6, 14, 5, 13, 11, 3, 4, 12]