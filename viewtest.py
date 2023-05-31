import glob
import time
import numpy as np
import open3d as o3d
from utils.parseFile import  parseFile
import datetime

# Configs
folder = "C:\\Users\\suppo\\Documents\\spannungswechsel logs\\logs-1685189669"
folder = "C:\\Users\\suppo\\Documents\\spannungswechsel logs\\logs-1685194131"
# folder = "C:\\Users\\suppo\\Documents\\spannungswechsel logs"
# folder = "G:\\spannungswechsel\\logs\\logs-1685194131"
line_color = 1
grid_color = 1
z_padding = 1

print(f"Welcome!\nFinding all coordinates inside: {folder}")

dir = glob.glob(f"{folder}\\logs\\*.xyz")


timestamps = []
for item in dir:
    item = item.split("\\")
    item = item[len(item)-1]
    timestamps.append(int(item.split(".")[0]))
timestamps.sort()
total_seconds = timestamps[len(timestamps)-1]-timestamps[0]
print(f"Found {len(timestamps)} Logs with a total time of: {str(datetime.timedelta(seconds=total_seconds))} Seconds ({round(len(timestamps)/total_seconds,2)} Logs/Second)")

pcd = o3d.geometry.PointCloud()
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.set_full_screen(True)


visible_area = [[-30,-200,-100],[30,200,100]]

def show(items):
    itms = []
    colors = []
    for x,y,z,c in items:
        color = c
        itms.append([x,y,z])
        colors.append([color,color,color])

    pcd.points = o3d.utility.Vector3dVector(itms)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    pcd.rotate(pcd.get_rotation_matrix_from_xyz((1.6 * np.pi, 0, 0)), center=(0,0,0))
    # pcd.rotate(pcd.get_rotation_matrix_from_xyz((0, 0, 0)), center=(0,0,0))
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.run()

def dings(data):
    arr = []
    n = 0

    dataArray = []
    lastY = 999999999999
    currentData = []

    min = 999
    max = -999
    zs = []
    for x,y,z,c in data:
        zs.append(z)
        if z < max:
            max = z
        if z > min:
            min = z
    
    # print(mode(zs))

    for x,y,z,c in data:


        # if x > -3 and x < 3 and y < 10 and y > 1.5 and z < 0:
        # if x > -3*4 and x < 3*4 and y < 10*4:
        # if x > -3*4 and x < 3*4 and y < 10*4 and y > 1.5*4 and z < 0:
            # print(z)
            # p = [x*4,y*4,round(z*4,2),c]
            p = [x,y,z,c]
            # n += 1
            arr.append(p)
        
            # if y < lastY - 2:
            #     lastY = 9999999999999
            #     if len(currentData):
            #         dataArray.append(currentData)
            #     currentData = []
            # currentData.append([x,y,z,n])
            # lastY = y

    else:
        print("done?")
        dataArray.append(currentData)

    show(arr)

# https://im-coder.com/wie-berechne-ich-den-schnittpunkt-zweier-linien-in-python.html
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def getZFunction(x_min,x_max,y):
    # https://math.stackexchange.com/questions/28043/finding-the-z-value-on-a-plane-with-x-y-values
    a1=x_min[0]
    a2=y[0]
    a3=x_max[0]

    b1=x_min[1]
    b2=y[1]
    b3=x_max[1]

    c1=x_min[2]
    c2=y[2]
    c3=x_max[2]
        
    v1 = np.array([a1-a2,b1-b2,c1-c2])
    v2 = np.array([a1-a3,b1-b3,c1-c3])
    r,s,t = np.cross(v1,v2)
    # print(n)
    
    def zfn(x,y):
        return (1/t)*(r*a1+s*b1+t*c1-r*x-s*y)
    return zfn
    
