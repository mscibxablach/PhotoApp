import cv2


class PlotCutter:
    plot_recognizer = None

    def __init__(self, plot_recognizer):
        self.plot_recognizer = plot_recognizer

    def cut_plot(self, image_path, output_path):
        image = cv2.imread(image_path)
        plot_coordinates = self.plot_recognizer.get_plot_coordinates(image)
        if len(plot_coordinates) > 0:
            plot_to_cut = image[
                plot_coordinates[0][0]:plot_coordinates[0][2],
                plot_coordinates[0][1]:plot_coordinates[0][3]
            ].copy()

            cv2.imwrite(output_path, plot_to_cut)

    def cut_plot(self, image):
        plot_coordinates = self.plot_recognizer.get_plot_coordinates(image)
        if len(plot_coordinates) > 0:
            plot_to_cut = image[
                plot_coordinates[0][0]:plot_coordinates[0][2],
                plot_coordinates[0][1]:plot_coordinates[0][3]
            ].copy()

            return plot_to_cut

    # add overloaded methods for geting byte_array, converting to cv2 image and cut plot for it
    # purpose: SaaS


