import cv2
import numpy as np
from sklearn.cluster import KMeans

import number_area_assignation

n_colors = 10
foto = 'imgs/rome.jpg'
resizing = .5
smoothen_ratio = 4

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

def load_image():
    img = cv2.imread(foto)
    img = cv2.resize(img,None, fx = resizing, fy= resizing)
    blur_img = cv2.GaussianBlur(img,(3,3),0)

    return blur_img

def get_kmeans(image):
    #Normalizing:
    data=image.reshape(-1,3)

    #K-means
    kmeans = KMeans(n_colors)
    coded_image = kmeans.fit_predict(data) #cluster center 

    coded_image = coded_image.reshape(image.shape[:-1])
    coded_image = coded_image.astype(np.uint8)

    return kmeans.cluster_centers_, coded_image 

def smoothen_image(image, smoothen_ratio):
    #Divide channels to do vvalue, smoothen y neighbors
    smoothed_img = smoothen(image, smoothen_ratio)
    smoothed_img = smoothen(smoothed_img, smoothen_ratio)

    return smoothed_img 


if __name__ == "__main__":
    print('Loading image...')
    image = load_image()
    print('Quantizising image...')
    centers, km_image = get_kmeans(image)
    print('Smoothing image...')
    smoothed_img = smoothen_image(km_image, smoothen_ratio)
    print('getting contours...')
    edges = get_outlines(smoothed_img)
    
    final_coloured_image = centers[smoothed_img].reshape(image.shape) #backproject to the color centers

    cv2.imwrite('results/edges.png', edges)
    cv2.imwrite('results/final.png', final_coloured_image)

    print('Calculating centroids...')
    numbers = number_area_assignation.get_centroids(smoothed_img, edges.copy())

    print('Drawing numbers...')
    new_edges = img_gray = cv2.cvtColor(np.ascontiguousarray(edges, dtype=np.uint8), cv2.COLOR_GRAY2RGB)
    number_area_assignation.draw_numbers(new_edges,numbers)

    cv2.imwrite('results/numbers.png', new_edges)

    cv2.imshow("smoothed",cv2.imread('results/final.png'))
    cv2.imshow("edges", cv2.imread('results/edges.png'))
    cv2.imshow("numbers", new_edges)

    cv2.waitKey(0)
