FORMCHAR = "w"
TABLECHAR = "o"

FORM = '''
.----------------> Weather <----------------------------------------------------------.
|   Current: w1wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww w2wwwwwwwwwwwwwwwwww |
'--------------------------------------------------.----------------------------------'
| Conditions       : w3wwwwwwwwwwwwwwwwwwwwwwwwwww | Temperature  : w5wwwww w6wwwwwww |
| Wind Speed       : w4wwwwwwwwwwwwwwwwwwwwwwwwwww | Dew Point    : w7wwwww w8wwwwwww |
| Chance of Rain   : w9wwwww                       |                                  |
| Relative Humidity: w10wwww                       | Visibility   : w43wwwwwww        |
| Actual Humidity  : w42wwww                       | Air Pressure : w44wwwwwww        |
'--------------------------------------------------'----------------------------------'
| w11wwwwwwwwwwwwwwwwwwwww                                           w13wwww w14wwwww |
|   w12wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww |
'-------------------------------------------------------------------------------------'
| w15wwwwwwwwwwwwwwwwwwwww                                           w17wwww w18wwwww |
|   w16wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww |
'-------------------------------------------------------------------------------------'
| w30wwwwwwwwwwwwwwwwwwwww                                           w32wwww w33wwwww |
|   w31wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww |
'-------------------------------------------------------------------------------------'
| w34wwwwwwwwwwwwwwwwwwwww                                           w36wwww w37wwwww |
|   w35wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww |
'-------------------------------------------------------------------------------------'
| w38wwwwwwwwwwwwwwwwwwwww                                           w40wwww w41wwwww |
|   w39wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww |
'-----------------------------------.-------------------------------------------------'
| Sun Information                   |                                                 |
|                                   | Day Length   : w22wwwwwwwww                     |
| Sunrise        : w19wwwwwwwww     | Distance     : w47wwwwwwwwwwwwwwwwwwww          |
| Sunrise Angle  : w45wwwwwwwww     | Sun Angle    : w48wwwwwwwww                     |
| Noon           : w20wwwwwwwww     | Sun Altitude : w49wwwwwwwww                     |
| Sunset         : w21wwwwwwwww     | Next w51wwwww: w50wwwwwwwwwwwwwwwwwwwwwwwwwwwww |
| Sunrise Angle  : w46wwwwwwwww     |                                                 |
'-----------------------------------'-------------------------------------------------'
| Moon Information                  |  Phase          : w26wwwwwwwwwwwwwwwwww         |
|                                   |  Distance       : w27wwwwwwwwwwwwwwwwww         |
|    Moon        : w23wwwwwwwwwwww  |  Illumination   : w28wwwwwwwwwwwwwww            |
|    Age         : w24wwwwwwwwwwww  |  Next New Moon  : w52wwwwwwwwwwwwwwwwww         |
|    Angle       : w25wwwwwwwwwwww  |  Next Full Moon : w53wwwwwwwwwwwwwwwwww         |
'-----------------------------------'-----------------.-------------------------------'
|  Snapshot: w29wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww |
'-----------------------------------------------------'
'''