"""Script for running simulation setup in a loop, with various settings and times."""
import datetime
import os
import clr
import time
import itertools
import json
import shutil

# Load the rFpro.Controller DLL/Assembly
clr.AddReference("C:/rFpro/2023b/API/rFproControllerExamples/Controller/rFpro.Controller")

# Import rFpro.controller and some other helpful .NET objects
from rFpro import Controller
from System import DateTime, Decimal

# Define save location (edit as needed)
campaign_name = 'generic_simulation'
save_loc = f'C:/Users/ElliotLondon/Documents/PythonLocal/Misc/results/{campaign_name}'

# Define location of .json to load SL settings
sl_settings = 'C:/Users/ElliotLondon/Documents/PythonLocal/Misc/configs/sl_settings.json'

# Simulation settings for the current campaign. Load from configs/sl_settings_default.json
with open(f'../configs/{sl_settings}.json', 'r') as file:
    jdict = json.load(file)
save = jdict['general']['save']
times = jdict['general']['times']
cloudiness = jdict['weather']['cloudiness']
rain = jdict['weather']['rain']
fog = jdict['weather']['fog']

# Create an instance of the rFpro.Controller
rFpro = Controller.DeserializeFromFile('../configs/autogen/2kFlatLHD.json')

# Static settings
rFpro.DynamicWeatherEnabled = True
rFpro.Camera = 'Nosecam'
rFpro.ParkedTrafficDensity = Decimal(0.5)
rFpro.Vehicle = 'Hatchback_AWD_Red'
rFpro.VehiclePlugin = 'RemoteModelPlugin'

# General comments for simulation run
comments = 'Generic test simulation run'

# Iterate over times within the .json folder
for t in times:
    rFpro.StartTime = DateTime.Parse(t)
    # Iterate for each combination of simulation settings
    for rFpro.Cloudiness, rFpro.Rain, rFpro.Fog in itertools.product(cloudiness, rain, fog):
        # Open the TrainingData.ini file and correctly adjust the saving folder (with date/time)
        with open(r"C:/rFpro/2023b/rFpro/Plugins/WarpBlend/TrainingData.ini", 'r') as f:
            training_data = f.readlines()
        now = datetime.datetime.now()
        folder_time = f'{now.year}{now.month:02d}{now.day:02d}_{now.hour:02d}{now.minute:02d}{now.second:02d}'
        save_loc = str(f'{save_loc}/{folder_time}')
        print(f'Saving at: {save_loc}')
        training_data[1] = 'OutputDir=' + save_loc + '\n'
        with open(r"C:/rFpro/2023b/rFpro/Plugins/WarpBlend/TrainingData.ini", 'w') as f:
            f.writelines(training_data)

        # Connect
        while rFpro.NodeStatus.NumAlive < rFpro.NodeStatus.NumListeners:
            print(f'{rFpro.NodeStatus.NumAlive} of {rFpro.NodeStatus.NumListeners} Listeners connected.')
            time.sleep(1)
        print(f'{rFpro.NodeStatus.NumAlive} of {rFpro.NodeStatus.NumListeners} Listeners connected.')

        # Start the session. Toggle traffic AI if necessary
        rFpro.StartSession()
        # rFpro.ToggleAi()

        # When a certain amount of time is reached, kill the session. If it is killed remotely, the next settings combo
        # will initiate automatically within the loop.
        t1 = time.time()
        while True:
            t2 = time.time()
            if (t2 - t1) >= 100.0:
                rFpro.StopSession()
                break

print("Simulation campaign complete!\n")
print("\nScript executed successfully. Exiting...")
