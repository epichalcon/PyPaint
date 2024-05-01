import numpy as np
import cv2

travelling_distance = 1000

original_edges = cv2.imread("edges.png")

def find_current_contour(mat, x, y, travelling_distance):
    current_contour = set()
    directions = [(-1, 0),
                  (1, 0),
                  (0, -1),
                  (0, 1),
                  ]


    queue = [(x,y)]

    while len(queue) != 0 and len(current_contour) < travelling_distance:
        x, y = queue.pop(0)

        if (x, y) in current_contour:
            continue

        if not( 0 <= x < len(mat) and 0 <= y < len(mat[0])) or mat[x,y] == 0: # es un borde
            continue

        current_contour.add((x,y))

        new_coords = [(x + nx,y+ny) for nx, ny in directions]
        
        queue.extend(new_coords)

    return current_contour

def load_image():
    with open('temp.txt', 'r') as f:
        image = np.array(f.readline()[1:-2].split(', ')).reshape(original_edges.shape[:-1])
        edges = np.array(f.readline()[1:-2].split(', ')).reshape(original_edges.shape[:-1])
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


for x, row in enumerate(edges):
    for y, color in enumerate(row):
        
        if (x, y) in visited or color == 0:
            continue

        current_contour = find_current_contour(edges, x, y, travelling_distance)
        visited = visited.union(current_contour)
        cx, cy = 0,0
        for px, py in current_contour:
            cx += px
            cy += py
        cx //= len(current_contour)
        cy //= len(current_contour)

        if (cx, cy) in current_contour:
            resulting_numbers[(cx,cy)] = image[cx, cy]
        else:
            resulting_numbers[(x,y)] = image[x, y]

for point, number in resulting_numbers.items():
    print(point, number)
    cv2.putText(original_edges, number, point, cv2.FONT_HERSHEY_PLAIN, .7, (0, 0, 255))

cv2.imwrite('numbers.png', original_edges)

cv2.imshow('edges', original_edges)
cv2.waitKey(0)
