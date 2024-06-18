#
# To load the file, use: 
#     reload
#     @py from space.batch_files import S02_aurorae_nexus_system; S02_aurorae_nexus_system.initialize()
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


    # ('valtorix', 4.609329386417696e+31, 702613.3850064023, (11812129476, 0, 0), , orbital_radius=0, orbital_period=0, inclination=0.0, obj_type='star'),
    valtorix=create_celestial_body('valtorix', 'star', '|YValtorix|n', 4.609329386417696e+31, 702613.3850064023, 11812129476, 0, 0, None, 0, 0, 0.0, ascii_art='STAR')
    valtorix.desc = "Glowing with a warm, amber hue, this star exudes a sense of ancient wisdom and timeless serenity. Its light is steady and calming, bathing the surroundings in a gentle glow that softens the harshness of the cosmos. This giant has witnessed the birth and death of countless worlds, its core a furnace where heavy elements are forged. Occasionally, it displays a spectacular coronal mass ejection, sending plumes of stellar material spiraling into the abyss, a slow and majestic dance of creation and destruction."
    valtorix.save()
    print("Created: Valtorix")
    

    ### ADD PLANETS ##################################################


    # ('vantoria', 8.530752425125963e+27, 27363.01995437835, (13608245408.469173, 0, 0), valtorix, orbital_radius=1796115932.4691725, orbital_period=1149.6713813233591, inclination=1.6615302768478692, obj_type='planet'),
    vantoria=create_celestial_body('vantoria', 'planet', '|gV|ga|Cn|Bt|bo|Rr|mi|ga|n', 8.530752425125963e+27, 27363.01995437835, 13608245408.469173, 0, 0, valtorix, 1796115932.4691725, 1149.6713813233591, 1.6615302768478692, 'BLUE_PLANET')
    vantoria.desc = "A swirling mass of green and blue gases shrouds this giant, with occasional flashes of purple lightning illuminating the churning clouds. Towering storms stretch across its equator, making it a spectacle of color and chaos."
    vantoria.save()
    print("Created: Vantoria")

    # ('celestara_prime', 4.211795933283002e+27, 9523.042927747072, (14305004030.962849, 0, 0), valtorix, orbital_radius=2492874554.9628477, orbital_period=5321.584414349226, inclination=2.856231862354968, obj_type='planet'),
    celestara_prime=create_celestial_body('celestara_prime', 'planet', '|gCelestara Prime|n', 4.211795933283002e+27, 9523.042927747072, 14305004030.962849, 0, 0, valtorix, 2492874554.9628477, 5321.584414349226, 2.856231862354968, 'GREEN_PLANET')
    celestara_prime.desc = "This planet glistens like an emerald in space, its lush, verdant forests visible even from afar. Jagged mountain ranges break the green monotony, capped with snow that sparkles under the distant sun."
    celestara_prime.save()
    print("Created: Celestara Prime")

    # ('drathis', 5.955644577882771e+27, 22831.83208429577, (19645632282.443066, 0, 0), valtorix, orbital_radius=7833502806.443066, orbital_period=6556.23198789332, inclination=2.956223653897837, obj_type='planet'),
    drathis=create_celestial_body('drathis', 'planet', 'Drathis', 5.955644577882771e+27, 22831.83208429577, 19645632282.443066, 0, 0, valtorix, 7833502806.443066, 6556.23198789332, 2.956223653897837, 'RED_PLANET')
    drathis.desc = "A striking blend of reds and oranges, this desert planet is covered in vast, undulating dunes. Occasional oases break the monotony, with shimmering lakes reflecting the fiery hues of the sand."
    drathis.save()
    print("Created: Drathis")

    # ('jorak_v', 9.847960450823403e+27, 54323.18777876431, (21509584315.966373, 0, 0), valtorix, orbital_radius=9697454839.966373, orbital_period=751.5988522226872, inclination=0.4414061483226924, obj_type='planet'),
    jorak_v=create_celestial_body('jorak_v', 'planet', 'Jorak V', 9.847960450823403e+27, 54323.18777876431, 21509584315.966373, 0, 0, valtorix, 9697454839.966373, 751.5988522226872, 0.4414061483226924, 'BLUE_PLANET')
    jorak_v.desc = "This world is dominated by a massive, icy ocean that covers nearly its entire surface. Gigantic icebergs drift lazily, their undersides glowing a mysterious blue from within."
    jorak_v.save()
    print("Created: Jorak V")

    # ('taronis', 4.3485509555321727e+27, 52434.10809529807, (15493826779.169096, 0, 0), valtorix, orbital_radius=3681697303.1690955, orbital_period=5617.883636150336, inclination=1.6767381593079422, obj_type='planet'),
    taronis=create_celestial_body('taronis', 'planet', 'Taronis', 4.3485509555321727e+27, 52434.10809529807, 15493826779.169096, 0, 0, valtorix, 3681697303.1690955, 5617.883636150336, 1.6767381593079422, 'GREEN_PLANET')
    taronis.desc = "Covered in dense, swirling clouds of silver and white, this planet is a mystery beneath its thick atmosphere. Occasional breaks in the clouds reveal flashes of its metallic surface, hinting at a world of industry below."
    taronis.save()
    print("Created: Taronis")

    # ('yelvor_prime', 5.628847904867129e+27, 3064.0851448066655, (14672060583.188318, 0, 0), valtorix, orbital_radius=2859931107.188318, orbital_period=3197.237205339558, inclination=2.564164717523088, obj_type='planet'),
    yelvor_prime=create_celestial_body('yelvor_prime', 'planet', 'Yelvor Prime', 5.628847904867129e+27, 3064.0851448066655, 14672060583.188318, 0, 0, valtorix, 2859931107.188318, 3197.237205339558, 2.564164717523088, 'RED_PLANET')
    yelvor_prime.desc = "The planet's surface is a patchwork of deep blue oceans and sprawling, multicolored archipelagos. Islands in vivid shades of red, green, and yellow dot the seas, suggesting rich mineral deposits or strange vegetative life."
    yelvor_prime.save()
    print("Created: Yelvor Prime")

    # ('quintara', 1.101213952585327e+27, 38883.032832337645, (21672968873.95954, 0, 0), valtorix, orbital_radius=9860839397.959541, orbital_period=7179.422783033693, inclination=2.521766019267239, obj_type='planet'),
    quintara=create_celestial_body('quintara', 'planet', 'Quintara', 1.101213952585327e+27, 38883.032832337645, 21672968873.95954, 0, 0, valtorix, 9860839397.959541, 7179.422783033693, 2.521766019267239, 'BLUE_PLANET')
    quintara.desc = "This gas giant boasts a breathtaking ring system, more vivid and varied than Saturn's. Shades of pink, purple, and gold swirl together, creating a cosmic artwork that can be seen from afar."
    quintara.save()
    print("Created: Quintara")

    # ('xephos', 9.97078367126152e+27, 17003.00885747731, (19582023870.03965, 0, 0), valtorix, orbital_radius=7769894394.039648, orbital_period=6043.0216854515365, inclination=2.417277303204801, obj_type='planet'),
    xephos=create_celestial_body('xephos', 'planet', 'Xephos', 9.97078367126152e+27, 17003.00885747731, 19582023870.03965, 0, 0, valtorix, 7769894394.039648, 6043.0216854515365, 2.417277303204801, 'BLUE_PLANET')
    xephos.desc = "A planet of perpetual twilight, its surface is bathed in the soft glow of bioluminescent plants. Forests of glowing flora spread across its continents, lighting up the night in eerie yet beautiful patterns."
    xephos.save()
    print("Created: Xephos")


    ### ADD MOONS ####################################################


    # ('name', mass, radius, (x, y, z), orb_obj, orbital_radius, orbital_period, inclination, obj_type),

    # ('aethis', 8.405302468123192e+23, 2090.930091897867, (13608265586.74337, 0, 0), vantoria, orbital_radius=20178.274197406936, orbital_period=386.84087850040726, inclination=2.6948569078902938, obj_type='moon'),
    aethis=create_celestial_body('aethis', 'moon', 'Aethis', 8.405302468123192e+23, 2090.930091897867, 13608265586.74337, 0, 0, vantoria, 20178.274197406936, 386.84087850040726, 2.6948569078902938, 'MOON')
    aethis.desc = "Orbiting majestically, this moon boasts an intricate network of glowing blue veins across its surface, pulsing rhythmically like a giant, celestial heartbeat. The rest of the surface is a deep, dark black, creating a stunning contrast."
    aethis.save()
    print("Created: Aethis")

    # ('thalos_minor', 3.095762208018673e+23, 2102.256305237824, (13608261326.89779, 0, 0), aethis, orbital_radius=15918.42861681908, orbital_period=419.821158516072, inclination=2.4636776523630552, obj_type='moon'),
    thalos_minor=create_celestial_body('thalos_minor', 'moon', 'Thalos Minor', 3.095762208018673e+23, 2102.256305237824, 13608261326.89779, 0, 0, aethis, 15918.42861681908, 419.821158516072, 2.4636776523630552, 'MOON')
    thalos_minor.desc = "Encased in a translucent, shimmering ice shell, this moon looks like a giant frozen pearl in space. The ice reflects the light from the nearby star, creating a dazzling halo effect that surrounds the entire moon."
    thalos_minor.save()
    print("Created: Thalos Minor")

    # ('velar_minor', 7.606872327743482e+23, 1750.5811015563079, (13608290464.202555, 0, 0), thalos_minor, orbital_radius=45055.73338125626, orbital_period=838.6632090435756, inclination=0.19838358228606387, obj_type='moon'),
    velar_minor=create_celestial_body('velar_minor', 'moon', 'Velar Minor', 7.606872327743482e+23, 1750.5811015563079, 13608290464.202555, 0, 0, thalos_minor, 45055.73338125626, 838.6632090435756, 0.19838358228606387, 'MOON')
    velar_minor.desc = "This moon is covered in a patchwork of vibrant, multicolored patches, resembling an artist’s palette. The bright reds, yellows, and greens suggest diverse, perhaps even exotic, mineral compositions."
    velar_minor.save()
    print("Created: Velar Minor")

    # ('yloth', 1.9822072694378902e+23, 442.0175957639682, (13608284488.827911, 0, 0), velar_minor, orbital_radius=39080.35873866055, orbital_period=129.1168161706986, inclination=2.7983149197261463, obj_type='moon'),
    yloth=create_celestial_body('yloth', 'moon', 'Yloth', 1.9822072694378902e+23, 442.0175957639682, 13608284488.827911, 0, 0, velar_minor, 39080.35873866055, 129.1168161706986, 2.7983149197261463, 'MOON')
    yloth.desc = "A dense ring of asteroids and debris orbits this small, rocky moon, giving it the appearance of a miniature planet with its own asteroid belt. The surface is pockmarked with craters, indicating a history of heavy bombardment."
    yloth.save()
    print("Created: Yloth")

    # ('zyphos', 1.3170888207006064e+23, 2909.0793347617196, (13608247790.167925, 0, 0), yloth, orbital_radius=2381.698752247017, orbital_period=203.73514175452738, inclination=2.428769183354077, obj_type='moon'),
    zyphos=create_celestial_body('zyphos', 'moon', 'Zyphos', 1.3170888207006064e+23, 2909.0793347617196, 13608247790.167925, 0, 0, yloth, 2381.698752247017, 203.73514175452738, 2.428769183354077, 'MOON')
    zyphos.desc = "A dense ring of asteroids and debris orbits this small, rocky moon, giving it the appearance of a miniature planet with its own asteroid belt. The surface is pockmarked with craters, indicating a history of heavy bombardment."
    zyphos.save()
    print("Created: Zyphos")

    # ('nyra', 8.766368572362858e+23, 859.5820646105415, (13608255847.574858, 0, 0), zyphos, orbital_radius=10439.105683840125, orbital_period=433.0642392084013, inclination=2.630502546714381, obj_type='moon'),
    nyra=create_celestial_body('nyra', 'moon', 'Nyra', 8.766368572362858e+23, 859.5820646105415, 13608255847.574858, 0, 0, zyphos, 10439.105683840125, 433.0642392084013, 2.630502546714381, 'MOON')
    nyra.desc = "This gas giant’s moon is enveloped in swirling clouds of green and gold, giving it a constantly changing, almost hypnotic appearance. Occasionally, flashes of lightning illuminate the clouds from within, creating brief but spectacular light shows."
    nyra.save()
    print("Created: Nyra")

    # ('jorath', 7.642286421343778e+23, 2992.7806592044176, (13608249519.465734, 0, 0), nyra, orbital_radius=4110.996561757187, orbital_period=798.8876151385061, inclination=2.350593488170654, obj_type='moon'),
    jorath=create_celestial_body('jorath', 'moon', 'Jorath', 7.642286421343778e+23, 2992.7806592044176, 13608249519.465734, 0, 0, nyra, 4110.996561757187, 798.8876151385061, 2.350593488170654, 'MOON')
    jorath.desc = "Covered in massive glaciers, this moon glows a bright white, with the occasional dark fissure breaking the monotony of the ice. The glaciers appear to slowly shift and flow, indicating a dynamic and ever-changing surface."
    jorath.save()
    print("Created: Jorath")

    # ('drathis_minor', 2.650222902118233e+22, 1570.2470498186888, (14305046794.81084, 0, 0), celestara_prime, orbital_radius=42763.84799140926, orbital_period=846.4251383153672, inclination=2.598801250365163, obj_type='moon'),
    drathis_minor=create_celestial_body('drathis_minor', 'moon', 'Drathis Minor', 2.650222902118233e+22, 1570.2470498186888, 14305046794.81084, 0, 0, celestara_prime, 42763.84799140926, 846.4251383153672, 2.598801250365163, 'MOON')
    drathis_minor.desc = "This moon has a rich, golden hue, with swirling dust storms visible from space. The surface is dotted with massive, ancient structures that hint at a lost civilization, their shadows stretching long across the landscape."
    drathis_minor.save()
    print("Created: Drathis Minor")

    # ('kryon', 6.770864687318126e+23, 370.7177179951168, (14305025538.454552, 0, 0), drathis_minor, orbital_radius=21507.49170373118, orbital_period=269.5105748313551, inclination=0.5487116356826799, obj_type='moon'),
    kryon=create_celestial_body('kryon', 'moon', 'Kryon', 6.770864687318126e+23, 370.7177179951168, 14305025538.454552, 0, 0, drathis_minor, 21507.49170373118, 269.5105748313551, 0.5487116356826799, 'MOON')
    kryon.desc = "A network of deep, glowing red lava flows can be seen crisscrossing the surface of this volcanic moon. The rest of the surface is a dark, ashen gray, giving it a striking and somewhat ominous appearance."
    kryon.save()
    print("Created: Kryon")

    # ('xylis', 5.821993346778236e+23, 2732.251610276083, (21509613652.520386, 0, 0), jorak_v, orbital_radius=29336.554011825345, orbital_period=168.2870408682272, inclination=1.1019977183993277, obj_type='moon'),
    xylis=create_celestial_body('xylis', 'moon', 'Xylis', 5.821993346778236e+23, 2732.251610276083, 21509613652.520386, 0, 0, jorak_v, 29336.554011825345, 168.2870408682272, 1.1019977183993277, 'MOON')
    xylis.desc = "This ocean-covered moon has a beautiful blue-green tint, with vast, swirling storms visible from space. Occasional landmasses break the surface, covered in lush, green vegetation that stands out against the blue water."
    xylis.save()
    print("Created: Xylis")

    # ('zylar', 3.235159121071837e+22, 2058.4570183116602, (21509587050.196125, 0, 0), xylis, orbital_radius=2734.229751036947, orbital_period=338.2599729614484, inclination=1.4075304588805237, obj_type='moon'),
    zylar=create_celestial_body('zylar', 'moon', 'Zylar', 3.235159121071837e+22, 2058.4570183116602, 21509587050.196125, 0, 0, xylis, 2734.229751036947, 338.2599729614484, 1.4075304588805237, 'MOON')
    zylar.desc = "A dense, swirling atmosphere of vibrant pinks and purples surrounds this moon, creating a stunning visual effect. The surface beneath the clouds is mostly hidden, but occasional glimpses reveal a rugged, mountainous terrain."
    zylar.save()
    print("Created: Zylar")

    # ('pheros', 5.783241792950441e+23, 2031.3612064337224, (21509631460.527946, 0, 0), zylar, orbital_radius=47144.561572128696, orbital_period=233.45381846820035, inclination=2.9324422144982485, obj_type='moon'),
    pheros=create_celestial_body('pheros', 'moon', 'Pheros', 5.783241792950441e+23, 2031.3612064337224, 21509631460.527946, 0, 0, zylar, 47144.561572128696, 233.45381846820035, 2.9324422144982485, 'MOON')
    pheros.desc = "This moon’s surface is covered in vast, reflective salt flats, giving it a brilliant, almost blindingly white appearance from space. Occasional dark mountains break the surface, creating a stark contrast against the salt."
    pheros.save()
    print("Created: Pheros")

    # ('eryndor_minor', 1.4541002162213387e+21, 946.7272954808337, (21509620357.17114, 0, 0), pheros, orbital_radius=36041.2047645003, orbital_period=373.83393743770955, inclination=1.0201474494914105, obj_type='moon'),
    eryndor_minor=create_celestial_body('eryndor_minor', 'moon', 'Eryndor Minor', 1.4541002162213387e+21, 946.7272954808337, 21509620357.17114, 0, 0, pheros, 36041.2047645003, 373.83393743770955, 1.0201474494914105, 'MOON')
    eryndor_minor.desc = "With its surface covered in a thick, yellow fog, this moon has an eerie, otherworldly appearance. The fog is dense and swirling, obscuring any surface details and creating a mysterious, almost haunted look."
    eryndor_minor.save()
    print("Created: Eryndor Minor")

    # ('jexis', 7.187226541913209e+23, 567.7122293157446, (21509609401.33763, 0, 0), eryndor_minor, orbital_radius=25085.37125703042, orbital_period=790.4632092658882, inclination=1.6302360332007393, obj_type='moon'),
    jexis=create_celestial_body('jexis', 'moon', 'Jexis', 7.187226541913209e+23, 567.7122293157446, 21509609401.33763, 0, 0, eryndor_minor, 25085.37125703042, 790.4632092658882, 1.6302360332007393, 'MOON')
    jexis.desc = ""
    jexis.save()
    print("Created: Jexis")

    # ('asteris', 5.554983270815911e+23, 1142.92079425058, (15493855856.957968, 0, 0), taronis, orbital_radius=29077.78887110694, orbital_period=468.05151845113556, inclination=2.358548488098312, obj_type='moon'),
    asteris=create_celestial_body('asteris', 'moon', 'Asteris', 5.554983270815911e+23, 1142.92079425058, 15493855856.957968, 0, 0, taronis, 29077.78887110694, 468.05151845113556, 2.358548488098312, 'MOON')
    asteris.desc = "This moon is covered in a network of vast, interconnected craters, giving it a honeycomb-like appearance. The craters are deep and shadowy, with the edges catching the light and creating a stark, high-contrast look."
    asteris.save()
    print("Created: Asteris")

    # ('tharion', 9.602694850305489e+23, 873.4830106078967, (15493868510.245855, 0, 0), asteris, orbital_radius=41731.07675916868, orbital_period=496.56991177590345, inclination=2.719125617792639, obj_type='moon'),
    tharion=create_celestial_body('tharion', 'moon', 'Tharion',9.602694850305489e+23, 873.4830106078967, 15493868510.245855, 0, 0, asteris, 41731.07675916868, 496.56991177590345, 2.719125617792639, 'MOON')
    tharion.desc = "A series of massive, concentric rings encircle this moon, made of fine, icy particles that sparkle in the light. The rings are thin but extensive, giving the moon a majestic, almost regal appearance."
    tharion.save()
    print("Created: Tharion")

    # ('voth', 8.805481355797569e+23, 2438.0240038068237, (14672088783.122663, 0, 0), yelvor_prime, orbital_radius=28199.93434477439, orbital_period=840.521917735792, inclination=2.0655255070353777, obj_type='moon'),
    voth=create_celestial_body('voth', 'moon', 'Voth', 8.805481355797569e+23, 2438.0240038068237, 14672088783.122663, 0, 0, yelvor_prime, 28199.93434477439, 840.521917735792, 2.0655255070353777, 'MOON')
    voth.desc = "This moon has a surface covered in deep, azure blue oceans, with only a few small islands breaking the water’s surface. The water is calm and reflective, creating a serene and peaceful appearance."
    voth.save()
    print("Created: Voth")

    # ('valtor_minor', 4.080251979119688e+23, 2805.4691092852227, (14672097112.851748, 0, 0), voth, orbital_radius=36529.663429371874, orbital_period=836.0953117846365, inclination=0.03603545799355821, obj_type='moon'),
    valtor_minor=create_celestial_body('valtor_minor', 'moon', 'Valtor Minor', 4.080251979119688e+23, 2805.4691092852227, 14672097112.851748, 0, 0, voth, 36529.663429371874, 836.0953117846365, 0.03603545799355821, 'MOON')
    valtor_minor.desc = "Enormous, swirling storms can be seen moving across the surface of this gas moon, with the most prominent being a massive, hurricane-like system that dominates one hemisphere. The clouds are a mix of whites and grays, with occasional flashes of lightning."
    valtor_minor.save()
    print("Created: Valtor Minor")

    # ('tylis', 6.0881463150130135e+22, 811.1979115971261, (14672099336.68321, 0, 0), valtor_minor, orbital_radius=38753.494891279755, orbital_period=705.8424072579915, inclination=0.9090846871762298, obj_type='moon'),
    tylis=create_celestial_body('tylis', 'moon', 'Tylis', 6.0881463150130135e+22, 811.1979115971261, 14672099336.68321, 0, 0, valtor_minor, 38753.494891279755, 705.8424072579915, 0.9090846871762298, 'MOON')
    tylis.desc = "This moon’s surface is covered in massive, glowing red and orange lava lakes, creating a fiery, hellish appearance. The lava constantly shifts and flows, giving the moon a dynamic and ever-changing look."
    tylis.save()
    print("Created: Tylis")

    # ('lorin', 7.3661970724084746e+22, 529.487623868946, (14672110261.780731, 0, 0), tylis, orbital_radius=49678.59241282729, orbital_period=908.8482324835651, inclination=2.126643025903475, obj_type='moon'),
    lorin=create_celestial_body('lorin', 'moon', 'Lorin', 7.3661970724084746e+22, 529.487623868946, 14672110261.780731, 0, 0, tylis, 49678.59241282729, 908.8482324835651, 2.126643025903475, 'MOON')
    lorin.desc = "Covered in dense, dark forests, this moon has a rich, green appearance from space. Occasional clearings and rivers can be seen breaking the green expanse, adding variety to the landscape."
    lorin.save()
    print("Created: Lorin")

    # ('krythos', 7.120392696472008e+23, 1425.5480020266182, (14672100758.179464, 0, 0), lorin, orbital_radius=40174.99114668387, orbital_period=816.0291945565702, inclination=0.8454946448044925, obj_type='moon'),
    krythos=create_celestial_body('krythos', 'moon', 'Krythos', 7.120392696472008e+23, 1425.5480020266182, 14672100758.179464, 0, 0, lorin, 40174.99114668387, 816.0291945565702, 0.8454946448044925, 'MOON')
    krythos.desc = "A thick, swirling atmosphere of dark blues and purples gives this moon a mysterious, almost sinister appearance. Occasional bright flashes of lightning illuminate the clouds from within, creating brief but dramatic light shows."
    krythos.save()
    print("Created: Krythos")

    # ('zyn', 1.356249708187283e+23, 2433.373305574545, (21672990067.846737, 0, 0), quintara, orbital_radius=21193.887195266245, orbital_period=391.38503990083825, inclination=1.4035219187524344, obj_type='moon'),
    zyn=create_celestial_body('zyn', 'moon', 'Zyn', 1.356249708187283e+23, 2433.373305574545, 21672990067.846737, 0, 0, quintara, 21193.887195266245, 391.38503990083825, 1.4035219187524344, 'MOON')
    zyn.desc = "This moon’s surface is covered in massive, glittering crystal formations, giving it a dazzling, almost magical appearance. The crystals reflect the light in a myriad of colors, creating a constantly shifting kaleidoscope of hues."
    zyn.save()
    print("Created: Zyn")

    # ('xerath_minor', 4.6522571096140403e+23, 1666.7197953940297, (19582072849.8651, 0, 0), xephos, orbital_radius=48979.82545059442, orbital_period=23.91486255395605, inclination=2.2638431088203945, obj_type='moon'),
    xerath_minor=create_celestial_body('xerath_minor', 'moon', 'Xerath Minor', 4.6522571096140403e+23, 1666.7197953940297, 19582072849.8651, 0, 0, xephos, 48979.82545059442, 23.91486255395605, 2.2638431088203945, 'MOON')
    xerath_minor.desc = "Covered in vast, golden deserts, this moon glows with a warm, inviting light. The sand dunes create intricate patterns that shift and change over time, adding to the moon’s dynamic and ever-changing appearance."
    xerath_minor.save()
    print("Created: Xerath Minor")

    # ('tharon', 8.882063204095301e+23, 1422.1663995621966, (19582027824.83442, 0, 0), xerath_minor, orbital_radius=3954.7947708813654, orbital_period=916.2380375679522, inclination=0.30502730177238657, obj_type='moon'),
    tharon=create_celestial_body('tharon', 'moon', 'Tharon', 8.882063204095301e+23, 1422.1663995621966, 19582027824.83442, 0, 0, xerath_minor, 3954.7947708813654, 916.2380375679522, 0.30502730177238657, 'MOON')
    tharon.desc = "A dense, swirling atmosphere of pale greens and yellows surrounds this moon, obscuring much of the surface. Occasional clear patches reveal a rugged, mountainous terrain below the clouds."
    tharon.save()
    print("Created: Tharon")


    ### ADD SPACE STATIONS AND OTHER ORBITTING DEBRIS ################


    # ('phoenix_base', 5.281397994124311e+17, 29.26469698019716, (14672117880.275295, 0, 0), lorin, orbital_radius=7618.494563999095, orbital_period=11.639736462549036, inclination=0.9956508381349549, obj_type='station'),
    phoenix_base=create_celestial_body('phoenix_base', 'station', 'Phoenix Base', 5.281397994124311e+17, 29.26469698019716, 14672117880.275295, 0, 0, lorin, 7618.494563999095, 11.639736462549036, 0.9956508381349549, 'STATION')
    phoenix_base.desc = "Floating serenely, the station glows with a soft, bioluminescent light, casting intricate patterns across its spherical surface. Delicate antennae extend outward, resembling the petals of an exotic space flower, capturing signals from distant stars."
    phoenix_base.save()
    print("Created: Phoenix Base")

    # ('vortex_outpost', 7.240968405162537e+17, 82.04615415057025, (13608260400.015938, 0, 0), zyphos, orbital_radius=12609.848012380377, orbital_period=31.617301410443094, inclination=2.348577426843729, obj_type='station'),
    vortex_outpost=create_celestial_body('vortex_outpost', 'station', 'Vortex Outpost', 7.240968405162537e+17, 82.04615415057025, 13608260400.015938, 0, 0, zyphos, 12609.848012380377, 31.617301410443094, 2.348577426843729, 'STATION')
    vortex_outpost.desc = "The station's angular, modular design creates a stark contrast against the backdrop of space, with solar panels glinting like shards of obsidian. Its central dome pulses with a rhythmic light, hinting at the bustling activity within."
    vortex_outpost.save()
    print("Created: Vortex Outpost")

    # ('stellar_node', 7.232564160772477e+16, 53.68491593614284, (14305038444.649487, 0, 0), celestara_prime, orbital_radius=34413.68663857763, orbital_period=46.47987660617217, inclination=1.1948845054065542, obj_type='station'),
    stellar_node=create_celestial_body('stellar_node', 'station', 'Stellar Node', 7.232564160772477e+16, 53.68491593614284, 14305038444.649487, 0, 0, celestara_prime, 34413.68663857763, 46.47987660617217, 1.1948845054065542, 'STATION')
    stellar_node.desc = "A colossal ring structure encircles a rotating habitat, shimmering with a metallic sheen. Docking bays open like flower petals, allowing shuttles to come and go with a graceful ballet of technology."
    stellar_node.save()
    print("Created: Stellar Node")
    
    

    # ('kryon_rock', 5.5610121952151315e+17, 0.6486833739725871, (14672121929.033457, 0, 0), phoenix_base, orbital_radius=4048.7581610587663, orbital_period=44.45034921992719, inclination=2.0671063615024146, obj_type='asteroid'),
    kryon_rock=create_celestial_body('kryon_rock', 'asteroid', 'Kryon Rock', 5.5610121952151315e+17, 0.6486833739725871, 14672121929.033457, 0, 0, phoenix_base, 4048.7581610587663, 44.45034921992719, 2.0671063615024146, 'ASTEROID')
    kryon_rock.desc = "A glimmering celestial pebble, this asteroid appears as a shimmering jewel amidst the vast darkness, its surface reflecting faint hues of blue and green."
    kryon_rock.save()
    print("Created: Asteroid Kryon Rock")

    # ('varyon', 2.7485553813748752e+17, 0.8243924565200212, (21509587912.78025, 0, 0), zylar, orbital_radius=862.5841271313473, orbital_period=4.905191854114422, inclination=0.3748546837497842, obj_type='asteroid'),
    varyon=create_celestial_body('varyon', 'asteroid', 'Varyon', 2.7485553813748752e+17, 0.8243924565200212, 21509587912.78025, 0, 0, zylar, 862.5841271313473, 4.905191854114422, 0.3748546837497842, 'ASTEROID')
    varyon.desc = "This asteroid displays a rugged terrain, dotted with sharp, jagged peaks that cast long shadows as the distant starlight grazes its uneven surface."
    varyon.save()
    print("Created: Asteroid Varyon")

    # ('thalorn', 3.2613105094090374e+17, 0.8390586930946998, (19582026769.21089, 0, 0), xephos, orbital_radius=2899.171242997943, orbital_period=17.584832935529874, inclination=2.45541119109591, obj_type='asteroid'),
    thalorn=create_celestial_body('thalorn', 'asteroid', 'Thalorn', 3.2613105094090374e+17, 0.8390586930946998, 19582026769.21089, 0, 0, xephos, 2899.171242997943, 17.584832935529874, 2.45541119109591, 'ASTEROID')
    thalorn.desc = "A solitary wanderer in the cosmic sea, this asteroid features a crater-pocked landscape, revealing the scars of countless impacts endured over eons."
    thalorn.save()
    print("Created: Asteroid Thalorn")

    # ('tylos', 1.9906778964661418e+17, 0.1456329090414374, (14672126193.351862, 0, 0), kryon_rock, orbital_radius=4264.318405853366, orbital_period=18.213485399009826, inclination=1.6927790870668016, obj_type='asteroid'),
    tylos=create_celestial_body('tylos', 'asteroid', 'Tylos', 1.9906778964661418e+17, 0.1456329090414374, 14672126193.351862, 0, 0, kryon_rock, 4264.318405853366, 18.213485399009826, 1.6927790870668016, 'ASTEROID')
    tylos.desc = "Bathed in a soft, ethereal glow, this asteroid appears almost translucent, its delicate silhouette against the velvet backdrop of space evoking a sense of fragile beauty."
    tylos.save()
    print("Created: Asteroid Tylos")

    # ('jyxos_shard', 5.992434950636927e+17, 0.1391058062286528, (13608254468.817513, 0, 0), jorath, orbital_radius=4949.351777957779, orbital_period=20.750558408344975, inclination=0.9353697472412873, obj_type='asteroid'),
    jyxos_shard=create_celestial_body('jyxos_shard', 'asteroid', 'Jyxos Shard', 5.992434950636927e+17, 0.1391058062286528, 13608254468.817513, 0, 0, jorath, 4949.351777957779, 20.750558408344975, 0.9353697472412873, 'ASTEROID')
    jyxos_shard.desc = "With a metallic sheen that catches the light just so, this asteroid gleams like a polished mirror, reflecting its surroundings in distorted patterns."
    jyxos_shard.save()
    print("Created: Asteroid Jyxos Shard")



    print(" ")
    print("Finished generating space objects.")
