from Display import Screen
from lib.sdl2 import Uint8
from Matrix4f import *
from Texture import *

class Scanner:

    sc:Screen = None
    scanBuffer = []
    width:int = None
    height:int = None

    def __init__(self, sc:Screen):
        self.sc = sc
        self.width = sc.width
        self.height = sc.height
        self.scanBuffer = [int for int in range(self.height * 2)]

    def setScanLine(self, y:int, xMin, xMax:int):
        self.scanBuffer[y * 2 + 0] = xMin
        self.scanBuffer[y * 2 + 1] = xMax

    def scanConvertLine(self, x1:int, y1:int, x2:int, y2:int, hand:int):
        xDist:int = x2 - x1
        yDist:int = y2 - y1
        if yDist <= 0:
            return
        xStep:float = float(xDist / yDist)
        curX:float  = x1
        for y in range(y1, y2):
            self.scanBuffer[y * 2 + hand] = int(curX)
            curX += xStep

    def drawScanBuffer(self, yStart:int, yStop:int):
        for y in range(yStart, yStop):
            xStart = self.scanBuffer[y * 2 + 0]
            xStop  = self.scanBuffer[y * 2 + 1]
            self.sc.renderLine(xStart, y, xStop, y)

    def scanConvertTriangle(self, x1:int, y1:int, x2:int, y2:int, x3:int, y3:int, hand:int):
        self.scanConvertLine(x1, y1, x3, y3, 0 + hand)
        self.scanConvertLine(x2, y2, x3, y3, 1 - hand)
        self.scanConvertLine(x1, y1, x2, y2, 1 - hand)

    def renderTexturedTriangle(self, tex:Texture, minYVert:Vector4f, midYVert:Vector4f, maxYVert:Vector4f):
        screenSpace = Matrix4f()
        screenSpace.screenSpaceTransform(self.width, self.height)
        minYTar = screenSpace.multiply(minYVert).perspectiveDivide()
        midYTar = screenSpace.multiply(midYVert).perspectiveDivide()
        maxYTar = screenSpace.multiply(maxYVert).perspectiveDivide()

        # Swapping vertices
        if maxYTar.y < midYTar.y:
            temp = maxYTar
            maxYTar = midYTar
            midYTar = temp
        if midYTar.y < minYTar.y:
            temp = midYTar
            midYTar = minYTar
            minYTar = temp
        if maxYTar.y < midYTar.y:
            temp = maxYTar
            maxYTar = midYTar
            midYTar = temp

        xRatio:float = tex.width / self.width
        yRatio:float = tex.height / self.height

        hand:int = 0
        if (minYTar.triangleArea(maxYTar, midYTar)) >= 0:
            hand = 1
        self.scanConvertTriangle(int(minYTar.x), int(minYTar.y), int(midYTar.x), int(midYTar.y), int(maxYTar.x),
                                 int(maxYTar.y), hand)
        for y in range(int(minYTar.y), int(maxYTar.y)):
            xStart = self.scanBuffer[y * 2 + 0]
            xStop  = self.scanBuffer[y * 2 + 1]
            for x in range(xStart, xStop):
                colorTuple = tex.getPixel(int((x * xRatio)), int((y * yRatio)))
                self.sc.setColor(Uint8(255), colorTuple[0], colorTuple[1], colorTuple[2])
                self.sc.setPixel(x, y)

    def renderTriangle(self, minYVert:Vector4f, midYVert:Vector4f, maxYVert:Vector4f):
        screenSpace = Matrix4f()
        screenSpace.screenSpaceTransform(self.width, self.height)
        minYTar = screenSpace.multiply(minYVert).perspectiveDivide()
        midYTar = screenSpace.multiply(midYVert).perspectiveDivide()
        maxYTar = screenSpace.multiply(maxYVert).perspectiveDivide()

        # Swapping
        if maxYTar.y < midYTar.y:
            temp = maxYTar
            maxYTar = midYTar
            midYTar = temp
        if midYTar.y < minYTar.y:
            temp = midYTar
            midYTar = minYTar
            minYTar = temp
        if maxYTar.y < midYTar.y:
            temp = maxYTar
            maxYTar = midYTar
            midYTar = temp

        hand:int = 0
        if (minYTar.triangleArea(maxYTar, midYTar)) >= 0:
            hand = 1
        self.scanConvertTriangle(int(minYTar.x), int(minYTar.y), int(midYTar.x), int(midYTar.y), int(maxYTar.x),
                                 int(maxYTar.y), hand)
        self.drawScanBuffer(int(minYTar.y), int(maxYTar.y))


class Test:
    screen = Screen()
    scanner = Scanner(screen)
    tex = Texture("C:\\Users\\theho\\Desktop\\test.png")

    def renderTriangle(self):
        self.screen.setColor(255, 255, 255, 255)
        self.screen.clear()
        self.scanner.renderTexturedTriangle(self.tex, Vector4f(-0.5, -0.5, -1, 1), Vector4f(0, 0.5, -1, 1),
                                            Vector4f(0.5, -0.5, -1, 1))

    def render(self):
        pass

    def loop(self):
        self.screen.loop(self.render, self.screen.defaultUpdate)

t = Test()
t.renderTriangle()
t.loop()