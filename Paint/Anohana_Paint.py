####################
#Anohana_paint.py
##ISC3U
###By:Jana Jandal ALrifai
#################################
##Import modules to use (load,save,colorpicker,collect photos from a file)
import glob
from pygame import *
from random import *
from math import *
import pygame_textinput
from tkinter import *
from tkinter.colorchooser import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

##setting up pygame and basic colours
size=width,height=1024,768 #sets width and height of the screen
screen=display.set_mode(size) #displays the screen
display.set_caption("AnoHana Paint") #dipalys a title
icon=image.load("pics/icon.png")  #the new icon pic
display.set_icon(icon) #changes the pygame picture to another one that fits the theme

GREEN=(0, 193, 6) #green used to draw toolRects
PURPLE=(226, 107, 255) #used on toolRects when hovering
BLUE=(0, 0, 255) #used to indicate if shapes are filled or unfilled
BLACK=(0,0,0)
WHITE=(255,255,255)
LBLUE=(154, 219, 244) #light blue to use for rectangles

#initlizing font,tkinter and pygame
font.init()
root=Tk()
root.withdraw()
init()

##initialize variables
alphacol=(0,0,100,10) #colours for the alpha brush(high) to use
col=BLACK #set colour for anything

dred = int(col[0])  # gets the first part of the colour tuple and elimnates the decimals
dgreen = int(col[1])  # gets the second part of the colour tuple and elimnates the decimals
dblue = int(col[2])  # gets the third part of the colour tuple and elimnates the decimals
tool="pencil" #tell the user which tool is selected at any moment
mmode="up" #mouse mode used to check if mosue is pressed and used in stickers
last=''

textinput = pygame_textinput.TextInput() #text module
texttool=False

sx,sy=0,0 #start x, start y that help draw from the user WAS to where they will be
th=2 #thickness for shape to allow user to have a range of thickness
pencilth=1
mp=0 #position of song in playlist (music position)

garamondFont=font.SysFont("garamond",16) #define font to render
explainTool =  garamondFont.render("", True, BLACK) #explain the tools' job to the user

#lists
undo=[]  #undo list to append screenshots in later for UNDO feature
redo=[] #pop screenshots from undo and add them to redo for REDO feature
stickers=[] #add ALL stickers to this list from glob
extra=[7,8,9,10,11] #the number of stickers found


mouse.set_cursor(*cursors.diamond) #change cursor to diamond

#load all music
playlist=["AnohanaSong.ogg","AnohanaSong2.ogg","AnohanaSong3.ogg"] #songs to play while user works
mixer.music.load(playlist[mp])
mixer.music.play()

#Loading ALL images (before 'while Running' loop)
palPic=image.load("pics/pal.png")
background=image.load("pics/AnoHana Back.png")
pencilPic=image.load("pics/pencil.png")
eraserPic=image.load("pics/eraser.png")
linePic=image.load("pics/line.png")
sprayPic=image.load("pics/spray.png")
rectPic=image.load("pics/rect.png")
ellPic=image.load("pics/ellipse.png")
brushPic=image.load("pics/brush.png")
highPic=image.load("pics/high.png")
savePic=image.load("pics/save.png")
loadPic=image.load("pics/load.png")
eyePic=image.load("pics/eye.png")
rrectPic=image.load("pics/rrect.png")
textPic=image.load("pics/text.png")
filterPic=image.load("pics/filter.png")


for i in glob.glob("stickers/*.png"): #get ALL stickers from stickers file using glob and append them to sticker list
    stickers.append(image.load(i).convert())
#Defining ALL rects
canvasRect=Rect(20,140,600,500)
palRect=Rect(320,0,145,137)
ownerRect=Rect(840,20,160,40)

sprayRect=Rect(20,20,40,40)
rectRect=Rect(70,20,40,40)
ellRect=Rect(120,20,40,40)
highRect=Rect(170,20,40,40)
rrectRect=Rect(220,20,40,40)
textRect=Rect(270,20,40,40)
pencilRect=Rect(20,80,40,40)
eraserRect=Rect(70,80,40,40)
lineRect=Rect(120,80,40,40)
brushRect=Rect(170,80,40,40)
eyeRect=Rect(220,80,40,40)
filterRect=Rect(270,80,40,40)


