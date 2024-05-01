import cv2

resulting_numbers = {
    (499, 48): 17,
    (950, 51): 7
}

edges = cv2.imread("edges.png")
print(edges.shape)
for point, number in resulting_numbers.items():
    cv2.putText(edges, str(number), point, 0, 0.5, (255, 0,0))

cv2.imshow('edges', edges)
cv2.waitKey(0)
