# 2025 Fall ECE Senior Design Miniproject Team 6

[Project definition](./Project.md)

## Features 
* Light to Sound conversion while continuously reading the photoresistor and mapping to a frequency range
* Recording with feedback, so when pressed the program clears past data and stores it using JSON Save/Load 
* Replay Mode to iterate through the stored samples in original order

This project, built with MicroPython and Thonny, takes the input of the photoresistor's brightness and outputs it as a sound, then is translated into a pitch on the piezo buzzer



## Hardware

* Raspberry Pi Pico WH [SC1634](https://pip.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w) (WiFi, Bluetooth, with header pins)
* Freenove Pico breakout board [FNK0081](https://store.freenove.com/products/fnk0081)
* Piezo Buzzer SameSky CPT-3095C-300
* 10k ohm resistor
* 2 [tactile switches](hhttps://www.mouser.com/ProductDetail/E-Switch/TL59NF160Q?qs=QtyuwXswaQgJqDRR55vEFA%3D%3D)


## Setup

* We have Install Thonny and picked Micropython as our language
* Plug in the Pi Pico
* Run main.py
* To record, type in the terminal the appropriate commands: start_recording(), stop_recording(), start_replay(), stop_replay()

## Tasks
* Tasks were distributed using the issues tab. We put all the tasks we needed to complete and used the assign function to assign them to the correct individual.
* Simulator Test - Yena Yu
* Hardware Test - Wenyuan Liu
* Light to Music - Leah Jones
* Play Music - Tadiwanashe Zinyongo
* Sensor Input - Astrid Elder
* Store Light - Charles Van Hook
