from PIL import Image
from os import listdir
from os.path import isfile, join
from math import sqrt
from PyQt5.QtWidgets import *
import sys

class makeComposite:
    def __init__(self, dir):
        self.resolutionH = None
        self.resolutionV = None
        self.totalFrames = None

        try:
            files = [f for f in listdir(dir) if isfile(join(dir, f))]

            sampleImage = Image.open(join(dir,files[0]))
            (imageW, imageH) = sampleImage.size

            totalPixels = imageW * imageH * len(files)

            side = (sqrt(totalPixels))

            self.totalFrames = len(files)
            self.resolutionH = side // imageW if side / imageW - side // imageW < 1/2 else side // imageW + 1
            self.resolutionV = len(files) // self.resolutionH if len(files) / self.resolutionH - len(files) // self.resolutionH == 0 else len(files) // self.resolutionH + 1

            composite = Image.new("RGBA", (int(imageW*self.resolutionH), int(imageH*self.resolutionV)), (255, 0, 0, 0))

            for row in range(0, int(self.resolutionV)):
                for column in range(0, int(self.resolutionH)):
                    currentImageIndex = int(row*self.resolutionH + column)
                    if len(files)-1 >= currentImageIndex:
                        currentImage = Image.open(join(dir,files[currentImageIndex]))
                        composite.paste(currentImage, (int(column*imageW), int(row*imageH)))
            self.image = composite
        except:
            raise

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.nameLabel = QLabel("Imager folder")

        self.folderLine = QLineEdit()
        self.openButton = QPushButton("Pick")
        self.generateButton = QPushButton("Generate")
        self.sizeLabel = QLabel("Image size")

        self.hLabel = QLabel("Height")
        self.wLabel = QLabel("Width")
        self.imageW = QLineEdit()
        self.imageH = QLineEdit()

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(self.nameLabel)
        buttonLayout1.addWidget(self.folderLine)

        buttonLayout2 = QVBoxLayout()
        buttonLayout2.addWidget(self.sizeLabel)

        buttonLayout3 = QHBoxLayout()
        buttonLayout3.addWidget(self.wLabel)
        buttonLayout3.addWidget(self.hLabel)

        buttonLayout4 = QHBoxLayout()
        buttonLayout4.addWidget(self.imageW)
        buttonLayout4.addWidget(self.imageH)

        buttonLayout5 = QHBoxLayout()
        buttonLayout5.addWidget(self.openButton)
        buttonLayout5.addWidget(self.generateButton)

        self.openButton.clicked.connect(self.pickFolder)
        self.generateButton.clicked.connect(self.generateComposite)
        self.imageH.editingFinished.connect(self.resizeH)
        self.imageW.editingFinished.connect(self.resizeW)

        mainLayout = QGridLayout()
        mainLayout.addLayout(buttonLayout1, 0, 1)
        mainLayout.addLayout(buttonLayout2, 1, 1)
        mainLayout.addLayout(buttonLayout3, 2, 1)
        mainLayout.addLayout(buttonLayout4, 3, 1)
        mainLayout.addLayout(buttonLayout5, 4, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Select folder")

    def resizeH(self):
        self.changeResolution("H")

    def resizeW(self):
        self.changeResolution("W")

    def changeResolution(self, label):
        ratioWH = self.oW / self.oH
        ratioHW = self.oH / self.oW

        if label == "H":
            try:
                if self.imageH.text() != "":
                    newW = str(int(round(float(self.imageH.text()) * ratioWH)))
                    self.imageW.clear()
                    self.imageW.insert(newW)
            except:
                print (sys.exc_info())
                pass
        else:
            try:
                if self.imageW.text() != "":
                    newH = str(int(round(float(self.imageW.text()) * ratioHW)))
                    self.imageH.clear()
                    self.imageH.insert(newH)
            except:
                print (sys.exc_info())
                pass

    def pickFolder(self):
        try:
            folder = QFileDialog.getExistingDirectory(self, 'Open folder', '')
            self.folderLine.clear()
            self.folderLine.insert(folder)
            imageObject = makeComposite(folder)
            self.composite = imageObject.image
            self.resolutionV = imageObject.resolutionV
            self.resolutionH = imageObject.resolutionH
            self.totalFrames = imageObject.totalFrames

            (width, height) = self.composite.size

            self.oW = width
            self.oH = height

            self.imageH.clear()
            self.imageW.clear()

            self.imageW.insert(str(width))
            self.imageH.insert(str(height))
        except FileNotFoundError:
            self.folderLine.clear()
            self.imageH.clear()
            self.imageW.clear()
            pass
        except:
            self.pickFolder()
            pass

    def generateComposite(self):
        saveLocation = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png)")
        try:
            newW = int(self.imageW.text())
            newH = int(self.imageH.text())

            resized = self.composite.resize((newW, newH), Image.ANTIALIAS)

            if saveLocation[0] != "":
                resized.save("{name}-{resolutionH}-{resolutionV}-{tiles}.png"
                             .format(**{"name": saveLocation[0][:-4],
                                        "resolutionH": int(self.resolutionH),
                                        "resolutionV": int(self.resolutionV),
                                        "tiles": self.totalFrames}),
                             format="PNG", optimize="1")
                resized.close()
        except:
            print (sys.exc_info())
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = Form()
    screen.show()

    sys.exit(app.exec_())