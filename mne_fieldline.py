from fieldline_api.fieldline_service import FieldLineService

import logging
import argparse
import queue
import time
import sys

fieldline_client = None


def call_done():
    global done
    done = True

def connect(ip_list):
    fieldline_client = FieldLineService(ip_list)
    sensors = fieldline_client.load_sensors()
    print(f"Sensors available: {sensors}")

def tune_sensors():
    global fieldline_client
    if isinstance(fieldline_client, FieldLineService):
        sensors = fieldline_client.load_sensors()
        fieldline_client.set_closed_loop(True)

        fieldline_client.restart_sensors(sensors, on_next=lambda c_id, s_id: print(f'sensor {c_id}:{s_id} finished restart'),
                                on_error=lambda c_id, s_id, err: print(f'sensor {c_id}:{s_id} failed with {hex(err)}'),
                                on_completed=lambda: call_done())
        while not done:
            time.sleep(1)

        fieldline_client.coarse_zero_sensors(sensors,
                                    on_next=lambda c_id, s_id: print(f'sensor {c_id}:{s_id} finished coarse zero'),
                                    on_error=lambda c_id, s_id, err: print(
                                        f'sensor {c_id}:{s_id} failed with {hex(err)}'),
                                    on_completed=lambda: call_done())
        while not done:
            time.sleep(1)

        fieldline_client.fine_zero_sensors(sensors, on_next=lambda c_id, s_id: print(f'sensor {c_id}:{s_id} finished fine zero'),
                                  on_error=lambda c_id, s_id, err: print(
                                      f'sensor {c_id}:{s_id} failed with {hex(err)}'), on_completed=lambda: call_done())
        while not done:
            time.sleep(1)


def start_measurement():
    pass

def stop_measurement():
    pass

def disconnect():
    pass

def print_commands():
    print("Commands:")
    print("connect \t Connects to fieldline chassis and fieldtrip buffer")
    print("init \t\t Restart and tune sensors.")
    print("start \t\t Start receiving data.")
    print("stop \t\t Stop receiving data.")
    print("exit \t\t Stop receiving data and quit.")
    print("help \t\t Prints command list.")

if __name__ == "__main__":
    print("MNE Fieldline Connector v0.0.2\n")
    print_commands()
    print("")
    continue_loop = True
    while(continue_loop):
        command = input("Select command: ")
        if command == "start":
            print("Starting measurement...")
            start_measurement()
        elif command == "stop":
            print("Stopping measurement...")
            stop_measurement()
        elif command == "init":
            tune_sensors()
        elif command == "exit" or command == "quit":
            continue_loop = False
        elif command == "connect":
            connect()
        elif command == "help":
            print_commands()
    stop_measurement()
    disconnect()
