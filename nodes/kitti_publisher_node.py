#!/usr/bin/env python
from __future__ import print_function
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2
import rospy
import sys
import os
import scipy.misc



class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher("/camera/rgb/image_color", Image, queue_size=1)
        self._publish_rate = rospy.get_param('~publish_rate', 5)

        self.bridge = CvBridge()
        self.image_dir = rospy.get_param("image_dir", "/media/hcg/My_Passport/master_thesis/data/dataset/sequences/05/image_2")

        image_namelist = sorted(os.listdir(self.image_dir))
        self.image_paths = [os.path.join(self.image_dir, x) for x in image_namelist]
        self.index = 0
        self.N = len(self.image_paths)

    def publish(self):
        img = cv2.imread(self.image_paths[self.index])
        # h, w = img.shape[:2]
        # image_max = max(h, w)
        # scale = float(1024) / image_max
        # img = scipy.misc.imresize(
        #     img, (int(round(h * scale)), int(round(w * scale))))

        img_msg = self.bridge.cv2_to_imgmsg(img, encoding="bgr8")
        self.image_pub.publish(img_msg)
        # print("publishing image ", self.index)
        self.index += 1
        if (self.index >= self.N):
            self.index = 0

    def run(self):
        rate = rospy.Rate(self._publish_rate)
        while not rospy.is_shutdown():
            self.publish()
            rate.sleep()


def main():
    rospy.init_node('kitti_publisher')

    node = image_converter()
    node.run()

if __name__ == '__main__':
    main()

