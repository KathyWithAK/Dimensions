# Starting Area for Dimensions : creation batch file
# This batch file sets up the initial planets for space
#
# To load the file, use: 
#     reload
#     @py from space.batch_files import S01_Initial_Solar_System; S01_Initial_Solar_System.initialize()
#
# 	 
#  CREATE RECORD
#   @py from world.space.models import SpaceDB; mars=SpaceDB(db_key="mars"); mars.save()
#
#  DELETE RECORD
#   @py from world.space.models import SpaceDB; match=SpaceDB.objects.filter(db_key__exact="mars"); match.delete()
#
#  GET DISTINCT LIST OF SOLAR SYSTEMS
#   @py from world.space.models import SpaceDB; matches=SpaceDB.objects.order_by().values('db_solar_system').distinct(); print(matches)
#
#  GET THE GOD CHARACTER
#   @py from typeclasses.characters import Character; obj=Character.objects.filter(id=1); print(obj)
#
######################################################
#
# Clear the database
#@py from world.space.models import SpaceDB; SpaceDB.objects.delete()
#
# Create the planets
#
#@py from world.space.models import SpaceDB; obj=SpaceDB(db_key="sun", db_category="star", db_name="Sun", db_desc="A space object.", db_mass=0.0, db_distance_from_sun=0, db_orbital_period=0.0); obj.save()
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

    # Clear the existing data
    try:
        for o in SpaceDB.objects.all():
            o.delete()
    except:
        pass


    ### ADD SUNS / STARS #############################################


    #sun = CelestialBody('Sun', 1.989e30, 696340, 0, 0, 0)       
    sun=create_celestial_body('sun', 'star', '|ySun|n', 1.989e30, 696340, 0, 0, 0, None, ascii_art='STAR')
    sun.desc="A mesmerizing sphere of boundless energy, radiating brilliant hues of yellow and white amidst a backdrop of infinite darkness. Its surface, a roiling sea of plasma, dances with tumultuous solar flares and magnetic storms, casting dynamic shadows across the celestial canvas. The star's gravitational influence, felt even from afar, orchestrates the intricate ballet of planets and asteroids, shaping the very fabric of the solar system."
    sun.save()
    print("Created: Sun")


    ### ADD PLANETS ##################################################
    

    #('Mercury', 3.3011e23, 2439.7, 57.91e6, 0, 0, sun, 57.91e6, 88, 7),
    mercury=create_celestial_body('mercury', 'planet', '|xMe|rrc|xur|ry|n', 3.3011e23, 2439.7, 57.91e6, 0, 0, sun, 57.91e6, 88, 7, 'RED_PLANET')
    mercury.desc="A rugged, desolate world, bathed in the unrelenting glare of the nearby sun. Its surface, scarred by countless impact craters and marked by vast plains of volcanic rock, reflects a muted palette of grays and browns. With no appreciable atmosphere to soften the harsh landscape, the stark contrast between sunlit and shadowed regions is starkly evident, showcasing the planet's extreme temperature variations."
    mercury.save()
    print("Created: Mercury")

    #('Venus', 4.8675e24, 6051.8, 108.2e6, 0, 0, sun, 108.2e6, 224.7, 3.4),
    venus=create_celestial_body('venus', 'planet', '|yVe|xnus|n', 4.8675e24, 6051.8, 108.2e6, 0, 0, sun, 108.2e6, 224.7, 3.4, 'GREEN_PLANET')
    venus.desc="The planet presents an otherworldly vista of swirling clouds and intense atmospheric dynamics. The thick blanket of sulfuric acid clouds obscures the surface below, casting the planet in an eerie yellowish hue. Occasional glimpses through the cloud cover reveal a barren, volcanic landscape marked by vast plains and towering mountain ranges. Despite its beauty, the planet's surface is inhospitable, with temperatures soaring high enough to melt lead and crushing atmospheric pressure."
    venus.save()
    print("Created: Venus")

    #earth = CelestialBody('Earth', 5.972e24, 6371, 1.496e8, 0, 0, orbiting_body=sun, orbital_radius=1.496e8, orbital_period=365.25, inclination=7)  # Example inclination of Earth's orbit is about 7 degrees
    earth=create_celestial_body('earth', 'planet', '|bEa|wrth|n', 5.972e24, 6371, 1.496e8, 0, 0, sun, 1.496e8, 365.25, 7, 'BLUE_PLANET')
    earth.desc="The planet presents a mesmerizing spectacle. Swirls of white clouds dance across the vibrant blue oceans and lush green landmasses, creating a mosaic of breathtaking beauty. Flecks of light dot the surface, evidence of bustling cities and human civilization's presence. The atmosphere shimmers with a delicate hue, casting an ethereal glow over the planet's curvature."
    earth.save()
    print("Created: Earth")

    #('Mars', 6.4171e23, 3389.5, 227.9e6, 0, 0, sun, 227.9e6, 687, 1.85),
    mars=create_celestial_body('mars', 'planet', '|rMars|n', 6.4171e23, 3389.5, 227.9e6, 0, 0, sun, 227.9e6, 687, 1.85, 'RED_PLANET')
    mars.desc = "Mars, the enigmatic rust-hued sentinel of our solar system, beckons with the allure of an ancient storyteller, its dusty surface whispering secrets of epochs past. A realm where fiery sunsets paint the horizon in hues unseen on Earth, casting a mesmerizing spell over the rugged landscapes dotted with towering volcanoes and deep chasms. Here, amidst the silent expanse, the echoes of humanity's aspirations resonate, as rovers roam like curious travelers, unraveling the mysteries of this desolate yet captivating world. In the dance of cosmic ballet, Mars stands as a tantalizing enigma, a canvas upon which we project our dreams of exploration, colonization, and perhaps, the echoes of life's persistence beyond our fragile blue cradle. It is a planet of contrasts, where the harshness of its arid plains belies the fragile hope that one day, amidst its dusty dunes, we may find a reflection of ourselves staring back from the vastness of the cosmos."
    mars.save()
    print("Created: Mars")

    #('Jupiter', 1.8982e27, 69911, 778.5e6, 0, 0, sun, 778.5e6, 4333, 1.3),
    jupiter=create_celestial_body('jupiter', 'planet', '|YJu|Rpiter|n', 1.8982e27, 69911, 778.5e6, 0, 0, sun, 778.5e6, 4333, 1.3, 'BLUE_PLANET')
    jupiter.desc = "Jupiter, the behemoth of our solar system, is a celestial marvel that dwarfs all other planets with its immense size and hypnotic swirling storms. It boasts a regal countenance adorned with bands of vivid hues, like strokes of an artist's brush on a cosmic canvas. Its magnetic field, a colossal shield, dances with charged particles, creating auroras that paint the polar skies in ethereal luminescence. Among its retinue of moons, the enigmatic Europa whispers secrets of possible alien oceans beneath its icy crust, tantalizing the imagination with the potential for extraterrestrial life. Jupiter stands as a silent sentinel, a guardian of the outer realms, beckoning us to explore the mysteries of our vast universe."
    jupiter.save()
    print("Created: Jupiter")

    #('Saturn', 5.6834e26, 58232, 1.434e9, 0, 0, sun, 1.434e9, 10759, 2.48),
    saturn=create_celestial_body('saturn', 'planet', '|ySa|xturn|n', 5.6834e26, 58232, 1.434e9, 0, 0, sun, 1.434e9, 10759, 2.48, 'RINGS')
    saturn.desc = "Saturn, the majestic jewel of our celestial neighborhood, dons an ethereal crown of shimmering rings, a cosmic tiara forged from icy particles and rocky debris. Its hypnotic dance around the Sun, a celestial waltz lasting 29 Earth years, mesmerizes astronomers and dreamers alike, as it spins gracefully on its axis, its day a languid 10.7 hours. Beneath its veils of swirling clouds lies a world of mystery and marvels: vast storms that rage for centuries, colossal hurricanes dwarfing our terrestrial tempests, and moons that keep silent vigil over their gas giant sovereign. With its hues of gold, ochre, and sapphire, Saturn stands as a testament to the boundless beauty and complexity of our universe, a celestial marvel worthy of our awe and admiration. As we gaze upon its serene visage through telescopic lenses, we cannot help but ponder the secrets it guards, the stories it whispers across the void, inviting us to journey beyond the confines of our imagination."
    saturn.save()
    print("Created: Saturn")

    #('Uranus', 8.6810e25, 25362, 2.871e9, 0, 0, sun, 2.871e9, 30687, 0.77),
    uranus=create_celestial_body('uranus', 'planet', '|cUr|banus|n', 8.6810e25, 25362, 2.871e9, 0, 0, sun, 2.871e9, 30687, 0.77, 'BLUE_PLANET')
    uranus.desc = "In the depths of our celestial dance, Uranus waltzes on the edge of convention, an enigmatic orb cloaked in icy hues. Its tranquil azure visage conceals a tumultuous heart, where tempests rage in whispered symphonies. Rings, like the ghostly remnants of forgotten dreams, encircle this distant titan, casting shadows that dance in the eternal twilight. Moons, each a silent witness to the cosmic drama, weave intricate tales of gravity's embrace and celestial ballet. Uranus, a celestial recluse in the vast expanse, beckons the curious soul to ponder the mysteries of our cosmic tapestry."
    uranus.save()
    print("Created: Uranus")

    #('Neptune', 1.02413e26, 24622, 4.495e9, 0, 0, sun, 4.495e9, 60190, 1.77),
    neptune=create_celestial_body('neptune', 'planet', '|bNe|Cptune|n', 1.02413e26, 24622, 4.495e9, 0, 0, sun, 4.495e9, 60190, 1.77, 'BLUE_PLANET')
    neptune.desc = "The enigmatic azure giant of our celestial ballet, dances on the outer fringes of our solar system, cloaked in mystery and crowned with storms. Its cobalt hue, a whispered secret of methane and other atmospheric alchemy, captivates the gaze of distant observers. Veiled in swirling veils of clouds, Neptune orchestrates a symphony of winds, boasting the mightiest gusts in the entire solar system. Moons like Triton, its loyal companion, weave tales of icy intrigue as they orbit this icy monarch, trailing whispers of a primordial past. Neptune, a celestial sentinel, stands as a reminder of the boundless wonders awaiting our exploration amidst the infinite depths of space."
    neptune.save()
    print("Created: Neptune")

    #('Pluto', 1.303e22, 1188.3, 5.906e9, 0, 0, sun, 5.906e9, 90560, 17.16)
    pluto=create_celestial_body('pluto', 'planet', '|rPl|buto|n', 1.303e22, 1188.3, 5.906e9, 0, 0, sun, 5.906e9, 90560, 17.16, 'BLUE_PLANET')
    pluto.desc = "In the vast, icy depths of our solar system dances a celestial enigma, Pluto. Once hailed as the ninth planet, it now proudly orbits beyond the traditional boundaries, embodying the resilience of the misunderstood. Wrapped in a cloak of mystery, this dwarf planet tantalizes the curious minds of astronomers, revealing its secrets begrudgingly, like a cosmic sphinx guarding its enigmatic riddles. With a heart of frozen nitrogen beating amidst its rocky terrain, Pluto stands as a testament to the enduring allure of the unknown, beckoning humanity to explore the farthest reaches of our cosmic neighborhood. In its lonely orbit, Pluto whispers tales of ancient collisions, icy plains, and perhaps, hidden depths yet to be unveiled by the intrepid gaze of future explorers."
    pluto.save()
    print("Created: Pluto")


    ### ADD MOONS ####################################################


    #moon = CelestialBody('Moon', 7.342e22, 1737, 1.496e8 + 384400, 0, 0, orbiting_body=earth, orbital_radius=384400, orbital_period=27.32)
    moon=create_celestial_body('moon', 'moon', '|xMoon|n', 7.342e22, 1737, 1.496e8 + 384400, 0, 0, earth, 384400, 27.32, 0, 'MOON')
    moon.desc = "The Moom's rugged terrain tells tales of cosmic collisions and volcanic upheavals, while its mesmerizing phases wax and wane in a timeless celestial ballet. Luna's gravitational embrace influences Earth's tides, weaving a subtle yet powerful connection between our planet and its nocturnal satellite."
    moon.save()
    print("Created: Moon")
    

    #('Phobos', 1.0659e16, 11.267, 227.9e6 + 9376, 0, 0, 'Mars', 9376, 0.319, 1.093),
    phobos=create_celestial_body('phobos', 'moon', '|rPhobos|n', 1.0659e16, 11.267, 227.9e6 + 9376, 0, 0, mars, 9376, 0.319, 1.093, 'MOON')
    phobos.desc = "The larger and closer of Mars' two moons and orbits very close to Mars. Its surface is heavily cratered and appears to be composed of a mixture of rock and regolith. Phobos is gradually spiraling inward towards Mars due to tidal forces and is expected to eventually break apart or crash into the planet."
    phobos.save()
    print("Created: Phobos")

    #('Deimos', 1.4762e15, 6.2, 227.9e6 + 23463, 0, 0, 'Mars', 23463, 1.263, 1.788),
    deimos=create_celestial_body('deimos', 'moon', '|bDeimos|n', 1.4762e15, 6.2, 227.9e6 + 23463, 0, 0, mars, 23463, 1.263, 1.788, 'MOON')
    deimos.desc = "The smaller and outermost moon of Mars, orbitting at a much greater distance from Mars compared to Phobos. Deimos has a smoother surface compared to Phobos, with fewer craters and a covering of dust and regolith. It is believed to be composed of carbon-rich rock, similar to C-type asteroids. Deimos' origin is thought to be from a captured asteroid due to its irregular shape and composition."
    deimos.save()
    print("Created: Deimos")


    #('Io', 8.9319e22, 1821.6, 778.5e6 + 421700, 0, 0, 'Jupiter', 421700, 1.769, 0.036),
    io=create_celestial_body('io', 'moon', '|rI|yo|n', 8.9319e22, 1821.6, 778.5e6 + 421700, 0, 0, jupiter, 421700, 1.769, 0.036, 'MOON')
    io.desc = "Known as Jupiter's 'pizza moon,' Io is a volcanic wonderland, where over 400 active volcanoes paint its surface with vibrant hues of sulfur. Tidal forces from Jupiter and its fellow moons create intense geological activity, making Io the most geologically active object in the solar system. Its surface constantly changes due to the eruptions, creating a surreal landscape reminiscent of a fiery painter's palette."
    io.save()
    print("Created: Io")

    #('Europa', 4.7998e22, 1560.8, 778.5e6 + 671034, 0, 0, 'Jupiter', 671034, 3.551, 0.466),
    europa=create_celestial_body('europa', 'moon', '|wE|buropa|n', 4.7998e22, 1560.8, 778.5e6 + 671034, 0, 0, jupiter, 671034, 3.551, 0.466, 'MOON')
    europa.desc = "An icy moon with a hidden ocean beneath its surface, making it one of the most intriguing places in the search for extraterrestrial life. Its smooth, cracked surface hints at the presence of subsurface water, possibly harboring microbial life in its vast ocean. The unique combination of tidal heating and the presence of liquid water makes Europa a prime candidate for future exploration missions, igniting scientific curiosity about its potential for hosting life beyond Earth."
    europa.save()
    print("Created: Europa")

    #('Ganymede', 1.4819e23, 2634.1, 778.5e6 + 1070412, 0, 0, 'Jupiter', 1070412, 7.155, 0.177),
    ganymede=create_celestial_body('ganymede', 'moon', '|wGan|gymede|n', 1.4819e23, 2634.1, 778.5e6 + 1070412, 0, 0, jupiter, 1070412, 7.155, 0.177, 'MOON')
    ganymede.desc = "The largest moon in the solar system and the only one known to have its own magnetic field, likely generated by a subsurface ocean of saltwater. Its surface displays a fascinating mix of ancient, heavily cratered terrain, as well as younger, grooved regions created by tectonic forces. Ganymede's complex geology and the possibility of a subsurface ocean have made it a target for future exploration, with scientists eager to uncover its secrets and unravel its geological history."
    ganymede.save()
    print("Created: Ganymede")

    #('Callisto', 1.0759e23, 2410.3, 778.5e6 + 1882700, 0, 0, 'Jupiter', 1882700, 16.689, 0.192),
    callisto=create_celestial_body('callisto', 'moon', '|wC|callisto|n', 1.0759e23, 2410.3, 778.5e6 + 1882700, 0, 0, jupiter, 1882700, 16.689, 0.192, 'MOON')
    callisto.desc = "A heavily cratered moon with a surface that preserves a record of impacts dating back billions of years, providing valuable insights into the history of the solar system. Its icy surface is scarred by countless impact craters, giving it a rugged and ancient appearance. Despite its battered exterior, Callisto's subsurface ocean and potential for hosting life have sparked interest among scientists, prompting plans for future exploration missions to delve deeper into its mysteries."
    callisto.save()
    print("Created: Callisto")


    #('Mimas', 3.7493e19, 198.2, 1.434e9 + 185520, 0, 0, 'Saturn', 185520, 0.942, 1.574),
    mimas=create_celestial_body('mimas', 'moon', '|wM|mimas|n', 3.7493e19, 198.2, 1.434e9 + 185520, 0, 0, saturn, 185520, 0.942, 1.574, 'MOON')
    mimas.desc = "Resembling the Death Star from the Star Wars saga, Mimas captivates with its enormous Herschel Crater, which dominates nearly a third of its diameter. This massive impact crater gives Mimas its distinctive appearance, earning it the nickname 'Saturn's Death Star.' Despite its small size, Mimas exerts a gravitational influence that helps shape the intricate patterns of Saturn's rings. Its heavily cratered surface tells a tale of violent cosmic collisions that have shaped the moon over billions of years. Mimas' proximity to Saturn places it in a dynamic orbital dance, contributing to the planet's gravitational symphony."
    mimas.save()
    print("Created: Mimas")
    
    #('Enceladus', 1.0802e20, 252.1, 1.434e9 + 238020, 0, 0, 'Saturn', 238020, 1.370, 0.009),
    enceladus=create_celestial_body('enceladus', 'moon', '|wE|mnceladus|n', 1.0802e20, 252.1, 1.434e9 + 238020, 0, 0, saturn, 238020, 1.370, 0.009, 'MOON')
    enceladus.desc = "This small, icy moon is renowned for its mysterious 'tiger stripe' fractures at its south pole, from which plumes of water vapor and icy particles erupt into space. These geysers suggest the presence of a subsurface ocean, potentially harboring the ingredients necessary for life. Enceladus' bright, reflective surface makes it one of the most reflective bodies in the solar system, dazzling observers with its brilliance. Its icy terrain is adorned with fractures, ridges, and smooth plains, hinting at a complex geological history. Enceladus' enigmatic nature continues to intrigue scientists, spurring plans for future missions to unlock its secrets."
    enceladus.save()
    print("Created: Enceladus")
    
    #('Tethys', 6.1745e20, 531.1, 1.434e9 + 294670, 0, 0, 'Saturn', 294670, 1.888, 1.091),
    tethys=create_celestial_body('tethys', 'moon', '|wT|yethys|n', 6.1745e20, 531.1, 1.434e9 + 294670, 0, 0, saturn, 294670, 1.888, 1.091, 'MOON')
    tethys.desc = "Nicknamed the 'Eyeball Moon' due to its prominent Odysseus Crater, Tethys is a celestial enigma with its mysterious markings resembling a giant eye. Its surface is scarred by a network of fractures, leading to speculation about its turbulent past. Tethys is also home to the massive Ithaca Chasma, a colossal canyon stretching over 1,000 kilometers long and 100 kilometers wide, hinting at violent geological processes."
    tethys.save()
    print("Created: Tethys")
    
    #('Dione', 1.0955e21, 561.4, 1.434e9 + 377400, 0, 0, 'Saturn', 377400, 2.737, 0.019),
    dione=create_celestial_body('dione', 'moon', '|wD|bione|n', 1.0955e21, 561.4, 1.434e9 + 377400, 0, 0, saturn, 377400, 2.737, 0.019, 'MOON')
    dione.desc = "With its icy plains and towering cliffs, Dione is Saturn's 'Frozen Cliffs Moon,' adorned with majestic scarps rising kilometers high. Its surface features a blend of old, cratered terrains and smoother, younger regions, hinting at a complex geological history. Dione's wispy terrain, composed of fine icy particles, adds an ethereal beauty to its landscape, captivating astronomers and artists alike."
    dione.save()
    print("Created: Dione")
    
    #('Rhea', 2.3065e21, 763.8, 1.434e9 + 527040, 0, 0, 'Saturn', 527040, 4.518, 0.345),
    rhea=create_celestial_body('rhea', 'moon', '|wR|mhea|n', 2.3065e21, 763.8, 1.434e9 + 527040, 0, 0, saturn, 527040, 4.518, 0.345, 'MOON')
    rhea.desc = "With its icy surface scarred by numerous impact craters, Rhea exudes a serene beauty against the backdrop of Saturn's rings. This moon harbors a wispy atmosphere composed of oxygen and carbon dioxide, though it's exceedingly thin compared to Earth's atmosphere. Rhea's surface features a network of bright, linear fractures, hinting at past geological activity. Its cratered plains and rugged highlands offer a glimpse into the moon's ancient history, shaped by eons of cosmic bombardment. Rhea's proximity to Saturn grants it a front-row seat to the planet's majestic rings, making it a captivating object of study for astronomers."
    rhea.save()
    print("Created: Rhea")
    
    #('Titan', 1.3452e23, 2574.73, 1.434e9 + 1221870, 0, 0, 'Saturn', 1221870, 15.945, 0.348),
    titan=create_celestial_body('titan', 'moon', '|wT|yitan|n', 1.3452e23, 2574.73, 1.434e9 + 1221870, 0, 0, saturn, 1221870, 15.945, 0.348, 'MOON')
    titan.desc = "As the largest moon of Saturn, Titan boasts an otherworldly atmosphere shrouded in orange haze, reminiscent of Earth's early years. It hosts lakes and rivers of liquid methane and ethane, making it the only celestial body beyond Earth with stable liquid bodies on its surface. Titan's icy crust hides a subsurface ocean of liquid water, raising tantalizing questions about the potential for life in its depths. Its terrain is sculpted by vast dunes of dark hydrocarbons, creating a landscape both alien and captivating. Titan's frigid temperatures and unique chemistry make it a captivating destination for future exploration."
    titan.save()
    print("Created: Titan")
    
    #('Hyperion', 5.62e18, 135, 1.434e9 + 1481000, 0, 0, 'Saturn', 1481000, 21.277, 0.43),
    hyperion=create_celestial_body('hyperion', 'moon', '|wH|yyperion|n', 5.62e18, 135, 1.434e9 + 1481000, 0, 0, saturn, 1481000, 21.277, 0.43, 'MOON')
    hyperion.desc = "Hyperion is a moon of Saturn that defies expectations with its irregular shape and chaotic rotation. Its surface is covered in a jumble of large, crater-like formations, giving it a sponge-like appearance unlike any other moon in the solar system. Hyperion's bizarre topography suggests a violent past, with numerous impacts and gravitational interactions sculpting its rugged terrain over billions of years. Despite its small size, Hyperion stands out as one of the most intriguing moons in the Saturnian system."
    hyperion.save()
    print("Created: Hyperion")
    
    #('Iapetus', 1.8056e21, 734.5, 1.434e9 + 3560820, 0, 0, 'Saturn', 3560820, 79.321, 15.47),
    iapetus=create_celestial_body('iapetus', 'moon', '|wI|mapetus|n', 1.8056e21, 734.5, 1.434e9 + 3560820, 0, 0, saturn, 3560820, 79.321, 15.47, 'MOON')
    iapetus.desc = "Dubbed the 'yin-yang moon' due to its stark color dichotomy, Iapetus presents a mesmerizing sight as one hemisphere is bright while the other is dark. This striking feature is attributed to the accumulation of dark material on one side, possibly from other Saturnian moons or from space dust. Iapetus boasts one of the tallest known mountain ranges in the solar system, towering up to 20 kilometers above its surface. Its heavily cratered landscape hints at a tumultuous past, with impacts shaping its rugged terrain. Iapetus' unique appearance and intriguing geology make it a compelling target for further study."
    iapetus.save()
    print("Created: Iapetus")


    #('Miranda', 6.59e19, 235.8, 2.871e9 + 129900, 0, 0, 'Uranus', 129900, 1.413, 4.232),
    miranda=create_celestial_body('miranda', 'moon', '|wM|biranda|n', 6.59e19, 235.8, 2.871e9 + 129900, 0, 0, uranus, 129900, 1.413, 4.232, 'MOON')
    miranda.desc = "Miranda, the innermost and smallest of Uranus' major moons, captivates with its stark and varied landscapes. Its surface is a patchwork quilt of cliffs, canyons, and bizarre formations, hinting at a turbulent past of geological upheaval. Despite its diminutive size, Miranda boasts one of the tallest known cliffs in the solar system, towering up to 20 kilometers high. Its fractured surface suggests a history of intense tectonic activity, perhaps shaped by gravitational interactions with Uranus and other moons."
    miranda.save()
    print("Created: Miranda")
    
    #('Ariel', 1.353e21, 578.9, 2.871e9 + 190900, 0, 0, 'Uranus', 190900, 2.520, 0.260),
    ariel=create_celestial_body('ariel', 'moon', '|wA|criel|n', 1.353e21, 578.9, 2.871e9 + 190900, 0, 0, uranus, 190900, 2.520, 0.260, 'MOON')
    ariel.desc = "Ariel, one of Uranus' five major moons, presents a study in contrasts with its smooth plains and complex cratered terrain. Its surface, marked by extensive grooves and valleys, hints at a tumultuous past sculpted by both tectonic forces and impacts. The presence of bright, youthful-looking features alongside older, darker regions suggests ongoing geological activity. Ariel's icy surface conceals a subsurface ocean of liquid water, potentially making it a promising target for future exploration in the search for extraterrestrial life."
    ariel.save()
    print("Created: Ariel")
    
    #('Umbriel', 1.172e21, 584.7, 2.871e9 + 266000, 0, 0, 'Uranus', 266000, 4.144, 0.128),
    umbriel=create_celestial_body('umbriel', 'moon', '|wU|mmbriel|n', 1.172e21, 584.7, 2.871e9 + 266000, 0, 0, uranus, 266000, 4.144, 0.128, 'MOON')
    umbriel.desc = "Umbriel, a dark and enigmatic moon of Uranus, entices with its mysterious surface features and ancient, cratered plains. Its heavily cratered terrain suggests a lack of significant geological activity in recent history, preserving a record of impacts dating back billions of years. Dark, nearly featureless regions contrast with bright, cratered areas, hinting at variations in surface composition and history. Umbriel's subdued appearance belies its complex geological past, shaped by impacts, tectonics, and possibly even cryovolcanism."
    umbriel.save()
    print("Created: Umbriel")
    
    #('Titania', 3.527e21, 788.4, 2.871e9 + 436300, 0, 0, 'Uranus', 436300, 8.706, 0.079),
    titania=create_celestial_body('titania', 'moon', '|wT|citania|n', 3.527e21, 788.4, 2.871e9 + 436300, 0, 0, uranus, 436300, 8.706, 0.079, 'MOON')
    titania.desc = "Titania, the largest moon of Uranus, commands attention with its rugged landscapes and icy plains. Its surface is scarred by impact craters, some of which are surrounded by bright ejecta blankets, while others display evidence of tectonic activity. The presence of valleys, ridges, and faults suggests a dynamic history of geological processes, including fracturing and uplift. Titania's surface is also marked by dark, smooth plains, indicating past episodes of cryovolcanism or resurfacing events."
    titania.save()
    print("Created: Titania")
    
    #('Oberon', 3.014e21, 761.4, 2.871e9 + 583500, 0, 0, 'Uranus', 583500, 13.463, 0.068),
    oberon=create_celestial_body('oberon', 'moon', '|wO|cberon|n', 3.014e21, 761.4, 2.871e9 + 583500, 0, 0, uranus, 583500, 13.463, 0.068, 'MOON')
    oberon.desc = "Oberon, the outermost and second-largest moon of Uranus, intrigues with its ancient and heavily cratered surface. Its landscape is a testament to billions of years of impacts, with numerous large craters and rugged terrains dominating its icy plains. Dark, fractured regions contrast with bright, cratered areas, hinting at a complex geological history shaped by impacts and tectonics. Oberon's surface features suggest a lack of significant geological activity in recent epochs, preserving a record of the moon's early evolution and the violent history of the Uranian system."
    oberon.save()
    print("Created: Oberon")


    #('Triton', 2.14e22, 1353.4, 4.495e9 + 354759, 0, 0, 'Neptune', 354759, 5.877, 157.349),
    triton=create_celestial_body('triton', 'moon', '|wT|briton|n', 2.14e22, 1353.4, 4.495e9 + 354759, 0, 0, neptune, 354759, 5.877, 157.349, 'MOON')
    triton.desc = "Triton, Neptune's largest moon, is a celestial oddity dancing to its own tune. Unlike most moons, Triton boasts a retrograde orbit, spinning backward against the flow of its planet's rotation. This icy world is a geologic wonderland, with towering cryovolcanoes spewing nitrogen geysers into its thin atmosphere. It's a frozen time capsule, potentially harboring insights into the early solar system's dynamics and the mysteries of Neptune's past."
    triton.save()
    print("Created: Triton")
    
    #('Nereid', 3.1e19, 170, 4.495e9 + 5513815, 0, 0, 'Neptune', 5513815, 360.14, 7.23),
    nereid=create_celestial_body('nereid', 'moon', '|wN|mereid|n', 3.1e19, 170, 4.495e9 + 5513815, 0, 0, neptune, 5513815, 360.14, 7.23, 'MOON')
    nereid.desc = "Nereid, one of Neptune's most enigmatic moons, is a small, distant wanderer, shrouded in mystery. Orbiting Neptune in an eccentric path, it is thought to be a captured object from the Kuiper Belt, the frigid domain beyond the orbit of Neptune. Its irregular shape hints at a turbulent past, perhaps shaped by cosmic collisions and gravitational perturbations. Nereid remains a tantalizing target for future exploration, promising to unveil secrets about the outer reaches of our solar system and its ancient inhabitants."
    nereid.save()
    print("Created: Nereid")


    #('Charon', 1.586e21, 606, 5.906e9 + 19591, 0, 0, 'Pluto', 19591, 6.387, 0.080),
    charon=create_celestial_body('charon', 'moon', '|wC|bharon|n', 1.586e21, 606, 5.906e9 + 19591, 0, 0, pluto, 19591, 6.387, 0.080, 'MOON')
    charon.desc = "Pluto's largest moon, Charon, is nearly half the size of Pluto itself, making it one of the largest moons in the solar system relative to its parent planet. Its surface is characterized by vast plains, deep canyons, and a prominent chasm called Serenity Chasma, hinting at a complex geological history."
    charon.save()
    print("Created: Charon")
    
    #('Nix', 4.5e17, 49.8, 5.906e9 + 48694, 0, 0, 'Pluto', 48694, 24.854, 0.133),
    nix=create_celestial_body('nix', 'moon', '|wN|gix|n', 4.5e17, 49.8, 5.906e9 + 48694, 0, 0, pluto, 48694, 24.854, 0.133, 'MOON')
    nix.desc = "Another small moon of Pluto, Nix was discovered in 2005 along with its sibling Hydra. Nix's surface displays a reddish hue, likely due to organic compounds called tholins formed by the interaction of solar radiation with methane and nitrogen ice. Its irregular shape and orbit contribute to the dynamic and intriguing nature of Pluto's moon system."
    nix.save()
    print("Created: Nix")
    
    #('Hydra', 4.8e17, 61.6, 5.906e9 + 64738, 0, 0, 'Pluto', 64738, 38.206, 0.242),
    hydra=create_celestial_body('hydra', 'moon', '|wH|gydra|n', 4.8e17, 61.6, 5.906e9 + 64738, 0, 0, pluto, 64738, 38.206, 0.242, 'MOON')
    hydra.desc = "With its chaotic orbit and irregular shape, Hydra roams the frigid expanse of the Pluto system like a cosmic nomad, its presence adding a layer of complexity to the enigmatic dance of moons around the distant dwarf planet. Named after the serpentine creature of Greek mythology, Hydra twists and turns through space, its surface marked by impact craters and icy plains. Despite its diminutive size, Hydra holds a fascination for astronomers, offering insights into the dynamic processes that shaped the outer reaches of our solar system. As it traverses its eccentric path, Hydra serves as a reminder of the mysteries that await discovery in the distant realms beyond the orbit of Neptune."
    hydra.save()
    print("Created: Hydra")
    
    #('Styx', 7.5e15, 5, 5.906e9 + 42656, 0, 0, 'Pluto', 42656, 20.161, 0.815),
    styx=create_celestial_body('styx', 'moon', '|wS|gtyx|n', 7.5e15, 5, 5.906e9 + 42656, 0, 0, pluto, 42656, 20.161, 0.815, 'MOON')
    styx.desc = "One of Pluto's smallest moons, Styx, orbits close to Charon within the Plutonian system. It was discovered in 2012 and is believed to have formed from the debris of a collision between Pluto and another celestial object. Its irregular shape and small size make it a fascinating object for study."
    styx.save()
    print("Created: Styx")
    
    #('Kerberos', 1.65e16, 12, 5.906e9 + 57783, 0, 0, 'Pluto', 57783, 32.167, 0.589)
    kerberos=create_celestial_body('kerberos', 'moon', '|wK|gerberos|n', 1.65e16, 12, 5.906e9 + 57783, 0, 0, pluto, 57783, 32.167, 0.589, 'MOON')
    kerberos.desc = "Like a spectral guardian of the underworld, Kerberos patrols the frigid depths of the Pluto system, its origin shrouded in the mists of cosmic history. Discovered in 2011, this small moon orbits its parent planet amidst the debris of the Kuiper Belt, a testament to the violent past that shaped the outer reaches of our solar system. Kerberos, with its irregular shape and enigmatic surface, stands as a silent witness to the tumultuous events that sculpted the distant realms beyond Neptune. Though small in stature, its presence adds to the rich tapestry of celestial bodies that populate the outskirts of our cosmic neighborhood."
    kerberos.save()
    print("Created: Kerberos")


    ### ADD SPACE STATIONS AND OTHER ORBITTING DEBRIS ################
    

    #('ISS2', 4.2e5, 50, 149.6e6 + 420, 0, 0, 'Earth', 420, 0.067, 51.6),
    iss2=create_celestial_body('iss2', 'station', '|wI|CS|wS|C2|n', 4.2e5, 50, 149.6e6 + 420, 0, 0, earth, 420, 0.067, 51.6, 'STATION')
    iss2.desc="The gleaming metal and glass surfaces of the orbiting station reflect the blue glow of Earth's atmosphere. Pulsating with life and activity, the station's multiple rotating rings create artificial gravity, bustling with spacecraft docking and departing like futuristic bees around a hive. Neon-lit walkways and observation decks offer panoramic views of the cosmos, while energy shields shimmer faintly, protecting the station from space debris. Advanced communication arrays extend from the station like delicate antennas, constantly transmitting data and signals across the galaxy. Beneath the sleek exterior, you can glimpse verdant biomes and hydroponic gardens, showcasing humanity's harmonious blend of nature and technology in the depths of space."
    iss2.save()
    print("Created: ISS2")

    #('LunaBaseAlpha', 7.3e3, 30, 149.6e6 + 384500, 0, 0, 'Moon', 500, 0.5, 0),
    lunabasealpha=create_celestial_body('lunabasealpha', 'station', '|cLunaBase|gAlpha|n', 7.3e3, 30, 149.6e6 + 384500, 0, 0, moon, 500, 0.5, 0, 'STATION')
    lunabasealpha.desc = "The Orbital Lunar Station is a massive, cylindrical structure that serves as a hub for scientific research, exploration, and habitation in the harsh environment of space. Positioned in a stable orbit around the moon, the station's design is a marvel of modern engineering, blending functionality with sustainability to support long-term human presence in space."
    lunabasealpha.save()
    print("Created: LunaBaseAlpha")

    #('MarsStation1', 1.2e4, 40, 227.9e6 + 500, 0, 0, 'Mars', 500, 0.07, 25),
    marsstation1=create_celestial_body('marsstation1', 'station', '|rM|ma|rr|ms|rS|mt|ra|mt|ri|mo|rn|m-|r1|n', 1e9, 500, 227.9e6 + 50000, 0, 0, mars, 50000, 1, 0, 'STATION')
    marsstation1.desc = "A high-tech facility designed for the study and exploration of Mars. It serves as a crucial hub for scientific missions and interplanetary communication."
    marsstation1.save()
    print("Created: MarsStation1 (Derelect Station)") # This is the derelect station we start on

    #('TitanOrbiter', 5.0e3, 25, 1.434e9 + 1200, 0, 0, 'Titan', 1200, 0.1, 0),
    titanorbiter=create_celestial_body('titanorbiter', 'station', '|wTitanOrbiter|n', 5.0e3, 25, 1.434e9 + 1200, 0, 0, titan, 1200, 0.1, 0, 'STATION')
    titanorbiter.desc = "The station is a marvel of human engineering, designed to withstand the harsh conditions of space and the unique challenges posed by orbiting Saturn's largest moon, Titan. The station is a large, multi-segmented structure with a sleek, utilitarian design, constructed from lightweight, durable materials that can endure the intense radiation and extreme temperatures of the Saturnian system."
    titanorbiter.save()
    print("Created: TitanOrbiter")

    #('GanymedeStation', 6.0e3, 35, 778.5e6 + 1000, 0, 0, 'Ganymede', 1000, 0.05, 10),
    ganymedestation=create_celestial_body('ganymedestation', 'station', '|YGanymedeStation|n', 6.0e3, 35, 778.5e6 + 1000, 0, 0, ganymede, 1000, 0.05, 10, 'STATION')
    ganymedestation.desc = "An advanced and sprawling facility designed to support the study and exploration of Ganymede, Jupiter's largest moon. This station is equipped to handle the unique challenges posed by its location in the Jovian system, including intense radiation and extreme cold."
    ganymedestation.save()
    print("Created: GanymedeStation")

    #('EuropaOrbital', 4.5e3, 20, 778.5e6 + 800, 0, 0, 'Europa', 800, 0.03, 15),
    europaorbital=create_celestial_body('europaorbital', 'station', '|MEuropaOrbital|n', 4.5e3, 20, 778.5e6 + 800, 0, 0, europa, 800, 0.03, 15, 'STATION')
    europaorbital.desc = "A station consists of interconnected cylindrical modules arranged around a central core. The exterior is coated with reflective materials to minimize thermal absorption and is built from radiation-resistant alloys to withstand Jupiter's intense radiation. Large, adjustable solar panels extend from the station, optimized to capture sunlight even at this great distance from the Sun. These panels are supplemented by compact nuclear reactors to ensure a stable power supply."
    europaorbital.save()
    print("Created: EuropaOrbital")

    #('IoResearchBase', 3.5e3, 18, 778.5e6 + 500, 0, 0, 'Io', 500, 0.02, 5),
    ioresearchbase=create_celestial_body('ioresearchbase', 'station', '|mIoResearchBase|n', 3.5e3, 18, 778.5e6 + 500, 0, 0, io, 500, 0.02, 5, 'STATION')
    ioresearchbase.desc = "A specialized facility designed to support the study and exploration of Io, Jupiter's most volcanically active moon. Strategically positioned in orbit around Io, this outpost is built to withstand the harsh radiation and intense heat emanating from the moon's surface. The outpost features a modular design composed of interconnected hexagonal modules, each reinforced with heat-resistant, radiation-proof alloys. The exterior is coated with a specialized reflective material to deflect heat and radiation. A towering spire extends from the core of the outpost, topped with a high-resolution observational dome. This dome offers unparalleled views of Io's surface, equipped with advanced sensors and telescopic instruments to monitor volcanic eruptions and lava flows in real time."
    ioresearchbase.save()
    print("Created: IoResearchBase")

    #('NeptuneOrbital', 8.0e3, 50, 4.495e9 + 2000, 0, 0, 'Neptune', 2000, 0.2, 20),
    neptuneorbital=create_celestial_body('neptuneorbital', 'station', '|CNeptuneOrbital|n', 8.0e3, 50, 4.495e9 + 2000, 0, 0, neptune, 2000, 0.2, 20, 'STATION')
    neptuneorbital.desc = "A pioneering station nestled in the far reaches of Neptune's orbit, dedicated to unraveling the mysteries of the cosmos. Unlike traditional research stations, NVDSO is not just a base for scientific endeavors but serves as a bridge between the known and unknown realms of deep space. Radiant energy wells, powered by the subtle energies of the cosmos, provide the station with an abundant and sustainable power source. An enigmatic portal, pulsating with ethereal energies, serves as a gateway to realms beyond comprehension. Though its purpose remains shrouded in mystery, it whispers of untold wonders and hidden dimensions waiting to be explored."
    neptuneorbital.save()
    print("Created: NeptuneOrbital")

    #('UranusResearch', 7.0e3, 45, 2.871e9 + 1500, 0, 0, 'Uranus', 1500, 0.15, 10),
    uranusresearch=create_celestial_body('uranusresearch', 'station', '|bUranusResearch|n', 7.0e3, 45, 2.871e9 + 1500, 0, 0, uranus, 1500, 0.15, 10, 'STATION')
    uranusresearch.desc = "A cutting-edge facility positioned in orbit around Uranus, dedicated to the exploration and study of this enigmatic ice giant and its moons. Constructed from advanced composite materials, the structure is engineered to withstand the extreme cold, radiation, and gravitational forces present in Uranus' orbit. Equipped with an array of high-gain antennas and communication dishes, the outpost maintains constant communication with Earth and other spacecraft."
    uranusresearch.save()
    print("Created: UranusResearch")

    #('SaturnStation', 6.5e3, 40, 1.434e9 + 1000, 0, 0, 'Saturn', 1000, 0.1, 5),
    saturnstation=create_celestial_body('saturnstation', 'station', '|[xS|[Ca|[xt|[Cu|[xr|[Cn|[xS|[Ct|[xa|[Ct|[xi|[Co|[xn|n', 6.5e3, 40, 1.434e9 + 1000, 0, 0, saturn, 1000, 0.1, 5, 'STATION')
    saturnstation.desc = "A mystical haven nestled within the rings of Saturn, blending advanced technology with ancient secrets. It serves as a sanctuary for scholars, mystics, and explorers seeking to unravel the cosmic mysteries surrounding the enigmatic gas giant. Within the station's confines lies a verdant sanctuary, a lush grove nurtured by the arcane energies coursing through the station. Fragrant blossoms and exotic flora thrive amidst the crystalline structures, offering respite to weary travelers."
    saturnstation.save()
    print("Created: SaturnStation")

    #('PlutoOrbital', 2.0e3, 15, 5.906e9 + 800, 0, 0, 'Pluto', 800, 0.1, 0),
    plutoorbital=create_celestial_body('plutoorbital', 'station', '|YPlutoOrbital|n', 2.0e3, 15, 5.906e9 + 800, 0, 0, pluto, 800, 0.1, 0, 'STATION')
    plutoorbital.desc = "Positioned in orbit around Pluto, this station serves as a base for scientific exploration and discovery in one of the most remote and enigmatic corners of the universe. Despite the dim sunlight at Pluto's distance, the station harnesses power from both advanced solar arrays and compact radioisotope thermoelectric generators to ensure uninterrupted operation. The solar arrays feature cutting-edge photovoltaic cells optimized for low-light conditions. Rising from the core of the outpost, an observation tower offers unobstructed views of Pluto's icy surface, its enigmatic atmosphere, and the distant stars."
    plutoorbital.save()
    print("Created: PlutoOrbital")

    #('CharonStation', 1.8e3, 10, 5.906e9 + 800 + 200, 0, 0, 'Charon', 200, 0.05, 0)
    charonstation=create_celestial_body('charonstation', 'station', '|xCharonStation|n', 1.8e3, 10, 5.906e9 + 800 + 200, 0, 0, charon, 200, 0.05, 0, 'STATION')
    charonstation.desc = "A pioneering facility designed to study the geology, atmosphere, and potential habitability of Charon, the largest moon of Pluto. The outpost serves as a critical hub for deep space research and interplanetary exploration. A reinforced, transparent dome atop the central core provides stunning views of Charon's rugged surface and the distant dwarf planet Pluto. The dome is equipped with powerful telescopic lenses and spectrometers for detailed observation and analysis."
    charonstation.save()
    print("Created: CharonStation")



    asteroid_ceres=create_celestial_body('ceres', 'asteroid', '|CCeres|n', 9.393e20, 473, 2.770e8, -3.964e7, -1.628e7, sun, 4.1439e8, 1680, 10.6, 'ASTEROID')
    asteroid_ceres.desc = "The asteroid appears as a massive, rough-hewn jewel, its surface glittering with crystalline deposits. Jagged mountains and deep, shadowy craters give the asteroid an ancient and majestic appearance. Occasionally, brilliant streaks of meteor showers skim past its rugged terrain, adding a touch of ephemeral beauty. The asteroid’s surface is pockmarked with impact scars, testament to countless collisions over eons. A faint, eerie luminescence seems to emanate from its core, casting an otherworldly glow."
    asteroid_ceres.save()
    print("Created: Asteroid Ceres")

    asteroid_pallas=create_celestial_body('pallas', 'asteroid', '|CPallas|n', 2.11e20, 256, 3.140e8, -1.667e8, -5.137e7, sun, 4.1439e8, 1686, 34.8, 'ASTEROID')
    asteroid_pallas.desc = "The rock's icy exterior sparkles like a diamond under the distant sun. Vast, frozen lakes stretch across its surface, surrounded by towering ice cliffs that glisten in the light. Wisps of vapor escape from hidden geysers, creating a delicate, ephemeral mist. The asteroid's surface is a palette of blues and whites, interrupted by dark, shadowy crevices. In the far distance, a gentle aurora dances across the thin atmosphere, adding a surreal beauty to the icy expanse."
    asteroid_pallas.save()
    print("Created: Asteroid Pallas")

    asteroid_vesta=create_celestial_body('vesta', 'asteroid', '|CVesta|n', 2.5907e20, 262.7, 3.219e8, -1.527e8, -7.360e7, sun, 3.5305e8, 1325, 7.1, 'ASTEROID')
    asteroid_vesta.desc = "A colossal rock with veins of glowing minerals crisscrossing its surface. Its rugged landscape is dotted with towering spires and deep ravines, giving it a formidable appearance. Occasional bursts of light from volcanic activity illuminate the dark crevices, casting flickering shadows. The asteroid's surface is covered in a fine layer of reddish dust, reminiscent of rusted iron. In the darkness of space, Prometheus glows with an internal fire, hinting at the geothermal forces at play within."
    asteroid_vesta.save()
    print("Created: Asteroid Vesta")

    asteroid_hygiea=create_celestial_body('hygiea', 'asteroid', '|CHygiea|n', 8.32e19, 215, -3.418e8, 1.779e8, -1.492e7, sun, 4.6974e8, 2030, 3.8, 'ASTEROID')
    asteroid_hygiea.desc = "The rock is a mesmerizing blend of vibrant colors and intricate patterns. Its surface is covered in swirling, iridescent dust, reflecting the sunlight in a kaleidoscope of hues. Massive crystal formations rise from its plains, sparkling like gemstones. Deep chasms crisscross the asteroid, their depths hidden in shadow. An ethereal mist floats above the ground, shimmering with a faint, otherworldly glow."
    asteroid_hygiea.save()
    print("Created: Asteroid Hygiea")

    asteroid_eunomia=create_celestial_body('eunomia', 'asteroid', '|CEunomia|n', 3.12e19, 136, -2.340e8, 2.832e8, 1.245e7, sun, 3.9494e8, 1572, 11.7, 'ASTEROID')
    asteroid_eunomia.desc = "The rock appears as a serene, almost tranquil body, with smooth plains interrupted by gently rolling hills. Its surface is covered in a fine, silver-grey dust that seems to absorb light, giving it a soft, muted appearance. Small, frozen pools of liquid methane glisten in the sunlight, surrounded by delicate frost patterns. The asteroid's surface is dotted with clusters of alien flora, bioluminescent and softly pulsing. Occasional, gentle winds stir the dust, creating ghostly, swirling patterns."
    asteroid_eunomia.save()
    print("Created: Asteroid Eunomia")

    asteroid_psyche=create_celestial_body('psyche', 'asteroid', '|CPsyche|n', 2.27e19, 112, 2.922e8, -2.207e8, -1.043e7, sun, 4.3683e8, 1823, 3.1, 'ASTEROID')
    asteroid_psyche.desc = "A chaotic landscape of sharp contrasts, with towering cliffs and deep, shadow-filled valleys. Its surface is marked by massive craters, some filled with strange, luminescent liquids that glow faintly in the dark. The asteroid is constantly bombarded by meteoroids, creating a dynamic, ever-changing terrain. Jagged rock formations protrude from the ground, casting long, eerie shadows. A thin atmosphere, barely perceptible, creates wisps of cloud that drift lazily across the surface."
    asteroid_psyche.save()
    print("Created: Asteroid Psyche")

    asteroid_aether=create_celestial_body('aether', 'asteroid', '|CAether|n', 1.5e12, 5, 1200, -850, 400, europa, 10500, 0.625, 5, 'ASTEROID')   
    asteroid_aether.desc = "A dark and mysterious presence, its surface almost entirely devoid of light. Occasional flashes of distant starlight reveal a rugged landscape of sharp ridges and deep canyons. The asteroid's surface is covered in a dark, almost black, dust that absorbs nearly all light. Strange, luminescent fungi cling to the shadowy recesses, casting an eerie, bioluminescent glow. The silence and darkness of Nyx are profound, creating an atmosphere of deep, cosmic solitude."
    asteroid_aether.save()
    print("Created: Asteroid Aether")

    asteroid_glacius=create_celestial_body('glacius', 'asteroid', '|CGlacius|n', 2.2e11, 3, -650, 1300, -200, enceladus, 8200, 0.5, 2, 'ASTEROID')
    asteroid_glacius.desc = "The rock shines brightly, its surface covered in reflective metals and glimmering solar panels from ancient probes. The asteroid is dotted with numerous small craters, each one filled with a liquid that shimmers like molten gold. Its landscape is a mix of smooth plains and rugged, rocky outcrops. A thin ring of dust and debris orbits Helios, catching the sunlight and creating a halo effect. The overall impression is one of a celestial body bathed in perpetual light and energy."
    asteroid_glacius.save()
    print("Created: Asteroid Glacius")

    asteroid_vulcan=create_celestial_body('vulcan', 'asteroid', '|CVulcan|n', 3.8e12, 6, 900, -700, 500, io, 11000, 0.583333, 7, 'ASTEROID')
    asteroid_vulcan.desc = "The rock is a serene and tranquil sight, its surface covered in soft, white regolith that reflects the sunlight beautifully. Gentle hills and shallow craters give the asteroid a gentle, rolling appearance. The surface is dotted with tiny, reflective particles that sparkle like stars. Occasional gusts of space wind stir the surface dust, creating delicate, swirling patterns. It seems to exude a calm, peaceful energy, a quiet haven in the vastness of space."
    asteroid_vulcan.save()
    print("Created: Asteroid Vulcan")

    asteroid_boreas=create_celestial_body('boreas', 'asteroid', '|CBoreas|n', 1.1e12, 4, -300, 1500, 600, titan, 15500, 0.75, 4, 'ASTEROID')
    asteroid_boreas.desc = "A massive, imposing presence, with a surface covered in jagged, metallic rocks. Deep, dark canyons crisscross the landscape, their depths filled with strange, glowing gases. The asteroid's surface is marked by large, circular impact craters, each one a testament to its violent history. Occasional outbursts of electrical discharges illuminate the canyons, casting flickering shadows. Titania’s rugged beauty is both awe-inspiring and intimidating."
    asteroid_boreas.save()
    print("Created: Asteroid Boreas")

    asteroid_thalassa=create_celestial_body('thalassa', 'asteroid', '|CThalassa|n', 2.5e12, 5, 1100, -900, -300, ganymede, 12000, 0.666667, 6, 'ASTEROID')
    asteroid_thalassa.desc = "A hauntingly beautiful sight, its surface covered in ancient, weathered rock formations. Deep, shadowy craters are filled with a strange, greenish mist that glows faintly in the dark. The asteroid's surface is marked by long, sinuous ridges that twist and turn like ancient riverbeds. Scattered across the landscape are strange, alien structures, remnants of an unknown civilization. The air of mystery and ancient history makes it a fascinating and enigmatic presence."
    asteroid_thalassa.save()
    print("Created: Asteroid Thalassa")

    asteroid_hades=create_celestial_body('hades', 'asteroid', '|CHades|n', 4.3e12, 7, 950, 750, 450, callisto, 13500, 0.708333, 3, 'ASTEROID')
    asteroid_hades.desc = "A vibrant and colorful world, its surface covered in strange, bioluminescent vegetation. The asteroid's landscape is a mix of lush, green valleys and towering, crystalline mountains. Deep, clear lakes dot the surface, their waters glowing with an inner light. Strange, alien creatures can occasionally be seen moving through the foliage, their forms outlined in bioluminescent hues. Pandora is a world of wonder and life, a small oasis in the vastness of space."
    asteroid_hades.save()
    print("Created: Asteroid Hades")




    print(" ")
    print("Finished generating inital space objects.")


