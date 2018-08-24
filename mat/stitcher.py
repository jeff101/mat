import csv


prefix = 'C:\\Users\\Workstation\\Desktop\\Calibrate\\1803173_Ice_Bath_(0)_'

orient_file = prefix + 'MA.txt'
temp_file = prefix + 'T.txt'

with open(orient_file) as orient_fid, open(temp_file) as temp_fid, open(prefix+'JOINED.txt', 'w') as out_file:
    orient_size = sum(1 for line in orient_fid)
    temp_size = sum(1 for line in temp_fid)
    orient_fid.seek(0)
    temp_fid.seek(0)

    orient_header = orient_fid.readline().strip().split(',')
    orient = csv.reader(orient_fid)
    assert orient_header[0] == 'ISO 8601 Time', 'Orient file must have ISO 8601 Time'

    temp_header = temp_fid.readline().strip().split(',')
    temp = csv.reader(temp_fid)
    assert temp_header[0] == 'ISO 8601 Time', 'Temperature file must have ISO 8601 Time'

    big_file, small_file = (orient, temp) if orient_size >= temp_size else (temp, orient)
    header = orient_header + temp_header[1:] if orient_size >= temp_size else temp_header + orient_header[1:]

    print(header)
    out_file.write(','.join(header) + '\n')
    for line_small in small_file:
        out_file.write(','.join(line_small))