"""
		--- GALAXY ---

A multiplayer game of exploration, building, and conquering

"""




########################################################################################
#---IMPORT MODULES
########################################################################################
from random import randint
from random import sample
from random import choice
from time import sleep
from copy import deepcopy

# since termcolor isn't a standard module, warn users who don't have it
try:
	from termcolor import colored, cprint
	#examples:
	# print colored('hello', 'red'), colored('world', 'green')
	# cprint("Hello World!", 'red', attrs=['bold'])
except ImportError:
	print "the python module 'termcolor' must be installed to use this program.  Please download and install, and try again."


import os 	#To clear the screen (inserts a page of black space) 	--> os.system('clear')
			#To clear terminal (delete current terminal commands)	--> os.system('tput reset')
			#To clear scrollback buffer, press CMD+K on keyboard... --> os.system("clear && printf '\e[3J' ")


#some special characters...
degree_symbol = unichr(176)		#For binary planet in solar system view




########################################################################################
#---DEFINE VARIABLES, LISTS, AND DICTIONARIES
########################################################################################

# Victory condition number (number of planets colonized to win)
victory_condition = 6



# Player starting resources
start_minerals = 1500
start_gas = 1500

# Cost to build a ship
ship_cost_minerals = 200
ship_cost_gas = 200

# Selling a ship
ship_sell_minerals = 50
ship_sell_gas = 50

# Cost to move a ship
ship_move_minerals = 0
ship_move_gas = 50

# Cost to defend a sector (attack all enemy ships)
ship_attack_minerals = 100
ship_attack_gas = 150

# Cost to build a colony
colony_cost_minerals = 700
colony_cost_gas = 800

# Cost to colonize a planet
colonize_cost_minerals = colony_cost_minerals * 1.2
colonize_cost_gas = colony_cost_gas * 1.5

# Selling a colony
colony_sell_minerals = 200
colony_sell_gas = 100

# Cost per colony for invading
colony_invade_minerals = 300
colony_invade_gas = 300

# Each player scavenges a bit of resources each turn
scavenge_minerals = 50
scavenge_gas = 50



# Maximum colony number per planet size
max_colonies = 	{ 	"Small" 	: 1,
					"Medium" 	: 2,
					"Large" 	: 4,
					"Binary" 	: 2
				}
colony_symbol = "###"




# GAME PLAYERS (up to 4)

#list of possible colors (randomized when defining players)
player_colors = ['red', 'cyan', 'magenta', 'yellow']

Players = {
			"P1" : {
				"name" : 'Kevin',	#just a placeholder name -- will change at game start
				"color" : player_colors.pop( randint( 0 , len(player_colors)-1) ), #random color
				"minerals" : start_minerals,
				"gas" : start_gas,
				"colonies" : {}, 
				"planets_colonized" : 0,
				"ships" : {"total_ships" : 0, "sectors" : [] }
				},

			"P2" : {
				"name" : 'Kara',	#just a placeholder name -- will change at game start
				"color" : player_colors.pop( randint( 0 , len(player_colors)-1) ), #random color
				"minerals" : start_minerals,
				"gas" : start_gas,
				"colonies" : {},
				"planets_colonized" : 0,
				"ships" : {"total_ships" : 0, "sectors" : [] }
				},

			"P3" : {
				"name" : 'Yosei',	#just a placeholder name -- will change at game start
				"color" : player_colors.pop( randint( 0 , len(player_colors)-1) ), #random color
				"minerals" : start_minerals,
				"gas" : start_gas,
				"colonies" : {},
				"planets_colonized" : 0,
				"ships" : {"total_ships" : 0, "sectors" : [] }
				},

			"P4" : {
				"name" : 'Chris',	#just a placeholder name -- will change at game start
				"color" : player_colors.pop( randint( 0 , len(player_colors)-1) ), #random color
				"minerals" : start_minerals,
				"gas" : start_gas,
				"colonies" : {},
				"planets_colonized" : 0,
				"ships" : {"total_ships" : 0, "sectors" : [] }
				}

}


#for cycling through to get current_player
#starts with "P4" because it will move it to the end each turn (including first turn)
player_list = ["P1", "P2", "P3", "P4"]


# Stars in 6 different sectors
map_size = 9 #number of sectors
Stars = {
	# "star_location" : '',
	# "planet_number" : '',
	# "planet_locations" : [],
	# "planets" : {	"2" : {	"location" : ''
	# 						"size" : '',
	# 						"type" : '',
	# 						"color" : '',
	# 						"zone" : '',
	# 						"minerals" : ,
	# 						"gas" : ,
	# 						"name" : '',
	# 						"colonies" : {}
	# 						}
	# # 				"6" : {}
	# },

	"0" : {}, #
	"1" : {},
	"2" : {},
	"3" : {},
	"4" : {},
	"5" : {},
	"6" : {},
	"7" : {},
	"8" : {}
}

# Planet attributes (to randomly call from using random.choice(LIST) )
planet_sizes 	= ['Small', 'Medium', 'Large', 'Binary']
planet_types 	= ['Rocky', 'Rocky', 'Gas', 'Frozen', 'Frozen', 'Liquid', 'Volcanic']
planet_zones	= ['a', 'b', 'c']
planet_colors	= ['red', 'yellow', 'cyan', 'green']


# Planet resources (to randomly assign to each planet)
# planet_resources	= [ [minerals_low, minerals_high] , [gas_low, gas_high] ]
Rocky_resources 	= [ [100, 400] 	, [100	, 400] 	]
Frozen_resources 	= [ [200, 500] 	, [50	, 100] 	]
Liquid_resources 	= [ [0	, 100] 	, [50	, 400] 	]
Gas_resources 		= [ [0	, 50] 	, [0	, 1500] ]
Volcanic_resources 	= [ [300, 900] 	, [400	, 1000] 	]

step = 25	#increment of resource range
big_step = 500

#list for randomization of planet resources
Resources = {
	"Rocky_minerals" 	: 	range(Rocky_resources[0][0]		, 	Rocky_resources[0][1], step),
	"Rocky_gas" 		: 	range(Rocky_resources[1][0]		, 	Rocky_resources[1][1], step),
	"Frozen_minerals" 	: 	range(Frozen_resources[0][0]	, 	Frozen_resources[0][1], step),
	"Frozen_gas" 		: 	range(Frozen_resources[1][0]	, 	Frozen_resources[1][1], step),
	"Liquid_minerals" 	: 	range(Liquid_resources[0][0]	, 	Liquid_resources[0][1], step),
	"Liquid_gas" 		: 	range(Liquid_resources[1][0]	, 	Liquid_resources[1][1], step),
	"Gas_minerals" 		: 	range(Gas_resources[0][0]		, 	Gas_resources[0][1], step),
	"Gas_gas" 			: 	range(Gas_resources[1][0]		, 	Gas_resources[1][1], big_step),
	"Volcanic_minerals" : 	range(Volcanic_resources[0][0]	, 	Volcanic_resources[0][1], step),
	"Volcanic_gas" 		: 	range(Volcanic_resources[1][0]	, 	Volcanic_resources[1][1], step)
}

#make different planet types cost different amounts to build on
Colony_Cost_Multiplier = {
	"Rocky" 	: 	{	"minerals" : 1.0	, "gas" : 1.0	},
	"Frozen" 	: 	{	"minerals" : 1.0 	, "gas" : 1.0	},
	"Liquid" 	: 	{	"minerals" : 1.4	, "gas" : 0.8	},
	"Gas" 		: 	{	"minerals" : 0.4	, "gas" : 0.6 	},
	"Volcanic" 	: 	{	"minerals" : 1.5 	, "gas" : 2		}
}


#SECTOR LIST

# Sectors -- one for each star system
sector_size = 3
sector_blank = []
#create blank 3x3 sector map
for x in range(sector_size):
	sector_blank.append(["   "] * sector_size)

sector_list = []
#create blank 6-sector sector list for the galaxy map
for x in range(sector_size**2):
	# the deepcopy makes sure the sectors don't replicate themselves in generating the map
	sector_list.append(deepcopy(sector_blank))



# Solar System (zoom)
solar_size = 16
solar_blank = []
#create blank solar system map
for x in range(solar_size):
	solar_blank.append(["   "] * solar_size)


# Planet (zoom)
planet_map_size = 13
planet_blank = []
#create blank planet map
for x in range(planet_map_size):
	planet_blank.append(["   "] * planet_map_size)
# planet_map = deepcopy(planet_blank)








########################################################################################
#---FUNCTIONS
########################################################################################


# PATCH FUNCTIONS

# Gets planet index into a [0:2][0:2] = [i][j] pair for locating planet in galaxy_map
# Returns [i,j]
def to_base_3(location):
	i = int(location/3)
	j = location%3
	return [i,j]

# Changes to next player in line, returns next player (player_list[0])
def next_player():
	global player_list

	#takes first player in list, and puts on the end
	player_list.append( player_list.pop(0) )
	return player_list[0]


