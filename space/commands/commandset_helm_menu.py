import evennia 
from evennia import Command

class CmdHelmMenu(Command):
    """
    Usage:

        controls / menu <section>

        Display the helm menu. You can list by section (GEN, NAV, ENG, COM, TAC, SCI)
        or you can exclude the <section> and see the entire menu.
    """
    key = "controls"
    aliases = ["menu"]
    help_category = "Space"

    import evennia.utils.ansi

    def func(self):
        # Ship Object
        ship = "None"
        if self.obj.db.ship_obj:
            ship_results = evennia.search_object(self.obj.db.ship_obj)
            if ship_results:
                ship = evennia.utils.ansi.strip_ansi(ship_results[0].name)

        # Ship Zone
        ship_zone = "None"
        if self.obj.db.ship_zone:
            ship_zone = self.obj.db.ship_zone.strip()

        # Engine Object
        engine = "None"
        engine_brand = "None"
        if self.obj.db.engine_obj:
            engine_results = evennia.search_object(self.obj.db.engine_obj)
            if engine_results:
                engine = f"{engine_results[0].name} ({engine_results[0].engine_status['desc']})"
                engine_brand = engine_results[0].db.brand

        # Define Menu

                        
        menu_header = (f"""
 .----------------> Helm Menu <-------------------------------------------------------.""")

        menu_gen = (f"""
 | |yGeneral                                                            |c{int(self.obj.db.power_to_gen):3d}% Allocation |n|
 |                                                                                    |
 |    Broadcast <msg> - Send a zone-wide message from the helm                        |
 '------------------------------------------------------------------------------------'""")                                           

        menu_nav = (f"""
 | |yNavigation                                                         |c{int(self.obj.db.power_to_nav):3d}% Allocation |n|
 |                                                                                    |
 |         Dock       - Enter ship/station docking bay                                |
 |         Undock     - Exit ship/station docking bay                                 |
 |         Plot       - Use to plot complex solutions for travel across space         |
 |                      /coord - Plot by specifying destination coords                |
 |                      /dist - Plot by specifying dist.(km), bearing & pitch         |
 |         Bearing #  - Set the ship's bearing                                        |
 |         Pitch #    - Set the ship's pitch                                          |
 |         Burn #     - Fire the ships main engines (in Newtons per Update)           |
 |         Retro #    - Fire the ships retro rockets (in Newtons per Update)          |
 |         Course xyz - Set the ship's course. xyz are broken into                    |
 |                      heading, bearing, & pitch                                     |
 '------------------------------------------------------------------------------------'""")   

        menu_sci = (f"""
 | |ySciences                                                           |c{int(self.obj.db.power_to_sci):3d}% Allocation |n|
 |                                                                                    |
 |       Sweep / Scan - Allocate energy from the engine to a given system to increase |
 |            History - Display a list of contacts in the helm database               |
 |             Recall - Call up the most recent, detailed information that was        |
 |                      aquired from the contact.                                     |
 '------------------------------------------------------------------------------------'""")   


        menu_eng = (f"""
 | |yEngineering                                                        |c{int(self.obj.db.power_to_eng):3d}% Allocation |n|
 |                                                                                    |
 | Allocate <SEC>=<%> - Allocate energy from the engine to a given system to increase |
 |                      performance/range. Sections are:  GEN, NAV, ENG, COM, TAC     |
 |       Engine-Start - Start the ship's engine. Output will be set to 100%           |
 |        Engine-Stop - Stop the ship's engine. Output will be set to 0%.             |
 |     Engine-Standby - Put the ship's engine on standby. Output will be set to 50%.  |
 '------------------------------------------------------------------------------------'""")   
        
        menu_com = (f"""
 | |yCommunications                                                     |c{int(self.obj.db.power_to_com):3d}% Allocation |n|
 '------------------------------------------------------------------------------------'""")   
        
        menu_tac = (f"""
 | |yTactical                                                           |c{int(self.obj.db.power_to_tac):3d}% Allocation |n|
 |                                                                                    |
 |               View - Look at the viewscreen, which can display objects within      |
 |                      four miles while in space. While docked, it displays the      |
 |                      contents of location                                          |
 |         View <obj> - Look at a specific object on viewscreen within four miles     |
 |                      while in space. While docked, it displays an object in        |
 |                      current location                                              |
 |           Tactical - Display a 2D respresentation of space around the ship         |
 '------------------------------------------.-----------------------------------------'""")   

        menu_footer = (f"""
 |      |wShip:|n {ship:<29s} | |wEngine:|n {engine:<31s} |
 | |wShip Zone:|n {ship_zone:<29s} |  |wBrand:|n {engine_brand:<31s} |
 '------------------------------------------'-----------------------------------------'
                        """)       

        # Draw Menu
        menu = menu_header

        if not self.args:
            menu += menu_gen
            menu += menu_nav
            menu += menu_sci
            menu += menu_eng
            menu += menu_com
            menu += menu_tac
        elif self.args.strip().upper() == 'GEN':
            menu += menu_gen
        elif self.args.strip().upper() == 'NAV':
            menu += menu_nav
        elif self.args.strip().upper() == 'SCI':
            menu += menu_sci
        elif self.args.strip().upper() == 'ENG':
            menu += menu_eng
        elif self.args.strip().upper() == 'COM':
            menu += menu_com
        elif self.args.strip().upper() == 'TAC':
            menu += menu_tac                        

        menu += menu_footer
        self.caller.msg(menu)
