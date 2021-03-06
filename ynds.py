import paddlehub as hub
import argparse
import cv2
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mpe
from moviepy.editor import VideoFileClip
import numpy as np
import random
import copy
from tqdm import tqdm

class segUtils():
    def __init__(self):
        super(segUtils, self).__init__()
        self.module = hub.Module(name="deeplabv3p_xception65_humanseg")

    def do_seg(self, frame):
        res = self.module.segmentation(images=[frame], use_gpu=True)
        return res[0]['data']

class detUtils():
    def __init__(self):
        super(detUtils, self).__init__()
        self.module = hub.Module(name="yolov3_resnet50_vd_coco2017")

    def do_det(self, frame):
        res = self.module.object_detection(images=[frame], use_gpu=True)
        for r in res[0]['data']:
            if r['label'] == 'person':
                return r

def cv2ImgAddText(img, text, left, top, textColor=(255, 0, 0), textSize=50):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(img)

    fontStyle = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")

    draw.text((left+1, top+1), text, (0, 0, 0), font=fontStyle)
    draw.text((left, top), text, textColor, font=fontStyle)

    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

su = segUtils()
du = detUtils()


class Position():
    def __init__(self, x, y, ranrange):
        super(Position, self).__init__()
        self.x = x
        self.y = y
        self.th = min(x, y) / 2
        self.index = 0
        self.speedx = 0
        self.speedy = 0
        self.ranrange = ranrange
 
    def getdirection(self):
        speed_x = random.randint(-self.ranrange, self.ranrange)
        speed_y = random.randint(-self.ranrange, self.ranrange)
        return speed_x, speed_y

    def getPos(self):
        if self.index % 7 == 0:
            self.speedx, self.speedy = self.getdirection()
        if self.index > 4:
            self.speedx *= 1.1
            self.speedy *= 1.1
        self.index += 1
        newx = self.x + self.speedx
        newy = self.y + self.speedy
        if newx < self.x - self.th:
            self.speedx = -self.speedx
            newx = self.x - self.th
        elif newx > self.x + self.th:
            self.speedx = -self.speedx
            newx = self.x + self.th
        if newy < self.y - self.th:
            self.speedy = -self.speedy
            newy = self.y - self.th
        elif newy > self.y + self.th:
            self.speedy = -self.speedy
            newy = self.y + self.th

        return newx if newx > 0 else 0, newy




def crop(frame, bbox, margin):

    h, w = frame.shape[:2]
    left = int(bbox['left'])
    right = int(bbox['right'])
    top = int(bbox['top'])
    bottom = int(bbox['bottom'])

    left = left - margin if left - margin > 0 else 0
    right = right + margin if right + margin < w else w - 1
    top = top - margin if top - margin > 0 else 0
    bottom = bottom + margin if bottom + margin < h else h - 1

    return frame[top:bottom, left:right,:]

def compose(humanimg, backimg, left):

    leftimg = cv2.imread(humanimg)
    leftback = cv2.imread(backimg)
    bbox = du.do_det(leftimg)
    leftimg = crop(leftimg, bbox, 20)
    
    height, width = leftback.shape[:2]
    h, w = leftimg.shape[:2]
    newheight = int(height * 3 / 5)
    newwidth = int(newheight * w / h)

    leftimg = cv2.resize(leftimg, (newwidth, newheight))
    
    leftmask = np.around(su.do_seg(leftimg) / 255)
    leftmask3 = np.repeat(leftmask[:,:,np.newaxis], 3, axis=2)
    if left:
        leftback[height-newheight:height, 0:newwidth] = leftback[height-newheight:height, 0:newwidth] * (1 - leftmask3) + leftmask3 * leftimg
    else:
        leftback[height-newheight:height, width - newwidth:width,:] = leftback[height-newheight:height, width - newwidth:width,:] * (1 - leftmask3) + leftmask3 * leftimg

    return leftback.astype(np.uint8)

def puttext(words, pos, out, fps, img):
    if len(words) < 8:
        second = 2
    else:
        second = 4
    temimg = None
    for si in range(second):
        for fi in range(fps):
            dx, dy = pos.getPos()
            temimg = copy.deepcopy(img)
            temimg = cv2ImgAddText(temimg, words, dx, dy)
            out.write(temimg)

def main(args):
    
    leftall = compose(args.lh, args.lb, True)
    rightall = compose(args.rh, args.rb, False)

    h,w = leftall.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    out = cv2.VideoWriter(args.output, fourcc, fps, (w,h))

    

    leftPos = Position(int(w / 4), int(h / 3), 25)
    rightPos = Position(int(w / 9), int(h / 3), 25)

    with open(args.txt, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        for index in tqdm(range(len(lines))):
            line = lines[index]
            speaker, words = line[0], line[1:]
            if speaker == 'A':
                puttext(words, rightPos, out, fps, rightall)
            elif speaker == 'B':
                puttext(words, leftPos, out, fps, leftall)
    
    out.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--lh", type=str, required=True)
    parser.add_argument("--rh", type=str, required=True)
    parser.add_argument("--lb", type=str, default="leftback.png")
    parser.add_argument("--rb", type=str, default="rightback.png")
    parser.add_argument("--txt", type=str, required=True)
    parser.add_argument("--output", type=str, default="res.mp4")
    args = parser.parse_args()
    main(args)