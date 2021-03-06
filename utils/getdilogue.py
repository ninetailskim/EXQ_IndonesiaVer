import paddlehub as hub
import cv2
import argparse
from tqdm import tqdm
import picker

class ocrUtils():
    def __init__(self):
        super(ocrUtils, self).__init__()
        self.module = hub.Module(name="chinese_ocr_db_crnn_server")
        self.picker = False
        self.X1 = 0
        self.X2 = 0
        self.Y1 = 0
        self.Y2 = 0
    def do_ocr(self, frame):
        res = self.module.recognize_text(images=[frame],use_gpu=True)
        if res[0]['data'] == []:
            return ""
        if not self.picker:
            (self.X1, self.Y1),(self.X2, self.Y2) = picker.picker(frame)
            print(self.X1, "---", self.Y1, "---", self.X2, "---", self.Y2)
            self.picker = True

        
        retext = ""
        for files in res[0]['data']:
            bbox = files['text_box_position']
            cx = (bbox[0][0] + bbox[1][0]) / 2
            if cx < self.X1 or cx > self.X2:
                continue
            cy = (bbox[0][1] + bbox[3][1]) / 2  
            if cy < self.Y1 or cy > self.Y2:
                continue
            retext = retext + files['text'] + " "
            cv2.rectangle(frame, (bbox[0][0], bbox[0][1]), (bbox[2][0], bbox[2][1]),(0, 255,00), 3)
        # cv2.imshow("tmp", frame)
        # cv2.waitKey(1)
        return retext


def main(args):

    ignoreIndex = 5

    ou = ocrUtils()
    cap = cv2.VideoCapture(args.videopath)
    framecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with open("dialogue.txt", "a+", encoding="utf-8") as fp:
        lasttext = None
        index = 0
        while True:
            if index % ignoreIndex == 0:
                ret, frame = cap.read()
                if ret:
                    text = ou.do_ocr(frame)  
                    if text == "":  
                        continue        
                    if lasttext != text:
                        fp.write(text +"\n")
                        print(text,"---",lasttext)
                        lasttext = text
                else:
                    break
            index += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--videopath", type=str, required=True)
    args = parser.parse_args()
    main(args)