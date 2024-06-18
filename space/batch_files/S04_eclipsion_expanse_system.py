#
# To load the file, use: 
#     reload
#     @py from space.batch_files import S04_eclipsion_expanse_system; S04_eclipsion_expanse_system.initialize()
#
#

from world.space.models import SpaceDB
from decimal import Decimal

def create_celestial_body(key, category, name, 
                        mass, # kg
                        radius, # km
                        x, y, z, 
                        orbiting_body,
                        orbital_radius=0.0, #km
                        orbital_period=0.0, #days
                        inclination=0.0, #degrees
                        ascii_art=None,
                        desc="A space object."):

    body=SpaceDB(db_key=key, db_category=category, db_name=name, 
                db_desc=desc, 
                db_mass="{:.50f}".format(float(mass)),
                db_radius="{:.50f}".format(float(radius)),

                db_x_coord=int(float(x)), 
                db_y_coord=y, db_z_coord=z,
                db_x_vel=0, db_y_vel=0, db_z_vel=0,

                orbiting_body=orbiting_body, 
                orbital_radius="{:.50f}".format(float(str(orbital_radius))), 
                orbital_period="{:.50f}".format(float(str(orbital_period))),
                db_inclination = "{:.50f}".format(float(str(inclination))),
                db_ascii_art = ascii_art,
                db_in_space = True,
                ) # Mass in kg
    return body
    
