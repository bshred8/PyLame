from lib.sdl2 import *

class Display:

    window:SDL_Window() = None
    width:int = None
    height:int = None
    rend:SDL_Renderer = None

    def __init__(self, title:bytes=b'PyLame', width:int=800, height:int=600):
        SDL_Init(SDL_INIT_EVERYTHING)
        self.width = width
        self.height = height
        self.window = SDL_CreateWindow(title,
                                        SDL_WINDOWPOS_CENTERED,
                                        SDL_WINDOWPOS_CENTERED,
                                        width,
                                        height,
                                        SDL_WINDOW_SHOWN)
        self.rend = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_SOFTWARE)

    def stop(self):
        SDL_DestroyRenderer(self.rend)
        SDL_DestroyWindow(self.window)
        SDL_Quit()

    def loop(self, update, rend):
        running = True
        mainEvent = SDL_Event()
        while(running):
            SDL_PollEvent(mainEvent)
            if(mainEvent.type == SDL_QUIT):
                running = False
            update()
            rend()
            SDL_RenderPresent(self.rend)
        self.stop()

class Screen(Display):

    def __init__(self, title:bytes=b'PyLame', width:int=800, height:int=600):
        Display.__init__(self, title, width, height)

    def defaultRender(self):
        self.setColor(Uint8(255), Uint8(255), Uint8(255), Uint8(255))
        self.clear()

    def defaultUpdate(self):
        pass

    def setColor(self, a:Uint8, r:Uint8, g:Uint8, b:Uint8):
        SDL_SetRenderDrawColor(self.rend, r, g, b, a)

    def clear(self):
        SDL_RenderClear(self.rend)

    def setPixel(self, x:int, y:int):
        SDL_RenderDrawPoint(self.rend, x, y)

    def renderLine(self, x1:int, y1:int, x2:int, y2:int):
        SDL_RenderDrawLine(self.rend, x1, y1, x2, y2)