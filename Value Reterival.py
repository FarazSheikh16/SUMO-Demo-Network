#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci #importing traci library
import traci.constants as tc
import pytz
from random import randrange
import pandas as pd

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


#The function that contains TraCI control loop and we will perform our main interfacing here
#By writing our code in run function
def run():
    VehicleData = []
    while traci.simulation.getMinExpectedNumber() > 0:
       
        traci.simulationStep()
        Vehicle_ID_List=traci.vehicle.getIDList()
        for i in range(0,len(Vehicle_ID_List)):
                #Storing ID of Current Vehicle
                Vehicle_ID = Vehicle_ID_List[i] 
                x, y = traci.vehicle.getPosition(Vehicle_ID_List[i])
                #Storing x,y coordinate
                Co_ordinates = [x, y] 
                #Storing speed of current vehicle and converting it into km/h with precision o 2 decimal places
                Speed = round(traci.vehicle.getSpeed(Vehicle_ID_List[i])*3.6,2) 
                #getRoadID() will return the current edge on which vehicle is travelling 
                Edge = traci.vehicle.getRoadID(Vehicle_ID_List[i])
                #getLaneID() will return the current Lane on which vehicle is travelling 
                Lane_No = traci.vehicle.getLaneID(Vehicle_ID_List[i])
                #getDisatnce will return the distance and we rounded it upto 2 decimal places
                displacement = round(traci.vehicle.getDistance(Vehicle_ID_List[i]),2)

                vehList = [Vehicle_ID, Co_ordinates, Speed, Edge, Lane_No, displacement]
                #Prints Vehicle ID and Position Co-ordinates
                print("Vehicle: ",Vehicle_ID_List[i], " Position: ", Co_ordinates, \
                                     " Speed: ", round(traci.vehicle.getSpeed(Vehicle_ID_List[i])*3.6,2), "km/h  ", \
                                      #Prints Edge ID of vehicle
                                       " EdgeID of veh: ", traci.vehicle.getRoadID(Vehicle_ID_List[i]), "  ", \
                                      #Prints the LaneID of vehicle
                                       " LaneID of veh: ", traci.vehicle.getLaneID(Vehicle_ID_List[i]), "  ", \
                                      #Prints the distance to the starting point.
                                       " Distance: ", round(traci.vehicle.getDistance(Vehicle_ID_List[i]),3), "m  ", \
                       )
                VehicleData.append(vehList)
    traci.close()

    #Now for generate Excel file I used Pandas library here
    Column_Names = ['Vehicle_ID', 'Co_ordinates', 'Speed', 'Edge', 'Lane_No', 'displacement']
    dataset = pd.DataFrame(VehicleData, index=None, columns=Column_Names)
    dataset.to_excel("output.xlsx", index=False)

# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "test.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()