#check if player has enough money to do something
def check_money(minerals_cost, gas_cost):
	minerals = Players[current_player]["minerals"]
	gas = Players[current_player]["gas"]

	if minerals < minerals_cost and gas < gas_cost:
		cprint("You do not have enough resources", 'red', attrs=['bold','blink'])
		sleep(2)
		return False
	elif minerals < minerals_cost:
		cprint("You do not have enough minerals", 'red', attrs=['bold','blink'])
		sleep(2)
		return False
	elif gas < gas_cost:
		cprint("You do not have enough vespene gas", 'red', attrs=['bold','blink'])
		sleep(2)
		return False

	#if there is enough money, return True
	else:
		return True


#subtract money from current player
def subtract_money(minerals_cost, gas_cost):
	Players[current_player]["minerals"] -= minerals_cost
	Players[current_player]["gas"] -= gas_cost

#add money to current player
def add_money(minerals_revenue, gas_revenue):
	Players[current_player]["minerals"] += minerals_revenue
	Players[current_player]["gas"] += gas_revenue

#mine resources from colonies at beginning of turn
def mine_resources():
	global current_player
	player = Players[current_player]

	#scavenge for resources
	player["minerals"] += scavenge_minerals
	player["gas"] += scavenge_gas

	# check if player has any colonies (before trying to access dictionary, which may not exist)
	if len(player["colonies"]) > 0 :

		for star in player["colonies"]:
			for planet in player["colonies"][star]:

				n = player["colonies"][star][planet]["colony_number"]

				player["minerals"] += player["colonies"][star][planet]["minerals"] * n
				player["gas"] += player["colonies"][star][planet]["gas"] * n




# GAME START
# get number of players
def get_players():
	number_of_players = 0
	#keep asking if they don't input a number
	num = ''
	while num.isdigit() == False:
		num = raw_input("How many players are there? (1-4 possible) >  ")
	number_of_players = int(num)
	
	#check for valid input
	if number_of_players not in range(1,5):
		print "Only 1-4 players can play this game..."
		get_players()
		return

	for i in range(number_of_players):
		# change name in Players library
		Players[player_list[i]]["name"] = raw_input("\tInput Player %s name >  " %(str(i+1)) )
		i+=1

	#delete the end of the player list (those who aren't playing)
	del(player_list[number_of_players:])

	#move the last player to the beginning of player_list, to prepare for first turn loop
	player_list.insert( 0 , player_list.pop() )

# (explain rules)
def explain_game():
	os.system("clear && printf '\e[3J' ")
	print "\n"
	cprint("\t"*9 + "---  GALAXY  ---", 'white', attrs=['bold'])
	print


	cprint("GOAL", attrs=['underline'])
	print "The goal of the game is to colonize planets, while preventing other players from colonizing planets."
	print "If a player has 0 ships and 0 colonies, they are destroyed and out of the game."
	# cprint("\t\t--> The first player to colonize %s planets wins." %(victory_condition), 'cyan')
	print "\n\t\t--> THE FIRST PLAYER TO COLONIZE %s PLANETS WINS." %(victory_condition)
	print "\n\n"


	cprint("TURNS", attrs=['underline'])
	print "You may perform ONE ACTION per turn:",
	print "\t- Build a ship"
	print "\t"*5, "- Move a ship"
	print "\t"*5, "- Defend a sector"
	print "\t"*5, "- Build a Colony  -->  ( COLONIZE a planet ... ADD a colony ... INVADE another player's planet )"
	print "\n"


	cprint("BUILDING COLONIES", attrs=['underline'])
	print "You must have a ship in a sector to colonize a planet there.  The ship is spent during colonization of a new planet."
	print "Once you have colonized a planet, you may add colonies without needing a ship.",
	print "Below are the max number of colonies each planet size can handle:"
	print
	print "\t\tSmall Planets  :\t1 colony"
	print "\t\tMedium Planets :\t2 colonies"
	print "\t\tBinary Planets :\t2 colonies"
	print "\t\tLarge Planets  :\t4 colonies"
	print
	print "\tPlanet colonies will mine RESOURCES each turn for you, which you use to do everything."
	print "\tDifferent planets have different amounts of resources, so it's good to survey your options.  The resource types are:"
	print "\n\t\t- MINERALS \t(used as material to build with)"
	print "\t\t- VESPENE GAS \t(used to power ships and machinery during construction)"
	print "\n\n"


	print colored("SHIPS", attrs=['underline']),
	print "\t\t\t\t\t\t\t\t\t\t\t",
	cprint("NAVIGATION", attrs=['underline'])

	print "You can BUILD ships in sectors where you have planets.",
	print "\t\t\t\t\tPosition layout (for Galaxy view and Solar System view) is as follows:"

	print "A ship can MOVE to an adjacent sector (including diagonally)"
	
	print "\t"*16, "0  1  2"
	print "\t"*16, "3  4  5"
	print "\t"*16, "6  7  8"

	print colored("DEFENDING", attrs=['underline'])
	print "A ship can DEFEND a sector from all enemy ships currently in the sector:"
	print "\tThe ship will pursue all ships in the sector."
	print "\tThe ships pursued may be destroyed, they may evade the attack, or they may flee to a nearby sector.",
	print "\n\n"


	cprint("INVADING", attrs=['underline'])
	print "You can invade another player's planet if you have a ship in its sector.  However, it is a risk to do so."
	print "You must give an ANTE (both minerals and gas).  This is your war expense."
	print "\tIf you succeed\t>>\tyou keep your ship and acquire the new colony"
	print "\tIf you fail\t>>\tyou lose your ship"
	print "In either case, you lose the ANTE you paid into the invasion"
	print ""

	#press any key to move on
	# print "\n"
	raw_input( colored("\t"*8 + "   Press Enter to continue  >  ", 'white') )




# GRAPHICS

# Create map of whole galaxy
def print_galaxy_map(galaxy_map):
	global current_player

	#...ROW 1...
	for row in range(3):
		print "\t",
		for sector in range(0,3):
			for i in range(3):

				print galaxy_map[sector][row][i],

			print "\t\t\t",  # Space between columns
		print "\n"
	print "\n\n\n\n"  # Space between rows

	#...ROW 2...
	for row in range(3):
		print "\t",
		for sector in range(3,6):
			for i in range(3):

				print galaxy_map[sector][row][i],

			print "\t\t\t",  # Space between columns
		print "\n"
	print "\n\n\n\n"  # Space between rows

	#...ROW 3...
	for row in range(3):
		print "\t",
		for sector in range(6,9):
			for i in range(3):
				
				print galaxy_map[sector][row][i],

			print "\t\t\t",
		print "\n"
	print "\n"

# Create a solar system map
def print_solar_map(sector):
	global current_player
	
	solar_map = deepcopy(solar_blank)

	# solar_map_graphic is for solar map with drawn circles (if I can get it to work...)
	solar_map_graphic = deepcopy(solar_blank)

	for j in range(3):
		for i in range(3):

			# planets' original grid placements
			x = (solar_size/3)*i + (solar_size/6)
			y = (solar_size/3)*j + (solar_size/6)
			# shift the planets over in the solar map, so they're not in such a grid
			left = [".  ", "'  ", ":  ", "*  ", "o  "]
			right = ["  .", "  '", "  :", "  *", "  o"]
			left_binary = [".. ", ".' "]
			right_binary = [" ..", " .'"]


			for a in left:
				if a in galaxy_map[sector][i][j]:
					x -= 2
					# y -= 1
			for a in right:
				if a in galaxy_map[sector][i][j]:
					x += 2
					# y += 1
			for a in left_binary:
				if a in galaxy_map[sector][i][j]:
					x -= 1
					# y -= 1
			for a in right_binary:
				if a in galaxy_map[sector][i][j]:
					x += 1
					# y -= 1


			#notice how [y] and [x] are switched -- this is okay, because of list format
			solar_map[y][x] = galaxy_map[sector][i][j]


			#add colored indicator of who has a colony there
			#... someday maybe

	# TO MAKE A LOCATION GRID
	# for j in range(solar_size):
	# 	for i in range(solar_size):
	# 		solar_map[solar_size/3][i] = colored(" ` ", 'white', attrs=grid_status[0])
	# 		solar_map[solar_size*2/3][i] = colored(" ` ", 'white', attrs=grid_status[0])
	# 		solar_map[j][solar_size/3] = colored(" ` ", 'white', attrs=grid_status[0])
	# 		solar_map[j][solar_size*2/3] = colored(" ` ", 'white', attrs=grid_status[0])
	# 		solar_map[solar_size/3][solar_size/3] = colored(" ` ", 'white', attrs=grid_status[0])
	# 		solar_map[solar_size*2/3][solar_size/3] = colored(" ` ", 'white', attrs=grid_status[0])
	# 		solar_map[solar_size/3][solar_size*2/3] = colored(" ` ", 'white', attrs=grid_status[0])
	# 		solar_map[solar_size*2/3][solar_size*2/3] = colored(" ` ", 'white', attrs=grid_status[0])


	for row in range( len(solar_map) ):
		print "\t\t", #shifts the whole map over to the right
		for col in range( len(solar_map[row]) ):

			#[row] and [col] are switched below because the list format is different

			# change the symbols to be more "zoomed in"
			print colored( solar_map[col][row]\

				.replace("o", "@")\
				.replace("'", degree_symbol)\
				.replace(".", "o")\
				.replace("*", "#")\
				# .replace(":", "8")\

				#spaces the binary planets a bit, so they look better in solar system view
				.replace(degree_symbol+"o ", degree_symbol+" o")\
				.replace(" "+degree_symbol+"o", degree_symbol+" o")\
				.replace("o"+degree_symbol+" ", "o "+degree_symbol)\
				.replace(" o"+degree_symbol, "o "+degree_symbol)\
				.replace("oo ", "o o")\
				.replace(" oo", "o o"),\

				attrs=['bold']),

			print " ",
		print "\n"

