# 2025 Fall ECE Senior Design Miniproject Team 6

This project, built using MicroPython and Thonny, produces sound based on the brightness of the input light. It takes the brightness input via a photodiode, which is then translated into a pitch, which is then sent to the piezo buzzer to output as sound.  


[Project definition](./Project.md)



## Features 
* Continuous light to sound conversion from reading from the photoresistor and mapping it to a frequency range
* Recording and and saving to record and save the played notes for use later
* Replay Mode to iterate through the stored samples in the original order



## Hardware

* Raspberry Pi Pico WH [SC1634](https://pip.raspberrypi.com/categories/1088-raspberry-pi-pico-2-w) (WiFi, Bluetooth, with header pins)
* Freenove Pico breakout board [FNK0081](https://store.freenove.com/products/fnk0081)
* Piezo Buzzer SameSky CPT-3095C-300
* 10k ohm resistor
* 2 [tactile switches](hhttps://www.mouser.com/ProductDetail/E-Switch/TL59NF160Q?qs=QtyuwXswaQgJqDRR55vEFA%3D%3D)


## Setup

* Install Thonny and pick Micropython as the language
* Plug in the Pi Pico
* Run light_orchestra.py
* When using the record function, type the appropriate commands into the terminal: start_recording(), stop_recording(), start_replay(), stop_replay()

## Tasks
* Tasks were distributed using the issues tab. We put all the tasks we needed to complete and used the assign function to assign them to the correct individuals.
* Simulator Test - Yena Yu
* Hardware Test - Wenyuan Liu
* Light to Music - Leah Jones
* Play Music - Tadiwanashe Zinyongo
* Sensor Input - Astrid Elder
* Store Light - Charles Van Hook
