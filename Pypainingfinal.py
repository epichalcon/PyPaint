import cv2
import numpy as np
from sklearn.cluster import KMeans

n_colors = 20
foto = 'rome.jpg'
resizing = 1
smoothen_ratio = 4

####funciones

def vvalue (mat, x, y, xyrange):
    ymax, xmax = mat.shape
    modas = mat[max(y - xyrange, 0):min(y + xyrange, ymax),
                max(x - xyrange, 0):min(x + xyrange, xmax)].flatten()
    modas = modas.astype(int) 
    counts = np.bincount(modas)

    return np.argmax(counts)


def smoothen(mat, filter_size):
    ymax, xmax = mat.shape
    flat_mat = np.array([
        vvalue(mat, x, y, filter_size)
        for y in range(0, ymax)
        for x in range(0, xmax)
    ])

    return flat_mat.reshape(mat.shape)


def neighbors(mat, x, y):
    width = len(mat[0])
    height = len(mat)
    val = mat[y][x]
    xRel = [1, 0]
    yRel = [0, 1]
    for i in range(0, len(xRel)):
        xx = x + xRel[i]
        yy = y + yRel[i]
        if xx >= 0 and xx < width and yy >= 0 and yy < height:
            if (mat[yy][xx] != val).all():
                return False
    return True

def smoothen_channel(channel):
    ymax, xmax = channel.shape
    smooth_channel = np.zeros_like(channel)
    for y in range(ymax):
        for x in range (xmax):
           smooth_channel [y,x] = vvalue(channel, x, y, smoothen_ratio) 
    return smooth_channel


def get_outlines(mat):
    ymax, xmax = mat.shape

    outlines = np.array([
        255 if neighbors(mat, x, y) else 0
        for y in range(0, ymax)
        for x in range(0, xmax)
    ])

    return outlines.reshape((ymax, xmax))

###

#load and resize
print('Loading image...')
img = cv2.imread(foto)
img = cv2.resize(img,None, fx = resizing, fy= resizing)

#disminuir ruido
print('Bluring image...')
blur_img = cv2.GaussianBlur(img,(3,3),0)

#Normalizing:
data=blur_img.reshape(-1,3)

#K-means
print('Quantizising image...')
kmeans = KMeans(n_colors)
kmeans.fit(data)
coded_image = kmeans.predict(data) #cluster center 
new_colors=kmeans.cluster_centers_[kmeans.labels_] #backproject to the color centers


#Recolored image with Kmeans
coded_image = coded_image.reshape(blur_img.shape[:-1])
img_recolored = coded_image.astype(np.uint8)

#Divide channels to do vvalue, smoothen y neighbors
print('Smoothing image...')
smoothed_img = smoothen(img_recolored, smoothen_ratio)
smoothed_img = smoothen(smoothed_img, smoothen_ratio)

#Get contours
print('getting contours...')
edges = get_outlines(smoothed_img)

final_coloured_image = kmeans.cluster_centers_[smoothed_img].reshape(img.shape) #backproject to the color centers

print(smoothed_img.shape)
print(edges.shape)

with open('temp.txt', 'w') as f:
    f.write(f"{list(smoothed_img.flatten())}\n{list(edges.flatten())}")


cv2.imwrite('edges.png', edges)
cv2.imwrite('final.png', final_coloured_image)

cv2.imshow("smoothed",cv2.imread('final.png'))
cv2.imshow("edges", cv2.imread('edges.png'))

cv2.waitKey(0)