# Draw the planet graphic
def print_planet_map(sector, planet_int):
	global current_player

	#start with a fresh new blank grid for drawing planet on
	#planet_map_size is the size of this grid
	planet_map = deepcopy(planet_blank)

	planet = str(planet_int)
	#find planet in planet list (Stars, dictionary)
	# planet_index 	= Stars[sector]["planet_locations"].index(planet)
	#get planet descriptors
	planet_size 	= Stars[sector]["planets"][planet]["size"]
	planet_type 	= Stars[sector]["planets"][planet]["type"]
	planet_zone 	= Stars[sector]["planets"][planet]["zone"]
	planet_color 	= Stars[sector]["planets"][planet]["color"]

	# planet colony info
	planet_colonies	= Stars[sector]["planets"][planet]["colonies"]
	if planet_colonies["colony_number"]:		#returns "True" if not equal to 0
		colony_color = Players[ planet_colonies["owner"] ]["color"]


	draw_planet(sector, planet_int, planet_map)


	for row in range( len(planet_map) ):
		print "\t\t", #shifts the whole map over to the right
		for col in range( len(planet_map[row]) ):

			if planet_map[col][row] != "   ":

				if planet_map[col][row] in ["###", "## ", " ##", "#  ", " # ", "  #"]:
					print colored(planet_map[col][row], colony_color),

				else:
					# print "".join(colored( planet_map[col][row], planet_color, attrs=['bold'])),
					print colored(planet_map[col][row], planet_color, attrs=['bold']),
					# print planet_map[col][row],
					# print "",

			else:
				# print "".join(planet_map[col][row]),
				print planet_map[col][row],

			print "",
		print "\n"
		# print

# Create the planet (draws it based on its "size" and "color")
def draw_planet(sector, planet_int, planet_map):
	global current_player

	planet = str(planet_int)
	#center of map
	cen = len(planet_map)/2

	# planet_index = Stars[sector]["planet_locations"].index(planet_int)
	planet_size = Stars[sector]["planets"][planet]["size"]
	planet_type = Stars[sector]["planets"][planet]["type"]
	planet_zone = Stars[sector]["planets"][planet]["zone"]
	planet_color = Stars[sector]["planets"][planet]["color"]

	#number of colonies on this planet
	colonies = Stars[sector]["planets"][planet]["colonies"]["colony_number"]
	colony_count = colonies

	#Current planet location planet_int (int from 0-8)
	i = to_base_3(planet_int)[0]
	j = to_base_3(planet_int)[1]

	planet_icon = galaxy_map[ int(sector) ][i][j]


	if planet_size == "Small":
		planet_map [cen][cen-2] 	= "---"		#top
		planet_map [cen][cen+2] 	= "---"		#bottom
		planet_map [cen-2][cen-1] 	= "  /" 	#top left
		planet_map [cen-2][cen] 	= " | "		#left
		planet_map [cen-2][cen+1] 	= "  \\" 	#bottom left
		planet_map [cen+2][cen-1] 	= "\  " 	#top right
		planet_map [cen+2][cen] 	= " | "		#right
		planet_map [cen+2][cen+1] 	= "/  " 	#bottom right

		if colonies:
			if colony_count > 0 :
				planet_map [cen][cen-1] = " ##"
				colony_count -= 1
				return




	elif planet_size == "Medium":
		planet_map [cen][cen-3] 	= "---"		#top
		planet_map [cen][cen+3] 	= "---"		#bottom
		planet_map [cen-1][cen-3] 	= "..." 	#top left up
		planet_map [cen+1][cen-3] 	= "..." 	#top right up
		
		planet_map [cen+1][cen+3] 	= "'''" 	#bottom right down
		planet_map [cen-1][cen+3] 	= "'''" 	#bottom left down

		planet_map [cen-2][cen-2] 	   = "/  " 	#top left
		planet_map [cen-3][cen-1] 	= "  |"		#left up
		planet_map [cen-3][cen] 	= " | "		#left
		planet_map [cen-3][cen+1] 	= "  |"		#left down
		planet_map [cen-2][cen+2] 	   = "\  " 	#bottom left 
		
		planet_map [cen+2][cen-2] 	= "  \\" 	#top right
		planet_map [cen+3][cen-1] 	   = "|  "		#right up
		planet_map [cen+3][cen] 	   = " | "		#right
		planet_map [cen+3][cen+1] 	   = "|  "		#right down
		planet_map [cen+2][cen+2] 	= "  /" 	#bottom right 

		if colonies:
			if colony_count > 0 :
				planet_map [cen][cen-1] = "###"
				colony_count -= 1
				if colony_count > 0 :
					planet_map [cen-1][cen] = "###"
					colony_count -= 1
					return
					







	#gas giants -- add rings!
	elif planet_size == "Large" and planet_type == "Gas":
		planet_map [cen][cen-5] 	= "---"		#top
		planet_map [cen][cen+5] 	= "---"		#bottom

		planet_map [cen-1][cen-5] 	= "..."		#top left
		planet_map [cen+1][cen-5] 	= "..."		#top right

		planet_map [cen-1][cen+5] 	= "'''"		#bottom left
		planet_map [cen+1][cen+5] 	= "'''"		#bottom right

		
		planet_map [cen-3][cen-4] 	      = "/  " 	#top left up up
		planet_map [cen-4][cen-3] 	   = "/  " 		#top left up
		planet_map [cen-5][cen-2] 	= "  /" 		#top left
		planet_map [cen-5][cen-1] 	= " | "			#left up
		planet_map [cen-5][cen] 	= "|  "			#left
		planet_map [cen-5][cen+1] 	= " | "			#left down
		planet_map [cen-5][cen+2] 	= "  \\" 		#bottom left 
		planet_map [cen-4][cen+3] 	  = "\  " 		#bottom left down
		planet_map [cen-3][cen+4] 	     = "\  " 	#bottom left down down

		
		planet_map [cen+3][cen-4] 	= "  \\" 		#top right up up
		planet_map [cen+4][cen-3] 	   = "  \\" 	#top right up
		planet_map [cen+5][cen-2] 	      = "\  " 	#top right
		planet_map [cen+5][cen-1] 	      = " | "	#right up
		planet_map [cen+5][cen] 	      = "  |"	#right
		planet_map [cen+5][cen+1] 	      = " | "	#right down
		planet_map [cen+5][cen+2] 	      = "/  " 	#bottom right 
		planet_map [cen+4][cen+3] 	   = "  /" 		#bottom right down
		planet_map [cen+3][cen+4] 	= "  /" 		#bottom right down down



		#Rings!
		planet_map [cen][cen] 		= "___" 	#center

		planet_map [cen-1][cen] 	= "___" 	#center lefts
		planet_map [cen-2][cen] 	= "___" 	#center
		planet_map [cen-3][cen] 	= "___" 	#center
		planet_map [cen-4][cen] 	= "___" 	#center
		planet_map [cen-5][cen] 	= "---" 	#center
		planet_map [cen-6][cen] 	= '"+-' 	#center planet width
		planet_map [cen-6][cen-1] 	= ".-'" 	#center

		planet_map [cen+1][cen] 	= "___" 	#center rights
		planet_map [cen+2][cen] 	= "___" 	#center
		planet_map [cen+3][cen] 	= "___" 	#center
		planet_map [cen+4][cen] 	= "___" 	#center
		planet_map [cen+5][cen] 	= "---" 	#center
		planet_map [cen+6][cen] 	= '-+"' 	#center planet width
		planet_map [cen+6][cen-1] 	= "'-." 	#center

		if colonies:
			if colony_count > 0 :
				planet_map [cen-5][cen-5] = "###"
				colony_count -= 1
				if colony_count > 0 :
					planet_map [cen+5][cen+5] = "###"
					colony_count -= 1
					if colony_count > 0 :
						planet_map [cen-4][cen+4] = "###"
						colony_count -= 1
						if colony_count > 0 :
							planet_map [cen+4][cen-4] = "###"
							colony_count -= 1
							return



	elif planet_size == "Large":
		planet_map [cen][cen-5] 	= "---"		#top
		planet_map [cen][cen+5] 	= "---"		#bottom

		planet_map [cen-1][cen-5] 	= "..."		#top left
		planet_map [cen+1][cen-5] 	= "..."		#top right

		planet_map [cen-1][cen+5] 	= "'''"		#bottom left
		planet_map [cen+1][cen+5] 	= "'''"		#bottom right

		
		planet_map [cen-3][cen-4] 	      = "/  " 	#top left up up
		planet_map [cen-4][cen-3] 	   = "/  " 		#top left up
		planet_map [cen-5][cen-2] 	= "  /" 		#top left
		planet_map [cen-5][cen-1] 	= " | "			#left up
		planet_map [cen-5][cen] 	= "|  "			#left
		planet_map [cen-5][cen+1] 	= " | "			#left down
		planet_map [cen-5][cen+2] 	= "  \\" 		#bottom left 
		planet_map [cen-4][cen+3] 	  = "\  " 		#bottom left down
		planet_map [cen-3][cen+4] 	     = "\  " 	#bottom left down down

		
		planet_map [cen+3][cen-4] 	= "  \\" 		#top right up up
		planet_map [cen+4][cen-3] 	   = "  \\" 	#top right up
		planet_map [cen+5][cen-2] 	      = "\  " 	#top right
		planet_map [cen+5][cen-1] 	      = " | "	#right up
		planet_map [cen+5][cen] 	      = "  |"	#right
		planet_map [cen+5][cen+1] 	      = " | "	#right down
		planet_map [cen+5][cen+2] 	      = "/  " 	#bottom right 
		planet_map [cen+4][cen+3] 	   = "  /" 		#bottom right down
		planet_map [cen+3][cen+4] 	= "  /" 		#bottom right down down

		if colonies:
			if colony_count > 0 :
				planet_map [cen][cen-2] = "###"
				colony_count -= 1
				if colony_count > 0 :
					planet_map [cen-2][cen] = "###"
					colony_count -= 1
					if colony_count > 0 :
						planet_map [cen][cen+2] = "###"
						colony_count -= 1
						if colony_count > 0 :
							planet_map [cen+2][cen] = "###"
							colony_count -= 1
							return

		

		

	elif planet_size == "Binary":

		planet_skew_list = ["'. ", " '.", ".' ", " .'", ".. ", " ..", ":  ", " : ", "  :"]
		Ay_offset = [1, 3, -1, -2, 0, 0, 3, 3, 3]
		By_offset = [-1, -3, 3, 2, 0, 0, -3 ,-3, -3]

		#2 centers for binary planet:
		cen_Ax = len(planet_map)/4
		cen_Ay = cen - Ay_offset[ planet_skew_list.index(planet_icon[5:8]) ]

		cen_Bx = len(planet_map)*3/4
		cen_By = cen - By_offset[ planet_skew_list.index(planet_icon[5:8]) ]

		#vertical binary planets:
		if str(planet_icon[5:8]) in [":  ", " : ", "  :"]:
			cen_Ax = len(planet_map)/2
			cen_Bx = len(planet_map)/2

		#center A
		planet_map [cen_Ax][cen_Ay-2] 	= "---"		#top
		planet_map [cen_Ax][cen_Ay+2] 	= "---"		#bottom
		planet_map [cen_Ax-2][cen_Ay-1] = "  /" 	#top left
		planet_map [cen_Ax-2][cen_Ay] 	= " | "		#left
		planet_map [cen_Ax-2][cen_Ay+1] = "  \\" 	#bottom left
		planet_map [cen_Ax+2][cen_Ay-1] = "\  " 	#top right
		planet_map [cen_Ax+2][cen_Ay] 	= " | "		#right
		planet_map [cen_Ax+2][cen_Ay+1] = "/  " 	#bottom right
		#center B
		planet_map [cen_Bx][cen_By-2] 	= "---"		#top
		planet_map [cen_Bx][cen_By+2] 	= "---"		#bottom
		planet_map [cen_Bx-2][cen_By-1] = "  /" 	#top left
		planet_map [cen_Bx-2][cen_By] 	= " | "		#left
		planet_map [cen_Bx-2][cen_By+1] = "  \\" 	#bottom left
		planet_map [cen_Bx+2][cen_By-1] = "\  " 	#top right
		planet_map [cen_Bx+2][cen_By] 	= " | "		#right
		planet_map [cen_Bx+2][cen_By+1] = "/  " 	#bottom right


		if colonies:
			if colony_count > 0 :
				planet_map [cen_Ax-1][cen_Ay] = "## "
				colony_count -= 1
				if colony_count > 0 :
					planet_map [cen_Bx][cen_By+1] = "  #"
					colony_count -= 1
					return





