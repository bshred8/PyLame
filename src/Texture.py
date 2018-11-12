from PIL import Image

class Texture:

    img:Image = None
    imgPixels = []
    width:int = 0
    height:int = 0

    def __init__(self, imagePath:str):
        self.img = Image.open(imagePath)
        self.width, self.height = self.img.size
        self.imgPixels = self.img.load()

    def setPixel(self, x:int, y:int, r:int, g:int, b:int):
        self.imgPixels[x, y] = (r, g, b)

    def getPixel(self, x:int, y:int):
        return self.imgPixels[x, y]