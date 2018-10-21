#!/usr/bin/python
# import RPi.GPIO as GPIO
import spidev, time, math, random, logging

class Gibson_LED_Driver:

    ## name constants ##
    proglist = {'static':0, 'fadeupdown':1, 'flyingcolor':2, 'throb':3, 'randomstatic':4, 'spin':5}
    colorlist = {'single':0, 'alternating':1, 'wide-alternating':2, 'colorwheel':3, 'rgb':4, 'random':5}

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

        #make the duplicate for the fade function
        self.pixelsCopy = list(self.pixels)

        #init program values
        self.stepnum=0
        self.progname = Gibson_LED_Driver.proglist['static']
        self.colorpattern = Gibson_LED_Driver.colorlist['single']
        self.color = (255,100,255)
        self.altcolor = (255,0,255)

        #default calibration
        self.progsleep = 0.1
        self.width = 3

        #log the start up
        logging.info("New Gibson_LED_Driver initiated @" + str(time.time()))
        logging.info("Programs: "+str(self.proglist.keys()))
        logging.info("Color Patterns: "+str(self.colorlist.keys()))


    ## global settings aka 'calibration'

    #speed is in Hz or steps/second
    def calibrate(self, speed, width):
        logging.info("calibrate speed: "+str(speed)+" & width: "+str(width))
        self.progsleep = 1.0/float(speed)
        self.width = int(width)


    # not super neccesarry as it should close on it's own
    def close(self):
        logging.info("Closing")
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

    ## This function actually puts the bits on the wire
    ## in some cases a [1,0,0,0] string may be read as an end of line
    ## for SPI and the rest of the LED's will not update - still researching
    def update(self):
#         logging.debug("update")
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
#         if(color[0] == 0 and color[1] == 0 and color[2] == 0):
#             #fixing the blackout glitch when the color is black, possibly not an issue
#             color = (1,1,1)
        self.pixels[index*4:index*4+4] = (1, color[0], color[1], color[2])

    def getPixelColor(self, index):
        thiscolor = []
        thiscolor.append(self.pixels[index*4 + 1])
        thiscolor.append(self.pixels[index*4 + 2])
        thiscolor.append(self.pixels[index*4 + 3])
        return thiscolor

    def getPixelCopyColor(self, index):
        thiscolor = []
        thiscolor.append(self.pixelsCopy[index*4 + 1])
        thiscolor.append(self.pixelsCopy[index*4 + 2])
        thiscolor.append(self.pixelsCopy[index*4 + 3])
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
        #self.update()

    def rgb(self):
        for p in range(self.nLeds):
            if p%3 == 0:
                self.setPixel(p, [255,0,0])
            elif p%3 == 1:
                self.setPixel(p, [0,255,0])
            else:
                self.setPixel(p, [0,0,255])
        #self.update()

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
        #self.update()

    def spiniteration(self, msdelay=25):
        tempcolor = self.getPixelColor(49)
        for p in reversed(range(1,self.nLeds)):
            self.setPixel(p, self.getPixelColor(p-1))
        self.setPixel(0,tempcolor)
        time.sleep(msdelay/1000.0)
        self.update()

    def alternate(self, color1, color2):
        for p in range(self.nLeds):
            if p%self.width == 0:
                self.setPixel(p, color1)
            else:
                self.setPixel(p, color2)
        #self.update()

    def resetStepNum(self):
        self.stepnum = 0

    def setColor(self,name,color1=[255,255,255],color2=[255,0,255]):
#         print("setting color")
        try:
            self.color=(color1[0], color1[1], color1[2])
            self.altcolor=(color2[0], color2[1], color2[2])
            self.colorpattern = self.colorlist[name]

#             print("Setting color: "+str(self.color)+" alt color: "+str(self.altcolor)+" and pattern: "+str(self.colorpattern))
            logging.debug("Setting color: "+str(self.color)+" alt color: "+str(self.altcolor)+" and pattern: "+str(self.colorpattern))

        except KeyError as e:
            logging.error(e)
            self.colorpattern = self.colorlist['single']
        except:
            logging.error(e)
#             print(e)
            self.colorpattern = self.colorlist['single']

#         print("..color complete")

    def setProgram(self,name):