def getZfn(data):
    temp = []
    for x,y,z in data:
        # if x > -3 and x < 3 and y < 10 and y > 1.5 and z < 0:
        if x > -3*4*100 and x < 3*4*100 and y < 10*4*100:
        # if x > -3*4 and x < 3*4 and y < 10*4 and y > 1.5*4 and z < 0:
            temp.append([x,y,z])
    data = temp
    # print(len(data))

    x_min = [999999,999999,999999]
    x_max = [-999999,-999999,-999999]
    y_min = [999999,999999,999999]
    y_max = [-999999,-999999,-999999]
    z_min = [999999,999999,999999]
    z_max = [-999999,-999999,-999999]
    for item in data:
        if item[0] < x_min[0]:
            x_min = item
        if item[0] > x_max[0]:
            x_max = item

        if item[1] < y_min[1]:
            y_min = item
        if item[1] > y_max[1]:
            y_max = item
            
        if item[2] < z_min[2]:
            z_min = item
        if item[2] > z_max[2]:
            z_max = item

    y_first = data[0]
    y_last = [0,0,0]
    for x,y,z in data:
        if y > y_last[1]:
            y_last = [x,y,z]
        else:
            break

    intersection = line_intersection((x_min, x_max), (y_first, y_last))
    print(intersection)

    # https://math.stackexchange.com/questions/28043/finding-the-z-value-on-a-plane-with-x-y-values
    a1=x_min[0]
    a2=y_last[0]
    a3=x_max[0]

    b1=x_min[1]
    b2=y_last[1]
    b3=x_max[1]

    c1=x_min[2]
    c2=y_last[2]
    c3=x_max[2]
        
    v1 = np.array([a1-a2,b1-b2,c1-c2])
    v2 = np.array([a1-a3,b1-b3,c1-c3])
    r,s,t = np.cross(v1,v2)
    # print(n)
    k = r*a1+s*b1+t*c1
    
    def zfn(x,y):
        return (1/t)*(r*a1+s*b1+t*c1-r*x-s*y)
    return zfn,x_min,x_max,y_first,y_last,intersection

def doDings(dir,n,fn):
    zfn,x_min,x_max,y_first,y_last,intersection = fn
    print(n,dir[n])
    data = parseFile(dir[n],visible_area)
    # print(len(data))

    updated_data = []
    for x,y,z in data:
        # if x > -3 and x < 3 and y < 10 and y > 1.5 and z < 0:
        if x > -3*4*100 and x < 3*4*100 and y < 10*4*100:
        # if x > -3*4 and x < 3*4 and y < 10*4 and y > 1.5*4 and z < 0:
            p = [x,y,z]
            updated_data.append(p)
    data = updated_data
    # print(len(data))

    # k = 
    temp = []
    for x,y,z in data:
        zz = zfn(x,y)+z_padding
        # print(f"z={z} zz={zz}")
        if z > zz:
            temp.append([x,y,z,1])
        else:
            temp.append([x,y,z,.5])
    data = temp

    def getPercentageValueInInterval(min,percentage,max):
        return (percentage * (max - min) / 100) + min

    def getPercentageValuesInIntervals(min,percentage,max):
        x = getPercentageValueInInterval(min[0],percentage,max[0])
        y = getPercentageValueInInterval(min[1],percentage,max[1])
        z = getPercentageValueInInterval(min[2],percentage,max[2])
        return x,y,z

    # print(x_min,x_max)
    l = range(x_min[0],x_max[0])
    l_len = len(l)
    for idx,x in enumerate(l):
        x,y,z = getPercentageValuesInIntervals(x_min,idx*100/l_len,x_max)
        data.append([x,y,z,line_color])
    data.append([x_min[0],x_min[1],x_min[2]+10,line_color])
    data.append([intersection[0],intersection[1],10,line_color])

    l = range(y_first[1],y_last[1])
    l_len = len(l)
    for idx,x in enumerate(l):
        x,y,z = getPercentageValuesInIntervals(y_first,idx*100/l_len,y_last)
        data.append([x,y,z+z_padding,line_color])
    
    # for x in range(x_min[0],x_max[0],50):
    #     for y in range(y_first[1],y_last[1],50):
    #         data.append([x,y,zfn(x,y)+z_padding,grid_color])

    dings(data)

dir = dir[100:]
zfn = getZfn(parseFile(dir[0],visible_area))

# for idx,file in enumerate(dir):
    # doDings(dir,idx,zfn)

# idx = random.randint(0,len(dir)-1)
idx = 91

doDings(dir,idx,zfn)