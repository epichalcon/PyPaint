import numpy as np
import cv2

original_edges = cv2.imread("edges.png")

print(original_edges.shape)

class Contour:
    coords: set
    leftmost:float 
    rightmost: int
    upmost: float 
    downmost: int
    color: int
    num_color: tuple 
    size: int

    def __init__(self, color):
        self.color = color
        self.coords = set()
        self.leftmost = float('inf')
        self.rightmost = 0
        self.upmost = float('inf')
        self.downmost = 0
        self.size = 0
        self.num_color = (0,0,225)

    def add_cord(self, px, py):
        self.coords.add((px, py))

        self.rightmost = max(self.rightmost, px)
        self.downmost = max(self.downmost, py)
        self.leftmost = min(self.leftmost, px)
        self.upmost = min(self.upmost, py)

        self.size += 1
        assert self.size == len(self.coords)

    def get_center(self):
        return tuple (np.mean(list(self.coords), axis=0, dtype=int))
    
    def __len__(self):
        return self.size

        

def find_current_contour(mat, image, x, y) -> Contour:
    current_contour = Contour(image[x,y])
    directions = [(-1, 0),
                  (1, 0),
                  (0, -1),
                  (0, 1),
                  ]

    queue = [(x,y)]


    while (queue):
        x, y = queue.pop(0)
        if not( 0 <= x < mat.shape[0] and 0 <= y < mat.shape[1]) or mat[x,y] == 0: # es un borde
            continue

        current_contour.add_cord(x,y)
        mat[x, y] = 0
        queue.extend((x+dx, y +dy) for dx, dy in directions if 0<= x +dx < mat.shape[0] and 0 <= y +dy < mat.shape[1])
        #return np.array(current_contour, dtype=np.int32)

        
    if current_contour.size < 50:
        return current_contour
    return current_contour

def reposition_number(cx, cy, contour: Contour, font_scale, text):

    if (cx, cy) in contour.coords:
        return cx,cy
    else:
        leftmost_x = contour.leftmost
        #new_cy = cy
        leftmost_y_candidates = [y for x, y in contour.coords if x == leftmost_x]
        leftmost_y = min(leftmost_y_candidates) if leftmost_y_candidates else cy
        new_cx = leftmost_x +10
        new_cy= leftmost_y
        contour.num_color = (255, 0, 0)
        

        if (new_cx, new_cy) in contour.coords:
            contour.num_color =(0,0,255)
            return new_cx,new_cy
        else:
            #leftmost_x = contour.leftmost
            #new_cy = cy
            #leftmost_y_candidates = [y for x, y in contour.coords if x == leftmost_x]
            #leftmost_y = min(leftmost_y_candidates) if leftmost_y_candidates else cy
            #new_cx = leftmost_x +10
            #new_cy= leftmost_y
            contour.num_color = (255, 0, 0)
        return new_cx, new_cy
        

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

def get_font_scale(contour):
    area= len(contour)
    #area= len(contour)/4
    if area<40:
        return 0.4
    elif area<250: 
        return 0.7
    else:
        return 1.0
    
image, edges = load_image()
    

visited = set()
resulting_numbers = {} # diccionario con una coordenada como clave y el color como valor

contours= []
print('Calculating centroids...')
for x, row in enumerate(edges):
    for y, color in enumerate(row):
        if color != 0:
            contour = find_current_contour(edges, image, x, y)
            if contour.size >= 15:
                contours.append(contour)
                number =image[x,y]
                font_scale = get_font_scale(contour)
                cx, cy = contour.get_center()
                new_cx, new_cy= reposition_number(cx,cy,contour, font_scale, str(number))
                resulting_numbers [(new_cx,new_cy)] = (number, font_scale, contour.num_color)


print('Drawing numbers...')
for point, (number, scale, num_color) in resulting_numbers.items():
    px, py = point  
    cv2.putText(original_edges, str(number), (py - 3, px + 3), cv2.FONT_HERSHEY_PLAIN, scale, num_color)

cv2.imwrite('numbers.png', original_edges)

cv2.imshow('edges', original_edges)
cv2.waitKey(0)