# INFO BARS

# Shows player Name, and Resources
def make_player_top_bar():
	global current_player

	player = Players[str(current_player)]
	os.system("clear && printf '\e[3J' ")
	#REFERENCE -- Player (P1) library
	# "name" : ''
	# "color" : ''
	# "minerals" : start_minerals,
	# "gas" : start_gas,
	# "colonies" : {},
	# "ships" : {}


	print colored("PLAYER: %s" %( player["name"] ), player["color"], attrs=['bold', 'underline']),

	#compensate for long player names...
	if len(player["name"]) <= 6:
		print "\t",
	if len(player["name"]) <= 14:
		print "\t",
	if len(player["name"]) <= 22:
		print "\t",
	if len(player["name"]) <= 30:
		print "\t",

	# print "\t\t\t\t\t\t\t",
	print colored("\t\t\t\tMinerals:\t%d" %( player["minerals"] ), player["color"], attrs=['bold'])
	print colored("\t\t\t\t\t\t\t\t\tGas:\t\t%d" %( player["gas"] ), player["color"], attrs=['bold'])
	print colored("\t\t\t\t\t\t\t\t\tShips:\t\t%d" %( player["ships"]["total_ships"] ), player["color"], attrs=['bold'])

	print colored("\t\t\t\t\t\t\t\t\tColonies:\t%d" %( player["planets_colonized"] ), player["color"], attrs=['bold']),
	print "\t",
	for star in player["colonies"]:
		for planet in player["colonies"][star]:
			print colored("%s(%s,%s)  " %(player["colonies"][star][planet]["colony_number"],star,planet) , player["color"]),
	print 

	# print colored("\t\t\t\t\t\t\t\t\tShip sectors:\t", player["color"], attrs=['bold']),
	# print colored(player["ships"]["sectors"], player["color"], attrs=['bold'])
	# print

# Description of the planets around this star
def print_atlas(star):
	global current_player

	#THIS DISPLAYS THE PLANETS IN A MORE LOGICAL ORDER -- CORRESPONDING FROM LEFT > RIGHT
	planet_list = ["0","3","6",  "1","4","7",  "2","5","8"]

	print colored("________________________"*5, 'white')
	print colored("STAR: %s" %( star ), 'white', attrs=['underline', 'bold'])


	# LOCATION
	for planet in planet_list:
		if planet in Stars[star]["planets"]:
		# for planet in Stars[star]["planets"]:
			planet_color = Stars[star]["planets"][planet]["color"]
			print colored("\tlocation: ", planet_color),
			print colored(Stars[star]["planets"][planet]["location"], planet_color),
			print "\t\t",
	print
	for planet in planet_list:
		if planet in Stars[star]["planets"]:
		# for planet in Stars[star]["planets"]:
			planet_color = Stars[star]["planets"][planet]["color"]
			print colored("\tsize: ", planet_color),
			print colored(Stars[star]["planets"][planet]["size"], planet_color),
			print "\t\t",
	print


	# TYPE
	for planet in planet_list:
		if planet in Stars[star]["planets"]:
		# for planet in Stars[star]["planets"]:
			planet_color = Stars[star]["planets"][planet]["color"]
			print colored("\ttype: ", planet_color),
			print colored(Stars[star]["planets"][planet]["type"], planet_color),
			if len( Stars[star]["planets"][planet]["type"] ) < 8:
				print "\t",
			print "\t",
	print
	

	# WHO HAS COLONIZED (if applicable)
	for planet in planet_list:
		if planet in Stars[star]["planets"]:
		# for planet in Stars[star]["planets"]:
			colony_owner = Stars[star]["planets"][planet]["colonies"]["owner"]
			if colony_owner:
				colony_color = Players[colony_owner]["color"]
				planet_color = Stars[star]["planets"][planet]["color"]

				if len(Players[colony_owner]["name"]) > 7:
					colony_owner_name = Players[colony_owner]["name"][:7]
				else:
					colony_owner_name = Players[colony_owner]["name"]

				print colored("\tcolonized by: ", planet_color),
				print colored(colony_owner_name, colony_color),
				print "\t",

			else:
				print "\t\t\t\t",
	print

#Description of the planet you're zoomed in on
def print_planet_info(star, planet_int):
	global current_player

	print colored("________________________"*5, 'white')
	print colored("STAR: %s" %( star ), 'white', attrs=['underline', 'bold'])

	# print colored("Star Position: ", 'white'),
	# print colored(Stars[star]["star_location"], 'white')

	print colored("Planets around star: ", 'white'),
	print colored(Stars[star]["planet_number"], 'white')

	planet = str(planet_int)

	# planet_index = Stars[star]["planet_locations"].index(planet_int)
	planet_size = Stars[star]["planets"][planet]["size"]
	planet_type = Stars[star]["planets"][planet]["type"]
	planet_zone = Stars[star]["planets"][planet]["zone"]
	planet_color = Stars[star]["planets"][planet]["color"]
	planet_minerals = Stars[star]["planets"][planet]["minerals"]
	planet_gas = Stars[star]["planets"][planet]["gas"]
	planet_name = Stars[star]["planets"][planet]["name"]
	colony_owner = Stars[star]["planets"][planet]["colonies"]["owner"]
	if colony_owner:
		colony_color = Players[colony_owner]["color"]

	cardinals = ["First Planet:", "Second Planet:", "Third Planet:", "Fourth Planet:"]
	
	# print "\t",
	# # print colored(cardinals[planet_index], planet_color, attrs=['underline', 'bold']),
	# print "\t\t",

	print colored("\tlocation: ", planet_color),
	print colored(Stars[star]["planets"][planet]["location"], planet_color)
	# print "\t\t"

	print colored("\tsize: ", planet_color),
	print colored(planet_size, planet_color)
	# print "\t\t"

	print colored("\ttype: ", planet_color),
	print colored(planet_type, planet_color)
	# print "\t\t"

	print colored("\tminerals: ", planet_color),
	print colored(planet_minerals, planet_color)
	# print "\t\t"

	print colored("\tgas: ", planet_color),
	print colored(planet_gas, planet_color)
	# print "\t\t"

	print colored("\tcolonies: ", planet_color),
	print colored(Stars[star]["planets"][planet]["colonies"]["colony_number"], planet_color)
	# print "\t\t"

	if colony_owner:
		print colored("\tcolonized by: ", planet_color),
		print colored(Players[ Stars[star]["planets"][planet]["colonies"]["owner"] ]["name"], colony_color),
		print colored("\t\t\tPLANET:  ", planet_color),
		print colored(planet_name, planet_color, attrs=['bold'])




