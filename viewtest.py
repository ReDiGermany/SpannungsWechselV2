import glob
import math
import random
import time
import jsonpickle
import numpy as np
import open3d as o3d
from statistics import mode

from utils.parseFile import  parseFile

# dir = glob.glob("C:\\Users\\suppo\\Documents\\spannungswechsel logs\\logs-1685189669\\logs\\*.xyz")
dir = glob.glob("G:\\spannungswechsel\\logs\\logs-1685194131\\logs\\*.xyz")

pcd = o3d.geometry.PointCloud()
vis = o3d.visualization.Visualizer()
vis.create_window()

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
    pcd.rotate(pcd.get_rotation_matrix_from_xyz((0, 0, 0)), center=(0,0,0))
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
        if x > -3*4 and x < 3*4 and y < 10*4:
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


def doDings(dir,n):
    print(n,dir[n])
    data = parseFile(dir[n],visible_area)
    print(len(data))

    updated_data = []
    for x,y,z in data:
        # if x > -3 and x < 3 and y < 10 and y > 1.5 and z < 0:
        if x > -3*4*100 and x < 3*4*100 and y < 10*4*100:
        # if x > -3*4 and x < 3*4 and y < 10*4 and y > 1.5*4 and z < 0:
            p = [x,y,z]
            updated_data.append(p)
    data = updated_data
    print(len(data))

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
    
    print(f"x_min={x_min}")
    print(f"x_max={x_max}")

    print(f"y_min={y_min}")
    print(f"y_max={y_max}")

    print(f"z_min={z_min}")
    print(f"z_max={z_max}")


    print(len(data))
    # print("data[0] =",data[0])
    z_idx = int(np.argmin(np.var(data, axis = 0)))
    # print("z_idx =",z_idx)
    # data_z = data[:,z_idx]
    temp = []
    for n in data:
        # if n[z_idx] < 0:
        temp.append(n[z_idx])

    data_z = np.array(temp).astype(int)
    # data_z = np.array([n[z_idx] for n in data]).astype(int)
    # print("data_z =",data_z)
    mean = np.mean(data_z)
    # print("mean =",mean)
    sd = np.std(data_z)
    # print("sd =",sd)
    padding = 0.3
    # print(f"(padding * sd) = {(padding * sd)}")
    # print(f"(mean + padding * sd) = {(mean + padding * sd)}")
    # print("padding =",padding)
    data_ground = []
    data_wo_ground = []
    for x,y,z in data:
        test = (z < (mean + padding * sd)) and (z > (mean - padding * sd))
        c = .5 if test else .5
        data_ground.append([x,y,z,c])
        # else:
            # data_wo_ground.append([x,y,z])
    # for itm in range(100):
    itm = 2
    data_ground[itm][3] = 1
    data_ground[itm][2] += 100
    print(itm)
    itm = round(len(data_ground)/2)
    data_ground[itm][3] = 1
    data_ground[itm][2] += 100
    print(itm)
    # print(data_ground[10])
    # data_ground[3][2] = 100

    # print("len(data_ground) =",len(data_ground))
    arr = []
    for x,y,z,c in data_ground:
        arr.append([x/100,y/100,z/100,c])
    # print(arr)
    print(len(arr))
    dings(arr)

    # print("len(data_wo_ground) =",len(data_wo_ground))
    # ydat = []
    # for item in data:
    #     ydat.append([item[0],item[1],item[2],1])
    # dings(ydat)

# for idx,file in enumerate(dir):
#     doDings(dir,idx)

# idx = random.randint(0,len(dir)-1)
idx = 91

doDings(dir,idx)