#         logging.info("Set program to: "+name)
        self.resetStepNum()

        try:
            self.progname = Gibson_LED_Driver.proglist[name]
        except KeyError as e:
            logging.error(e)
            self.progname = self.proglist['static']

#         logging.debug("progname: "+str(self.progname))
#         logging.debug("colorpattern: "+str(self.colorpattern))

#         logging.info("Set colorpattern to: "+str(self.colorpattern))
        if(self.colorpattern == self.colorlist['alternating']):
            for p in range(self.nLeds):
                if p%2 == 0:
                    self.setPixel(p, self.color)
                else:
                    self.setPixel(p, self.altcolor)
        elif(self.colorpattern == self.colorlist['colorwheel']):
            self.colorwheel()
        elif(self.colorpattern == self.colorlist['wide-alternating']):
            for p in range(self.nLeds):
                if p%(2*self.width) < self.width:
                    self.setPixel(p, self.color)
                else:
                    self.setPixel(p, self.altcolor)
        elif(self.colorpattern == self.colorlist['rgb']):
            self.rgb()
        elif(self.colorpattern == self.colorlist['random']):
            self.randomstatic()
        elif(self.colorpattern == self.colorlist['single']):
#             logging.debug('Color pattern single '+str(self.color))
            self.setAll(self.color)


        if(self.progname == self.proglist['fadeupdown']):
            #self.setAll(self.color)
            #uses the previous pattern to fade instead of just one color
            #to avoid really bad rounding closer to the bottom of cycles we duplicate the original pattern:
            self.pixelsCopy = list(self.pixels)
        elif(self.progname == self.proglist['flyingcolor']):
            self.setAll(self.color)
        elif(self.progname == self.proglist['throb']):
            pass
        elif(self.progname == self.proglist['randomstatic']):
            self.randomstatic()
        elif(self.progname == self.proglist['spin']):
            pass

        self.update()

    def increment(self):
        #if(self.progname == self.proglist['static']):
            # do nothing!
#         logging.debug("inc:"+str(self.stepnum))

        if(self.progname == self.proglist['fadeupdown']):
            if(self.stepnum > self.nLeds*2):
                self.resetStepNum()

            if(self.stepnum < self.nLeds):
                #get darker
                for n in range(self.nLeds):
                    nColor = self.getPixelCopyColor(n)

                    newR = nColor[0]*(float(self.nLeds-self.stepnum)/float(self.nLeds))
                    newG = nColor[1]*(float(self.nLeds-self.stepnum)/float(self.nLeds))
                    newB = nColor[2]*(float(self.nLeds-self.stepnum)/float(self.nLeds))
                    nextColor = ( int(round(newR,0)), int(round(newG,0)), int(round(newB,0)) )

                    self.setPixel(n, nextColor)
            else:
                #gets brighter
                for n in range(self.nLeds):
                    nColor = self.getPixelCopyColor(n)

                    newR = nColor[0]*(float(self.stepnum % self.nLeds)/float(self.nLeds))
                    newG = nColor[1]*(float(self.stepnum % self.nLeds)/float(self.nLeds))
                    newB = nColor[2]*(float(self.stepnum % self.nLeds)/float(self.nLeds))
                    nextColor = ( int(round(newR,0)), int(round(newG,0)), int(round(newB,0)) )

                    self.setPixel(n, nextColor)

        elif(self.progname == self.proglist['flyingcolor']):
            # NOT IMPLEMENTED YET
            logging.error("flyingcolor not implemented"+str(self.stepnum))
        elif(self.progname == self.proglist['throb']):
            # NOT IMPLEMENTED YET
            logging.error("throb not implemented"+str(self.stepnum))
        elif(self.progname == self.proglist['randomstatic']):
            self.randomstatic()
        elif(self.progname == self.proglist['spin']):
            tempcolor = self.getPixelColor(49)
            for p in reversed(range(1,self.nLeds)):
                self.setPixel(p, self.getPixelColor(p-1))
            self.setPixel(0,tempcolor)
        elif(self.progname == self.proglist['static']):
#             logging.debug('static prog')
            pass

        time.sleep(self.progsleep)
        self.stepnum = self.stepnum + 1
        self.update()