# GAME PAGES

# page with galaxy view
def galaxy_page():
	global current_player

	os.system("clear && printf '\e[3J' ")
	make_player_top_bar()
	print "GALAXY MAP:\n"
	print " "+"---"*30+"\n\n\n"
	print_galaxy_map(galaxy_map)
	print " "+"---"*30+"\n"
	galaxy_page_options()
	return

#page with view of solar system (sector)
def solar_page(sector):
	global current_player

	os.system("clear && printf '\e[3J' ")
	make_player_top_bar()
	print colored("SOLAR SYSTEM -- SECTOR %s:" %(sector), 'white', attrs=['bold'])
	print_atlas(sector)
	print colored(" "+"---"*39+"\n", 'white')
	print_solar_map(int(sector))
	print colored(" "+"---"*39+"\n", 'white')
	solar_page_options(sector)
	return

# page with view of planet
def planet_page(sector, planet_int):
	global current_player

	os.system("clear && printf '\e[3J' ")
	make_player_top_bar()
	print colored("SOLAR SYSTEM -- SECTOR %s:" %(sector), 'white', attrs=['bold'])

	print_planet_info(sector, planet_int)
	print colored(" "+"---"*39+"\n", 'white')
	print_planet_map(sector, planet_int)
	print colored(" "+"---"*39+"\n", 'white')
	planet_page_options(sector, planet_int)
	return



# visual of galaxy page to show a chance, without giving options...
# (so turn_loop() can successfully chance turns)
def galaxy_page_visual():
	global current_player

	os.system("clear && printf '\e[3J' ")
	make_player_top_bar()
	print "GALAXY MAP:\n"
	print " "+"---"*30+"\n\n\n"
	print_galaxy_map(galaxy_map)
	print " "+"---"*30+"\n"
	return

# visual of planet page to show a chance, without giving options...
# (so turn_loop() can successfully chance turns)
def solar_page_visual(sector):
	global current_player

	os.system("clear && printf '\e[3J' ")
	make_player_top_bar()
	print colored("SOLAR SYSTEM -- SECTOR %s:\n" %(sector), 'white', attrs=['bold'])
	print_atlas(sector)
	print colored(" "+"---"*39+"\n", 'white')
	print_solar_map(int(sector))
	print colored(" "+"---"*39+"\n", 'white')
	return

# visual of planet page to show a chance, without giving options...
# (so turn_loop() can successfully chance turns)
def planet_page_visual(sector, planet_int):
	global current_player

	os.system("clear && printf '\e[3J' ")
	make_player_top_bar()
	print colored("SOLAR SYSTEM -- SECTOR %s:\n" %(sector), 'white', attrs=['bold'])

	print_planet_info(sector, planet_int)
	print colored(" "+"---"*39+"\n", 'white')
	print_planet_map(sector, planet_int)
	print colored(" "+"---"*39+"\n", 'white')
	return




# Information page
def information_page():
	global current_player

	# Turn
	# Atlas
	# player resources, ships, colonies
	return




# PAGE OPTIONS

# Options for galaxy page
def galaxy_page_options():
	global current_player

	print colored("OPTIONS:", attrs=['underline', 'bold']) + "\t",
	print "(Z)\tZoom into Solar System (enter number -- sector)" # (or press a number 0-8)"
	print "\n\t\t(B)\tBuy a ship\t:\t%s minerals\n\t\t\t\t\t\t%s gas" %(ship_cost_minerals, ship_cost_gas)
	print "\n\t\t(M)\tMove a ship\t:\t%s gas" %(ship_move_gas)
	print "\n\t\t(D)\tDefend sector from enemy ships\t:\t%s minerals\n\t\t\t\t\t\t\t\t%s gas" %(ship_attack_minerals, ship_attack_gas)
	print "\t\t(T)\tSkip Turn"


	# Zoom to sector (input a number)
	press = raw_input()
	if press.isdigit():
		if press in Stars:
			solar_page(press)
			return

	# action = raw_input().lower()
	action = press.lower()
	# Make sure input is valid
	if action not in ['z', 'b', 'm', 't', 'd']:
		print "INVALID INPUT"
		sleep(0.5)
		galaxy_page()
		# os.system('tput reset')


	# Zoom to sector
	if action.lower() == 'z':
		sector = raw_input("\t\t\t\tWhich sector would you like to see? : ")

		# Make sure input is valid
		if sector not in Stars:
			cprint("This sector is outside of the observable universe...", 'red', attrs=['bold', 'blink'])
			sleep(2)
			galaxy_page()
			return

		solar_page(sector)


	# Build ship
	elif action.lower() == 'b':
		if check_money(ship_cost_minerals, ship_cost_gas):
			sector = raw_input("\t\t\t\t\t(X) TO CANCEL -- Where would you like to purchase a ship?: ")
			if sector.lower() == 'x':
				galaxy_page()
				return
			if sector not in Stars:
				cprint("This sector is outside of the observable universe...", 'red', attrs=['bold', 'blink'])
				sleep(3)
				galaxy_page()
				return

			if sector not in Players[current_player]["colonies"]:
				cprint("You can only build a ship in a sector where you have a colony.", 'red', attrs=['bold', 'blink'])
				sleep(3)
				galaxy_page()
				return

			subtract_money(ship_cost_minerals, ship_cost_gas)
			add_ship(current_player, int(sector))
			#Show confirmation
			galaxy_page_visual()
			print "Ship purchased"
			sleep(2)
			turn_loop()
			return

		#if player doesn't have enough money
		else:
			galaxy_page()
			return


	# Move ship
	elif action.lower() == 'm':
		if check_money(ship_move_minerals, ship_move_gas):

			player_color = Players[current_player]["color"]
			ship_occupying = colored(">  ", player_color, attrs=['bold', 'blink'])

			# Take ship From sector
			From = raw_input("\t\t\t\t\t(X) TO CANCEL -- Move ship FROM sector: ")
			if From.lower() == 'x':
				galaxy_page()
				return
			if From not in Stars:
				cprint("This sector is outside of the observable universe...", 'red', attrs=['bold', 'blink'])
				sleep(3)
				galaxy_page()
				return

			# Make sure they are not cheating...
			if ship_occupying not in galaxy_map[int(From)][0]\
			and ship_occupying not in galaxy_map[int(From)][1]\
			and ship_occupying not in galaxy_map[int(From)][2]:
				print "\t\t\t\t",
				cprint("! -- You don't have a ship in that sector -- !\n", 'red', attrs=['bold', 'blink'])
				sleep(3)
				galaxy_page()
				# galaxy_page_options()
				return

			#  Send shit To sector
			To = raw_input("\t\t\t\t\t(X) TO CANCEL -- Send ship TO sector: ")
			if To.lower() == 'x':
				galaxy_page()
				return
			if To not in Stars:
				cprint("This sector is outside of the observable universe...", 'red', attrs=['bold', 'blink'])
				sleep(3)
				galaxy_page()
				return

			if move_ship(current_player, int(From), int(To)):
				subtract_money(ship_move_minerals, ship_move_gas)
				galaxy_page_visual()
				print "Ship moved successfully"
				sleep(2)
				turn_loop()
				return
			#if too far to move ship
			else:
				galaxy_page()

		#if player doesn't have enough money
		else:
			galaxy_page()
			return


	elif action.lower() == 'd':
		if check_money(ship_attack_minerals, ship_attack_gas):
			zone = ''
			zone = raw_input("\t\t\t\t\t(X) TO CANCEL -- Which sector will you defend? >  ")
			#(X) to cancel
			if zone.lower() == 'x':
				galaxy_page()
				return

			#check to see if input is valid
			if zone not in Stars:
				cprint("This sector is outside of the observable universe...", 'red', attrs=['bold', 'blink'])
				sleep(3)
				galaxy_page()
				return
			#check to see if player has ship in sector
			if int(zone) not in Players[current_player]["ships"]["sectors"]:
				cprint("You do not have a ship in that sector", 'red', attrs=['bold', 'blink'])
				sleep(3)
				galaxy_page()
				return

			#if all conditions are met, defend the territory!
			ship_attack(int(zone))
			turn_loop()

		#if player doesn't have enough money
		else:
			galaxy_page()
			return


	# Skip turn
	elif action.lower() == 't':
		galaxy_page_visual()
		sleep(1)
		turn_loop()

	return

