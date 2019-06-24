def read(file_path):
    f = open(file_path, mode="r")
    lines = f.readlines()
    result = []
    for line in lines[2:]:
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        data = line.split(" ")
        data_dict = {}
        data_dict['x'] = int(data[0])
        data_dict['y'] = int(data[1])
        data_dict['rad'] = float(data[2])
        result.append(data_dict)
        # print(result[-1])
    return result


if __name__ == "__main__":
    read(r"C:\Users\skconan\Desktop\FingerPrint\pysource\FingerNet\Minutiae\F0024301.mnt")
