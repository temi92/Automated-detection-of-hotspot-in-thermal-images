import numpy as np
import mahotas
import cv2
from skimage import measure


class Roi(object):
    def __init__(self, image):
        #check image is RGB..
        if (len(image.shape) ==3):
            #convert to gray scale..
            self.image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            self.image = image
        
    def threshold(self):

        thresh_value = mahotas.thresholding.otsu(self.image)

        #grab a copy of the image
        otsu_frame = self.image.copy()
        #apply threshold to copy image
        otsu_frame[otsu_frame> thresh_value] = 255
        otsu_frame[otsu_frame < 255] = 0

        #apply morph operations
        thresh = cv2.erode(otsu_frame, None, iterations=3)
        thresh_image = cv2.dilate(thresh, None, iterations=4)
        return thresh_image

    def extract_contour(self, image):
        labels = measure.label(image, neighbors=8)
        mask = np.zeros(image.shape, dtype="uint8")
        for label in np.unique(labels):
                if label == 0:
                        continue
                labelMask = np.zeros(image.shape, dtype="uint8")
                labelMask[labels==label] = 255
                numPixels = cv2.countNonZero(labelMask)
                if numPixels > 100:
                        mask = cv2.add(mask,labelMask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[0]
        #grab original image 
        display = self.image.copy()
        cv2.drawContours(display,cnts, -1, (0,0 ,255), 3)
        return display

    def get_roi(self):
        thresh_image= self.threshold()
        image = self.extract_contour(thresh_image)
        return image
    

if __name__ == "__main__":
    #read image 
    img = cv2.imread("image.jpg")
    roi = Roi(img)
    image = roi.get_roi()
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