# Options for solar page
def solar_page_options(sector):
	global current_player

	print colored("OPTIONS:", attrs=['underline', 'bold']) + "\t",
	print "(Z)\tZOOM INTO PLANET (enter a number -- planet location)"		
	print "\n\t\t(G)\tBack to Galaxy view"
	print "\n\t\t(T)\tSkip Turn"



	# Zoom to planet (input a number)
	press = raw_input()
	if press.isdigit():
		if press in Stars[sector]["planets"]:
			planet_page(sector, int(press))
			return

	# action = raw_input().lower()
	action = press.lower()

	# Make sure input is valid
	if action not in ['z', 'g', 't']:
		print "INVALID INPUT"
		sleep(2)
		solar_page(sector)


	# Zoom to planet
	if action.lower() == 'z':
		planet = raw_input("Which planet would you like view? ")
		#make sure input is a number
		if planet.isdigit() == False:
			print "INVALID INPUT"
			sleep(1)
			solar_page(sector)
			return
		#check for valid planet
		if str(planet) not in Stars[sector]["planets"]:
			cprint("Planet does not exist", 'red', attrs=['bold','blink'])
			sleep(2)
			solar_page(sector)
			return

		planet_page(sector, int(planet))

	# Galaxy View
	if action.lower() == 'g':
		galaxy_page()


	# Skip Turn
	elif action.lower() == 't':
		solar_page_visual(sector)
		sleep(1)
		turn_loop()


	return


# Options for planet page
def planet_page_options(sector, planet_int):
	global current_player

	player = Players[current_player]
	planet = str(planet_int)
	star = str(sector)
	current_planet = Stars[sector]["planets"][planet]
	size = current_planet["size"]



	# DIFFERENT PLANET TYPES COST DIFFERENT AMOUNTS TO BUILD ON
	cost_multiplier_minerals = Colony_Cost_Multiplier[ current_planet["type"] ]["minerals"]
	cost_multiplier_gas = Colony_Cost_Multiplier[ current_planet["type"] ]["gas"]

	#colonize cost
	this_colonize_minerals = colonize_cost_minerals * cost_multiplier_minerals
	this_colonize_gas = colonize_cost_gas * cost_multiplier_gas
	#round it down
	colonize_rounded_minerals = this_colonize_minerals - (this_colonize_minerals % 25)
	colonize_rounded_gas = this_colonize_gas - (this_colonize_gas % 25)


	#add colony cost
	this_colony_minerals = colony_cost_minerals * cost_multiplier_minerals
	this_colony_gas = colony_cost_gas * cost_multiplier_gas
	#round it down
	colony_rounded_minerals = this_colony_minerals - (this_colony_minerals % 25)
	colony_rounded_gas = this_colony_gas - (this_colony_gas % 25)



	existing_colony_number = current_planet["colonies"]["colony_number"]
	if existing_colony_number:
		colony_owner = Stars[star]["planets"][planet]["colonies"]["owner"]
		colony_color = Players[colony_owner]["color"]

	print colored("OPTIONS:", attrs=['underline', 'bold']) + "\t",
	# print "\t"


	# if current player has already colonized
	if existing_colony_number and colony_owner == current_player:

		if existing_colony_number < max_colonies[size]:
			print "(A)\tADD COLONY\t:\t%d Minerals" %(colony_rounded_minerals)
			print "\t\t\t\t\t\t%d Vespene Gas" %(colony_rounded_gas)
		else:
			print "\n"

		print "\n\t\t(S)\tBack to Solar System view"		
		print "\n\t\t(G)\tBack to Galaxy view"
		print "\n\t\t(T)\tSkip Turn"
		


	# if there are colonies owned by another player
	elif existing_colony_number:
		print "(I)\tINVADE\t:\t\t(What are you willing to"
		print "\t\t\t\t\t\tspend on an invasion attempt...?)"

		print "\n\t\t(S)\tBack to Solar System view"		
		print "\n\t\t(G)\tBack to Galaxy view"
		print "\n\t\t(T)\tSkip Turn"

	# if there are no colonies
	else:
		print "(C)\tCOLONIZE PLANET\t:\t%d Minerals" %(colonize_rounded_minerals)
		print "\t\t\t\t\t\t%d Vespene Gas" %(colonize_rounded_gas)

		print "\n\t\t(S)\tBack to Solar System view"		
		print "\n\t\t(G)\tBack to Galaxy view"
		print "\n\t\t(T)\tSkip Turn"



	#get user action
	action = raw_input().lower()

	# Make sure input is valid
	if action not in ['a', 'i', 'c', 's', 'g', 't']:
		print colored("\t\tINVALID OPTION", 'red', attrs=['blink'])
		sleep(3)
		planet_page(sector, planet_int)

	if action == 's':
		solar_page(sector)
	if action == 'g':
		galaxy_page()


	# colonize planet
	if action == 'c':

		# Check if player has a ship in this sector
		if int(sector) not in player["ships"]["sectors"]:
			cprint("You must have a ship in the planet's sector to colonize a planet", 'red', attrs=['bold','blink'])
			sleep(3)
			planet_page(sector, planet_int)
			return

		#Check if player has enough money
		if check_money(colonize_rounded_minerals, colonize_rounded_gas):
			#make sure they want to colonize
			if raw_input("Are you sure you want to colonize? (Y) or (N) >  ").lower() != 'y':
				planet_page(sector, planet_int)
				return

			#first, let's name this new planet!
			name = raw_input("What will you name this planet? >  ")
			while name == '':
				name = raw_input("You've gotta name it SOMETHING...  ")
			current_planet["name"] = name

			# Requirements met --> colonize the planet
			print "Colonizing planet..."
			sleep(1)
			# cost of colonizing a planet
			subtract_money(colonize_rounded_minerals, colonize_rounded_gas)
			remove_ship(current_player, int(sector))
			# build the colony and display to player
			build_colony(sector, planet_int)
			# add 1 to number -- keeping track for victory condition
			player["planets_colonized"] += 1

			planet_page_visual(sector, planet_int)
			print "Planet colonized."
			sleep(2)
			#next player's turn
			turn_loop()
			return

		#if player doesn't have enough resources
		else:
			planet_page(sector, planet_int)
			return

	# add colony
	if action == 'a':
		if check_money(colony_rounded_minerals, colony_rounded_gas):
			#make sure they want to add a colony
			if raw_input("Are you sure you want to add a colony? (Y) or (N) >  ").lower() != 'y':
				planet_page(sector, planet_int)
				return

			print "Adding colony..."
			sleep(1)
			# cost of building a colony
			subtract_money(colony_rounded_minerals, colony_rounded_gas)
			# build the colony and display to player
			build_colony(sector, planet_int)
			planet_page_visual(sector, planet_int)
			print "Colony added."
			sleep(2)
			#next player's turn
			turn_loop()
			return

		#if player doesn't have enough resources
		else:
			planet_page(sector, planet_int)
			return

	# invade
	if action == 'i':
		# Check if player has a ship in this sector
		if int(sector) not in player["ships"]["sectors"]:
			cprint("You must have a ship in the planet's sector to invade a planet", 'red', attrs=['bold','blink'])
			sleep(2)
			planet_page(sector, planet_int)
			return

		#make sure they want to invade
		if raw_input("Are you sure you want to invade? (Y) or (N) >  ").lower() != 'y':
			planet_page(sector, planet_int)
			return

		
		planet_page_visual(sector, planet_int)
		

		outcome = invade_planet(sector, planet_int)

		#if True, the invasion succeeded
		if outcome == True:
			planet_page_visual(sector, planet_int)
			print "THE INVASION WAS SUCCESSFUL!..."
			sleep(1)
			print "Enslaving local workforce..."
			sleep(3)
			#next player's turn
			planet_page_visual(sector, planet_int)
			turn_loop()
			return

		# otherwise, invasion failed
		elif outcome == False:
			planet_page_visual(sector, planet_int)
			sleep(1)
			#next player's turn
			turn_loop()
			return


		# aborted invasion
		elif outcome == 'aborted':
			print "outcome = aborted"
			planet_page(sector, planet_int)
			return

		# didn't type 'y' or 'n'
		elif outcome == 'invalid':
			planet_page(sector, planet_int)
			return



	# attack nearby enemy ship

	# Skip turn
	elif action.lower() == 't':
		planet_page_visual(sector, planet_int)
		sleep(1)
		turn_loop()

	return


# Options for information page
def information_page_options():
	global current_player

	# Turn
	# Atlas
	# player resources, ships, colonies
	return





# PLAYER ACTIONS

# Adds ship at "sector"
def add_ship(selected_player, sector_int):
	global current_player

	player = Players[selected_player]
	player_color = player["color"]

	#Check if player has no ships in sector
	if sector_int in player["ships"]["sectors"]:
		cprint("You already have a ship in that sector", 'red', attrs=['bold', 'blink'])
		sleep(2)
		galaxy_page()
		return 0

	cond = 0
	for row in range(3):
		if cond == 1:
			break
		for i in range(3):
			if galaxy_map[sector_int][row][i] == "   ":
				galaxy_map[sector_int][row][i] = colored(">  ", player_color, attrs=['bold', 'blink'])
				cond = 1
				break
	

	player["ships"]["total_ships"] += 1
	player["ships"]["sectors"].append(sector_int) #only one ship per player per sector
	return

