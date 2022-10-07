from msilib.schema import Error
import pyrealsense2 as rs
import argparse
import json
import os
import sys
import pprint

def enumerate_connected_devices(context):
    """
    Enumerate the connected Intel RealSense devices

    Parameters:
    -----------
    context 	   : rs.context()
                     The context created for using the realsense library

    Return:
    -----------
    connect_device : array
                     Array of (serial, product-line) tuples of devices which are connected to the PC

    """
    connect_device = []

    for d in context.devices:
        if d.get_info(rs.camera_info.name).lower() != 'platform camera':
            serial = d.get_info(rs.camera_info.serial_number)
            product_line = d.get_info(rs.camera_info.product_line)
            device_info = (serial, product_line)  # (serial_number, product_line)
            connect_device.append(device_info)
    return connect_device

def get_base_dir(path: str) -> str:
    DEFAULT_BASE_DIR: str = "./realsense_data"
    if os.path.exists(path):
        try:
            tmp = json.load(open(path, 'r'))
            assert 'realsense_data_dir' in tmp.keys()
            return tmp['realsense_data_dir']
        except:
            return DEFAULT_BASE_DIR
    return DEFAULT_BASE_DIR
    
    
def main(args):
    EXEC_STRING = "python"
    context = rs.context()
    available_devices = enumerate_connected_devices(context)
    enumerated_device_types = set([device[1] for device in available_devices])

    device_by_type = {tag:list(filter(lambda x: x[1] == tag, available_devices)) for tag in enumerated_device_types}

    if args.a:
        print("Available devices connected to the system:")
        pprint.pprint(device_by_type)
        return

    port = args.port
    base_dir = get_base_dir(args.config)
    if len(device_by_type) > 0:
        for tag in device_by_type.keys():
            for idx in range(len(device_by_type[tag])):
                if sys.platform == "win32":
                    print(f"Start-Process {EXEC_STRING} -ArgumentList \"-m\", \"realsense_remote.main\", \"--device={tag}\", \"--idx={idx}\", \"--port={port}\", \"--base_dir={base_dir}\"")
                    port += 1
                elif sys.platform == "linux":
                    print(f"{EXEC_STRING} -m realsense_remote.main --device={tag} --idx={idx} --port={port} --base_dir={base_dir} 2>&1 & ")
                    port += 1
                else:
                    raise Error(f"Platform {sys.platform} not supported")
    else:
        print("realsense camera not found")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="Starting port number, default is 5050", default=5050)
    parser.add_argument('--config', type=str, default='./config.json')
    parser.add_argument('-a', action="store_true", help="Show all connected devices")
    args = parser.parse_args()
    main(args)