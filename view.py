import glob
import sys
import numpy as np
import open3d as o3d

from utils.parseFile import getParsedFiles

dir = glob.glob("C:\\Users\\suppo\\Documents\\spannungswechsel logs\\logs\\*.xyz")

# basedir = "data"

# if len(sys.argv)!=10:
#     basedir = sys.argv[1]

pcd = o3d.geometry.PointCloud()
vis = o3d.visualization.Visualizer()
vis.create_window()

# dir = glob.glob(f"{basedir}\\*.point")
# Sort by filename like data\\raw\\123-133.point - windows shows 0,1,11,12,13,2,21 etc.
print(dir)
# dir.sort(key=lambda el: int(el.split(".")[0]))
# print(dir)

visible_area = [[-30,-200,-100],[30,200,100]]

files = getParsedFiles(dir,visible_area)

def show(items):

    pcd.points = o3d.utility.Vector3dVector(items)
    # pcd.rotate(pcd.get_rotation_matrix_from_xyz((1.5 * np.pi, 0, 1.1 * np.pi)), center=(0,0,0))
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.run()

for items in files:
    show(items)