import glob
import math
import random
import time
import jsonpickle
import numpy as np
import open3d as o3d

from utils.parseFile import  parseFile

dir = glob.glob("G:\\spannungswechsel\\logs\\logs-1685194698\\logs\\*.xyz")
# dir = glob.glob("G:\\spannungswechsel\\logs\\logs-1685189669\\logs\\*.xyz")

pcd = o3d.geometry.PointCloud()
vis = o3d.visualization.Visualizer()
vis.create_window()

visible_area = [[-30,-200,-100],[30,200,100]]

def show(items):
    itms = []
    colors = []
    for x,y,z,c in items:
        itms.append([x,y,z])
        colors.append([c/255,c/255,c/255])

    pcd.points = o3d.utility.Vector3dVector(itms)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    pcd.rotate(pcd.get_rotation_matrix_from_xyz((1.6 * np.pi, 0, 0)), center=(0,0,0))
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.run()

def dings(file):
    data = parseFile(file,visible_area)
    # print(data)
    miny = 9999999999
    arr = []
    for x,y,z in data:
        if x > -3 and x < 3 and y < 10:
            arr.append([x,y,z,255])
        # if miny > point[2]:
            # miny = point[2]
    # print(miny)
    # show(arr)
    narr = []
    padding = 0.1
    for i in range(round(len(arr)/16)):
        dat = arr[i*16:(i+1)*16]
        rdat = []
        ref = dat[0]
        ref1 = dat[1]
        distance = [ref[0] - ref1[0], ref[1] - ref1[1], ref[2] - ref1[2]]
        norm = math.sqrt(distance[0] ** 2.0 + distance[1] ** 2.0 + distance[2] ** 2.0)
        direction = [distance[0] / norm, distance[1] / norm, distance[2] / norm]
        
        for l in dat:
            # TODO: check if l[2] is within padding on line with ref[2] and ref1[2]
            if ref[2] + padding <= l[2] and ref[2] - padding >= l[2]:
                print(l)
                if ref1[2] + padding <= l[2] and ref1[2] - padding >= l[2]:
                    print(l)
                    l[3] = 30  
            # if l[2] < -0.3:
            #     l[3] = 30
            narr.append(l)
            # print(z)
            # if z + padding <= ref[2] and z - padding >= ref[2]:
            #     rdat.append([x,y,z])

        # print(dat)
    show(narr)
        # time.sleep(1/10)
    # f = open(f"test.json", "a")
    # f.write(jsonpickle.encode(arr,unpicklable=False,indent=2))
    # f.close()
    # print("Done")
    # show(data)

dings(dir[random.randint(0,len(dir)-1)])

# for file in dir:
    # dings(file)
