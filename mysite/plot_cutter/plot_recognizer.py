import tensorflow as tf
import cv2
import numpy as np
import sys
from utils import label_map_util


class PlotRecognizer:

    model_path = ''
    labels_path = ''
    number_of_classes = 0
    label_map = None
    categories = None
    detection_graph = None

    def __init__(self, model_path, labels_path, number_of_classes):
        # Validate incoming arguments
        self.model_path = model_path
        self.labels_path = labels_path
        self.number_of_classes = number_of_classes

        self.load_label_map()
        self.load_categories()
        self.load_model()

    def __init__(self):
        self.model_path = 'mysite/plot_cutter/frozen_inference_graph.pb'
        self.labels_path = 'mysite/plot_cutter/labelmap.pbtxt'
        self.number_of_classes = 1

        self.load_label_map()
        self.load_categories()
        self.load_model()

    def load_label_map(self):
        self.label_map = label_map_util.load_labelmap(self.labels_path)

    def load_categories(self):
        if self.label_map is None:
            # throw exception
            return
        self.categories = label_map_util.convert_label_map_to_categories(
            self.label_map,
            self.number_of_classes,
            True
        )

    def load_model(self):
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.model_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

    def get_plot_coordinates(self, image):
        session = tf.Session(graph=self.detection_graph)

        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        image_expanded = np.expand_dims(image, axis=0)
        height, width, channels = image.shape

        (boxes, scores, classes, num) = session.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})

        return self.get_boxes_coordinates(boxes, scores, width, height)

    def get_boxes_coordinates(self, boxes, scores, width, height):
        min_score_treshold = 0.95
        filtered_boxes = boxes[0][scores[0] > min_score_treshold]
        result = []
        for i in range(filtered_boxes.shape[0]):
            result.append([
                int(filtered_boxes[i, 0] * height),  # ymin
                int(filtered_boxes[i, 1] * width),  # xmin
                int(filtered_boxes[i, 2] * height),  # ymax
                int(filtered_boxes[i, 3] * width)  # xmax
            ])
        return result




