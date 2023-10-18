#!/usr/bin/env python

import time
from tqdm import tqdm
import json

class Particle:
    def __init__(self):
        self.density = 0.0
        self.xForce = 0.0
        self.xVelocity = 0.0
        self.yForce = 0.0
        self.yVelocity = 0.0
        self.wallflag = 0
        self.dead = False
        self.xPos = 0.0
        self.yPos = 0.0

CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 24

particles = []
totalOfParticles = 0

simulation_data_file_directory = 'simulation_data.json'
gravity = 1
pressure = 4
viscosity = 7

def settings():
    global simulation_data_file_directory
    global gravity
    global pressure
    global viscosity
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    settingsNavigation = input("Change Simulation File Directory - 1, Change Simulation Parameters - 2, Reset to Defaults - 3, Return to main menu - 4: \n\n\n")
    if settingsNavigation == "1":
        simulation_data_file_directory_input = input("Input File Directory (include file name, relative file directry supported): \n\n\n")
        changeOrNot_directory= input("Press Enter to cancel change, enter 'y' to save setting, enter 'r' to reset to default: \n\n\n")
        if changeOrNot_directory == '':
            pass
        elif changeOrNot_directory == 'y':
            simulation_data_file_directory = simulation_data_file_directory_input
        elif changeOrNot_directory == 'r':
            simulation_data_file_directory = 'simulation_data.json'
        else:
            print("Please enter a valid imput!\n\n\n")
            pass
    if settingsNavigation == "2":
        while True:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            parametersNavigation = input("Gravity - 1, Pressure - 2, Viscosity - 3, Return - 4: \n\n\n")
            if parametersNavigation == "1":
                gravity_input = input("Input gravity parameter: \n\n\n")
                changeOrNot_gravity = input("Press Enter to cancel change, enter 'y' to save setting, enter 'r' to reset to default: \n\n\n")
                if changeOrNot_gravity == '':
                    pass
                elif changeOrNot_gravity == 'y':
                    gravity = int(gravity_input)
                elif changeOrNot_gravity == 'r':
                    gravity = 1
                else:
                    print("Please enter a valid imput!\n\n\n")
                    pass
            if parametersNavigation == "2":
                pressure_input = input("Input pressure parameter: \n\n\n")
                changeOrNot_pressure = input("Press Enter to cancel change, enter 'y' to save setting, enter 'r' to reset to default: \n\n\n")
                if changeOrNot_pressure == '':
                    pass
                elif changeOrNot_pressure == 'y':
                    pressure = int(pressure_input)
                elif changeOrNot_pressure == 'r':
                    pressure = 1
                else:
                    print("Please enter a valid imput!\n\n\n")
                    pass
            if parametersNavigation == "3":
                viscosity_input = input("Input viscosity parameter: \n\n\n")
                changeOrNot_viscosity = input("Press Enter to cancel change, enter 'y' to save setting, enter 'r' to reset to default: \n\n\n")
                if changeOrNot_viscosity == '':
                    pass
                elif changeOrNot_viscosity == 'y':
                    viscosity = int(viscosity_input)
                elif changeOrNot_viscosity == 'r':
                    viscosity = 1
                else:
                    print("Please enter a valid imput!\n\n\n")
                    pass
            if parametersNavigation == "4":
                settings()
    if settingsNavigation == "3":
        confirmResetSettings = input("Input y to reset to defaults, input anything else to cancel: \n\n\n")
        if confirmResetSettings == 'y':
            simulation_data_file_directory = 'simulation_data.json'
            gravity = 1
            pressure = 4
            viscosity = 7
        else:
            pass
    if settingsNavigation == "4":
        main()
    
def create_simulation():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    input_lines = []
    create_output = ""
    preventEmptySimulation = 0
    for i in range(0, 24):
        input_value = input("Enter input (max 80x24): ")
        if input_value == "":
            input_lines.append(input_value + '\n')
        else:
            input_lines.append(input_value + '\n')
            preventEmptySimulation = preventEmptySimulation + 1
    if preventEmptySimulation == 0:
        print("Error: Empty Simulation!")
    else:
        pass
        create_output = ''.join(input_lines)
        saveOrNot = input("Save Simulation?(y/n) \n\n\n")
        if saveOrNot == "y":
            create_simulation_name = input("Enter Simulation Name: \n\n\n")

            with open(f'{simulation_data_file_directory}', 'r') as json_file:
                data_before = dict(json.load(json_file))
                data_before[f"{create_simulation_name}"] = {
                    "data": f"{create_output}"
                    }
            with open(f'{simulation_data_file_directory}', 'w') as json_file:
                data_after = data_before
                print(data_after)
                json.dump(data_after, json_file)
        else:
            pass

# Define the simulations

with open(f'{simulation_data_file_directory}', 'r') as json_file:
    simulation_data = json.load(json_file)

