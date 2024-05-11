import cv2
from contours import Contour

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
        
    if current_contour.size < 50:
        return current_contour

    return current_contour

def reposition_number(cx, cy, contour: Contour):

    if (cx, cy) in contour.coords:
        return cx,cy
    else:
        leftmost_x = contour.leftmost
        leftmost_y_candidates = [y for x, y in contour.coords if x == leftmost_x]
        leftmost_y = min(leftmost_y_candidates) if leftmost_y_candidates else cy
        new_cx = leftmost_x + 10
        new_cy= leftmost_y
        contour.num_color = (255, 0, 0)

    while (new_cx, new_cy) not in contour.coords:
        new_cx = new_cx - 2

    contour.num_color =(0,0,255)
    return new_cx, new_cy   


def get_font_scale(contour):
    area= len(contour)
    if area<40:
        return 0.4
    elif area<250: 
        return 0.7
    else:
        return 1.0
    
def get_centroids(image, edges):
    resulting_numbers = {} # diccionario con una coordenada como clave y el color como valor
    contours= []
    for x, row in enumerate(edges):
        for y, color in enumerate(row):
            if color != 0:
                contour = find_current_contour(edges, image, x, y)
                if contour.size >= 15:
                    contours.append(contour)
                    number =image[x,y]
                    font_scale = get_font_scale(contour)
                    cx, cy = contour.get_center()
                    new_cx, new_cy= reposition_number(cx,cy,contour)
                    resulting_numbers [(new_cx,new_cy)] = (number, font_scale)

    return resulting_numbers

def draw_numbers(edges, numbers):
    for point, (number, scale) in numbers.items():
        px, py = point  
        cv2.putText(edges, str(number), (py - 3, px + 3), cv2.FONT_HERSHEY_PLAIN, scale, (0,0,255) )

