# 2025 Fall ECE Senior Design Miniproject Team 6

This project, built using MicroPython and Thonny, produces sound based on the brightness of the input light. It takes the brightness input via a photodiode, which is then translated into a pitch, which is then sent to the piezo buzzer to output as sound.  


[Project definition](./Project.md)



## Features 
* Light to Sound conversion while continuously reading the photoresistor and mapping to a frequency range
* Recording with feedback, so when pressed the program clears past data and stores it using JSON Save/Load 
* Replay Mode to iterate through the stored samples in original order



## Hardware

* Raspberry Pi Pico WH [SC1634](https://pip.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w) (WiFi, Bluetooth, with header pins)
* Freenove Pico breakout board [FNK0081](https://store.freenove.com/products/fnk0081)
* Piezo Buzzer SameSky CPT-3095C-300
* 10k ohm resistor
* 2 [tactile switches](hhttps://www.mouser.com/ProductDetail/E-Switch/TL59NF160Q?qs=QtyuwXswaQgJqDRR55vEFA%3D%3D)


## Setup

* Install Thonny and picked Micropython as our language
* Plugged in the Pi Pico
* Ran main.py
* When using the record function, typed in the terminal the appropriate commands: start_recording(), stop_recording(), start_replay(), stop_replay()

## Tasks
* Tasks were distributed using the issues tab. We put all the tasks we needed to complete and used the assign function to assign them to the correct individual.
* Simulator Test - Yena Yu
* Hardware Test - Wenyuan Liu
* Light to Music - Leah Jones
* Play Music - Tadiwanashe Zinyongo
* Sensor Input - Astrid Elder
* Store Light - Charles Van Hook
