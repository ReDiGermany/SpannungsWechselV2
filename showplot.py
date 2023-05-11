import glob
import numpy as np
import open3d as o3d

pcd = o3d.geometry.PointCloud()


vis = o3d.visualization.Visualizer()
vis.create_window()

def parseFile(name):
    items = []

    with open(name) as file:
        lines = file.read().split("\n")
        if len(lines) > 10:
            items = []
            for line in lines:
                l = line.split(" ")
                for idx,n in enumerate(l):
                    l[idx] = int(n)
                items.append(l)
    return items

def showFile(name):
    items = parseFile(name)
    print(len(items))
    pcd.points = o3d.utility.Vector3dVector(items)
    # o3d.visualization.draw_geometries([pcd])
    pcd.rotate(pcd.get_rotation_matrix_from_xyz((1.5 * np.pi, 0, 1.1 * np.pi)), center=(0,0,0))

    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.run()

dir = glob.glob("data\\raw\\*.point")

def take(el):
    n = el.split(".")[0].split("-")[1]
    return int(n)

dir.sort(key=take)

files = []
for file in dir:
    data = parseFile(file)
    files.append(data)

for items in files:
    pcd.points = o3d.utility.Vector3dVector(items)
    pcd.rotate(pcd.get_rotation_matrix_from_xyz((1.5 * np.pi, 0, 1.1 * np.pi)), center=(0,0,0))

    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.run()