toolRect=Rect(700,215,300,70)
posRect=Rect(700,20,70,40)
rgbRect=Rect(700,80,120,20)
shortcutRect=Rect(700,400,300,170)

saveRect=Rect(620,20,40,40)
loadRect=Rect(620,80,40,40)

sticker1Rect=Rect(460,20,40,40)
sticker2Rect=Rect(510,20,40,40)
sticker3Rect=Rect(560,20,40,40)
sticker4Rect=Rect(460,80,40,40)
sticker5Rect=Rect(510,80,40,40)
sticker6Rect=Rect(560,80,40,40)


#blit images
screen.blit(background,(0,0))
draw.rect(screen,WHITE,canvasRect)
screen.blit(palPic,(palRect))
screen.blit(pencilPic,pencilRect)
screen.blit(eraserPic,eraserRect)
screen.blit(linePic,lineRect)
screen.blit(sprayPic,sprayRect)
screen.blit(rectPic,rectRect)
screen.blit(ellPic,ellRect)
screen.blit(brushPic,brushRect)
screen.blit(highPic,highRect)
screen.blit(savePic,saveRect)
screen.blit(loadPic,loadRect)
screen.blit(eyePic,eyeRect)
screen.blit(rrectPic,rrectRect)
screen.blit(textPic,textRect)
screen.blit(filterPic,filterRect)

screen.blit(stickers[6],sticker1Rect)
screen.blit(stickers[7],sticker2Rect)
screen.blit(stickers[8], sticker3Rect)
screen.blit(stickers[9],sticker4Rect)
screen.blit(stickers[10], sticker5Rect)
screen.blit(stickers[11],sticker6Rect)

screenCapture=screen.copy() #a blank canvas for the first undo(blank screen)
undo.append(screenCapture)