# Removes ship at "sector"
def remove_ship(selected_player, sector_int):
	global current_player

	player = Players[selected_player]
	player_color = player["color"]

	#Check if player has ships in sector
	# if not player["ships"]["sectors"].index(sector_int):
	if sector_int not in player["ships"]["sectors"]:
		cprint("You don't have a ship in that sector", 'red', attrs=['bold', 'blink'])
		sleep(2)
		galaxy_page()
		return

	cond = 0
	for row in range(3):
		for i in range(3):
			if cond == 1:
				break
			if galaxy_map[sector_int][row][i] == colored(">  ", player_color, attrs=['bold', 'blink']):
				galaxy_map[sector_int][row][i] = "   "
				cond = 1
				break

	player["ships"]["total_ships"] -= 1
	player["ships"]["sectors"].remove(sector_int) #if only one ship per player per sector
	return

# Removes ship at "From" -- Adds ship at "To"
def move_ship(player, From, To):
	f = to_base_3(From)
	t = to_base_3(To)

	if abs(t[0]-f[0]) > 1 or abs(t[1]-f[1]) > 1:
		cprint("This is too far for the ship to move in one turn", 'red', attrs=['bold','blink'])
		sleep(3)
		return False

	add_ship(player, To)
	remove_ship(player, From)
	return True


# Sell a ship


# Build a colony
def build_colony(sector, planet_int):
	global current_player

	player = Players[current_player]
	planet = str(planet_int)
	star = str(sector)
	current_planet = Stars[sector]["planets"][planet]
	size = current_planet["size"]

	previous_colony_number = current_planet["colonies"]["colony_number"]

	# Add to the number of colonies (for printing planet)
	new_colony_number = previous_colony_number + 1


	# check if star dictionary exists for this player.  If not, create it.
	if star not in player["colonies"]:
		player["colonies"][star] = {}

	# add colony to player's dictionary
	player["colonies"][star][planet] = {
										"colony_number" : new_colony_number,
										"minerals" : current_planet["minerals"],
										"gas" : current_planet["gas"]
										}

	# # add 1 to number -- keeping track for victory condition
	# player["planets_colonized"] += 1
	# !!!  moved this to planet_page_options -- add colony doesn't add to planets_colonized


	# add colony to planet's dictionary
	current_planet["colonies"] = 	{
									"owner" : current_player,
									"colony_number" : new_colony_number
									}


	return


# Sell a colony

# Attack enemy ship near planet
def ship_attack(sector_int):
	global current_player

	ships_destroyed = []
	ships_fled = []

	ship_i = to_base_3(sector_int)[0]
	ship_j = to_base_3(sector_int)[1]

	#show galaxy page so players can see what happened to ships
	galaxy_page_visual()
	print "Defending sector %s!" % (sector_int)
	sleep(2)


	#go through each player
	for player in player_list:
		if player == current_player:
			continue
		player_color = Players[player]["color"]


		#if they have a ship in sector:
		if sector_int in Players[player]["ships"]["sectors"]:

			#show galaxy page so players can see what happened to ships
			galaxy_page_visual()
			sleep(1)
			print "pursuing " + colored("%s : \n" %(Players[player]["name"]), player_color)
			sleep(1)


			#randomize:  ship okay / ship flees / ship destroyed
			#if it's the player's last ship and they have no colonies, give them a good chance to flee
			if Players[player]["planets_colonized"] == 0 and Players[player]["ships"]["total_ships"] == 1:
				#3 chances to flee
				ship_status = randint(2,7)

			#otherwise, randomize:  ship okay / ship flees / ship destroyed
			else:
				ship_status = randint(1,9)



			# SHIP TRIES TO FLEE
			if ship_status in range(1,3):

				cprint("\t%s's ship attempting to flee." % (Players[player]["name"]), player_color)
				sleep(1)

				#player's ship gets a random number of attempts to flee...
				print "\n\tATTEMPTS : %s" %(ship_status + 1)
				for attempt in range(ship_status + 1):
					sleep(1)
					#try to flee to a random sector
					attempt_sector = randint(0,8)
					attempt_sector_i = to_base_3(attempt_sector)[0]
					attempt_sector_j = to_base_3(attempt_sector)[1]
					cprint("\t\tattempt %s : trying to flee to sector %s" % (attempt+1, attempt_sector), player_color)
					sleep(0.5)

					#if not too far to flee (it's an adjacent sector)...
					if abs(attempt_sector_i - ship_i) <= 1 and abs(attempt_sector_j - ship_j) <= 1 and attempt_sector != sector_int:

						#if player doesn't have a ship there already (it's available)...
						if attempt_sector not in Players[player]["ships"]["sectors"]:
							sleep(1)
							#the ship successfully flees!
							move_ship(player, sector_int, attempt_sector)
							#show galaxy page so players can see what happened to ships
							galaxy_page_visual()
							cprint("\t%s's ship fled from sector %s to sector %s.\n" \
							% (Players[player]["name"], sector_int, attempt_sector), player_color )
							sleep(2)
							#ship successfully fled, so break out of the "attempt" for-loop
							break

					#if ship wasn't able to flee, their ship gets destroyed
					if attempt == ship_status :
						sleep(1)
						remove_ship(player, sector_int)
						#show galaxy page so players can see what happened to ships
						galaxy_page_visual()
						cprint("\tAfter trying to flee, %s's ship was destroyed by %s in sector %s.\n" \
						% (Players[player]["name"], Players[current_player]["name"], attempt_sector), player_color )
						sleep(3)
						break



			# SHIP IS OKAY (NOTHING HAPPENS)
			elif ship_status in range(3,7):
				#show galaxy page so players can see what happened to ships
				galaxy_page_visual()
				print "pursuing " + colored("%s : \n" %(Players[player]["name"]), player_color)
				cprint("\t%s's ship evaded attack by %s.\n" \
				% (Players[player]["name"], Players[current_player]["name"]), player_color )
				sleep(3)


			# SHIP IS DESTROYED
			elif ship_status in range(7,10):
				remove_ship(player, sector_int)
				#show galaxy page so players can see what happened to ships
				galaxy_page_visual()
				print "pursuing " + colored("%s : \n" %(Players[player]["name"]), player_color)
				cprint("\t%s's ship was destroyed by %s in sector %s.\n" \
				% (Players[player]["name"], Players[current_player]["name"], sector_int), player_color )
				sleep(3)

	return