def loadSimulation(selectedSimulation):
    global particles, totalOfParticles
    particles = []
    totalOfParticles = 0
    xSandboxAreaScan = 0
    ySandboxAreaScan = 0
    particlesCounter = 0
    simulation_data_loaded = ""
    try:
        simulation_data_loaded = simulation_data[selectedSimulation]["data"]
    except KeyError:
        print("Invalid Simulation Name!")
    for x in simulation_data_loaded:
        if x == "\n":
            ySandboxAreaScan += 2
            xSandboxAreaScan = -1
        elif x != " ":
            particles.append(Particle())
            particles.append(Particle())
            if x == "#":
                particles[particlesCounter].wallflag = particles[particlesCounter + 1].wallflag = 1
            particles[particlesCounter].xPos = xSandboxAreaScan
            particles[particlesCounter].yPos = ySandboxAreaScan
            particles[particlesCounter + 1].xPos = xSandboxAreaScan
            particles[particlesCounter + 1].yPos = ySandboxAreaScan + 1
            particlesCounter += 2
            totalOfParticles = particlesCounter
        xSandboxAreaScan += 1

def calculateDensities(particles, totalOfParticles):
    for particlesCursor in range(totalOfParticles):
        if particles[particlesCursor].dead:
            continue
        particles[particlesCursor].density = particles[particlesCursor].wallflag * 9
        for particlesCursor2 in range(totalOfParticles):
            if particles[particlesCursor2].dead:
                continue
            xParticleDistance = particles[particlesCursor].xPos - particles[particlesCursor2].xPos
            yParticleDistance = particles[particlesCursor].yPos - particles[particlesCursor2].yPos
            particlesDistance = ((xParticleDistance ** 2) + (yParticleDistance ** 2)) ** 0.5
            particlesInteraction = particlesDistance / 2.0 - 1.0
            if int(1.0 - particlesInteraction) > 0:
                particles[particlesCursor].density += particlesInteraction ** 2

def calculateForces(particles, totalOfParticles):
    for particlesCursor in range(totalOfParticles):
        if particles[particlesCursor].wallflag == 1 or particles[particlesCursor].dead:
            continue
        particles[particlesCursor].yForce = gravity
        particles[particlesCursor].xForce = 0
        for particlesCursor2 in range(totalOfParticles):
            if particles[particlesCursor2].dead:
                continue
            xParticleDistance = particles[particlesCursor].xPos - particles[particlesCursor2].xPos
            yParticleDistance = particles[particlesCursor].yPos - particles[particlesCursor2].yPos
            particlesDistance = ((xParticleDistance ** 2 + yParticleDistance ** 2)) ** 0.5
            particlesInteraction = particlesDistance / 2.0 - 1.0
            if int(1.0 - particlesInteraction) > 0:
                particles[particlesCursor].xForce += particlesInteraction * (
                    xParticleDistance * (3 - particles[particlesCursor].density - particles[particlesCursor2].density) * pressure +
                    particles[particlesCursor].xVelocity * viscosity - particles[particlesCursor2].xVelocity * viscosity
                ) / particles[particlesCursor].density

                particles[particlesCursor].yForce += particlesInteraction * (
                    yParticleDistance * (3 - particles[particlesCursor].density - particles[particlesCursor2].density) * pressure +
                    particles[particlesCursor].yVelocity * viscosity - particles[particlesCursor2].yVelocity * viscosity
                ) / particles[particlesCursor].density

def simulationNextStep(particles, totalOfParticles):
    calculateDensities(particles, totalOfParticles)
    calculateForces(particles, totalOfParticles)
    screenBuffer = [0] * (CONSOLE_WIDTH * CONSOLE_HEIGHT)

    for screenBufferIndex in range(CONSOLE_WIDTH * CONSOLE_HEIGHT):
        screenBuffer[screenBufferIndex] = 0

    for particlesCursor in range(totalOfParticles):
        if particles[particlesCursor].wallflag == 0:
            if (particles[particlesCursor].xForce ** 2 + particles[particlesCursor].yForce ** 2) < 4.2:
                particles[particlesCursor].xVelocity += particles[particlesCursor].xForce / 10
                particles[particlesCursor].yVelocity += particles[particlesCursor].yForce / 10
            else:
                particles[particlesCursor].xVelocity += particles[particlesCursor].xForce / 11
                particles[particlesCursor].yVelocity += particles[particlesCursor].yForce / 11

            particles[particlesCursor].xPos += particles[particlesCursor].xVelocity
            particles[particlesCursor].yPos += particles[particlesCursor].yVelocity

        x = round(particles[particlesCursor].xPos)
        y = round(particles[particlesCursor].yPos / 2)
        screenBufferIndex = round(x + CONSOLE_WIDTH * y)

        if 0 <= y < CONSOLE_HEIGHT - 1 and 0 <= x < CONSOLE_WIDTH - 1:
            screenBuffer[screenBufferIndex] |= 8
            screenBuffer[screenBufferIndex + 1] |= 4
            screenBuffer[screenBufferIndex + CONSOLE_WIDTH] |= 2
            screenBuffer[screenBufferIndex + CONSOLE_WIDTH + 1] |= 1
        else:
            particles[particlesCursor].dead = True

    screenBufferString = ''
    for screenBufferIndex in range(CONSOLE_WIDTH * CONSOLE_HEIGHT):
        if screenBufferIndex % CONSOLE_WIDTH == CONSOLE_WIDTH - 1:
            screenBufferString += '\n'
        else:
            screenBufferString += " '`-.|//,\\|\\_\\/#"[screenBuffer[screenBufferIndex]]
    
    simulation_steps.append(screenBufferString)
    