running=True
while running:
    events=event.get()
    for evt in events:
        if evt.type==QUIT:
            running=False
        if evt.type == MOUSEBUTTONDOWN:
            sx, sy = mouse.get_pos() # sx and sy are used for drawing shapes
            screenShot = screen.copy() #copies screen for the shapes
        if evt.type==MOUSEBUTTONUP and canvasRect.collidepoint(mx,my):
            screenCapture = screen.copy()
            undo.append(screenCapture) #append the screen.capture when the user stops drawing
            if evt.button == 4:
                 th += 2 #scroll up to increase th (thickness)
                 if th < 40:
                     th += 2  # scroll up to increase th (thickness)
                 if pencilth < 5:
                     pencilth += 1
            if evt.button == 5: #scroll down to lower th (thickness)
                 if th > 1: #ensure th doesnt become 0
                     th -= 2
                     pencilth -= 1
        if evt.type==KEYDOWN and texttool==False:
            if evt.key==K_f: #fills all shapes
                 #th2 ensures that when the user unfills thier shapes again the thickness stays the same as before the filling
                th=0
            if evt.key==K_u: #unfills all shape
                th=th2
            if evt.key==K_r: #generates  a random sticker
                tool="random sticker"
                rsticker = randint(0, 5) #provide the position for the random sticker from the stickers list
            if evt.key==K_p:
                mixer.music.pause() #pauses the music
            if evt.key==K_s:
                mixer.music.unpause() #stops the music
            if evt.key==K_n: #goes to the next song
                if mp < 2: #increase the mp by 1 thus moving on to the next song
                    mp += 1
                elif mp == 2: #if its playing the last song to go the firt song
                    mp = 0
                mixer.music.load(playlist[mp])
                mixer.music.play()
            if evt.key==K_b: #go to the song before the current one
                if mp > 0:
                    mp -= 0
                elif mp == 0: #if its playing the first song to go the last song
                    mp = 2
                mixer.music.load(playlist[mp])
                mixer.music.play()
            if evt.key==K_1: #goes to the first song
                mp=0
                mixer.music.load(playlist[mp])
                mixer.music.play()
            if evt.key==K_2: #goes to the second song
                mp=1
                mixer.music.load(playlist[mp])
                mixer.music.play()
            if evt.key==K_3: #goes to the third song
                mp=2
                mixer.music.load(playlist[mp])
                mixer.music.play()
            if evt.key==K_z: #undo the last thing drawn on the canvas
                if len(undo)!=1: #ensures that if z is reapeadtly pressed it doesnt crash
                    last=undo.pop() #pops the last thing drawn
                    screen.blit(undo[-1],(0,0))
                    redo.append(last) #adds the last drawn thing to redo list
            if evt.key==K_v:
                if len(redo) != 0:
                    screen.blit(redo[-1],(0,0)) #blits the last undid image
                    redo.pop()
    mb=mouse.get_pressed() #sees if mouse get pressed
    mx,my=mouse.get_pos() #gets mouses current position
    if th!=0:
        th2 = th

    if mixer.music.get_busy() == False: #ensures that music is contunisly playing
        mp += 1
        mixer.music.load(playlist[mp])
        mixer.music.play()
    #drawing the rects
    draw.rect(screen,GREEN,(pencilRect),2)
    draw.rect(screen,GREEN,(eraserRect),2)
    draw.rect(screen, GREEN,(lineRect), 2)
    draw.rect(screen,GREEN,(sprayRect),2)
    draw.rect(screen,GREEN,(rectRect),2)
    draw.rect(screen, GREEN, (ellRect), 2)
    draw.rect(screen, GREEN, (brushRect), 2)
    draw.rect(screen, GREEN, (highRect), 2)
    draw.rect(screen,GREEN,(rrectRect),2)
    draw.rect(screen,GREEN,(eyeRect),2)
    draw.rect(screen,GREEN,(filterRect),2)


    draw.rect(screen,LBLUE,(toolRect))
    draw.rect(screen,LBLUE,(posRect))
    draw.rect(screen, LBLUE, rgbRect)
    draw.rect(screen,LBLUE, (shortcutRect))
    draw.rect(screen,LBLUE,(ownerRect))

    draw.rect(screen,BLUE,(posRect),2)
    draw.rect(screen,BLUE,(toolRect),2)
    draw.rect(screen,BLUE,(rgbRect),2)
    draw.rect(screen,BLUE,(posRect),2)
    draw.rect(screen,BLUE,(shortcutRect),2)
    draw.rect(screen, BLUE, (ownerRect), 2)

    draw.rect(screen,GREEN,(saveRect),2)
    draw.rect(screen,GREEN,(loadRect),2)
    draw.rect(screen,GREEN,(textRect),2)


    draw.rect(screen, GREEN, (sticker1Rect), 2)
    draw.rect(screen, GREEN, (sticker2Rect), 2)
    draw.rect(screen, GREEN, (sticker3Rect), 2)
    draw.rect(screen, GREEN, (sticker4Rect), 2)
    draw.rect(screen,GREEN,(sticker5Rect),2)
    draw.rect(screen, GREEN, (sticker6Rect), 2)
    #selecting the tool
    if mb[0]==1: #checks if left click was pressed
        if pencilRect.collidepoint(mx,my):
            tool="pencil"
        elif eraserRect.collidepoint(mx,my):
            tool="eraser"
        elif lineRect.collidepoint(mx,my):
            tool="line"
        elif sprayRect.collidepoint(mx,my):
            tool="spray"
        elif rectRect.collidepoint(mx,my):
            tool="rect"
        elif ellRect.collidepoint(mx,my):
            tool="ellipse"
        elif brushRect.collidepoint(mx,my):
            tool="brush"
        elif highRect.collidepoint(mx,my):
            tool="high"
        elif rrectRect.collidepoint(mx,my):
            tool = "round rect"
        elif eyeRect.collidepoint(mx,my):
            tool="eyedrop"
        elif textRect.collidepoint(mx,my):
            tool="text"
        elif filterRect.collidepoint(mx,my):
            tool="greyscale"
        elif sticker1Rect.collidepoint(mx,my):
            tool="sticker1"
        elif sticker2Rect.collidepoint(mx,my):
            tool="sticker2"
        elif sticker3Rect.collidepoint(mx,my):
            tool="sticker3"
        elif sticker4Rect.collidepoint(mx,my):
            tool="sticker4"
        elif sticker5Rect.collidepoint(mx,my):
            tool="sticker5"
        elif sticker6Rect.collidepoint(mx,my):
            tool="sticker6"
    #using the tool
    if mb[0]==1:
        if canvasRect.collidepoint(mx,my):
            screen.set_clip(canvasRect) #ensures that nothing is drawn outside the canvas
            if tool=="pencil":
                draw.line(screen,col,(omx,omy),(mx,my)) #draws a line following the mouse
            elif tool=="eraser": #erases anything it touches
               #no matter how fast the user earses it would still erase
                dx = mx - omx #ditsnace between the current x position and original x position
                dy = my - omy #ditsnace between the current y position and original y position
                dist = int(sqrt(dx ** 2 + dy ** 2)) #distance between 2 points formula
                if dist == 0: #draw s circle if only one click is done
                    draw.circle(screen, WHITE, (mx, my), th2)
                for i in range(1, dist + 1): #draws a circle in between the gaps
                    dotX = int(omx + i * dx / dist)
                    dotY = int(omy + i * dy / dist)
                    draw.circle(screen, WHITE, (dotX, dotY), th2)
            elif tool=="line":
                screen.blit(screenShot, (0, 0)) #only blits the last version of the line (so not many lines show where the user clicked
                draw.line(screen, col, (sx, sy), (mx, my), th2) #draws a line from the previous position of mx,my to the current one
            elif tool=="spray": #draws a spray-like effect
                for i in range(15):
                    rx=randint(-15,15) #radnomly selects a number within 15 pixels from the mouse position
                    ry=randint(-15,15) #radnomly selects a number within 15 pixels from the mouse position
                    if hypot(rx,ry)<15: #ensures that the points are inside the circle
                        draw.circle(screen, col,(mx+rx,my-ry),0)
            elif tool=="rect":
                screen.blit(screenShot, (0, 0))
                draw.rect(screen, col,Rect(sx, sy, mx - sx, my - sy),th) #draws a rectangle using the mouse
                draw.rect(screen, col, (sx - th / 2 + 1, sy - th / 2 + 1, th, th)) ##draws rectangles on the corners
                draw.rect(screen, col, (mx - th / 2, sy - th / 2 + 1, th, th))
                draw.rect(screen, col, (mx - th / 2, my - th / 2, th, th))
                draw.rect(screen, col, (sx - th / 2 + 1, my - th / 2, th, th))
            elif tool=="round rect": #draws a rectangle with rounded edges
                screen.blit(screenShot, (0, 0))
                draw.rect(screen, col, (sx, sy, mx - sx, my - sy), th * 3)  # draws a rectangle using the mouse
                draw.circle(screen, col, (sx, sy), th - 1)  # draws a circle at the corners
                draw.circle(screen, col, (mx, my), th - 1)  # draws a circle at the corners
                draw.circle(screen, col, (mx, sy), th - 1)  # draws a circle at the corners
                draw.circle(screen, col, (sx, my), th - 1)  # draws a circle at the corners
            elif tool=="ellipse":
                    radx = (mx - sx) #variable to draw diagonally
                    rady = (my - sy) #variable to draw diagonally
                    try:
                        screen.blit(screenShot, (0, 0))
                        for i in range(6): #improves the quality of the ellipse
                            ellDraw = Rect(sx + i, sy, radx, rady)
                            draw.ellipse(screen, col, ellDraw, th)
                            ellRect.normalize()
                            ellDraw = Rect(sx - i, sy, radx, rady)
                            ellRect.normalize()
                            draw.ellipse(screen, col, ellDraw, th)
                            ellDraw = Rect(sx, sy + i, radx, rady)
                            ellRect.normalize()
                            draw.ellipse(screen, col, ellDraw, th)
                            ellDraw = Rect(sx, sy - i, radx, rady)
                            ellRect.normalize()
                            draw.ellipse(screen, col, ellDraw, th)
                    except:
                        pass
            elif tool=="brush":
                dx = mx - omx
                dy = my - omy
                dist = int(sqrt(dx ** 2 + dy ** 2))
                if dist==0:
                    draw.circle(screen, col, (mx, my), th2*2)
                for i in range(1, dist + 1):
                    dotX = int(omx + i * dx / dist)
                    dotY = int(omy + i * dy / dist)
                    draw.circle(screen, col, (dotX, dotY), th2*2)
            elif tool=="high":
                marker = Surface((40, 40), SRCALPHA)  # make blank screen
                draw.circle(marker, alphacol, (20, 20), 20)  # drawing a circle on the small screen
                dx = mx - omx
                dy = my - omy
                dist = int(sqrt(dx ** 2 + dy ** 2))
                for i in range(1, dist + 1):
                    dotX = int(omx + i * dx / dist)
                    dotY = int(omy + i * dy / dist)
                    screen.blit(marker, (dotX, dotY))
                screen.blit(marker, (mx, my))
            elif tool=="sticker1":
                if mmode == "up" and mb[0] == 1: #the moment you clicked
                    screenShot = screen.copy()
                    mmode = "down"
                if mmode == "down" and mb[0] == 0: #take screen capture
                    mmode = "up"
                if mb[0] == 1: #the moment you release
                    screen.blit(screenShot, (0, 0))
                    screen.blit(stickers[0],(mx,my)) #blits the assigned sticker from my stickers list
            elif tool=="sticker2":
                if mmode == "up" and mb[0] == 1:
                    screenShot = screen.copy()
                    mmode = "down"
                if mmode == "down" and mb[0] == 0:
                    mmode = "up"
                if mb[0] == 1:
                    screen.blit(screenShot, (0, 0))
                    screen.blit(stickers[1], (mx, my))
            elif tool=="sticker3":
                if mmode == "up" and mb[0] == 1:
                    screenShot = screen.copy()
                    mmode = "down"
                if mmode == "down" and mb[0] == 0:
                    mmode = "up"
                if mb[0] == 1:
                    screen.blit(screenShot, (0, 0))
                    screen.blit(stickers[2], (mx, my))
            elif tool=="sticker4":
                if mmode == "up" and mb[0] == 1:
                    screenShot = screen.copy()
                    mmode = "down"
                if mmode == "down" and mb[0] == 0:
                    mmode = "up"
                if mb[0] == 1:
                    screen.blit(screenShot, (0, 0))
                    screen.blit(stickers[3], (mx, my))
            elif tool=="sticker5":
                if mmode == "up" and mb[0] == 1:
                    screenShot = screen.copy()
                    mmode = "down"
                if mmode == "down" and mb[0] == 0:
                    mmode = "up"
                if mb[0] == 1:
                    screen.blit(screenShot, (0, 0))
                    screen.blit(stickers[4], (mx, my))
            elif tool=="sticker6":
                if mmode == "up" and mb[0] == 1:
                    screenShot = screen.copy()
                    mmode = "down"
                if mmode == "down" and mb[0] == 0:
                    mmode = "up"
                if mb[0] == 1:
                    screen.blit(screenShot, (0, 0))
                    screen.blit(stickers[5], (mx, my))
            elif tool=="random sticker":
                if mmode == "up" and mb[0] == 1:
                    screenShot = screen.copy()
                    mmode = "down"
                if mmode == "down" and mb[0] == 0:
                    mmode = "up"
                if mb[0] == 1:
                    screen.blit(screenShot, (0, 0))
                    screen.blit(stickers[rsticker], (mx, my))
    if tool == "text":
        texttool=True #doesnt activate shortcuts accidently while typing
        if texttool==True:
            textpos = sx, sy #text appears where user first clicked
            screen.set_clip(canvasRect) #only draw text inside canvas
            screen.blit(screenShot, (0, 0)) #eleminates cursor appearing after each letter
            screen.blit(textinput.get_surface(),(textpos)) #blits the text all the time
    else:
        texttool=False #allows the keyboard shortcuts to work
        textinput = pygame_textinput.TextInput(text_color=(dred, dgreen, dblue), cursor_color=(dred, dgreen, dblue))
        #refreshs the text everytime the tool is selcted  # allow the text tool cursor to change colours
    screen.set_clip(None) #allows to change the toolRects

    if tool=="eyedrop" and mb[0]==1:
        screen.set_clip(None)
        col = screen.get_at((mx, my)) #gets colour from anything
    if tool == "greyscale":
        for x in range(20, 620):
            for y in range(140, 640):
                r, g, b, a = screen.get_at((x, y))
                r2 = min(255, int(0.333 * r + 0.333 * g + 0.333 * b))
                g2 = min(255, int(0.333 * r + 0.333 * g + 0.333 * b))
                b2 = min(255, int(0.333 * r + 0.333 * g + 0.333 * b))

                screen.set_at((x, y), (r2, g2, b2))
        tool="pencil"
    #changing colour
    if palRect.collidepoint(mx,my):
        if mb[2]==1:
            c = askcolor(title="Pick Colour") #uses tkinter to open a colour selection window with a title "pick color"
            if c[0]!=None:
               col=c[0] #gets the first set of tuples of what tkinter provides
               alphacol=(col[0], col[1], col[2], 10) #makes transparent colour for the highlighter tool
               displayred = int(col[0])  # gets the first part of the colour tuple and elimnates the decimals
               displaygreen = int(col[1])  # gets the second part of the colour tuple and elimnates the decimals
               displayblue = int(col[2])  # gets the third part of the colour tuple and elimnates the decimals
            else:
                pass
        if mb[0]==1:
            col = screen.get_at((mx, my))
            alphacol = (col[0], col[1], col[2], 10)
            displayred = int(col[0])
            displaygreen = int(col[1])
            displayblue = int(col[2])


    ##save and load
    if mb[0]==1:
        if saveRect.collidepoint(mx, my):
            try:
                fname = asksaveasfilename(defaultextension=".png") #uses tkinter to save by default png files
                # make sure to not save if the user didnt enter a file name
                if fname != "": #ensures that an image with a name is saved
                    image.save(screen.subsurface(canvasRect), fname) #saves only the drawing(canvas) to device
            except:
                pass
        if loadRect.collidepoint(mx, my):
            fname = askopenfilename() #uses tkinter to open file selection
            if fname != "": #ensures that an image is loaded
                loadedImage=image.load(fname) #load selected image
                imageWidth=loadedImage.get_width() #gets width from loaded image to resize it to canvas size
                imageHeight=loadedImage.get_height()#gets hight from loaded image to resize it to canvas size
                if imageWidth>600 or imageHeight>500:
                  loadedImage=transform.scale(loadedImage,(600,500))
                  screen.blit(loadedImage, canvasRect)
                else:
                  screen.blit(loadedImage, canvasRect)

    #change colour when hovered on
    if pencilRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (pencilRect), 2)
    if eraserRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (eraserRect), 2)
    if lineRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (lineRect), 2)
    if sprayRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (sprayRect), 2)
    if rectRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (rectRect), 2)
    if ellRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (ellRect), 2)
    if brushRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (brushRect), 2)
    if highRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (highRect), 2)
    if rrectRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (rrectRect), 2)
    if eyeRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (eyeRect), 2)
    if saveRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (saveRect), 2)
    if loadRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (loadRect), 2)
    if textRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (textRect), 2)
    if filterRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (filterRect), 2)
    if saveRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (saveRect), 2)
    if loadRect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (loadRect), 2)
    if sticker1Rect.collidepoint(mx,my):
        draw.rect(screen, PURPLE,(sticker1Rect), 2)
    if sticker2Rect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (sticker2Rect), 2)
    if sticker3Rect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (sticker3Rect), 2)
    if sticker4Rect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (sticker4Rect), 2)
    if sticker5Rect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (sticker5Rect), 2)
    if sticker6Rect.collidepoint(mx,my):
        draw.rect(screen, PURPLE, (sticker6Rect), 2)

     # change col when selected
    if tool == "pencil":
        draw.rect(screen, WHITE, (pencilRect), 2)
    elif tool == "eraser":
        draw.rect(screen, WHITE, (eraserRect), 2)
    elif tool == "line":
        draw.rect(screen, WHITE, (lineRect), 2)
    elif tool=="spray":
        draw.rect(screen, WHITE,(sprayRect ), 2)
    elif tool=="rect":
        draw.rect(screen, WHITE, (rectRect), 2)
    elif tool=="ellipse":
        draw.rect(screen, WHITE, (ellRect), 2)
    elif tool=="brush":
        draw.rect(screen, WHITE, (brushRect), 2)
    elif tool=="high":
        draw.rect(screen, WHITE, (highRect), 2)
    elif tool=="round rect":
        draw.rect(screen, WHITE, (rrectRect), 2)
    elif tool=="eyedrop":
        draw.rect(screen, WHITE, (eyeRect), 2)
    elif tool=="text":
        draw.rect(screen, WHITE, (textRect), 2)
    elif tool=="greyscale":
        draw.rect(screen, WHITE, (filterRect), 2)
    elif tool=="sticker1":
        draw.rect(screen, WHITE, (sticker1Rect), 2)
    elif tool=="sticker2":
        draw.rect(screen, WHITE, (sticker2Rect), 2)
    elif tool=="sticker3":
        draw.rect(screen, WHITE, (sticker3Rect), 2)
    elif tool=="sticker4":
        draw.rect(screen, WHITE, (sticker4Rect), 2)
    elif tool=="sticker5":
        draw.rect(screen, WHITE, (sticker5Rect), 2)
    elif tool=="sticker6":
        draw.rect(screen, WHITE, (sticker6Rect), 2)
    selectedTool=garamondFont.render(tool, True, BLACK) #renders the seleted tool name
    screen.blit(selectedTool,(850,215)) #blits the name of the selected tool
    ##explains what each tool does and renders it when selectd
    if tool=="pencil":
        explainTool= garamondFont.render("Draw thin lines with this",True,BLACK)
    elif tool=="eraser":
        explainTool= garamondFont.render("Erase anything you want",True,BLACK)
    elif tool=="spray":
        explainTool= garamondFont.render("Draw a spray-like effect",True,BLACK)
    elif tool=="line":
        explainTool= garamondFont.render("Draw a straight line",True,BLACK)
    elif tool=="rect":
        explainTool= garamondFont.render("Draw a rectangle",True,BLACK)
    elif tool=="ellipse":
        explainTool= garamondFont.render('Draw an ellipse',True,BLACK)
    elif tool=="brush":
        explainTool =  garamondFont.render('Draw thicker lines than pencil', True, BLACK)
    elif tool=="high":
        explainTool =  garamondFont.render("Draw a highlighter effect", True, BLACK)
    elif tool=="round rect":
        explainTool= garamondFont.render("Draw a round-edged rectangle",True,BLACK)
    elif tool=="eyedrop":
        explainTool= garamondFont.render("Pick the color from anything",True,BLACK)
    elif tool=="text":
        explainTool = garamondFont.render("Enter text anywhere", True, BLACK)
    elif tool=="greyscale":
        explainTool = garamondFont.render("Applies greyscale filter", True, BLACK)
    elif tool=="random sticker":
        explainTool =  garamondFont.render("Selects a random sticker", True, BLACK)
    elif tool=="sticker1" or tool=="sticker2" or tool=="sticker3" or tool=="sticker4" or tool=="sticker5" or tool=="sticker6":
       explainTool=  garamondFont.render("Drag to use the sticker",True,BLACK)
    screen.blit(explainTool, (780, 245))
    xcanvaspos=mx-20 #x position making the canvas top left corner 0
    ycanvaspos=my-140 #y position making the canvas top left corner 0
    mousex= garamondFont.render(str(xcanvaspos),True,BLACK) #renders mouse x position
    mousey =  garamondFont.render(str(ycanvaspos), True, BLACK) #renders mouse y position
    if canvasRect.collidepoint(mx,my): #shows mouse position if its on the canvas
        screen.blit(mousey,(700,40))
        screen.blit(mousex, (posRect))
    omx=mx #original place for mouse x position
    omy=my #original place for mouse y position
    dred = int(col[0])  # gets the first part of the colour tuple and elimnates the decimals
    dgreen = int(col[1])  # gets the second part of the colour tuple and elimnates the decimals
    dblue = int(col[2])  # gets the third part of the colour tuple and elimnates the decimals
    #renders all the blitted text
    #renders the different aspect of the colouur component
    displayred= garamondFont.render(str(dred), True, BLACK)
    displaygreen= garamondFont.render(str(dgreen),True,BLACK)
    displayblue= garamondFont.render(str(dblue),True,BLACK)
    explainrgb= garamondFont.render("Colour:",True,BLACK)

    #renders the text that explains the keyboard shortcuts
    shortcutExplain1= garamondFont.render('1=1st song',True,BLACK)
    shortcutExplain2 =  garamondFont.render("2=2nd song",True,BLACK)
    shortcutExplain3 =  garamondFont.render("3=3rd song",True,BLACK)
    shortcutExplain4 =  garamondFont.render("b=last song",True,BLACK)
    shortcutExplain5 =  garamondFont.render("n= next song",True,BLACK)
    shortcutExplain6=  garamondFont.render("p=pauses music",True,BLACK)
    shortcutExplain7 =  garamondFont.render("s=starts music",True,BLACK)
    shortcutExplain8 =  garamondFont.render("scroll up=larger width",True,BLACK)
    shortcutExplain9 =  garamondFont.render("scroll down=smaller width",True,BLACK)
    shortcutExplain10 =  garamondFont.render("f=fills all shapes",True,BLACK)
    shortcutExplain11 =  garamondFont.render("u= unfills all shapes",True,BLACK)
    shortcutExplain12 =  garamondFont.render("r= selects a random sticker",True,BLACK)
    shortcutExplain13 =  garamondFont.render("z=undo",True,BLACK)
    shortcutExplain14=  garamondFont.render("v=redo",True,BLACK)
    shortcutExplain15 = garamondFont.render("Right click on pallette for more colors", True, BLACK)
    if th==0: #highlightes the unfilled section if the shapes are unfilled
        shortcutExplain10 =  garamondFont.render("f=fills all shapes", True, BLUE)
    else:   #highlightes the unfilled section if the shapes are filled
        shortcutExplain11 =  garamondFont.render("u= unfills all shapes", True, BLUE)
   #blits all rendered font
    screen.blit(displayred, (rgbRect))
    screen.blit(displaygreen, (730,80))
    screen.blit(displayblue, (760,80))
    screen.blit(explainrgb, (700, 60))
    screen.blit(shortcutExplain1,shortcutRect)
    screen.blit(shortcutExplain2, (700,420))
    screen.blit(shortcutExplain3, (700,440))
    screen.blit(shortcutExplain4, (700,460))
    screen.blit(shortcutExplain5, (700,480))
    screen.blit(shortcutExplain6, (700,500))
    screen.blit(shortcutExplain7, (700,520))
    screen.blit(shortcutExplain8, (820,400))
    screen.blit(shortcutExplain9, (820,420))
    screen.blit(shortcutExplain10,(820,440))
    screen.blit(shortcutExplain11,(820,460))
    screen.blit(shortcutExplain12,(820,480))
    screen.blit(shortcutExplain13,(820,500))
    screen.blit(shortcutExplain14,(820,520))
    screen.blit(shortcutExplain15,(700,540))
    if textinput.update(events):
        textool=False
        pygame_textinput.TextInput(text_color=(dred, dgreen, dblue), cursor_color=(dred, dgreen, dblue))
    ownerExplain= garamondFont.render("Anohana paint by:Jana J", True, BLACK)
    screen.blit(ownerExplain,ownerRect)

    display.update() #updaets the screen
#saves CPU to quit all functions used
font.quit()
mixer.quit()
del garamondFont
quit()
