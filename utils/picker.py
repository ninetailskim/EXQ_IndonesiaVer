import cv2


sx = 0
sy = 0
ex = 0
ey = 0
img = None

def drawRectangle(event, x, y, flags, param):
    global sx
    global sy
    global ex
    global ey
    global img
    if event == cv2.EVENT_LBUTTONDOWN:
        sx = x
        sy = y
    elif event == cv2.EVENT_LBUTTONUP:
        ex = x
        ey = y
        cv2.rectangle(img, (sx, sy), (ex,ey), (0,255,0), 2)


def picker(frame):
    global img
    img = frame
    cv2.namedWindow("Picker")
    cv2.setMouseCallback("Picker", drawRectangle)
    while True:
        cv2.imshow("Picker", img)
        if cv2.waitKey(1) == ord('y'):
            break

    cv2.destroyAllWindows()
    print(sx, "---", sy, "---", ex, "---", ey)
    return (sx,sy), (ex, ey)