from Display import Screen
from lib.sdl2 import Uint8
from Vector4f import *
from Matrix4f import *


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
        xDist:float = x2 - x1
        yDist:float = y2 - y1
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
        self.scanConvertLine(x1, y1, x2, y2, 1 - hand)
        self.scanConvertLine(x2, y2, x3, y3, 1 - hand)

    def renderTriangle(self, minYVert:Vector4f, midYVert:Vector4f, maxYVert:Vector4f):

        screenSpace = Matrix4f()
        screenSpace.screenSpaceTransform(self.width, self.height)
        minYTar = screenSpace.multiply(minYVert)
        midYTar = screenSpace.multiply(midYVert)
        maxYTar = screenSpace.multiply(maxYVert)

        # Swapping
        if maxYTar.y < midYTar.y:
            temp = maxYTar
            maxYTar = midYTar
            midYTar = temp
        if maxYTar.y < minYTar.y:
            temp = maxYTar
            maxYTar = minYTar
            minYTar = temp
        if maxYTar.y < midYTar.y:
            temp = maxYTar
            maxYTar = midYTar
            midYTar = temp

        hand:int = 0
        if (minYTar.triangleArea(maxYTar, midYTar)) * 2 >= 0:
            hand = 1
        self.scanConvertTriangle(int(minYTar.x), int(minYTar.y), int(midYTar.x), int(midYTar.y), int(maxYTar.x), int(maxYTar.y), hand)
        self.drawScanBuffer(int(minYTar.y), int(maxYTar.y))

screen = Screen()
scanner = Scanner(screen)

def render():
    screen.setColor(255, 64, 128, 64)
    scanner.renderTriangle(Vector4f(0.5, -0.5, 0, 1), Vector4f(0, 1, 0, 1), Vector4f(-0.5, -0.5, 0, 1))

screen.loop(render, screen.defaultUpdate)