def main():
    global simulation_steps
    simulation_steps = []
    navigation = input("NAVIGATION: Start new simulation - 1, Import simulation - 2, Create Simulation - 3, Settings - 4, Exit - 5: \n\n\n")
    if navigation == "1":
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        selectedSimulation = input("Select simulation: \n\n\n")
        if selectedSimulation != '':
            pass
        else:
            print("Please enter a valid simulation name!")
            main()
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        simulationSteps = input("Simulation Steps (50 Step = 1sec, Max 180,000 steps (1 hour)): \n\n\n")
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        displaysimulation = input("Display simulation while simulating (may cause lag)?(y/n) \n\n\n")
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if simulationSteps.isdigit() and 1 <= int(simulationSteps) <= 180000:
            loadSimulation(selectedSimulation) 
            if displaysimulation == "y":
                for _ in tqdm(range(int(simulationSteps)), desc="Simulating...", ncols=100):
                    simulationNextStep(particles, totalOfParticles)
                    print(simulation_steps[-1])
            else:
                for _ in tqdm(range(int(simulationSteps)), desc="Simulating...", ncols=100):
                    simulationNextStep(particles, totalOfParticles)

            def playSimulation():
                for step in simulation_steps:
                    print(step)
                    time.sleep(0.02)
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("Finished Simulating\n\n\n")
            print("Press enter to play simulation, type anything else to skip.\n\n\n")
            playSimulationInput = input()
            if playSimulationInput == '':
                playSimulation()
            else:
                pass
            print("Press enter to continue, type anything else to repeat.\n\n\n")
            repeatSimulation = input()
            if repeatSimulation != '':
                playSimulation()
            else:
                pass
            
            with open('simulation_backup.json', 'w') as json_file:
                    json.dump(simulation_steps, json_file)

            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            export = input("Export simulation as json ?(y/n) \n\n\n")
            if export == "y":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                export_name = input("Simulation name: \n\n\n")
                with open(f'{export_name}.json', 'w') as json_file:
                    json.dump(simulation_steps, json_file)
            else:
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            main()
        
        else:
            if simulationSteps == "debug":
                loadSimulation(selectedSimulation) 
                while True:
                    simulationNextStep(particles, totalOfParticles)
                    print(simulation_steps[-1])
                    print("\nTotal of particles: ")
                    print(totalOfParticles)
            else:
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                print("Please enter a valid integer\n\n\n")
    elif navigation == "2":
        import_steps = []
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        import_file = input("Enter file directroy: \n\n\n")
        with open(import_file, 'r') as json_file:
            import_steps = json.load(json_file)
        for import_step in import_steps:
            print(import_step)
            time.sleep(0.02)
            
    elif navigation == "3":
        create_simulation()
        main()
        
    elif navigation == "4":
        settings()
        
    elif navigation == "5":
        exit()
        
    else:
        print("Please enter a valid input!")
        main()
            
# Main execution
if __name__ == "__main__":
    title = str("                                                                    ########\n#############################                     ####              #......#\n#....................##.....#                    #....#             #......#\n#....................##.....#                     ####              #......#\n##......#########....##.....#                                       #.....# \n  #.....#       ###### #....# ######    ######  #######     #########.....# \n  #.....#              #....# #....#    #....#  #.....#   ##..............# \n  #......##########    #....# #....#    #....#   #....#  #................# \n  #...............#    #....# #....#    #....#   #....# #.......#####.....# \n  #...............#    #....# #....#    #....#   #....# #......#    #.....# \n  #......##########    #....# #....#    #....#   #....# #.....#     #.....# \n  #.....#              #....# #....#    #....#   #....# #.....#     #.....# \n  #.....#              #....# #.....####.....#   #....# #.....#     #.....# \n##.......##           #......##...............###......##......#####......##\n#........##           #......# #...............##......# #.................#\n#........##           #......#  ##........##...##......#  #.........###....#\n###########           ########    ########  ############   #########   #####\n\n\n\n\n----------------------------------------------------------------------------\n")
    print(title)
    time.sleep(1)
    with open('title.json', 'r') as json_file:
        title_steps = json.load(json_file)
        for title_step in title_steps:
            print(f'\n{title_step}')
            time.sleep(0.02)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Welcome to Fluid.\n\n\n")
    time.sleep(2)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    while True:
        main()