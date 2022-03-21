from fieldline_api.fieldline_service import FieldLineService

import logging
import argparse
import queue
import time
import sys
import FieldTrip
import numpy as np

def connect_to_fieldline(fieldline_client, ip_list):
    fieldline_client = FieldLineService(ip_list)
    fieldline_client.open() # this is where we connect
    sensors = fieldline_client.load_sensors()
    print(f"Sensors available: {sensors}")

def connect_to_fieldtrip_buffer(ft_client, ft_ip, ft_port):
    ft_client.connect(ft_ip, ft_port)
    if ft_client.isConnected:
        print("Fieldtrip Client connected")


def init_ft_header(ft_client, fieldline_client, frequency):
    if ft_client.isConnected and fieldline_client:
        num_sensors = len(fieldline_client.load_sensors())
        ft_client.putHeader(num_sensors, frequency, FieldTrip.DATATYPE_FLOAT32)
        header = ft_client.getHeader()
        if header.nChannels == num_sensors:
            print("Fieldtrip header initialized")


def restart_sensors(fieldline_client):
    sensors = fieldline_client.load_sensors()
    done = False
    def call_when_done():
        nonlocal done
        done = True
    fieldline_client.restart_sensors(sensors,
                                     on_next=lambda c_id, s_id: print(f'sensor {c_id}:{s_id} finished restart'),
                                     on_error=lambda c_id, s_id, err: print(
                                         f'sensor {c_id}:{s_id} failed with {hex(err)}'),
                                     on_completed=lambda: call_when_done())

    while not done:
        time.sleep(1)


def coarse_tune_sensors(fieldline_client):
    sensors = fieldline_client.load_sensors()
    done = False
    def call_when_done():
        nonlocal done
        done = True
    fieldline_client.coarse_zero_sensors(sensors,
                                         on_next=lambda c_id, s_id: print(f'sensor {c_id}:{s_id} finished coarse zero'),
                                         on_error=lambda c_id, s_id, err: print(
                                             f'sensor {c_id}:{s_id} failed with {hex(err)}'),
                                         on_completed=lambda: call_when_done())
    while not done:
        time.sleep(1)


def fine_tune_sensors(fieldline_client):
    sensors = fieldline_client.load_sensors()
    done = False
    def call_when_done():
        nonlocal done
        done = True
    fieldline_client.fine_zero_sensors(sensors,
                                       on_next=lambda c_id, s_id: print(f'sensor {c_id}:{s_id} finished fine zero'),
                                       on_error=lambda c_id, s_id, err: print(
                                           f'sensor {c_id}:{s_id} failed with {hex(err)}'),
                                       on_completed=lambda: call_when_done())
    while not done:
        time.sleep(1)


def tune_sensors(fieldline_client):
    if isinstance(fieldline_client, FieldLineService):
        fieldline_client.set_closed_loop(True)

        restart_sensors(fieldline_client)
        coarse_tune_sensors(fieldline_client)
        fine_tune_sensors(fieldline_client)


def start_measurement(fieldline_client, callback_function):
    fieldline_client.read_data(callback_function)
    fieldline_client.start_adc(0)


def stop_measurement(fieldline_client):
    fieldline_client.stop_adc(0)
    fieldline_client.read_data()


def turn_off_sensors(fieldline_client):
    sensors = fieldline_client.load_sensors()
    fieldline_client.turn_off_sensors(sensors)


def disconnect(fieldline_client):
    pass


class MNEClient:
    def __init__(self, fieldline_chassis_ips = None, fieldtrip_ip = "127.0.0.1", fieldtrip_port = 1972):
        self.fieldline_client = None
        self.fieldtrip_client = None
        self.fieldline_chassis_ips = fieldline_chassis_ips
        self.fieldtrip_ip = fieldtrip_ip
        self.fieldtrip_port = fieldtrip_port

    def connect_to_chassis(self):
        if self.fieldline_chassis_ips:
            connect_to_fieldline(self.fieldline_client, self.fieldline_chassis_ips)

    def connect_to_buffer(self):
        self.fieldtrip_client = FieldTrip.Client()
        connect_to_fieldtrip_buffer(self.fieldtrip_client, self.fieldtrip_ip, self.fieldtrip_port)

    def tune(self):
        tune_sensors(self.fieldline_client)

    def start_acquisition(self):
        def parse_data(data):
            chunk = np.zeros((len(data), num_working_sensors()), dtype=np.single)
            for sample_i in range(len(data)):
                for ch_i, channel in enumerate(channel_key_list):
                    chunk[sample_i, ch_i] = data[0][channel]["data"] * data[0][channel]["calibration"]
            # ft_client.putData(chunk)
            self.fieldline_client.putData(chunk)
        start_measurement(self.fieldline_client, parse_data)

    def stop_acquisition(self):
        pass


def _test_print_data(iplist):
    pass

# def print_commands():
#     print("Commands:")
#     print("connect \t Connects to fieldline chassis and fieldtrip buffer")
#     print("init \t\t Restart and tune sensors.")
#     print("start \t\t Start receiving data.")
#     print("stop \t\t Stop receiving data.")
#     print("exit \t\t Stop receiving data and quit.")
#     print("help \t\t Prints command list.")
#
# if __name__ == "__main__":
#     print("MNE Fieldline Connector v0.0.2\n")
#     print_commands()
#     print("")
#     continue_loop = True
#     while(continue_loop):
#         command = input("Select command: ")
#         if command == "start":
#             print("Starting measurement...")
#             start_measurement()
#         elif command == "stop":
#             print("Stopping measurement...")
#             stop_measurement()
#         elif command == "init":
#             tune_sensors()
#         elif command == "exit" or command == "quit":
#             continue_loop = False
#         elif command == "connect":
#             connect()
#         elif command == "help":
#             print_commands()
#     stop_measurement()
#     disconnect()
