import jsonpickle
import numpy as np

class PointField:
    name:str = ""
    offset:int = 0
    datatype:int = 0
    count:int = 0

class Header:
    seq: int = 0
    frame_id: str = ""
    stamp: int = 0

class PointCloud2:
    header:Header = Header()
    height: int = 0
    width: int = 0
    fields = []
    is_bigendian: bool = False
    point_step:int = 0
    row_step:int = 0
    is_dense: bool = False
    data:any

def msg_construct(data):
    print("decode")
    list = data.split(',',20)
    print(list)
    Cloud = PointCloud2()
    Cloud.header.seq = int(list[1])#uint32
    Cloud.header.frame_id = str(list[0])
    Cloud.header.stamp = 0
    Cloud.height = int(list[2])#uint32
    Cloud.width = int(list[3])#uint32

    Fieldx = PointField()
    Fieldx.name = "x"
    Fieldx.offset = int(list[4])#uint32
    Fieldx.datatype = int(list[5])
    Fieldx.count = int(list[6])
    Cloud.fields.append(Fieldx)

    Fieldy = PointField()
    Fieldy.name = "y"
    Fieldy.offset = int(list[7])#uint32
    Fieldy.datatype = int(list[8])
    Fieldy.count = int(list[9])
    Cloud.fields.append(Fieldy)

    Fieldz= PointField()
    Fieldz.name = "z"
    Fieldz.offset = int(list[10])#uint32
    Fieldz.datatype = int(list[11])
    Fieldz.count = int(list[12])
    Cloud.fields.append(Fieldz)

    Fieldi = PointField()
    Fieldi.name = "intensity"
    Fieldi.offset = int(list[13])#uint32
    Fieldi.datatype = int(list[14])
    Fieldi.count = int(list[15])
    Cloud.fields.append(Fieldi)

    if list[16]=="false":
        Cloud.is_bigendian = bool(0)
    else:
        Cloud.is_bigendian = bool(1)
    Cloud.point_step = int(list[17])#uint32
    Cloud.row_step = int(list[18])#uint32
    if list[19]=="false":
        Cloud.is_dense = bool(0)
    else:
        Cloud.is_dense = bool(1)

    count = Cloud.height*Cloud.row_step

    data_ = list[20]
    for i in range(0,count):
        Cloud.data+=data_[i]
    #print str(Cloud)
    print (f"save points from seq: {Cloud.header.seq}")
    return Cloud

if __name__=="__main__":
    with open('test.csv', 'r') as file:
        data = file.read().split('\n')
        data_array = data[2].split(",")
        header = data_array[:32]
        timstamp,dunno1,name,dunno2,dunno3,\
            xName,xOffset,xDatatype,xCount,\
            yName,yOffset,yDatatype,yCount,\
            zName,zOffset,zDatatype,zCount,\
            intensityName,intensityOffset,intensityDatatype,intensityCount,\
            ringName,ringOffset,ringDatatype,ringCount,\
            timeName,timeOffset,timeDatatype,timeCount,\
            dunno4,dunno5,totaldatalength = header
        content = data_array[32:-1]
        
        # print(header)
        # print(f"xName = {xName} | yName = {yName} | zName = {zName} | intensityName = {intensityName} | ringName = {ringName} | timeName = {timeName}")
        points = []
        points_ply = []
        for n in range(int(len(content)/4)):
            dat = {
                "x": content[(n*4)+0],
                "y": content[(n*4)+1],
                "z": content[(n*4)+2],
                "intensity": content[(n*4)+3],
            }
            points.append(dat)
            points_ply.append(f"{dat['x']} {dat['y']} {dat['z']}")

        # print(jsonpickle.encode(points,unpicklable=True))
        print("\n".join(points_ply))
        # Cloud = msg_construct(data[0])
        # print(Cloud)