"""

# Define the Sun and planets
sun = CelestialBody('Sun', 1.989e30, 696340, 0, 0, 0)
    ('Mercury', 3.3011e23, 2439.7, 57.91e6, 0, 0, sun, 57.91e6, 88, 7),
    ('Venus', 4.8675e24, 6051.8, 108.2e6, 0, 0, sun, 108.2e6, 224.7, 3.4),
    ('Earth', 5.972e24, 6371, 149.6e6, 0, 0, sun, 149.6e6, 365.25, 0),
    ('Moon', 7.342e22, 1737, 149.6e6 + 384400, 0, 0, 'Earth', 384400, 27.32, 5.145),
    ('Mars', 6.4171e23, 3389.5, 227.9e6, 0, 0, sun, 227.9e6, 687, 1.85),
    ('Phobos', 1.0659e16, 11.267, 227.9e6 + 9376, 0, 0, 'Mars', 9376, 0.319, 1.093),
    ('Deimos', 1.4762e15, 6.2, 227.9e6 + 23463, 0, 0, 'Mars', 23463, 1.263, 1.788),
    ('Jupiter', 1.8982e27, 69911, 778.5e6, 0, 0, sun, 778.5e6, 4333, 1.3),
    ('Io', 8.9319e22, 1821.6, 778.5e6 + 421700, 0, 0, 'Jupiter', 421700, 1.769, 0.036),
    ('Europa', 4.7998e22, 1560.8, 778.5e6 + 671034, 0, 0, 'Jupiter', 671034, 3.551, 0.466),
    ('Ganymede', 1.4819e23, 2634.1, 778.5e6 + 1070412, 0, 0, 'Jupiter', 1070412, 7.155, 0.177),
    ('Callisto', 1.0759e23, 2410.3, 778.5e6 + 1882700, 0, 0, 'Jupiter', 1882700, 16.689, 0.192),
    ('Saturn', 5.6834e26, 58232, 1.434e9, 0, 0, sun, 1.434e9, 10759, 2.48),
    ('Mimas', 3.7493e19, 198.2, 1.434e9 + 185520, 0, 0, 'Saturn', 185520, 0.942, 1.574),
    ('Enceladus', 1.0802e20, 252.1, 1.434e9 + 238020, 0, 0, 'Saturn', 238020, 1.370, 0.009),
    ('Tethys', 6.1745e20, 531.1, 1.434e9 + 294670, 0, 0, 'Saturn', 294670, 1.888, 1.091),
    ('Dione', 1.0955e21, 561.4, 1.434e9 + 377400, 0, 0, 'Saturn', 377400, 2.737, 0.019),
    ('Rhea', 2.3065e21, 763.8, 1.434e9 + 527040, 0, 0, 'Saturn', 527040, 4.518, 0.345),
    ('Titan', 1.3452e23, 2574.73, 1.434e9 + 1221870, 0, 0, 'Saturn', 1221870, 15.945, 0.348),
    ('Hyperion', 5.62e18, 135, 1.434e9 + 1481000, 0, 0, 'Saturn', 1481000, 21.277, 0.43),
    ('Iapetus', 1.8056e21, 734.5, 1.434e9 + 3560820, 0, 0, 'Saturn', 3560820, 79.321, 15.47),
    ('Uranus', 8.6810e25, 25362, 2.871e9, 0, 0, sun, 2.871e9, 30687, 0.77),
    ('Miranda', 6.59e19, 235.8, 2.871e9 + 129900, 0, 0, 'Uranus', 129900, 1.413, 4.232),
    ('Ariel', 1.353e21, 578.9, 2.871e9 + 190900, 0, 0, 'Uranus', 190900, 2.520, 0.260),
    ('Umbriel', 1.172e21, 584.7, 2.871e9 + 266000, 0, 0, 'Uranus', 266000, 4.144, 0.128),
    ('Titania', 3.527e21, 788.4, 2.871e9 + 436300, 0, 0, 'Uranus', 436300, 8.706, 0.079),
    ('Oberon', 3.014e21, 761.4, 2.871e9 + 583500, 0, 0, 'Uranus', 583500, 13.463, 0.068),
    ('Neptune', 1.02413e26, 24622, 4.495e9, 0, 0, sun, 4.495e9, 60190, 1.77),
    ('Triton', 2.14e22, 1353.4, 4.495e9 + 354759, 0, 0, 'Neptune', 354759, 5.877, 157.349),
    ('Nereid', 3.1e19, 170, 4.495e9 + 5513815, 0, 0, 'Neptune', 5513815, 360.14, 7.23),
    ('Pluto', 1.303e22, 1188.3, 5.906e9, 0, 0, sun, 5.906e9, 90560, 17.16),
    ('Charon', 1.586e21, 606, 5.906e9 + 19591, 0, 0, 'Pluto', 19591, 6.387, 0.080),
    ('Nix', 4.5e17, 49.8, 5.906e9 + 48694, 0, 0, 'Pluto', 48694, 24.854, 0.133),
    ('Hydra', 4.8e17, 61.6, 5.906e9 + 64738, 0, 0, 'Pluto', 64738, 38.206, 0.242),
    ('Styx', 7.5e15, 5, 5.906e9 + 42656, 0, 0, 'Pluto', 42656, 20.161, 0.815),
    ('Kerberos', 1.65e16, 12, 5.906e9 + 57783, 0, 0, 'Pluto', 57783, 32.167, 0.589)

# Define fictional space stations
    ('ISS2', 4.2e5, 50, 149.6e6 + 420, 0, 0, 'Earth', 420, 0.067, 51.6),
    ('LunaBaseAlpha', 7.3e3, 30, 149.6e6 + 384500, 0, 0, 'Moon', 500, 0.5, 0),
    ('MarsStation1', 1.2e4, 40, 227.9e6 + 500, 0, 0, 'Mars', 500, 0.07, 25),
    ('TitanOrbiter', 5.0e3, 25, 1.434e9 + 1200, 0, 0, 'Titan', 1200, 0.1, 0),
    ('GanymedeStation', 6.0e3, 35, 778.5e6 + 1000, 0, 0, 'Ganymede', 1000, 0.05, 10),
    ('EuropaOrbital', 4.5e3, 20, 778.5e6 + 800, 0, 0, 'Europa', 800, 0.03, 15),
    ('IoResearchBase', 3.5e3, 18, 778.5e6 + 500, 0, 0, 'Io', 500, 0.02, 5),
    ('NeptuneOrbital', 8.0e3, 50, 4.495e9 + 2000, 0, 0, 'Neptune', 2000, 0.2, 20),
    ('UranusResearch', 7.0e3, 45, 2.871e9 + 1500, 0, 0, 'Uranus', 1500, 0.15, 10),
    ('SaturnStation', 6.5e3, 40, 1.434e9 + 1000, 0, 0, 'Saturn', 1000, 0.1, 5),
    ('PlutoOrbital', 2.0e3, 15, 5.906e9 + 800, 0, 0, 'Pluto', 800, 0.1, 0),
    ('CharonStation', 1.8e3, 10, 5.906e9 + 800 + 200, 0, 0, 'Charon', 200, 0.05, 0)

"""    