#Invade a planet currently colonized by another player
def invade_planet(sector_int, planet_int):
	global current_player

	planet = str(planet_int)
	star = str(sector_int)
	current_planet = Stars[star]["planets"][planet]
	colony_number = current_planet["colonies"]["colony_number"]
	cost_multiplier = 	Colony_Cost_Multiplier[ current_planet["type"] ]["minerals"] + \
						Colony_Cost_Multiplier[ current_planet["type"] ]["minerals"] / 2

	player = Players[current_player]
	defending_player = Players[ current_planet["colonies"]["owner"] ]

	decision = '' #in case this is the defender's last planet, set decision to empty string


	# used to give defender a boost when randomizing victory
	defense_factor = int(colonize_cost_minerals * colonize_cost_gas * cost_multiplier * colony_number)
	defense_boost = [defense_factor]



	#if this is the defender's ONLY  planet, it will be nearly impossible to invade successfuly
	if defending_player["planets_colonized"] == 1 :
		print "This is %s's only remaining planet." %(defending_player["name"])
		sleep(1)
		print "The planet's population will fight viciously to protect their home."
		sleep(2)
		print "It will be nearly impossible to successfully invade their last planet..."
		sleep(3)
		print "\t...Are you sure you want to attempt to invade?",
		decision = raw_input("\n\t(Y) to invade, (N) to abort  >  ")
		print 

		# invalid input
		if decision.lower() not in ['y', 'n']:
			print "That wasn't a clear answer..."
			sleep(2)
			print "I guess you aren't really serious about genocide, then, huh?"
			sleep(2)
			planet_page_visual(sector_int, planet_int)
			print "Invasion aborted."
			sleep(2)
			return 'invalid'

		# decide not to invade
		elif decision.lower() == 'n':
			print "That's what I figured."
			sleep(2)
			planet_page_visual(sector_int, planet_int)
			print "Invasion aborted."
			sleep(2)
			return 'aborted'

		# if they still want to try to invade, then continue.
		elif decision.lower() == 'y':
			print "Alright then.  Let's get this invasion under way!"
			defense_boost = [x for x in range(defense_factor*10, defense_factor*30, defense_factor)]
			sleep(2)



	planet_page_visual(sector_int, planet_int)

	# ask for resource ante (minerals)
	ante_m =''
	while ante_m.isdigit() == False:
		ante_m = raw_input("How much MINERALS will you put into this effort? >  ")
	ante_minerals = int(ante_m)
	# Prevent error from max memory storage for large list
	if ante_minerals > 10000:
		print "This is too large an investment.  The board won't allow you to spend this much on this one planet."
		sleep(3)
		planet_page(sector_int, planet_int)
		return
	# Prevent cheating by input of negative numbers
	if ante_minerals <= 0:
		print "Well, that's just impossible"
		sleep(3)
		planet_page(sector_int, planet_int)
		return

	# ask for resource ante (gas)
	ante_g = ''
	while ante_g.isdigit() == False:
		ante_g = raw_input("How much GAS will you put into this effort? >  ")
	ante_gas = int(ante_g)
	# Prevent error from max memory storage for large list
	if ante_gas > 10000:
		print "This is too large an investment.  The board won't allow you to spend this much on this one planet."
		sleep(3)
		planet_page(sector_int, planet_int)
		return
	# Prevent cheating by input of negative numbers
	if ante_minerals <= 0:
		print "Well, that's just impossible"
		sleep(3)
		planet_page(sector_int, planet_int)
		return


	# take the money (it's an ante, afterall)
	subtract_money(ante_minerals, ante_gas)


	#factors for randomizing invasion effectiveness
	ante_factor = ante_minerals * ante_gas
	#add an initial element to list [0] to avoid error 
	ante_list = range(0, int(ante_factor), 500) + [0]
	ante_random = choice(ante_list)


	#factors for randomizing defense effectiveness
	#add an initial element to list [defense_factor] to avoid error 
	defense_list = range(int((colony_cost_gas+colony_cost_minerals)*cost_multiplier), defense_factor, 500) + [defense_boost]
	defense_random = choice(defense_list)


	#Build the suspense...
	planet_page_visual(sector_int, planet_int)
	print "Prepare for invasion..."
	sleep(2)
	print "Invasion in progress..."
	sleep(2)
	


	# invasion failed
	if ante_random <= defense_random:
		# Invading player loses their ship
		planet_page_visual(sector_int, planet_int)
		print "The invasion was unsuccessful..."
		remove_ship(current_player, int(sector_int))
		sleep(2)
		return False




	# invasion was successful!
	else:
		# remove colony from defender["colonies"]
		del defending_player["colonies"][star][planet]

		# add colony to player["colonies"]
		
		# check if star dictionary exists for this player.  If not, create it.
		if star not in player["colonies"]:
			player["colonies"][star] = {}

		player["colonies"][star][planet] = {
											"colony_number" : current_planet["colonies"]["colony_number"],
											"minerals" : current_planet["minerals"],
											"gas" : current_planet["gas"]
											}

		# add 1 to number -- keeping track for victory condition
		player["planets_colonized"] += 1

		# subtract 1 to number -- keeping track for victory condition
		defending_player["planets_colonized"] -= 1

		# add colony to planet's dictionary
		current_planet["colonies"]["owner"] = current_player

	return True








########################################################################################
#---INITIAL CONDITIONS
########################################################################################




###...randomize stars, planets, resources...###

#randomize >> star location / number of planets / planet locations / planet descriptions
for star in Stars:
	planet_number = randint(1,4) #number of planets around this star
	location_list = sample( range(9) , planet_number + 1 ) #list of solar system locations
	star_location = location_list[planet_number] #star_location is last element in list
	planet_locations = location_list[:planet_number] #get all but star location


	Stars[star]["star_location"] = star_location
	Stars[star]["planet_number"] = planet_number
	Stars[star]["planet_locations"] = planet_locations
	Stars[star]["planets"] = {}


	for i in range(planet_number):
		#assign planet locations as the first elements in list (excluding last, which is star_location)
		planet_locations.append(location_list[i])
		planet_location = planet_locations[i]

		#get planet as a string (ex: "4"), since i is an int
		planet = str(planet_locations[i])
		#current planet location (from 0-8)
		Stars[star]["planets"][planet] = {}

		#This may be redundant... but just in case
		Stars[star]["planets"][planet]["location"] = planet_location

		#assign random description to each planet
		Stars[star]["planets"][planet]["size"] = choice(planet_sizes)
		Stars[star]["planets"][planet]["type"] = choice(planet_types)
		Stars[star]["planets"][planet]["color"] = choice(planet_colors)
		Stars[star]["planets"][planet]["zone"] = choice(planet_zones)

		#simpler to type for randomizing resources
		planet_type = Stars[star]["planets"][planet]["type"]
		#randomize resources!
		Stars[star]["planets"][planet]["minerals"] = choice( Resources[planet_type+"_minerals"] )
		Stars[star]["planets"][planet]["gas"] = choice( Resources[planet_type+"_gas"] )

		#leave this empty --> will name planet when you colonize it
		Stars[star]["planets"][planet]["name"] = 'unnamed planet'

		#leave this empty --> will add when it's colonized
		Stars[star]["planets"][planet]["colonies"] = 	{
														"owner" : '',
														"colony_number" : 0
														}



	

	


#Generate the list of solar systems in the galaxy
galaxy_map = deepcopy(sector_list) # Blank list to begin with

####    REFERENCE for Stars library:
# Stars[key]  =  [star_location, planet_number, [planet_locations], [planet_description]]
# planet_description = [planet_sizes, planet_types, planet_zones, planet_colors]

# Place the stars
for star in Stars:
	#Current star location (int from 0-8)
	i = to_base_3(Stars[star]["star_location"])[0]
	j = to_base_3(Stars[star]["star_location"])[1]
	# Place the star icon
	galaxy_map[ int(star) ][i][j] = colored( "("+star+")" , 'white')


	# Place the planets
	# for i in range( len(Stars[star]["planet_locations"]) ) :
	for planet in Stars[star]["planets"] :

		#current planet color
		planet_color = Stars[star]["planets"][planet]["color"]

		#Current planet location PL (int from 0-8)
		PL = Stars[star]["planets"][planet]["location"]
		# get PL into base 3
		i = to_base_3(PL)[0]
		j = to_base_3(PL)[1]

		# Place the planet icon

		#################################################################################
		# FOR A MORE COMPLEX MAP:
		if Stars[star]["planets"][planet]["size"] == "Large" and Stars[star]["planets"][planet]["type"] == "Gas":
			#ringed gas giants
			galaxy_map[ int(star) ][i][j] = colored( choice(["o  ", " o ", "  o"]),\
													planet_color)
		
		elif Stars[star]["planets"][planet]["size"] == "Large":
			# For large planets
			galaxy_map[ int(star) ][i][j] = colored( choice(["*  ", " * ", "  *"]),\
													planet_color)

		elif Stars[star]["planets"][planet]["size"] == "Binary":
			# For binary planets
			galaxy_map[ int(star) ][i][j] = colored( choice([\
													"'. ", ".' ", " '.", " .'",\
													":  ", " : ", "  :",\
													".. ", " .."]),\
													planet_color)
		
		else:
			# For Small and Medium planets (diversity)
			galaxy_map[ int(star) ][i][j] = colored( choice([\
													".  ", " . ", "  .",\
													".  ", " . ", "  .",\
													".  ", " . ", "  .",\

													"'  ", " ' ", "  '",\
													"'  ", " ' ", "  '"]),\
													planet_color)
		#################################################################################

		######################################################
		# IF WE WANT A SIMPLER MAP ... A PLANET IS JUST A PLANET:
		# galaxy_map[ int(star) ][i][j] = choice([".  ", " . ", "  ."])
		######################################################











########################################################################################
#---GAME START
########################################################################################

#explain purpose and rules of game
explain_game()


#give a preview of the map, in case you want to change it
current_player = "P1"
galaxy_page_visual()


# sleep(1)
# os.system('tput reset')


# get number of players
# os.system("clear && printf '\e[3J' ")
get_players()


# starting ship for everyone
for player in player_list:
	add_ship(player, choice(range(9)))








########################################################################################
#---TURN LOOP
########################################################################################
current_player = player_list[0]


def turn_loop():
		global current_player
		global player_list

		player_list.append( player_list.pop(0) )
		current_player = player_list[0]



		#player has no ships and no colonies --> Game Over for them
		for player in player_list:
			if Players[player]["planets_colonized"] == 0 and Players[player]["ships"]["total_ships"] == 0:
				os.system("clear && printf '\e[3J' ")
				print "\n"*15
				cprint("\t\t\t\t\t\t%s has been destroyed..." % (Players[player]["name"]), Players[player]["color"])
				print "\n"*15
				sleep(3)
				os.system("clear && printf '\e[3J' ")
				sleep(0.5)
				player_list.remove(player)
				
				#if last competing player is killed, then remaining player wins
				if len(player_list) == 1:
					cprint("\n"*15+"\t"*5+"%s IS VICTORIOUS!" % (	Players[player_list[0]]["name"].upper()),\
																	Players[player_list[0]]["color"], attrs=['blink']  )
					print "\n"*15
					sleep(5)
					return


				#if there are still more players in the game, continue playing
				turn_loop()
				return

		#Victory condition:
		if Players[current_player]["planets_colonized"] >= victory_condition:
			os.system("clear && printf '\e[3J' ")
			cprint("\n"*15+"\t"*5+"%s IS VICTORIOUS!" % (	Players[current_player]["name"].upper()),\
														Players[current_player]["color"], attrs=['blink']  )
			print "\n"*15
			sleep(5)
			return
		
		print "\nNow changing players..."
		sleep(1)

		mine_resources()

		galaxy_page()


		



turn_loop()

