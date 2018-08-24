import serial
import serial.tools.list_ports
import re
import time
import datetime


def scan_for_gps():
    port_info = serial.tools.list_ports.grep('067B:2303')
    ports = []
    for port in port_info:
        ports.append(port.device)
    return ports


class Gps:
    def __init__(self, device):
        self.port = serial.Serial(device, 4800)
        self.latitude = None
        self.longitude = None
        self.utc = None
        self.observers = []

    def add_observer(self, observer):
        print('Adding observer')
        self.observers.append(observer)

    def run(self):
        # This is the format of the string we are parsing
        # $GPGGA,125742.000,4119.6607,N,07301.3281,W,1,09,1.0,100.3,M,-34.3,M,,0000*6D
        while True:
            while self.port.inWaiting():
                in_line = self.port.readline().decode('IBM437')
                if not self.verify_string(in_line):
                    continue
                if not in_line.startswith('$GPGGA'):
                    continue

                fields = in_line.split(',')
                latitude = self.convert_lat(fields[2], fields[3])
                longitude = self.convert_lon(fields[4], fields[5])
                utc = self.convert_time(fields[1])

                for observer in self.observers:
                    observer((utc, latitude, longitude))
            time.sleep(0.1)

    def verify_string(self, string):
        """
        Confirm the correct string format and calculate checksum
        The checksum is calculated by xor'ing each byte between the $ and *
        The checksum is the two digit value after the * (and is in hex)
        """
        regexp = re.search('^\$(GP[A-Z]{3}.+)\*([0-9A-F]{2})', string)
        if not regexp:
            return False
        checksum = int(regexp.group(2), 16)
        int_values = [ord(x) for x in regexp.group(1)]
        value = 0
        for x in int_values:
            value = value ^ x
        return True if value == checksum else False

    def convert_lat(self, lat_str, ns):
        latitude = float(lat_str[0:2]) + float(lat_str[2:9])/60
        latitude = -latitude if ns == 'S' else latitude
        return latitude


    def convert_lon(self, lon_str, ew):
        longitude = float(lon_str[0:3]) + float(lon_str[3:10])/60
        longitude = -longitude if ew == 'W' else longitude
        return longitude


    def convert_time(self, time_str):
        time_struct = time.strptime(time_str, '%H%M%S.%f')
        return '{:0>2d}:{:0>2d}:{:0>2d}'.format(time_struct.tm_hour, time_struct.tm_min, time_struct.tm_sec)


