import cv2 as cv
from utilities import *
import read_mnt
import math
from operator import itemgetter

degree_range = 30
radian_range = math.radians(degree_range)
radius_range = 50

def draw_mnt(img, mnt_point):
    font = cv.FONT_HERSHEY_SIMPLEX
    for i, p in enumerate(mnt_point):
        center = (p['x'], p['y'])
        radian = p['rad']

        r = 6
        color = [255, 0, 0]
        border = 1

        x_new = p['x'] + int(r*2 * math.cos(radian))
        y_new = p['y'] + int(r*2 * math.sin(radian))

        cv.circle(img, center, r, color, border)
        cv.line(img, center, (x_new, y_new), color, border)
        cv.putText(img, str(i), center, font, 0.25, (0, 0, 0), 1, cv.LINE_AA)
    return img


def group_minutiae(mnt_point, mnt_img):
    """
            Group mintiae by radius and radian
        """
    

    r = 6
    color = [255, 0, 0]
    border = -1

    length_mnt = len(mnt_point)
    mnt_group = []

    for i in range(length_mnt):
        mnt = {}
        mnt['index'] = i
        mnt['child'] = []

        xi = mnt_point[i]['x']
        yi = mnt_point[i]['y']
        radi = mnt_point[i]['rad']
        pi = [xi, yi]

        result = mnt_img.copy()

        # cv.circle(result, tuple(pi), r, (255, 255, 0), border)
        # cv.circle(result, tuple(pi), radius_range, (255, 255, 0), 1)
        # cv.waitKey(-1)

        for j in range(length_mnt):
            if i == j:
                continue

            xj = mnt_point[j]['x']
            yj = mnt_point[j]['y']
            radj = mnt_point[j]['rad']

            pj = [xj, yj]

            # print(i, j, distance(pi, pj), distance([radi], [radj], "L1"))

            if distance(pi, pj) <= radius_range and distance([radi], [radj], "L1") <= radian_range:
                mnt['child'].append(j)
                cv.circle(result, tuple(pj), r, color, border)

            # cv.imshow("Group"+str(i), result)

        mnt['density'] = len(mnt['child'])
        mnt_group.append(mnt)

        # cv.imshow("Group"+str(i), result)
        # cv.waitKey(-1)
        # cv.destroyWindow("Group"+str(i))
# def find_density_of_minutiae(radius):
    mnt_group = sorted(mnt_group, key=itemgetter('density'),reverse=True)
    return mnt_group


def main():
    img_dir = r"C:\Users\skconan\Desktop\FingerPrint\pysource\images"
    mnt_dir = r"C:\Users\skconan\Desktop\FingerPrint\pysource\FingerNet\Minutiae"
    img_path_list = get_file_path(img_dir)

    for path in img_path_list:
        name = get_file_name(path)
        mnt_path = mnt_dir + "\\" + name + ".mnt"
        mnt_point = read_mnt.read(mnt_path)
        img = cv.imread(path, 1)
        img_with_mnt = draw_mnt(img, mnt_point)
        mnt_group = group_minutiae(mnt_point, img_with_mnt)

        for mnt in mnt_group[:10]:
            result = img_with_mnt.copy()
            i = mnt['index']
            child = mnt['child']
            mnt = mnt_point[i]
            r = 6
            p = [mnt['x'],mnt['y']]
            cv.circle(result, tuple(p), r, (0,0, 255), -1)
            cv.circle(result, tuple(p), radius_range, (0,0, 255), 1)
            
            for i in child:
                mnt = mnt_point[i]
                p = [mnt['x'],mnt['y']]
                cv.circle(result, tuple(p), r, (255, 255, 0), -1)

            # cv.imshow(name, result)
            # cv.waitKey(-1)
            # implot(result)

        # cv.imwrite("./"+name+".jpg", img_with_mnt)
        # cv.waitKey(-1)


if __name__ == "__main__":
    main()
