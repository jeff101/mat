import numpy as np
from mat import odlfile, converter
import matplotlib.pyplot as plt

with open(r'C:\Users\Workstation\Desktop\Tasks\Paul Lenz\1705130_Rotation_Test_(0).lid', 'rb') as fid:
    odl = odlfile.load_file(fid)
    conv = converter.Converter(odl.hoststorage)

    odl.load_page(0)
    mag = odl.magnetometer()
    mag = mag[:, 0:36000]

    intervals = 45
    mag = np.stack(np.hsplit(mag, intervals))
    mag = np.transpose(np.mean(mag, 2))

    mag = conv.magnetometer(mag)
    plt.plot(mag[1,:])
    plt.show()
