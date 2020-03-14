from mysite.plot_bound_detector.PlotBoundCalculator import PlotBoundCalculator


class PlotBoundService:
    def __init__(self, plot_bound_detector):
        self.plot_bound_detector = plot_bound_detector

    def get_plot_bound_ratio(self, image):
        top_chunks, bottom_chunks = self.plot_bound_detector.get_plot_bound(image)

        top, bottom, ratio = PlotBoundCalculator.calculate_distance_ratio(top_chunks, bottom_chunks)

        return top, bottom, ratio