def initialize():
    print(" ")
    print("Initializing planets.")


    ### ADD SUNS / STARS #############################################


    # ('solara_prime', 4.57395568898503e+31, 1049244.2395815607, (0, 0, 11812129476), , orbital_radius=0, orbital_period=0, inclination=0.0, obj_type='star'),
    solara_prime=create_celestial_body('solara_prime', 'star', '|wSol|bara |wPri|bme|n', 4.57395568898503e+31, 1049244.2395815607, 0, 0, 11812129476, None, 0, 0, 0.0, ascii_art='STAR')
    solara_prime.desc = "A radiant orb of blue-white light, this star burns with an intensity that illuminates the surrounding void, casting long, eerie shadows on any nearby celestial bodies. Pulsating slightly, its surface dances with flares of energy that ripple outward, creating a mesmerizing display. The contrast between its fierce brightness and the darkness of space around it makes it a beacon of beauty and power. Every now and then, it sends out a burst of solar wind, a reminder of the raw, unbridled forces at play within its core."
    solara_prime.save()
    print("Created: Solara Prime")


    ### ADD PLANETS ##################################################


    # ('galaxis', 1.5811343052906104e+27, 15057.062677655087, (6865366389.72334, 0, 11812129476), solara_prime, orbital_radius=6865366389.72334, orbital_period=3855.30861103219, inclination=1.6479417742198785, obj_type='planet')
    galaxis=create_celestial_body('galaxis', 'planet', 'Galaxis', 1.5811343052906104e+27, 15057.062677655087, 6865366389.72334, 0, 11812129476, solara_prime, 6865366389.72334, 3855.30861103219, 1.6479417742198785, 'GREEN_PLANET')
    galaxis.desc = "A planet of endless sand seas, with colossal, ever-shifting dunes that resemble waves frozen in time. Occasional rocky outcrops break the expanse, standing like ancient sentinels in the desert."
    galaxis.save()
    print("Created: Galaxis")

    # ('ventoris', 7.683484672504391e+26, 2176.735895590269, (4303874249.495439, 0, 11812129476), solara_prime, orbital_radius=4303874249.495439, orbital_period=5919.914233378793, inclination=2.1917914199210857, obj_type='planet')
    ventoris=create_celestial_body('ventoris', 'planet', 'Ventoris', 7.683484672504391e+26, 2176.735895590269, 4303874249.495439, 0, 11812129476, solara_prime, 4303874249.495439, 5919.914233378793, 2.1917914199210857, 'RED_PLANET')
    ventoris.desc = "This world is covered in vast, sprawling fields of strange, luminescent plants that give off a soft, otherworldly glow. The light from these plants makes the night almost as bright as the day."
    ventoris.save()
    print("Created: Ventoris")

    # ('phylara', 9.951219183084722e+27, 45347.84407379854, (1623583037.3493588, 0, 11812129476), solara_prime, orbital_radius=1623583037.3493588, orbital_period=8971.3565382498, inclination=1.0827039325196721, obj_type='planet'),
    phylara=create_celestial_body('phylara', 'planet', 'Phylara', 9.951219183084722e+27, 45347.84407379854, 1623583037.3493588, 0, 11812129476, solara_prime, 1623583037.3493588, 8971.3565382498, 1.0827039325196721, 'BLUE_PLANET')
    phylara.desc = "A water world with only small patches of land visible, mostly towering, rugged islands rising from the endless ocean. The sea is a deep, mesmerizing blue, teeming with unseen life beneath its surface."
    phylara.save()
    print("Created: Phylara")

    # ('draconia', 6.013110209954197e+27, 45888.91448248057, (5194710667.835474, 0, 11812129476), solara_prime, orbital_radius=5194710667.835474, orbital_period=4456.467430724251, inclination=1.0769110734035194, obj_type='planet'),
    draconia=create_celestial_body('draconia', 'planet', 'Draconia', 6.013110209954197e+27, 45888.91448248057, 5194710667.835474, 0, 11812129476, solara_prime, 5194710667.835474, 4456.467430724251, 1.0769110734035194, 'GREEN_PLANET')
    draconia.desc = "The surface of this planet is a striking contrast of dark, basalt plains and bright, neon-green vegetation. The sharp delineation creates a checkerboard effect visible from orbit."
    draconia.save()
    print("Created: Draconia")

    # ('lytheria', 6.322006047155231e+27, 53879.42980549387, (1381749948.9387095, 0, 11812129476), solara_prime, orbital_radius=1381749948.9387095, orbital_period=7288.0406472285085, inclination=0.27582930891157786, obj_type='planet'),
    lytheria=create_celestial_body('lytheria', 'planet', 'Lytheria', 6.322006047155231e+27, 53879.42980549387, 1381749948.9387095, 0, 11812129476, solara_prime, 1381749948.9387095, 7288.0406472285085, 0.27582930891157786, 'RED_PLANET')
    lytheria.desc = "A dense, tropical world, its surface hidden beneath thick layers of dark, green foliage. Massive trees tower over the landscape, their canopies forming a continuous, unbroken expanse."
    lytheria.save()
    print("Created: Lytheria")

    # ('velos', 3.8269426075071624e+27, 15986.026883074439, (509737716.5043107, 0, 11812129476), solara_prime, orbital_radius=509737716.5043107, orbital_period=3036.5282113212465, inclination=1.8981318671980218, obj_type='planet'),
    velos=create_celestial_body('velos', 'planet', 'Velos', 3.8269426075071624e+27, 15986.026883074439, 509737716.5043107, 0, 11812129476, solara_prime, 509737716.5043107, 3036.5282113212465, 1.8981318671980218, 'BLUE_PLANET')
    velos.desc = "This planet's surface is covered in thick, reddish-brown dust, which swirls into massive, planet-wide storms. Occasional, rugged mountain ranges break through the dust, standing as solitary giants."
    velos.save()
    print("Created: Velos")

    # ('eryndor', 5.856532506172085e+27, 48021.46390242641, (2841805273.7584133, 0, 11812129476), solara_prime, orbital_radius=2841805273.7584133, orbital_period=2024.5801964786358, inclination=2.456839448530419, obj_type='planet'),
    eryndor=create_celestial_body('eryndor', 'planet', 'Eryndor', 5.856532506172085e+27, 48021.46390242641, 2841805273.7584133, 0, 11812129476, solara_prime, 2841805273.7584133, 2024.5801964786358, 2.456839448530419, 'GREEN_PLANET')
    eryndor.desc = "A glittering ocean world, with enormous, crystalline waves that sparkle under the sun. The occasional island breaks the surface, covered in shimmering, reflective minerals."
    eryndor.save()
    print("Created: Eryndor")

    # ('zorath_prime', 1.3004480147493989e+26, 32226.458081154124, (5908692745.075945, 0, 11812129476), solara_prime, orbital_radius=5908692745.075945, orbital_period=8388.725169749154, inclination=0.33399144068358383, obj_type='planet'),
    zorath_prime=create_celestial_body('zorath_prime', 'planet', 'Zorath Prime', 1.3004480147493989e+26, 32226.458081154124, 5908692745.075945, 0, 11812129476, solara_prime, 5908692745.075945, 8388.725169749154, 0.33399144068358383, 'RED_PLANET')
    zorath_prime.desc = "The planet's surface is an expanse of black rock, punctuated by glowing, lava-filled craters. The intense heat and light from these molten lakes create an eerie, hellish glow."
    zorath_prime.save()
    print("Created: Zorath Prime")


    ### ADD MOONS ####################################################


    # ('valtis', 7.886926839086227e+23, 2636.401451227995, (6865377368.529952, 0, 11812129476), galaxis, orbital_radius=10978.806611897831, orbital_period=131.82029934866495, inclination=2.9248507003799786, obj_type='moon'),
    valtis=create_celestial_body('valtis', 'moon', 'Valtis', 7.886926839086227e+23, 2636.401451227995, 6865377368.529952, 0, 11812129476, galaxis, 10978.806611897831, 131.82029934866495, 2.9248507003799786, 'MOON')
    valtis.desc = "This moon is enveloped in a swirling, iridescent mist that glows with shades of green and blue. The haze obscures the surface but creates a mesmerizing, ever-changing display of colors."
    valtis.save()
    print("Created: Valtis")

    # ('thaloria_minor', 5.491177447389051e+23, 843.20985566001, (6865411170.919031, 0, 11812129476), valtis, orbital_radius=44781.19569150482, orbital_period=280.0245711871364, inclination=2.426282777646976, obj_type='moon'),
    thaloria_minor=create_celestial_body('thaloria_minor', 'moon', 'Thaloria Minor', 5.491177447389051e+23, 843.20985566001, 6865411170.919031, 0, 11812129476, valtis, 44781.19569150482, 280.0245711871364, 2.426282777646976, 'MOON')
    thaloria_minor.desc = "With its surface covered in enormous, crater-filled plains, this moon has a pockmarked appearance. The craters are so deep that shadows create intricate patterns across the landscape."
    thaloria_minor.save()
    print("Created: Thaloria Minor")

    # ('norith', 5.696408511790233e+23, 2176.2969446707307, (6865376640.090039, 0, 11812129476), thaloria_minor, orbital_radius=10250.36669928205, orbital_period=713.9541168675171, inclination=1.0379988886557905, obj_type='moon'),
    norith=create_celestial_body('norith', 'moon', 'Norith', 5.696408511790233e+23, 2176.2969446707307, 6865376640.090039, 0, 11812129476, thaloria_minor, 10250.36669928205, 713.9541168675171, 1.0379988886557905, 'MOON')
    norith.desc = "This moon is adorned with vast, glistening ice caps at its poles, connected by a network of winding, frozen rivers. The central regions are rocky and rugged, providing a stark contrast to the smooth ice."
    norith.save()
    print("Created: Norith")

    # ('nexar', 3.341337971074522e+23, 1486.7208094049602, (6865391391.448842, 0, 11812129476), norith, orbital_radius=25001.725501699333, orbital_period=547.225043730809, inclination=0.9370612098771511, obj_type='moon'),
    nexar=create_celestial_body('nexar', 'moon', 'Nexar', 3.341337971074522e+23, 1486.7208094049602, 6865391391.448842, 0, 11812129476, norith, 25001.725501699333, 547.225043730809, 0.9370612098771511, 'MOON')
    nexar.desc = "A delicate lattice of dark, interlocking ridges and valleys covers this moon, giving it the appearance of a cracked, ancient egg. The rugged terrain casts long, dramatic shadows."
    nexar.save()
    print("Created: Nexar")

    # ('phex', 2.5987568428034146e+23, 1762.7818700177215, (6865371643.0555105, 0, 11812129476), nexar, orbital_radius=5253.332170047569, orbital_period=683.4353909591711, inclination=0.17522330101625821, obj_type='moon'),
    phex=create_celestial_body('phex', 'moon', 'Phex', 2.5987568428034146e+23, 1762.7818700177215, 6865371643.0555105, 0, 11812129476, nexar, 5253.332170047569, 683.4353909591711, 0.17522330101625821, 'MOON')
    phex.desc = "This moon is encircled by a halo of glowing plasma, casting an eerie light over its otherwise dark, cratered surface. The plasma pulses rhythmically, creating a hypnotic effect."
    phex.save()
    print("Created: Phex")

    # ('kronis', 1.2542233909861237e+23, 2436.0629049427644, (4303906717.359843, 0, 11812129476), ventoris, orbital_radius=32467.864405104523, orbital_period=663.5773756904902, inclination=0.5072167116244027, obj_type='moon'),
    kronis=create_celestial_body('kronis', 'moon', 'Kronis', 1.2542233909861237e+23, 2436.0629049427644, 4303906717.359843, 0, 11812129476, ventoris, 32467.864405104523, 663.5773756904902, 0.5072167116244027, 'MOON')
    kronis.desc = "Covered in a thick, yellowish fog, this moon has a mysterious, shrouded appearance. Occasional clearings reveal vast plains of sulfurous rock, adding to its alien ambiance."
    kronis.save()
    print("Created: Kronis")

    # ('thalax', 6.65920955635088e+23, 1014.322924979317, (4303915508.370512, 0, 11812129476), kronis, orbital_radius=41258.875073876196, orbital_period=196.82212811104844, inclination=0.3853682858511731, obj_type='moon'),
    thalax=create_celestial_body('thalax', 'moon', 'Thalax', 6.65920955635088e+23, 1014.322924979317, 4303915508.370512, 0, 11812129476, kronis, 41258.875073876196, 196.82212811104844, 0.3853682858511731, 'MOON')
    thalax.desc = "This moon features sprawling, reflective seas of quicksilver, interspersed with dark, rocky outcrops. The metallic surface catches the light, creating a dazzling, almost mirror-like effect."
    thalax.save()
    print("Created: Thalax")

    # ('zynara', 7.185667346874072e+23, 221.2433701023366, (4303905420.037253, 0, 11812129476), thalax, orbital_radius=31170.541814698103, orbital_period=374.8782966330995, inclination=0.7061102245136401, obj_type='moon'),
    zynara=create_celestial_body('zynara', 'moon', 'Zynara', 7.185667346874072e+23, 221.2433701023366, 4303905420.037253, 0, 11812129476, thalax, 31170.541814698103, 374.8782966330995, 0.7061102245136401, 'MOON')
    zynara.desc = "This moon is marked by immense, spiraling storm systems, their colorful bands visible even from space. The storms create a dynamic, ever-shifting pattern on the surface."
    zynara.save()
    print("Created: Zynara")

    # ('orinth', 8.6431479645869e+23, 311.63673755141195, (4303879679.645315, 0, 11812129476), zynara, orbital_radius=5430.149876632957, orbital_period=982.1584328244986, inclination=2.7301402501800984, obj_type='moon'),
    orinth=create_celestial_body('orinth', 'moon', 'Orinth', 8.6431479645869e+23, 311.63673755141195, 4303879679.645315, 0, 11812129476, zynara, 5430.149876632957, 982.1584328244986, 2.7301402501800984, 'MOON')
    orinth.desc = "The surface of this moon is a patchwork of bright, neon-lit cities and dark, uninhabited wastelands. The city lights form intricate geometric patterns, visible from space as a web of illumination."
    orinth.save()
    print("Created: Orinth")

    # ('nexis', 3.7804145467715006e+23, 1617.50321305907, (4303879046.009735, 0, 11812129476), orinth, orbital_radius=4796.51429632273, orbital_period=181.0195244130105, inclination=1.2886163228549727, obj_type='moon'),
    nexis=create_celestial_body('nexis', 'moon', 'Nexis', 3.7804145467715006e+23, 1617.50321305907, 4303879046.009735, 0, 11812129476, orinth, 4796.51429632273, 181.0195244130105, 1.2886163228549727, 'MOON')
    nexis.desc = "A series of massive, concentric rings of varying colors encircle this moon, made up of fine dust and ice particles. The rings give the moon a majestic and regal appearance."
    nexis.save()
    print("Created: Nexis")

    # ('taryn', 8.360322880533728e+23, 2961.22160000568, (1623606634.9318075, 0, 11812129476), phylara, orbital_radius=23597.58244878735, orbital_period=293.1686604030859, inclination=0.1304024428253077, obj_type='moon'),
    taryn=create_celestial_body('taryn', 'moon', 'Taryn', 8.360322880533728e+23, 2961.22160000568, 1623606634.9318075, 0, 11812129476, phylara, 23597.58244878735, 293.1686604030859, 0.1304024428253077, 'MOON')
    taryn.desc = "This moon’s surface is a kaleidoscope of shifting colors, caused by a thick atmosphere of constantly changing gases. The effect is mesmerizing, creating a vibrant, dynamic landscape."
    taryn.save()
    print("Created: Taryn")

    # ('velar', 3.245632239463559e+23, 184.9782063855462, (5194744696.738311, 0, 11812129476), draconia, orbital_radius=34028.90283651574, orbital_period=355.82320287011567, inclination=3.082477866916813, obj_type='moon'),
    velar=create_celestial_body('velar', 'moon', 'Velar', 3.245632239463559e+23, 184.9782063855462, 5194744696.738311, 0, 11812129476, draconia, 34028.90283651574, 355.82320287011567, 3.082477866916813, 'MOON')
    velar.desc = "Vast, glowing coral reefs cover this oceanic moon, their bioluminescence visible even from space. The light from the reefs illuminates the deep blue waters, creating a surreal underwater glow."
    velar.save()
    print("Created: Velar")

    # ('drathos', 4.1380112641393093e+23, 2242.2826874342327, (5194734802.5890875, 0, 11812129476), velar, orbital_radius=24134.75361318811, orbital_period=524.7399817532088, inclination=2.994156202413967, obj_type='moon'),
    drathos=create_celestial_body('drathos', 'moon', 'Drathos', 4.1380112641393093e+23, 2242.2826874342327, 5194734802.5890875, 0, 11812129476, velar, 24134.75361318811, 524.7399817532088, 2.994156202413967, 'MOON')
    drathos.desc = "This moon is covered in vast, metallic plains that shimmer with a coppery hue. The surface is dotted with massive, ancient ruins, suggesting a long-lost civilization."
    drathos.save()
    print("Created: Drathos")

    # ('zyra', 4.982759219447277e+23, 880.4733269982902, (5194736156.528327, 0, 11812129476), drathos, orbital_radius=25488.692853121953, orbital_period=456.7904872067142, inclination=0.9912038652666237, obj_type='moon'),
    zyra=create_celestial_body('zyra', 'moon', 'Zyra', 4.982759219447277e+23, 880.4733269982902, 5194736156.528327, 0, 11812129476, drathos, 25488.692853121953, 456.7904872067142, 0.9912038652666237, 'MOON')
    zyra.desc = "A dense, swirling atmosphere of deep purple and black gases surrounds this moon, giving it a dark and mysterious appearance. The clouds occasionally part to reveal glimpses of a rocky surface."
    zyra.save()
    print("Created: Zyra")

    # ('vixor', 2.158674711141788e+23, 2091.1367752915357, (5194731994.8930025, 0, 11812129476), zyra, orbital_radius=21327.057528512087, orbital_period=283.85845185832494, inclination=3.0976526466388026, obj_type='moon'),
    vixor=create_celestial_body('vixor', 'moon', 'Vixor', 2.158674711141788e+23, 2091.1367752915357, 5194731994.8930025, 0, 11812129476, zyra, 21327.057528512087, 283.85845185832494, 3.0976526466388026, 'MOON')
    vixor.desc = "This moon is covered in a vast, interconnected network of bright blue lakes, giving it a striking, almost otherworldly appearance. The lakes are interconnected by winding rivers, visible from space as a web of blue."
    vixor.save()
    print("Created: Vixor")

    # ('krya', 1.6408956071628464e+23, 2874.909284507372, (5194717659.59338, 0, 11812129476), vixor, orbital_radius=6991.757906287075, orbital_period=502.1045776947593, inclination=2.7775580089048972, obj_type='moon'),
    krya=create_celestial_body('krya', 'moon', 'Krya', 1.6408956071628464e+23, 2874.909284507372, 5194717659.59338, 0, 11812129476, vixor, 6991.757906287075, 502.1045776947593, 2.7775580089048972, 'MOON')
    krya.desc = "With a surface covered in deep, dark forests, this moon has a rich, verdant appearance. Occasional clearings reveal vast plains of bright, colorful flowers, adding a splash of color to the green expanse."
    krya.save()
    print("Created: Krya")

    # ('erya', 1.684278069613996e+22, 1584.3001514254915, (1381799529.7018597, 0, 11812129476), lytheria, orbital_radius=49580.76315015086, orbital_period=106.7251333232128, inclination=2.0467658994074136, obj_type='moon'),
    erya=create_celestial_body('erya', 'moon', 'Erya', 1.684278069613996e+22, 1584.3001514254915, 1381799529.7018597, 0, 11812129476, lytheria, 49580.76315015086, 106.7251333232128, 2.0467658994074136, 'MOON')
    erya.desc = "This moon features vast, arid deserts with towering sand dunes that shift and change with the winds. The golden sands create intricate patterns that are visible even from space."
    erya.save()
    print("Created: Erya")

    # ('phos', 3.964659031645978e+23, 1831.7697420768513, (1381784623.0066073, 0, 11812129476), erya, orbital_radius=34674.06789771597, orbital_period=992.2516060253814, inclination=1.4883106495292655, obj_type='moon'),
    phos=create_celestial_body('phos', 'moon', 'Phos', 3.964659031645978e+23, 1831.7697420768513, 1381784623.0066073, 0, 11812129476, erya, 34674.06789771597, 992.2516060253814, 1.4883106495292655, 'MOON')
    phos.desc = "A thick, swirling atmosphere of vibrant orange and yellow gases gives this moon a fiery, almost volcanic appearance. The clouds are dense and turbulent, creating a dynamic and ever-changing display."
    phos.save()
    print("Created: Phos")

    # ('noris', 4.5457607484594827e+23, 2370.442844287118, (1381796689.3634543, 0, 11812129476), phos, orbital_radius=46740.42474488587, orbital_period=733.599808904949, inclination=3.0879460031010844, obj_type='moon'),
    noris=create_celestial_body('noris', 'moon', 'Noris', 4.5457607484594827e+23, 2370.442844287118, 1381796689.3634543, 0, 11812129476, phos, 46740.42474488587, 733.599808904949, 3.0879460031010844, 'MOON')
    noris.desc = "This moon’s surface is covered in vast, reflective salt flats that shine brilliantly under the light. Occasional rocky outcrops provide a stark contrast to the otherwise flat, white landscape."
    noris.save()
    print("Created: Noris")

    # ('xenor', 2.33166427475601e+23, 1038.7638720532582, (1381765949.0442004, 0, 11812129476), noris, orbital_radius=16000.105490942558, orbital_period=703.7108156856175, inclination=2.825036311639158, obj_type='moon'),
    xenor=create_celestial_body('xenor', 'moon', 'Xenor', 2.33166427475601e+23, 1038.7638720532582, 1381765949.0442004, 0, 11812129476, noris, 16000.105490942558, 703.7108156856175, 2.825036311639158, 'MOON')
    xenor.desc = "A dense ring of debris and small asteroids surrounds this moon, creating a dynamic and chaotic appearance. The surface is heavily cratered, suggesting a history of frequent impacts."
    xenor.save()
    print("Created: Xenor")

    # ('jyn', 8.828680498582977e+23, 789.6997514106138, (1381782954.2533584, 0, 11812129476), xenor, orbital_radius=33005.31464888505, orbital_period=195.05113043241778, inclination=1.0728701408672583, obj_type='moon'),
    jyn=create_celestial_body('jyn', 'moon', 'Jyn', 8.828680498582977e+23, 789.6997514106138, 1381782954.2533584, 0, 11812129476, xenor, 33005.31464888505, 195.05113043241778, 1.0728701408672583, 'MOON')
    jyn.desc = "This moon is covered in vast, interconnected seas of liquid methane, giving it a deep, bluish-green hue. The seas are calm and reflective, creating a serene and otherworldly appearance."
    jyn.save()
    print("Created: Jyn")

    # ('arion', 2.2877096449899057e+22, 2364.075861275444, (1381778782.0465991, 0, 11812129476), jyn, orbital_radius=28833.107889570954, orbital_period=998.904763604311, inclination=2.2387806752527832, obj_type='moon'),
    arion=create_celestial_body('arion', 'moon', 'Arion', 2.2877096449899057e+22, 2364.075861275444, 1381778782.0465991, 0, 11812129476, jyn, 28833.107889570954, 998.904763604311, 2.2387806752527832, 'MOON')
    arion.desc = "A thick, swirling atmosphere of pale green and blue gases surrounds this moon, creating a soft, ethereal glow. The clouds are thin and wispy, giving the moon a delicate and fragile appearance."
    arion.save()
    print("Created: Arion")

    # ('zethis', 4.005090078816832e+23, 1742.5914876024665, (1381794127.4863195, 0, 11812129476), arion, orbital_radius=44178.54761009037, orbital_period=722.3875168434708, inclination=3.1376233531886797, obj_type='moon'),
    zethis=create_celestial_body('zethis', 'moon', 'Zethis', 4.005090078816832e+23, 1742.5914876024665, 1381794127.4863195, 0, 11812129476, arion, 44178.54761009037, 722.3875168434708, 3.1376233531886797, 'MOON')
    zethis.desc = "This moon’s surface is covered in vast, rolling plains of bright red grass, giving it a striking and unusual appearance. The grass sways gently in the breeze, creating a sense of movement and life."
    zethis.save()
    print("Created: Zethis")

    # ('lyria', 1.926418462406591e+23, 864.4909171033489, (509744488.9860291, 0, 11812129476), velos, orbital_radius=6772.481718331981, orbital_period=801.7065478124696, inclination=2.6948174292772267, obj_type='moon'),
    lyria=create_celestial_body('lyria', 'moon', 'Lyria', 1.926418462406591e+23, 864.4909171033489, 509744488.9860291, 0, 11812129476, velos, 6772.481718331981, 801.7065478124696, 2.6948174292772267, 'MOON')
    lyria.desc = "A dense, rocky surface covered in massive, jagged peaks gives this moon a rugged and imposing appearance. The rocks are a deep, dark gray, almost black, contrasting sharply with the surrounding space."
    lyria.save()
    print("Created: Lyria")

    # ('taris', 2.94783916903488e+23, 2021.636461215561, (509784966.38187575, 0, 11812129476), lyria, orbital_radius=47249.877565015435, orbital_period=649.3014098851567, inclination=1.3127105227308813, obj_type='moon'),
    taris=create_celestial_body('taris', 'moon', 'Taris', 2.94783916903488e+23, 2021.636461215561, 509784966.38187575, 0, 11812129476, lyria, 47249.877565015435, 649.3014098851567, 1.3127105227308813, 'MOON')
    taris.desc = "This moon is covered in a thick layer of bright, white frost, giving it a pristine and almost untouched appearance. The frost sparkles in the light, creating a dazzling effect."
    taris.save()
    print("Created: Taris")

    # ('qorath', 6.904988034335912e+23, 2437.991152476995, (509781442.4543538, 0, 11812129476), taris, orbital_radius=43725.950043089004, orbital_period=282.74292734690056, inclination=2.66212708946735, obj_type='moon'),
    qorath=create_celestial_body('qorath', 'moon', 'Qorath', 6.904988034335912e+23, 2437.991152476995, 509781442.4543538, 0, 11812129476, taris, 43725.950043089004, 282.74292734690056, 2.66212708946735, 'MOON')
    qorath.desc = "A swirling, stormy atmosphere of dark blue and black gases surrounds this moon, giving it a dynamic and ever-changing appearance. The clouds are thick and turbulent, with occasional flashes of lightning."
    qorath.save()
    print("Created: Qorath")


    ### ADD SPACE STATIONS AND OTHER ORBITTING DEBRIS ################


    # ('starfall_outpost', 2.3880234792583018e+17, 38.642244963172615, (5194753794.641836, 0, 11812129476), velar, orbital_radius=9097.903525313022, orbital_period=1.0525504548580498, inclination=1.632372761499757, obj_type='station'),
    starfall_outpost=create_celestial_body('starfall_outpost', 'station', 'Starfall Outpost', 2.3880234792583018e+17, 38.642244963172615, 5194753794.641836, 0, 11812129476, velar, 9097.903525313022, 1.0525504548580498, 1.632372761499757, 'STATION')
    starfall_outpost.desc = "A vast, cylindrical habitat spins slowly, creating a sense of artificial gravity for its inhabitants. The outer shell is adorned with murals depicting scenes of interstellar exploration, a testament to the station's storied history."
    starfall_outpost.save()
    print("Created: Starfall Outpost")

    # ('galactic_waypoint', 2.1755948350214637e+17, 61.34769566967959, (5194712068.283895, 0, 11812129476), draconia, orbital_radius=1400.4484204584883, orbital_period=58.32485849669347, inclination=0.07069365495138896, obj_type='station'),
    galactic_waypoint=create_celestial_body('galactic_waypoint', 'station', 'Galactic Waypoint', 2.1755948350214637e+17, 61.34769566967959, 5194712068.283895, 0, 11812129476, draconia, 1400.4484204584883, 58.32485849669347, 0.07069365495138896, 'STATION')
    galactic_waypoint.desc = "Orbiting silently, the station resembles an enormous spider with eight extending arms. Each arm is a docking platform, bustling with activity as ships dock and depart, carrying goods and passengers."
    galactic_waypoint.save()
    print("Created: Galactic Waypoint")

    # ('celestial_node', 6.636362094304074e+17, 26.12530987333009, (1381831978.7630677, 0, 11812129476), noris, orbital_radius=35289.39961332387, orbital_period=54.84767113533872, inclination=2.090728558069538, obj_type='station'),
    celestial_node=create_celestial_body('celestial_node', 'station', 'Celestial Node', 6.636362094304074e+17, 26.12530987333009, 1381831978.7630677, 0, 11812129476, noris, 35289.39961332387, 54.84767113533872, 2.090728558069538, 'STATION')
    celestial_node.desc = "The station's tiered structure rises like a stepped pyramid, with each level housing a different function. Lights flicker from within the windows, creating a pattern reminiscent of a digital skyline."
    celestial_node.save()
    print("Created: Celestial Node")

    

    # ('xyphon_rock', 6.286225335873085e+17, 0.8445426994331421, (1623609779.1007385, 0, 11812129476), taryn, orbital_radius=3144.1689310088277, orbital_period=95.53259135863259, inclination=0.8647754499037859, obj_type='asteroid'),
    xyphon_rock=create_celestial_body('xyphon_rock', 'asteroid', 'Xyphon Rock', 6.286225335873085e+17, 0.8445426994331421, 1623609779.1007385, 0, 11812129476, taryn, 3144.1689310088277, 95.53259135863259, 0.8647754499037859, 'ASTEROID')
    xyphon_rock.desc = "This asteroid displays a striking, hexagonal shape, an enigmatic geometric anomaly amidst the irregular forms commonly found in the asteroid belt."
    xyphon_rock.save()
    print("Created: Xyphon Rock")

    # ('krylon', 9.787743506015683e+17, 0.8381462297410643, (5908696055.080522, 0, 11812129476), zorath_prime, orbital_radius=3310.0045770776246, orbital_period=27.09265457026346, inclination=0.3428787952253023, obj_type='asteroid'),
    krylon=create_celestial_body('krylon', 'asteroid', 'Krylon', 9.787743506015683e+17, 0.8381462297410643, 5908696055.080522, 0, 11812129476, zorath_prime, 3310.0045770776246, 27.09265457026346, 0.3428787952253023, 'ASTEROID')
    krylon.desc = "With a crater resembling a giant eye, this asteroid seems to gaze back at the observer, its surface weathered by the relentless barrage of micrometeoroids."
    krylon.save()
    print("Created: Krylon")

    # ('veltor', 1.205196169873702e+17, 0.5523073357542617, (5194736835.56035, 0, 11812129476), vixor, orbital_radius=4840.667347659186, orbital_period=67.46199088993257, inclination=1.4616976875081278, obj_type='asteroid'),
    veltor=create_celestial_body('veltor', 'asteroid', 'Veltor', 1.205196169873702e+17, 0.5523073357542617, 5194736835.56035, 0, 11812129476, vixor, 4840.667347659186, 67.46199088993257, 1.4616976875081278, 'ASTEROID')
    veltor.desc = "A pristine sphere in space, this asteroid is unusually smooth and spherical, lacking the rugged features typically seen on its rocky counterparts."
    veltor.save()
    print("Created: Veltor")

    # ('ydris_shard', 8.645658132033698e+16, 0.6779041192972213, (5194745289.307346, 0, 11812129476), velar, orbital_radius=592.5690350689067, orbital_period=57.465925358192074, inclination=0.7724284041028384, obj_type='asteroid'),
    ydris_shard=create_celestial_body('ydris_shard', 'asteroid', 'Ydris Shard', 8.645658132033698e+16, 0.6779041192972213, 5194745289.307346, 0, 11812129476, velar, 592.5690350689067, 57.465925358192074, 0.7724284041028384, 'ASTEROID')
    ydris_shard.desc = "This asteroid is adorned with bands of color, reminiscent of the rings of a gas giant, hinting at its complex geological history."
    ydris_shard.save()
    print("Created: Ydris Shard")

    # ('thalor', 4.280279912295803e+17, 0.7101034811671416, (5908693190.915467, 0, 11812129476), zorath_prime, orbital_radius=445.83952246933103, orbital_period=88.76016198794869, inclination=0.34528450179619957, obj_type='asteroid'),
    thalor=create_celestial_body('thalor', 'asteroid', 'Thalor', 4.280279912295803e+17, 0.7101034811671416, 5908693190.915467, 0, 11812129476, zorath_prime, 445.83952246933103, 88.76016198794869, 0.34528450179619957, 'ASTEROID')
    thalor.desc = "Veined with streaks of precious minerals, this asteroid glitters with hidden wealth, its surface a potential treasure trove for future prospectors."
    thalor.save()
    print("Created: Thalor")



    print(" ")
    print("Finished generating space objects.")
