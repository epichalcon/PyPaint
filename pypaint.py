import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

####funciones

def vvalue (mat, x, y, xyrange):
    ymax, xmax = mat.shape
    modas = mat[max(y - xyrange, 0):min(y + xyrange, ymax),
                max(x - xyrange, 0):min(x + xyrange, xmax)].flatten()
    modas = modas.astype(int) 
    counts = np.bincount(modas)

    return np.argmax(counts)


def smoothen(mat, filter_size=16):
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
           smooth_channel [y,x] = vvalue(channel, x, y, 1) 
    return smooth_channel

###

#load and resize
img = cv2.imread('C:\\Users\\maria\\4genf.jpg')
img = cv2.resize(img,None, fx = 0.5, fy= 0.5)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#disminuir ruido
blur_img = cv2.GaussianBlur(img,(3,3),0)

#Visualizar imagenes:
fig, axs = plt.subplots(1,2, figsize=(20,5))
axs[0].imshow(img)
axs[0].set_title('Original Image')
axs[0].axis('off')

axs[1].imshow(blur_img)
axs[1].set_title('Blurred Image')
axs[1].axis('off')

plt.show()
cv2.waitKey(0)

#Normalizing:
data=blur_img/255.0
data=data.reshape(-1,3)

#K-means
kmeans = KMeans(5)
kmeans.fit(data)
y_est = kmeans.predict(data) #cluster center 
new_colors=kmeans.cluster_centers_[kmeans.labels_] #backproject to the color centers

#3D point cloud

fig= plt.figure(figsize=(10,7))
ax= fig.add_subplot(projection='3d')
data_sampled=data[::50] #1 punto cada 50 (velocidad)
ax.scatter(data_sampled[:,0], data_sampled[:,1],data_sampled[:,2], marker='.', color=data_sampled)
ax.set_title('3D Point Cloud of Original Data')
ax.set_xlabel('R')
ax.set_ylabel('G')
_=ax.set_zlabel('B')

# 3d después de Kmeans
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(projection = '3d')
data_sampled = new_colors[::50]
ax.scatter(data_sampled[:,0], data_sampled[:,1],data_sampled[:,2], marker='.', color= data_sampled, s=200)
ax.set_title('3D Point Cloud of Kmeans Data')
ax.set_xlabel('R')
ax.set_ylabel('G')
_=ax.set_zlabel('B')

plt.show()
cv2.waitKey(0)

#Recolored image with Kmeans
img_recolored = new_colors.reshape(blur_img.shape) * 255
img_recolored = img_recolored.astype(np.uint8)

#Divide channels to do vvalue, smoothen y neighbors
R= img_recolored[:, :, 0]
G= img_recolored[:, :, 1]
B= img_recolored[:, :, 2]

Rsmooth = smoothen_channel(R).astype(np.uint8)
Gsmooth = smoothen_channel(G).astype(np.uint8)
Bsmooth = smoothen_channel(B).astype(np.uint8)

smoothed_img = cv2.merge((Rsmooth, Gsmooth, Bsmooth))

fig, ax = plt.subplots(1,3,figsize = (16,6),
                     subplot_kw = {'xticks': [], 'yticks': []})
fig.subplots_adjust(wspace=0.05)
ax[0].imshow(img)
ax[0].set_title('Original Image', size = 16)
ax[1].imshow(img_recolored)
ax[1].set_title('Recolored Image', size =16)
ax[2].imshow(smoothed_img)
ax[2].set_title('Smoothed Image', size =16)

plt.show()
cv2.waitKey(0)