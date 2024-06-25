import numpy as np
import cv2
from AbstractImageProcessing import ImageProcessing

class LegoBrickRecognition(ImageProcessing):
    def __init__ (self, red_color_threshold=200, shape_threshold = 0.95, dummy_method=True):
        """
        Dummy rule based image recognition algorithm on checking if current image has lego bricks or not
        Assumptions: 
        1. We are only expecting red lego brick, 
        2. Cameras is prependicularly mounted on the top. 
        3. No perspective correction is needed.
        4. Camera is calibrated, no image distortion

        Args:
            red_color_threshold (int, optional): intensity threshold on segmenting red color, maximum set to 255, adjustable. Defaults to 200.
            shape_threshold (float, optional): describe how well the contour fit the shape, maximum set to 1, adjustable. Defaults to 0.95.
            dummy_method (bool, optional): this method is dummy. Defaults to True.
        """
        self.red_color_threshold = red_color_threshold
        self.shape_threshold = shape_threshold
        self.is_dummy = dummy_method
    
    def run(self, image: np.ndarray) -> bool:
        """
        Algorithm principle:
        1. Thresholding the image with red color and create a mask
        2. Clean the mask and find contours 
        3. Check if we can find circles and rectange shapes
        4. Identified circles should be inside the detected rectanges
        Args:
            image (np.ndarray): input image

        Returns:
            bool: return True if find lego brick, otherwise return False
        """

        red_channel = image[:, :, 2]  # assuming a black back ground and only look at red pixels
        red_channel_mask = red_channel > self.red_color_threshold
        mask = cv2.morphologyEx(red_channel_mask, cv2.MORPH_OPEN, kernel = np.ones((5,5),np.uint8))
        # find contors of segmented red blobs
        contours, _= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        circles = []
        rectangles = []
        for cnt in contours:
            if self.check_circularity(cnt) == True:
                circles.append(cnt)
            if self.check_check_rectangularity(cnt) == True:
                rectangles.append(cnt)

        for rect in rectangles:
            for circle in circles:
                if cv2.pointPolygonTest(rect, tuple(circle[0][0]), False) >= 0:  # positive return value means points are inside the contour
                    return True  # if we find any circle inside a rectangle
        
        return False # if we find nothing, return False on finding lego bricks
            

    def check_circularity(self, contour) ->bool : 
        """
        Approximate contour points with most compact enclsoing circle and compare it against contour area
        Perfect circle should have exact same area

        Args:
            contour (_type_): contours detected via OpenCV contour finder

        Returns:
            bool: returns True if contour is circular shape
        """
        _, radius = cv2.minEnclosingCircle(contour)
        radius = int(radius)
        estimated_area = np.pi * radius**2
        contour_area = cv2.contourArea(contour)
        ratio = estimated_area / contour_area

        return 1 * self.shape_threshold < ratio < 1 / self.shape_threshold

    def check_rectangularity(self, contour) -> bool:
        """
        Try to fit contour points with a rectangular, length and width of the points is approximated with PCA
        Perfect points with rectangular shape area should match with contour area
        Args:
            contour (cv contour points): contours detected via OpenCV contour finder

        Returns:
            bool: returns True if contour is rectangular shape
        """
        # Convert OpenCV contour points to a 2D array
        data_pts = contour.reshape(-1, 2).astype(np.float32)
        
        # Start of PCA analysis
        # Calculate points mean
        mean = np.mean(data_pts, axis=0)
        
        # Calculate covariance matrix
        centered_data = data_pts - mean
        cov_matrix = np.cov(centered_data.T)
        
        # Extract principle axis of the points
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # Project the points onto the principal axes
        projected = np.dot(centered_data, eigenvectors)
        
        # Calculate the lengths of the bounding box along the principal axes
        min_proj = np.min(projected, axis=0)
        max_proj = np.max(projected, axis=0)
        length = max_proj[0] - min_proj[0]
        width = max_proj[1] - min_proj[1]

        # Estimate rectangularity based area caculated with length and width against contour size
        area = length * width
        contour_area = cv2.contourArea(contour)
        ratio = area / contour_area
        return 1 * self.shape_threshold < ratio < 1 / self.shape_threshold


## Quick functionality test on lego brick recongition.
def test():
    classifier = LegoBrickRecognition()
    img = cv2.imread("PATH to Sample Testing image contains lego brick")
    result = classifier.classify(img)


if __name__ == "__main__":
    test()