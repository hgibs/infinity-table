#!/usr/bin/python
# import RPi.GPIO as GPIO
import spidev, time, math, random

class Gibson_LED_Driver:
    def __init__(self, spi_x=0, spi_y=0, nLeds=50):
        self.spi = spidev.SpiDev()
        self.spi.open(spi_x,spi_y)

        self.spi.max_speed_hz = 25000000
        # set the number of LEDs in string
        self.nLeds = nLeds

        #fixing scope
        self.correctPixels = []

        # store every LED as a pixel
        self.pixels = []
        for b in range(0,nLeds):
            self.pixels.append(1)
            self.pixels.append(0)
            self.pixels.append(0)
            self.pixels.append(0)


    ### NEED TO do functions on step by step basis!! ###

    # not super neccesarry as it should close on it's own
    def close(self):
        if (self.spi != None):
            self.spi.close()
            self.f = None

    def brightnessCorrect(self, val):
        ##this corrects the luminosity of LEDs - they are not linear ##
        ## This should done in a look up table for speed, but all we really need is 30 frames
        ## per second to appear fluid so no one should notice

        ## not perfect yet, but much better than direct metering

        #return int(math.ceil(math.pow(2,(val*4) / 128) - 1))
        #return int(math.ceil((math.pow(2,val/255) - 1) * 255))
        return int(val)

    def update(self):
        #correct for LED brightness s-curve instead of linear
        self.correctPixels = []
        for i in range(0, self.nLeds):
            #4 values for every pixel (y, R, G, B)
            self.correctPixels.append(1)

            red = self.brightnessCorrect(self.pixels[i*4 + 1])
            gr = self.brightnessCorrect(self.pixels[i*4 + 2])
            blu = self.brightnessCorrect(self.pixels[i*4 + 3])

            self.correctPixels.append(red)
            self.correctPixels.append(gr)
            self.correctPixels.append(blu)

        #print str(self.correctPixels)

        self.spi.writebytes(self.correctPixels)
        #self.spi.writebytes(self.pixels)
        self.spi.writebytes([0,0,0,0])

    def setPixel(self, index, color):
        self.pixels[index*4:index*4+4] = (1, color[0], color[1], color[2])

    def getPixelColor(self, index):
        thiscolor = []
        thiscolor.append(self.pixels[index*4 + 1])
        thiscolor.append(self.pixels[index*4 + 2])
        thiscolor.append(self.pixels[index*4 + 3])
        return thiscolor

    def setAll(self, color):
        for i in range(0, self.nLeds):
            self.setPixel(i,color)

    def fadeupdown(self, speed):
        for i in range(1,256):
            self.setAll([i,i,i])
            self.update()
            time.sleep(speed/1000.0)
        for i in reversed(range(1,256)):
            self.setAll([i,i,i])
            self.update()
            time.sleep(speed/1000.0)

    # this sends a color orbiting the strand once
    def flyingcolor(self, color, speed=50):
        for p in range(self.nLeds):
            temppixel = self.getPixelColor(p)
            self.setPixel(p, color)
            self.update()
            self.setPixel(p, temppixel)
            time.sleep(speed/1000.0)

    def throb(self, speed):
        math.sin()

    def static(self, color):
        self.setAll(color)
        self.update()

    def randomstatic(self):
        for p in range(self.nLeds):
            randomred = random.randint(1,255)
            randomgreen = random.randint(1,255)
            randomblue = random.randint(1,255)
            randcolor = [randomred, randomgreen, randomblue]
            self.setPixel(p, randcolor)
        self.update()

    def rgb(self):
        for p in range(self.nLeds):
            if p%3 == 0:
                self.setPixel(p, [255,0,0])
            elif p%3 == 1:
                self.setPixel(p, [0,255,0])
            else:
                self.setPixel(p, [0,0,255])
        self.update()

    def colorwheel(self):
        self.setPixel(0, [125,255,0]) #
        self.setPixel(1, [157,255,0])
        self.setPixel(2, [189,255,0])
        self.setPixel(3, [255,255,0]) #
        self.setPixel(4, [125,222,0])
        self.setPixel(5, [125,190,0])
        self.setPixel(6, [125,158,0])
        self.setPixel(7, [255,125,0]) #
        self.setPixel(8, [255,94,0])
        self.setPixel(9, [255,62,0])
        self.setPixel(10,[255,30,0])
        self.setPixel(11,[255,0,0])   #
        self.setPixel(12,[255,0,30])
        self.setPixel(13,[255,0,62])
        self.setPixel(14,[255,0,94])
        self.setPixel(15,[255,0,126]) #
        self.setPixel(16,[255,0,158])
        self.setPixel(17,[255,0,190])
        self.setPixel(18,[255,0,222])
        self.setPixel(19,[255,0,255]) #
        self.setPixel(20,[222,0,255])
        self.setPixel(21,[190,0,255])
        self.setPixel(22,[158,0,255])
        self.setPixel(23,[124,0,255]) #
        self.setPixel(24,[94,0,255])
        self.setPixel(25,[62,0,255])
        self.setPixel(26,[32,0,255])
        self.setPixel(27,[0,0,255])   #
        self.setPixel(28,[32,0,255])
        self.setPixel(29,[62,0,255])
        self.setPixel(30,[94,0,255])
        self.setPixel(31,[124,0,255]) #
        self.setPixel(32,[83,43,255])
        self.setPixel(33,[42,83,255])
        self.setPixel(34,[0,125,255]) #
        self.setPixel(35,[0,158,255])
        self.setPixel(36,[0,190,255])
        self.setPixel(37,[0,222,255])
        self.setPixel(38,[0,255,255]) #
        self.setPixel(39,[0,255,222])
        self.setPixel(40,[0,255,190])
        self.setPixel(41,[0,255,157])
        self.setPixel(42,[0,255,123]) #
        self.setPixel(43,[0,255,94])
        self.setPixel(44,[0,255,62])
        self.setPixel(45,[0,255,30])
        self.setPixel(46,[0,255,0])   #
        self.setPixel(47,[32,255,0])
        self.setPixel(48,[64,255,0])
        self.setPixel(49,[96,255,0])
        self.update()

    def spiniteration(self, msdelay=25):
        tempcolor = self.getPixelColor(49)
        for p in reversed(range(1,self.nLeds)):
            self.setPixel(p, self.getPixelColor(p-1))
        self.setPixel(0,tempcolor)
        time.sleep(msdelay/1000.0)
        self.update()

    def alternate(self, color1, color2):
        for p in range(self.nLeds):
            if p%2 == 0:
                self.setPixel(p, color1)
            else:
                self.setPixel(p, color2)
        self.update()
