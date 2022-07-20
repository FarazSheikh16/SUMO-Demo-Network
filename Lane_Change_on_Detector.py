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
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():
    step = 0
    # Loop will run untill the minimum number of active vehicles is greater than 0. 
    while traci.simulation.getMinExpectedNumber() > 0: 
        # traci.simulationStep() will start the time steps of Simulation
        traci.simulationStep()
        print(step)
        #Storing the ID's of Vehicle that has last passed from detector named "det_2"
        det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_2")
        for veh in det_vehs:
            print(veh) # Prints The vehicle ID of vehicle that will be passed from detector
            # Detector has been Placed in the Lane 0 whenever the vehicle arrives on it.
            # Its lane will be changed from 0 to 1 for 20 time steps
            traci.vehicle.changeLane(veh, 1, 20)
        step += 1
    #When the condition of loop becomes false the traci will close the simulation using traci.close()
    traci.close()
    # This will clear the data that has been buffered to memory while printing steps
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