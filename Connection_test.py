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


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


#The function that contains TraCI control loop and we will perform our main interfacing 
#By writing our code in run function
def run():
    step = 0
    while step < 100:
        # traci.simulationStep() will start the time steps of Simulation
        traci.simulationStep() 
        print(step)
        # If the number of vehicles that were on the named induction loop within the last simulation step > 0 .
        # Then Set The Traffic Light of that lane 0 and its opp lane on opposite side to Green 
        # and other 2 on red in a junction.
        #if traci.inductionloop.getLastStepVehicleNumber("0") > 0: 
            #traci.trafficlight.setRedYellowGreenState("0", "GrGr")
        step += 1
    #When the condition of loop becomes false the traci will close the simulation using traci.close()
    traci.close()
    # This will clear the data that has been buffered to memory while printing steps/vehicles
    sys.stdout.flush() 

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