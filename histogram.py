from  PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvas

from  matplotlib.figure  import  Figure

class Histogram(QtWidgets.QWidget):    
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)        
        self.canvas = FigureCanvas(Figure())
    
        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.figure.set_facecolor("xkcd:wheat")
        self.setLayout(vertical_layout)