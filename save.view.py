import glob
import math
import random
import time
import jsonpickle
import numpy as np
import open3d as o3d
from statistics import mode

from utils.parseFile import  parseFile

dir = glob.glob("C:\\Users\\suppo\\Documents\\spannungswechsel logs\\logs-1685189669\\logs\\*.xyz")
# dir = glob.glob("G:\\spannungswechsel\\logs\\logs-1685194131\\logs\\*.xyz")

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


def doDings(dir,n):
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
            print("break")
            break
    # print(">",y_first,y_last)


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
    # k = 
    temp = []
    for x,y,z in data:
        zz = zfn(x,y)-10
        print(f"z={z} zz={zz}")
        if z > zz:
            temp.append([x,y,z,1])
        else:
            temp.append([x,y,z,.5])
    data = temp

    print(len(data))
    # # print("data[0] =",data[0])
    # z_idx = int(np.argmin(np.var(data, axis = 0)))
    # # print("z_idx =",z_idx)
    # # data_z = data[:,z_idx]
    # z_items = []
    # for n in data:
    #     # if n[z_idx] < 0:
    #     z_items.append(n[z_idx])

    # data_z = np.array(z_items).astype(int)
    # # data_z = np.array([n[z_idx] for n in data]).astype(int)
    # # print("data_z =",data_z)
    # mean = np.mean(data_z)
    # # print("mean =",mean)
    # sd = np.std(data_z)
    # # print("sd =",sd)
    # padding = 0.3
    # # print(f"(padding * sd) = {(padding * sd)}")
    # # print(f"(mean + padding * sd) = {(mean + padding * sd)}")
    # # print("padding =",padding)
    # data_ground = []
    # data_wo_ground = []
    # for x,y,z,c in data:
    #     test = (z < (mean + padding * sd)) and (z > (mean - padding * sd))
    #     # c = .5 if test else .5
    #     data_ground.append([x,y,z,c])
    #     # else:
    #         # data_wo_ground.append([x,y,z])
    # # for itm in range(100):

    # itm = 2
    # data_ground[itm][3] = 1
    # data_ground[itm][2] += 100
    # print(itm)
    # itm = round(len(data_ground)/2)
    # data_ground[itm][3] = 1
    # data_ground[itm][2] += 100
    # print(itm)

    # print(data_ground[10])
    # data_ground[3][2] = 100

    # print("len(data_ground) =",len(data_ground))
    arr = data
    # for x,y,z,c in data_ground:
        # arr.append([x/100,y/100,z/100,c])
    # print(arr)
    # print(len(arr))

    # print("###############")
    # print(f"Y: {y_first} - {y_last}")
    # print(f"X: {x_min} - {x_max}")
    # print("###############")
    
    # range 100 - 200
    # percentage = 30
    # erwartet: 30
    
    # def getPercentageValueInInterval(min,percentage,max):
    #     # return ((max - min) * percentage) + min
    #     return (percentage * (max - min) / 100) + min
    
    # z_padding = 0.1

    # l = range(x_min[0],x_max[0])
    # l_len = len(l)
    # for idx,x in enumerate(l):
    #     percentage = idx*100/l_len
        
    #     x = getPercentageValueInInterval(x_min[0],percentage,x_max[0])/100
    #     y = getPercentageValueInInterval(x_min[1],percentage,x_max[1])/100
    #     z = getPercentageValueInInterval(x_min[2],percentage,x_max[2])/100
    #     arr.append([x,y,z+z_padding,1])

    # l = range(y_first[1],y_last[1])
    # l_len = len(l)
    # for idx,x in enumerate(l):
    #     percentage = idx*100/l_len
    #     x = getPercentageValueInInterval(y_first[0],percentage,y_last[0])/100
    #     y = getPercentageValueInInterval(y_first[1],percentage,y_last[1])/100
    #     z = getPercentageValueInInterval(y_first[2],percentage,y_last[2])/100
    #     arr.append([x,y,z+z_padding,1])

    # top_left = [
    #     x_min[0]/100,
    #     y_last[1]/100,
    #     y_last[2]/100,
    #     1
    # ]
    # top_right = [
    #     x_max[0]/100,
    #     y_last[1]/100,
    #     y_last[2]/100,
    #     1
    # ]
    # # print(f"y={y_first[2]} x={x_min[2]}")
    # bottom_left = [
    #     x_min[0]/100,
    #     y_first[1]/100,
    #     y_first[2]/100,
    #     1
    # ]
    # bottom_right = [
    #     x_max[0]/100,
    #     y_first[1]/100,
    #     y_first[2]/100,
    #     1
    # ]

    # arr.append(top_left)
    # arr.append(top_right)
    # arr.append(bottom_left)
    # arr.append(bottom_right)
    # zfn
    # for x in range(-15,15):
    #     for y in range(0,30):
    #         arr.append([x,y,zfn(x,y)/100,1])


    dings(data)

    # print("len(data_wo_ground) =",len(data_wo_ground))
    # ydat = []
    # for item in data:
    #     ydat.append([item[0],item[1],item[2],1])
    # dings(ydat)

# for idx,file in enumerate(dir):
    # doDings(dir,idx)

# idx = random.randint(0,len(dir)-1)
idx = 91

doDings(dir,idx)
