import numpy as np
import cv2

original_edges = cv2.imread("edges.png")

print(original_edges.shape)

def find_current_contour(mat, x, y):
    current_contour = set()
    directions = [(-1, 0),
                  (1, 0),
                  (0, -1),
                  (0, 1),
                  ]

    original = (x, y)

    queue = [(x,y)]

    cx, cy = 0,0


    while len(queue) != 0:
        x, y = queue.pop(0)
        if not( 0 <= x < len(mat) and 0 <= y < len(mat[0])) or mat[x,y] == 0: # es un borde
            continue

        current_contour.add((x,y))
        mat[x, y] = 0
        cx += x
        cy += y

        new_coords = [(x + nx,y+ny) for nx, ny in directions]
        
        queue.extend(new_coords)

    if len(current_contour) < 15:
        return -1, -1

    if (cx, cy) not in current_contour:
        return cx // len(current_contour), cy // len(current_contour)

    else:
        return original

def load_image():
    with open('temp.txt', 'r') as f:
        image = np.array(f.readline()[1:-2].split(', '), dtype=np.uint8).reshape(original_edges.shape[:-1])
        edges = np.array(f.readline()[1:-2].split(', '), dtype=np.uint8).reshape(original_edges.shape[:-1])
    return image, edges

def load_demo():
    image = np.array([
             [  1,   1,   1,   2],
             [  1,   1,   2,   2],
             [  1,   2,   2,   2],
             ])
    edges = np.array([
             [255, 255,   0, 255],
             [255,   0, 255, 255],
             [  0, 255, 255, 255],
            ])
    return image, edges

image, edges = load_image()
    

visited = set()
resulting_numbers = {} # diccionario con una coordenada como clave y el color como valor


print('Calculating centroids...')
for x, row in enumerate(edges):
    for y, color in enumerate(row):
        
        if color == 0:
            continue

        cx, cy = find_current_contour(edges, x, y)

        if (cx, cy) == (-1, -1):
            continue
        resulting_numbers[(cy,cx)] = image[cx, cy]

print('Drawing numbers...')
for point, number in resulting_numbers.items():
    px, py = point
    cv2.putText(original_edges, str(number), (px - 3, py + 3), cv2.FONT_HERSHEY_PLAIN, .5, (0, 0, 255))

cv2.imwrite('numbers.png', original_edges)

cv2.imshow('edges', original_edges)
cv2.waitKey(0)
