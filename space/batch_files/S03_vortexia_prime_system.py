#
# To load the file, use: 
#     reload
#     @py from space.batch_files import S03_vortexia_prime_system; S03_vortexia_prime_system.initialize()
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


    # ('name', mass, radius, (x, y, z), orb_obj, orbital_radius, orbital_period, inclination, obj_type),

    # ('luminaris', 3.605233820315807e+31, 1811183.6137465949, (0, 11812129476, 0), , orbital_radius=0, orbital_period=0, inclination=0.0, obj_type='star'),
    luminaris=create_celestial_body('luminaris', 'star', '|rLuminaris|n', 3.605233820315807e+31, 1811183.6137465949, 0, 11812129476, 0, None, 0, 0, 0.0, ascii_art='STAR')
    luminaris.desc = "An enigmatic crimson giant, this star appears almost mystical, its deep red light suffusing the space around it with an otherworldly glow. The surface is turbulent, marked by colossal storms and solar flares that erupt with unpredictable ferocity. Despite its tempestuous nature, it has a captivating allure, drawing the gaze with its dramatic and ever-changing visage. The immense forces at work within it hint at the star's imminent transformation, a prelude to the next stage in its cosmic journey."
    luminaris.save()
    print("Created: Luminaris")


    ### ADD PLANETS ##################################################


    # ('tormax_iv', 6.591093568789392e+27, 30474.940900102923, (9499111461.697992, 11812129476, 0), luminaris, orbital_radius=9499111461.697992, orbital_period=9273.199683947036, inclination=1.3884775913764085, obj_type='planet'),
    tormax_iv=create_celestial_body('tormax_iv', 'planet', 'Tormax IV', 6.591093568789392e+27, 30474.940900102923, 9499111461.697992, 11812129476, 0, luminaris, 9499111461.697992, 9273.199683947036, 1.3884775913764085, 'RED_PLANET')
    tormax_iv.desc = "The surface of this rocky planet is covered in sprawling, crystalline formations that sparkle like diamonds. These enormous structures catch and refract light, creating dazzling displays of color and brilliance."
    tormax_iv.save()
    print("Created: Tormax IV")

    # ('lyronis', 4.2342762846059845e+27, 10243.40904582538, (6690855074.67746, 11812129476, 0), luminaris, orbital_radius=6690855074.67746, orbital_period=237.68481875090188, inclination=2.292812549997771, obj_type='planet'),
    lyronis=create_celestial_body('lyronis', 'planet', 'Lyronis', 4.2342762846059845e+27, 10243.40904582538, 6690855074.67746, 11812129476, 0, luminaris, 6690855074.67746, 237.68481875090188, 2.292812549997771, 'BLUE_PLANET')
    lyronis.desc = "This planet appears as a tranquil blue and white marble, with vast, calm oceans interspersed with small, white clouds. Its serene beauty is complemented by the occasional appearance of large, tranquil seas."
    lyronis.save()
    print("Created: Lyronis")

    # ('vexara', 2.626653969626243e+27, 40453.57487512082, (3069544137.718095, 11812129476, 0), luminaris, orbital_radius=3069544137.718095, orbital_period=6295.022569821897, inclination=1.3074571821419874, obj_type='planet'),
    vexara=create_celestial_body('vexara', 'planet', 'Vexara', 2.626653969626243e+27, 40453.57487512082, 3069544137.718095, 11812129476, 0, luminaris, 3069544137.718095, 6295.022569821897, 1.3074571821419874, 'GREEN_PLANET')
    vexara.desc = "A crimson world covered in a thick, reddish haze, it looks as though it’s perpetually at sunset. The surface below appears rugged and mountainous, with great, deep valleys cutting through the landscape."
    vexara.save()
    print("Created: Vexara")

    # ('thaloria', 8.539477933007192e+27, 30560.752297327243, (6184116145.397059, 11812129476, 0), luminaris, orbital_radius=6184116145.397059, orbital_period=1357.5919689635518, inclination=0.04162513462371183, obj_type='planet'),
    thaloria=create_celestial_body('thaloria', 'planet', 'Thaloria', 8.539477933007192e+27, 30560.752297327243, 6184116145.397059, 11812129476, 0, luminaris, 6184116145.397059, 1357.5919689635518, 0.04162513462371183, 'RED_PLANET')
    thaloria.desc = "This planet is shrouded in a dense fog of electric blue, which occasionally parts to reveal a surface crisscrossed with glowing rivers of what seems to be liquid light, illuminating the otherwise dark world."
    thaloria.save()
    print("Created: Thaloria")

    # ('nixoria', 1.7543061911079438e+27, 49241.78451887483, (2505571910.933554, 11812129476, 0), luminaris, orbital_radius=2505571910.933554, orbital_period=5019.689514657793, inclination=0.5846718574685945, obj_type='planet'),
    nixoria=create_celestial_body('nixoria', 'planet', 'Nixoria', 1.7543061911079438e+27, 49241.78451887483, 2505571910.933554, 11812129476, 0, luminaris, 2505571910.933554, 5019.689514657793, 0.5846718574685945, 'BLUE_PLANET')
    nixoria.desc = "The surface of this planet is a vibrant mosaic of sprawling, tropical jungles interspersed with large, clear lakes. The rich green canopy is punctuated by occasional bursts of colorful flowers and fruit."
    nixoria.save()
    print("Created: Nixoria")

    # ('zylath', 6.532664638106463e+27, 43658.6140074045, (5677356658.450992, 11812129476, 0), luminaris, orbital_radius=5677356658.450992, orbital_period=827.4544546934193, inclination=2.876171481480168, obj_type='planet'),
    zylath=create_celestial_body('zylath', 'planet', 'Zylath', 6.532664638106463e+27, 43658.6140074045, 5677356658.450992, 11812129476, 0, luminaris, 5677356658.450992, 827.4544546934193, 2.876171481480168, 'GREEN_PLANET')
    zylath.desc = "A barren, rocky world with a surface covered in shimmering, reflective minerals that glitter under the sun. The effect is like looking at a vast, silver desert, occasionally broken by deep, shadowy craters."
    zylath.save()
    print("Created: Zylath")

    # ('venoria', 4.686516926468181e+27, 18254.578359429517, (237937274.81193328, 11812129476, 0), luminaris, orbital_radius=237937274.81193328, orbital_period=3224.051056658128, inclination=0.02501370524192876, obj_type='planet'),
    venoria=create_celestial_body('venoria', 'planet', 'Venoria', 4.686516926468181e+27, 18254.578359429517, 237937274.81193328, 11812129476, 0, luminaris, 237937274.81193328, 3224.051056658128, 0.02501370524192876, 'RED_PLANET')
    venoria.desc = "This planet’s surface is a harsh, volcanic landscape, with rivers of molten lava cutting through dark, jagged rock. The fiery glow from the lava casts an eerie light over the whole world."
    venoria.save()
    print("Created: Venoria")

    # ('xerath', 2.6797896745156214e+27, 41438.31904912719, (9109081605.200924, 11812129476, 0), luminaris, orbital_radius=9109081605.200924, orbital_period=1784.2334348861573, inclination=0.5684794543626962, obj_type='planet'),
    xerath=create_celestial_body('xerath', 'planet', 'Xerath', 2.6797896745156214e+27, 41438.31904912719, 9109081605.200924, 11812129476, 0, luminaris, 9109081605.200924, 1784.2334348861573, 0.5684794543626962, 'BLUE_PLANET')
    xerath.desc = "An icy planet with a surface covered in thick, crystalline ice sheets, reflecting a spectrum of colors from its star. Vast, frozen oceans and towering ice cliffs create a breathtaking, if frigid, landscape."
    xerath.save()
    print("Created: Xerath")


    ### ADD MOONS ####################################################


    # ('kryos_minor', 4.916410432532804e+23, 1833.8815824577762, (9499152452.919813, 11812129476, 0), tormax_iv, orbital_radius=40991.22182010081, orbital_period=750.7357735442091, inclination=1.506592271379501, obj_type='moon'),
    kryos_minor=create_celestial_body('kryos_minor', 'moon', 'Kryos Minor', 4.916410432532804e+23, 1833.8815824577762, 9499152452.919813, 11812129476, 0, tormax_iv, 40991.22182010081, 750.7357735442091, 1.506592271379501, 'MOON')
    kryos_minor.desc = "This moon glows with an ethereal silver light, its surface covered in shimmering, reflective dust. The light creates an otherworldly halo that seems to pulse gently, giving the moon a dreamlike quality."
    kryos_minor.save()
    print("Created: Kryos Minor")

    # ('oryn', 3.66887621560623e+23, 2787.616950604046, (6690888336.326578, 11812129476, 0), lyronis, orbital_radius=33261.64911856118, orbital_period=33.906695708640335, inclination=1.084946279154932, obj_type='moon'),
    oryn=create_celestial_body('oryn', 'moon', 'Oryn', 3.66887621560623e+23, 2787.616950604046, 6690888336.326578, 11812129476, 0, lyronis, 33261.64911856118, 33.906695708640335, 1.084946279154932, 'MOON')
    oryn.desc = "This moon is encircled by thin, wispy rings of ice and rock, creating a delicate and almost fragile appearance. The surface is smooth and slightly blue, with large, frozen lakes dotting the landscape."
    oryn.save()
    print("Created: Oryn")

    # ('zyth', 2.6420154724633792e+22, 2887.7326174562595, (6690874939.38421, 11812129476, 0), oryn, orbital_radius=19864.706749716846, orbital_period=437.92786944817914, inclination=0.06888699596330854, obj_type='moon'),
    zyth=create_celestial_body('zyth', 'moon', 'Zyth', 2.6420154724633792e+22, 2887.7326174562595, 6690874939.38421, 11812129476, 0, oryn, 19864.706749716846, 437.92786944817914, 0.06888699596330854, 'MOON')
    zyth.desc = "A vibrant green hue envelops this moon, with thick bands of vegetation visible from space. The lush greenery stands out sharply against the dark, rocky areas, creating a striking contrast."
    zyth.save()
    print("Created: Zyth")

    # ('korin', 5.192435037642986e+23, 805.9696084021905, (6690863238.303331, 11812129476, 0), zyth, orbital_radius=8163.625871343365, orbital_period=760.4912451783617, inclination=0.8606688737390918, obj_type='moon'),
    korin=create_celestial_body('korin', 'moon', 'Korin', 5.192435037642986e+23, 805.9696084021905, 6690863238.303331, 11812129476, 0, zyth, 8163.625871343365, 760.4912451783617, 0.8606688737390918, 'MOON')
    korin.desc = "This moon has an intricate network of bright, luminescent veins crisscrossing its dark surface. The veins pulse with a soft, blue light, resembling a giant, glowing web."
    korin.save()
    print("Created: Korin")

    # ('zorin', 6.764870859806806e+23, 2102.810060485289, (6184149272.963917, 11812129476, 0), thaloria, orbital_radius=33127.56685694791, orbital_period=34.77982144119512, inclination=1.809584047939941, obj_type='moon'),
    zorin=create_celestial_body('zorin', 'moon', 'Zorin', 6.764870859806806e+23, 2102.810060485289, 6184149272.963917, 11812129476, 0, thaloria, 33127.56685694791, 34.77982144119512, 1.809584047939941, 'MOON')
    zorin.desc = "Covered in swirling clouds of pink and orange, this moon looks like a celestial marble. The atmosphere is thick and dynamic, constantly shifting and creating new patterns and shapes."
    zorin.save()
    print("Created: Zorin")

    # ('xynar_minor', 4.0443308500526586e+23, 892.804946947365, (6184136918.796813, 11812129476, 0), zorin, orbital_radius=20773.399753869515, orbital_period=531.2086907104535, inclination=3.0320959144166473, obj_type='moon'),
    xynar_minor=create_celestial_body('xynar_minor', 'moon', 'Xynar Minor', 4.0443308500526586e+23, 892.804946947365, 6184136918.796813, 11812129476, 0, zorin, 20773.399753869515, 531.2086907104535, 3.0320959144166473, 'MOON')
    xynar_minor.desc = "This moon's surface is dominated by massive, shimmering crystals that reflect light in a rainbow of colors. The effect is mesmerizing, making the moon appear as though it is covered in glittering gems."
    xynar_minor.save()
    print("Created: Xynar Minor")

    # ('lorin_minor', 2.57694258316593e+23, 757.8645224121703, (6184126687.976823, 11812129476, 0), xynar_minor, orbital_radius=10542.579763328213, orbital_period=857.7112902124475, inclination=1.218287687382925, obj_type='moon'),
    lorin_minor=create_celestial_body('lorin_minor', 'moon', 'Lorin Minor', 2.57694258316593e+23, 757.8645224121703, 6184126687.976823, 11812129476, 0, xynar_minor, 10542.579763328213, 857.7112902124475, 1.218287687382925, 'MOON')
    lorin_minor.desc = "A dense, swirling atmosphere of dark red and brown gases surrounds this moon, giving it a menacing, almost volcanic appearance. Occasional flashes of lightning illuminate the stormy clouds."
    lorin_minor.save()
    print("Created: Lorin Minor")

    # ('qyra', 2.0589906380879453e+23, 1822.6477624426325, (6184164501.110546, 11812129476, 0), lorin_minor, orbital_radius=48355.713486510394, orbital_period=480.81004170916447, inclination=2.7045573245269128, obj_type='moon'),
    qyra=create_celestial_body('qyra', 'moon', 'Qyra', 2.0589906380879453e+23, 1822.6477624426325, 6184164501.110546, 11812129476, 0, lorin_minor, 48355.713486510394, 480.81004170916447, 2.7045573245269128, 'MOON')
    qyra.desc = "This moon has a surface that appears almost metallic, with large, flat plains of reflective metal. The light reflects in such a way that the moon glows with a dull, bronze hue."
    qyra.save()
    print("Created: Qyra")

    # ('phylis', 2.6701815417643566e+23, 686.1214346814063, (6184159346.518048, 11812129476, 0), qyra, orbital_radius=43201.12098927433, orbital_period=145.9408770249515, inclination=1.3968753700648882, obj_type='moon'),
    phylis=create_celestial_body('phylis', 'moon', 'Phylis', 2.6701815417643566e+23, 686.1214346814063, 6184159346.518048, 11812129476, 0, qyra, 43201.12098927433, 145.9408770249515, 1.3968753700648882, 'MOON')
    phylis.desc = "A thick, hazy atmosphere gives this moon a soft, golden glow. The surface is largely obscured, but the faint outlines of vast mountain ranges can be seen through the haze."
    phylis.save()
    print("Created: Phylis")

    # ('thalix', 2.4879873628606634e+23, 157.12254883321668, (6184159764.392235, 11812129476, 0), phylis, orbital_radius=43618.99517515976, orbital_period=39.526423393690706, inclination=2.569491793971381, obj_type='moon'),
    thalix=create_celestial_body('thalix', 'moon', 'Thalix', 2.4879873628606634e+23, 157.12254883321668, 6184159764.392235, 11812129476, 0, phylis, 43618.99517515976, 39.526423393690706, 2.569491793971381, 'MOON')
    thalix.desc = "This moon is covered in massive, undulating dunes of golden sand. The dunes catch the light, creating a shimmering effect that makes the entire moon look like a giant, glowing orb."
    thalix.save()
    print("Created: Thalix")

    # ('thalyn', 6.968008423445372e+23, 1360.7049965767542, (2505615915.0152416, 11812129476, 0), nixoria, orbital_radius=44004.08168724986, orbital_period=899.2480678915525, inclination=0.9633525133380869, obj_type='moon'),
    thalyn=create_celestial_body('thalyn', 'moon', 'Thalyn', 6.968008423445372e+23, 1360.7049965767542, 2505615915.0152416, 11812129476, 0, nixoria, 44004.08168724986, 899.2480678915525, 0.9633525133380869, 'MOON')
    thalyn.desc = "A network of interconnected, glowing lakes covers this moon, giving it a unique, patchwork appearance. The lakes are a bright, electric blue, standing out sharply against the dark, rocky surface."
    thalyn.save()
    print("Created: Thalyn")

    # ('trion', 1.46254139506888e+23, 2808.654568816996, (2505586388.02757, 11812129476, 0), thalyn, orbital_radius=14477.09401538375, orbital_period=577.4727010217539, inclination=2.5758624107235883, obj_type='moon'),
    trion=create_celestial_body('trion', 'moon', 'Trion', 1.46254139506888e+23, 2808.654568816996, 2505586388.02757, 11812129476, 0, thalyn, 14477.09401538375, 577.4727010217539, 2.5758624107235883, 'MOON')
    trion.desc = "This moon has a rich, coppery hue, with swirling patterns of rust-colored dust. The surface is smooth and slightly reflective, giving the moon a warm, metallic sheen."
    trion.save()
    print("Created: Trion")

    # ('valis', 5.3074221959598924e+23, 1877.8007978887429, (2505600136.4279456, 11812129476, 0), trion, orbital_radius=28225.49439132121, orbital_period=230.56025565976728, inclination=0.060171038084127056, obj_type='moon'),
    valis=create_celestial_body('valis', 'moon', 'Valis', 5.3074221959598924e+23, 1877.8007978887429, 2505600136.4279456, 11812129476, 0, trion, 28225.49439132121, 230.56025565976728, 0.060171038084127056, 'MOON')
    valis.desc = "A dense ring of debris and ice surrounds this moon, casting long shadows on its surface. The surface itself is covered in large, dark craters, adding to its mysterious and rugged appearance."
    valis.save()
    print("Created: Valis")

    # ('aster', 3.3717789214321574e+23, 1280.3336255591976, (2505586827.7874007, 11812129476, 0), valis, orbital_radius=14916.853846539996, orbital_period=206.28292914834233, inclination=1.2577069282517055, obj_type='moon'),
    aster=create_celestial_body('aster', 'moon', 'Aster', 3.3717789214321574e+23, 1280.3336255591976, 2505586827.7874007, 11812129476, 0, valis, 14916.853846539996, 206.28292914834233, 1.2577069282517055, 'MOON')
    aster.desc = "This moon is encased in a thick, white fog that diffuses the light, creating a soft, glowing halo. The surface is hidden beneath the fog, giving the moon an enigmatic and ethereal look."
    aster.save()
    print("Created: Aster")

    # ('pheron', 4.737341893614993e+23, 545.1429119351629, (2505585816.125849, 11812129476, 0), aster, orbital_radius=13905.192294485643, orbital_period=331.8156414785358, inclination=1.1769343041865727, obj_type='moon'),
    pheron=create_celestial_body('pheron', 'moon', 'Pheron', 4.737341893614993e+23, 545.1429119351629, 2505585816.125849, 11812129476, 0, aster, 13905.192294485643, 331.8156414785358, 1.1769343041865727, 'MOON')
    pheron.desc = "This moon has a surface covered in massive, jagged rock formations, giving it a rugged and untamed appearance. The rocks are a dark, deep gray, almost black, contrasting sharply with the surrounding space."
    pheron.save()
    print("Created: Pheron")

    # ('jorath_minor', 7.849109150203097e+23, 2909.4322750740043, (2505607589.530842, 11812129476, 0), pheron, orbital_radius=35678.59728789076, orbital_period=419.9071271396031, inclination=0.9001744966516475, obj_type='moon'),
    jorath_minor=create_celestial_body('jorath_minor', 'moon', 'Jorath Minor', 7.849109150203097e+23, 2909.4322750740043, 2505607589.530842, 11812129476, 0, pheron, 35678.59728789076, 419.9071271396031, 0.9001744966516475, 'MOON')
    jorath_minor.desc = "A series of bright, glowing rings encircle this moon, made of fine, icy particles that sparkle in the light. The rings are thin and delicate, adding a touch of elegance to the moon's appearance."
    jorath_minor.save()
    print("Created: Jorath Minor")

    # ('velos_minor', 5.300717593695073e+23, 865.2500112910398, (2505607426.4377217, 11812129476, 0), jorath_minor, orbital_radius=35515.504167521365, orbital_period=18.062580432767056, inclination=1.7335189036331486, obj_type='moon'),
    velos_minor=create_celestial_body('velos_minor', 'moon', 'Velos Minor', 5.300717593695073e+23, 865.2500112910398, 2505607426.4377217, 11812129476, 0, jorath_minor, 35515.504167521365, 18.062580432767056, 1.7335189036331486, 'MOON')
    velos_minor.desc = "This moon's surface is covered in vast, rolling plains of deep purple vegetation. The plants appear to glow faintly, giving the moon a surreal and otherworldly look."
    velos_minor.save()
    print("Created: Velos Minor")

    # ('lynar', 1.6951534406272487e+23, 2283.980833321059, (5677376548.26145, 11812129476, 0), zylath, orbital_radius=19889.810457941127, orbital_period=533.994666581652, inclination=2.21624495446482, obj_type='moon'),
    lynar=create_celestial_body('lynar', 'moon', 'Lynar', 1.6951534406272487e+23, 2283.980833321059, 5677376548.26145, 11812129476, 0, zylath, 19889.810457941127, 533.994666581652, 2.21624495446482, 'MOON')
    lynar.desc = "A network of deep, dark fissures covers this moon, creating a spiderweb-like pattern on its surface. The fissures are filled with a faintly glowing, blue liquid that stands out against the dark rock."
    lynar.save()
    print("Created: Lynar")

    # ('phyra', 1.0700393742003585e+23, 579.0662406846855, (5677397968.504035, 11812129476, 0), lynar, orbital_radius=41310.05304312694, orbital_period=163.4335409950958, inclination=0.7427232271214557, obj_type='moon'),
    phyra=create_celestial_body('phyra', 'moon', 'Phyra', 1.0700393742003585e+23, 579.0662406846855, 5677397968.504035, 11812129476, 0, lynar, 41310.05304312694, 163.4335409950958, 0.7427232271214557, 'MOON')
    phyra.desc = "This moon is covered in a thick layer of bright, white frost, giving it a pristine and almost untouched appearance. The frost sparkles in the light, creating a dazzling effect."
    phyra.save()
    print("Created: Phyra")

    # ('vorin', 5.453664937998748e+23, 1432.4310085928107, (5677385116.62514, 11812129476, 0), phyra, orbital_radius=28458.17414824573, orbital_period=160.7052539810274, inclination=2.1126856764943254, obj_type='moon'),
    vorin=create_celestial_body('vorin', 'moon', 'Vorin', 5.453664937998748e+23, 1432.4310085928107, 5677385116.62514, 11812129476, 0, phyra, 28458.17414824573, 160.7052539810274, 2.1126856764943254, 'MOON')
    vorin.desc = "A swirling, stormy atmosphere of dark green and blue gases surrounds this moon, giving it a dynamic and ever-changing appearance. The clouds are thick and turbulent, with occasional flashes of lightning."
    vorin.save()
    print("Created: Vorin")

    # ('vylar', 3.433477571092572e+22, 1540.2975111190406, (5677379577.614705, 11812129476, 0), vorin, orbital_radius=22919.163713390502, orbital_period=993.975069340963, inclination=2.0694076237345103, obj_type='moon'),
    vylar=create_celestial_body('vylar', 'moon', 'Vylar', 3.433477571092572e+22, 1540.2975111190406, 5677379577.614705, 11812129476, 0, vorin, 22919.163713390502, 993.975069340963, 2.0694076237345103, 'MOON')
    vylar.desc = "This moon has a surface covered in vast, reflective oceans, with only a few small islands breaking the water's surface. The oceans are calm and mirror-like, creating a serene and peaceful appearance."
    vylar.save()
    print("Created: Vylar")

    # ('kryth', 6.307901521377002e+23, 1421.289657937047, (5677358390.756012, 11812129476, 0), vylar, orbital_radius=1732.3050207494164, orbital_period=774.7961828124926, inclination=2.3913094141965323, obj_type='moon'),
    kryth=create_celestial_body('kryth', 'moon', 'Kryth', 6.307901521377002e+23, 1421.289657937047, 5677358390.756012, 11812129476, 0, vylar, 1732.3050207494164, 774.7961828124926, 2.3913094141965323, 'MOON')
    kryth.desc = "A dense, swirling atmosphere of vibrant pinks and purples surrounds this moon, creating a stunning visual effect. The surface beneath the clouds is mostly hidden, but occasional glimpses reveal a rugged, mountainous terrain."
    kryth.save()
    print("Created: Kryth")

    # ('pyris', 5.153452565136836e+23, 2626.355877704714, (237940430.35236692, 11812129476, 0), venoria, orbital_radius=3155.5404336353486, orbital_period=572.8823493111627, inclination=2.4846591245536813, obj_type='moon'),
    pyris=create_celestial_body('pyris', 'moon', 'Pyris', 5.153452565136836e+23, 2626.355877704714, 237940430.35236692, 11812129476, 0, venoria, 3155.5404336353486, 572.8823493111627, 2.4846591245536813, 'MOON')
    pyris.desc = "This moon's surface is covered in vast, reflective salt flats, giving it a brilliant, almost blindingly white appearance from space. Occasional dark mountains break the surface, creating a stark contrast against the salt."
    pyris.save()
    print("Created: Pyris")

    # ('orin', 5.378596242541264e+23, 789.883010020084, (237969649.70134476, 11812129476, 0), pyris, orbital_radius=32374.889411486023, orbital_period=713.5286078446287, inclination=2.596863089961099, obj_type='moon'),
    orin=create_celestial_body('orin', 'moon', 'Orin', 5.378596242541264e+23, 789.883010020084, 237969649.70134476, 11812129476, 0, pyris, 32374.889411486023, 713.5286078446287, 2.596863089961099, 'MOON')
    orin.desc = "Covered in dense, dark forests, this moon has a rich, green appearance from space. Occasional clearings and rivers can be seen breaking the green expanse, adding variety to the landscape."
    orin.save()
    print("Created: Orin")

    # ('xandros', 9.345153253494603e+23, 1778.147953890713, (237941956.69833088, 11812129476, 0), orin, orbital_radius=4681.886397591458, orbital_period=864.2057127834707, inclination=0.902794193020105, obj_type='moon'),
    xandros=create_celestial_body('xandros', 'moon', 'Xandros', 9.345153253494603e+23, 1778.147953890713, 237941956.69833088, 11812129476, 0, orin, 4681.886397591458, 864.2057127834707, 0.902794193020105, 'MOON')
    xandros.desc = "A thick, swirling atmosphere of pale blues and whites gives this moon a serene, almost tranquil appearance. The clouds are soft and billowy, obscuring much of the surface below."
    xandros.save()
    print("Created: Xandros")

    # ('xelis', 8.825027626537393e+23, 2514.577224290146, (237950902.09019086, 11812129476, 0), xandros, orbital_radius=13627.278257590622, orbital_period=274.0054664293921, inclination=1.8702486262873217, obj_type='moon'),
    xelis=create_celestial_body('xelis', 'moon', 'Xelis', 8.825027626537393e+23, 2514.577224290146, 237950902.09019086, 11812129476, 0, xandros, 13627.278257590622, 274.0054664293921, 1.8702486262873217, 'MOON')
    xelis.desc = "This moon's surface is covered in a thick layer of volcanic ash, giving it a dark, almost charcoal-like appearance. Occasional red-hot lava flows can be seen, adding a touch of color to the otherwise dark landscape."
    xelis.save()
    print("Created: Xelis")

    # ('ydris_minor', 8.234887143318166e+23, 1064.2869414615707, (237947136.7755153, 11812129476, 0), xelis, orbital_radius=9861.963582010783, orbital_period=558.0207730114486, inclination=2.2318113330928666, obj_type='moon'),
    ydris_minor=create_celestial_body('ydris_minor', 'moon', 'Ydris Minor', 8.234887143318166e+23, 1064.2869414615707, 237947136.7755153, 11812129476, 0, xelis, 9861.963582010783, 558.0207730114486, 2.2318113330928666, 'MOON')
    ydris_minor.desc = "A dense, rocky surface dotted with massive, jagged peaks gives this moon a rugged and imposing appearance. The rocks are a deep, dark gray, almost black, contrasting sharply with the surrounding space."
    ydris_minor.save()
    print("Created: Ydris Minor")

    # ('zeth', 9.716631347416055e+23, 1735.1929461013988, (9109088851.477371, 11812129476, 0), xerath, orbital_radius=7246.276447971363, orbital_period=234.32829053687254, inclination=1.8607848243187586, obj_type='moon'),
    zeth=create_celestial_body('zeth', 'moon', 'Zeth', 9.716631347416055e+23, 1735.1929461013988, 9109088851.477371, 11812129476, 0, xerath, 7246.276447971363, 234.32829053687254, 1.8607848243187586, 'MOON')
    zeth.desc = "This moon is covered in vast, open plains of golden grass, giving it a warm, inviting appearance. The grass sways gently in the breeze, creating a sense of movement and life."
    zeth.save()
    print("Created: Zeth")

    # ('quara', 9.444463752078005e+23, 1122.87676696562, (9109131505.206276, 11812129476, 0), zeth, orbital_radius=49900.00535216896, orbital_period=28.191758731098776, inclination=1.3178111309172076, obj_type='moon'),
    quara=create_celestial_body('quara', 'moon', 'Quara', 9.444463752078005e+23, 1122.87676696562, 9109131505.206276, 11812129476, 0, zeth, 49900.00535216896, 28.191758731098776, 1.3178111309172076, 'MOON')
    quara.desc = "A thick, swirling atmosphere of dark purple and black gases surrounds this moon, giving it a mysterious and almost sinister appearance. The clouds are dense and turbulent, occasionally illuminated by flashes of lightning."
    quara.save()
    print("Created: Quara")


    ### ADD SPACE STATIONS AND OTHER ORBITTING DEBRIS ################


    # ('pulsar_station', 9.173522570511941e+17, 71.31037594955559, (6184138708.151257, 11812129476, 0), xynar_minor, orbital_radius=1789.3544437240867, orbital_period=66.70109560592341, inclination=0.8481415855692882, obj_type='station'),
    pulsar_station=create_celestial_body('pulsar_station', 'station', 'Pulsar Station', 9.173522570511941e+17, 71.31037594955559, 6184138708.151257, 11812129476, 0, xynar_minor, 1789.3544437240867, 66.70109560592341, 0.8481415855692882, 'STATION')
    pulsar_station.desc = "Resembling an enormous crystal chandelier, the station's spires and arches are illuminated by thousands of tiny lights. Each segment reflects the surrounding starlight, creating a mesmerizing, twinkling effect."
    pulsar_station.save()
    print("Created: Pulsar Station")

    # ('solstice_station', 7.918817600754451e+17, 18.39782185573428, (6690878432.478982, 11812129476, 0), korin, orbital_radius=15194.175650317693, orbital_period=83.71308683065322, inclination=0.531710688031034, obj_type='station'),
    solstice_station=create_celestial_body('solstice_station', 'station', 'Solstice Station', 7.918817600754451e+17, 18.39782185573428, 6690878432.478982, 11812129476, 0, korin, 15194.175650317693, 83.71308683065322, 0.531710688031034, 'STATION')
    solstice_station.desc = "Suspended in the void, the station's translucent dome reveals a thriving ecosystem of alien flora. Vines and tendrils stretch towards the dome's surface, reaching for the distant light of far-off suns."
    solstice_station.save()
    print("Created: Solstice Station")

    # ('titan_spire', 8.805510363353249e+17, 79.43978864709219, (237944727.7254181, 11812129476, 0), venoria, orbital_radius=7452.91348482132, orbital_period=23.313587227265195, inclination=1.3734090174768252, obj_type='station'),
    titan_spire=create_celestial_body('titan_spire', 'station', 'Titan Spire', 8.805510363353249e+17, 79.43978864709219, 237944727.7254181, 11812129476, 0, venoria, 7452.91348482132, 23.313587227265195, 1.3734090174768252, 'STATION')
    titan_spire.desc = "The station's sleek, aerodynamic form is accentuated by its elongated structure, tapering to a point at both ends. Thrusters positioned along its length emit a gentle blue glow, keeping it in a stable orbit."
    titan_spire.save()
    print("Created: Titan Spire")
    
    

    # ('aether_shard', 6.532467908588576e+17, 0.9914977201608149, (2505608471.15473, 11812129476, 0), jorath_minor, orbital_radius=881.6238878187481, orbital_period=14.288056324329428, inclination=1.5939807883269628, obj_type='asteroid'),
    aether_shard=create_celestial_body('aether_shard', 'asteroid', 'Aether Shard', 6.532467908588576e+17, 0.9914977201608149, 2505608471.15473, 11812129476, 0, jorath_minor, 881.6238878187481, 14.288056324329428, 1.5939807883269628, 'ASTEROID')
    aether_shard.desc = "A dark, mysterious presence in the void, this asteroid's surface is shrouded in shadows, revealing little of its secrets to the distant observer."
    aether_shard.save()
    print("Created: Asteroid Aether Shard")

    # ('phos', 5.0913558346775014e+17, 0.37094660559204196, (237939965.76140058, 11812129476, 0), venoria, orbital_radius=2690.949467311735, orbital_period=41.88543887742494, inclination=0.6905183640291452, obj_type='asteroid'),
    phos=create_celestial_body('phos', 'asteroid', 'Phos', 5.0913558346775014e+17, 0.37094660559204196, 237939965.76140058, 11812129476, 0, venoria, 2690.949467311735, 41.88543887742494, 0.6905183640291452, 'ASTEROID')
    phos.desc = "This asteroid is a study in contrasts, with patches of smooth plains juxtaposed against rugged mountains, creating a mesmerizing landscape of textures."
    phos.save()
    print("Created: Asteroid Phos")

    # ('quarion', 6.502950570262525e+17, 0.8716644048974556, (2505609333.063151, 11812129476, 0), velos_minor, orbital_radius=1906.6254291774924, orbital_period=48.40364530110755, inclination=2.1777544724655016, obj_type='asteroid'),
    quarion=create_celestial_body('quarion', 'asteroid', 'Quarion', 6.502950570262525e+17, 0.8716644048974556, 2505609333.063151, 11812129476, 0, velos_minor, 1906.6254291774924, 48.40364530110755, 2.1777544724655016, 'ASTEROID')
    quarion.desc = "Resembling a celestial sculpture, this asteroid features intricate ridges and valleys, carved by the forces of cosmic erosion over countless millennia."
    quarion.save()
    print("Created: Asteroid Quarion")

    # ('tyla', 4.7836607512952826e+17, 0.1549055785156098, (5677402434.035873, 11812129476, 0), phyra, orbital_radius=4465.531838749964, orbital_period=20.589469424643355, inclination=2.9447728410163427, obj_type='asteroid'),
    tyla=create_celestial_body('tyla', 'asteroid', 'Tyla', 4.7836607512952826e+17, 0.1549055785156098, 5677402434.035873, 11812129476, 0, phyra, 4465.531838749964, 20.589469424643355, 2.9447728410163427, 'ASTEROID')
    tyla.desc = "Cloaked in a fine veil of cosmic dust, this asteroid appears hazy and ephemeral, its outline softened by the particles that dance around it in microgravity."
    tyla.save()
    print("Created: Asteroid Tyla")

    # ('ydros', 3.360414162413602e+17, 0.7833292676714906, (5677400904.3598385, 11812129476, 0), phyra, orbital_radius=2935.855803626209, orbital_period=26.793440783166805, inclination=2.5307263857747353, obj_type='asteroid'),
    ydros=create_celestial_body('ydros', 'asteroid', 'Ydros', 3.360414162413602e+17, 0.7833292676714906, 5677400904.3598385, 11812129476, 0, phyra, 2935.855803626209, 26.793440783166805, 2.5307263857747353, 'ASTEROID')
    ydros.desc = "A fiery orb in miniature, this asteroid glows with internal heat, casting a warm, orange hue against the surrounding darkness."
    ydros.save()
    print("Created: Asteroid Ydros")



    print(" ")
    print("Finished generating space objects.")
