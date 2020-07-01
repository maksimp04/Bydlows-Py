import pygame
import datetime
import math
import colorsys
from enum import Enum
#==//==//==#
pygame.init()
w = pygame.display.set_mode((512,512))
pygame.display.set_caption("Bydlows Py")
icon = pygame.image.load('icons/icon.jpg')
pygame.display.set_icon(icon)

run = True
fpslock = 25
#==//==//==#

#==//==//==#
def snap(val=0):
    return 512-val
def c(val=0):
    return val*8
rect = lambda pos,col,x=0: pygame.draw.rect(w,col,pos,x)
def text(pos,txt,clr=(255,255,255),antialias=True,centered=True):
    t = font.render(txt,antialias,clr)
    if centered == True:
        text_rect = t.get_rect()
        text_rect.midtop = pos
        w.blit(t,text_rect)
        return text_rect
    else:
        w.blit(t,pos)
        return t.get_rect()
def hover(mpos,boxpos,boxsize):
    if mpos[0] >= boxpos[0] and mpos[1] >= boxpos[1] and mpos[0] <= boxpos[0] + boxsize[0] and mpos[1] <= boxpos[1] + boxsize[1]:
        return True
    else:
        return False
_changed = {}
def changed(index,var):
    if index in _changed:
        if _changed[index] != var:
            _changed[index] = var
            return True
        else:
            return False
    else:
        _changed[index] = var
        return True
icons = {
    "folder":pygame.image.load('icons/folder.png'),
    "folder":pygame.image.load('icons/folder32.png'),
    "cross":pygame.image.load('icons/cross.png'),
    "picture":pygame.image.load('icons/picture.png'),
    "terminal":pygame.image.load('icons/terminal.png'),
    "palette":pygame.image.load('icons/palette.png'),
    "palette2":pygame.image.load('icons/palette2.png'),
    "palette3":pygame.image.load('icons/palette3.png'),
}
def sub(first,second):
    result = []
    for i in range(len(first)):
        result.append(first[i] - second[i])
    return result
def add(first,second):
    result = []
    for i in range(len(first)):
        result.append(first[i] + second[i])
    return result
#==//==//==#

style = {
    "bgcolor": (105,105,215),
    "panel": (0,0,0),
    "window": (255,255,255),
    "text": (255,255,255),
}

class type(Enum):
    folder = 1
    exec = 2
    image = 3
    _mover = 4
    _styleeditor = 5

class system(Enum):
    style = 1

tree = [
    {
        "name":"Desktop",
        "type":type.folder,
        "value":[],
    }
]
opened = []
contextmenu = {'pos':(0,0),'value':[]}
textbox = {'active':False,'box':(0,0,0,0),'input':"",'func':None,"tag":""}

def create_folder(name="new_folder",path="Desktop"):
    for i in tree:
        if i["name"] == path:
            samenamers=1
            for x in i["value"]:
                if x['name'].find(name) != -1:
                    samenamers += 1
            i["value"].append({
                "name":name+str(samenamers),
                "type":type.folder,
                "value":[],
                "x":0,
                "y":0,
            })

def create_image(name="new_image",path="Desktop"):
    for i in tree:
        if i["name"] == path:
            samenamers=1
            for x in i["value"]:
                if x['name'].find(name) != -1:
                    samenamers += 1
            i["value"].append({
                "name":name+str(samenamers),
                "type":type.image,
                "value":'',
                "x":0,
                "y":0,
            })

def open_mover(appname,apppath,curpath):
    p = apppath.split("/")
    f = tree
    for index,i in enumerate(p):
        for x in f:
            if i == x["name"]:
                if index == len(p)-1:
                    f = x
                else:
                    f = x["value"]
                    break
    opened.append({
    "name":"Move %s to..."%appname,
    "execute":[
        lambda x,y: rect((x+10,y+16+15,192-20,256-16-15-10),(215,215,215)),
        lambda x,y: text((x+10,y+2+14),curpath+"/",(0,0,0),True,False),
        lambda x,y: script(type._mover,x,y)
    ],
    "x":512/2-192/2,
    "y":512/2-256/2,
    "width":192,
    "height":256,
    "type":type._mover,})

def open_folder(path):
    p = path.split("/")
    f = tree
    for index,i in enumerate(p):
        for x in f:
            if i == x["name"]:
                if index == len(p)-1:
                    f = x
                else:
                    f = x["value"]
                    break
    opened.append({
    "name":f["name"],
    "value":f,
    "x":0,
    "y":0,
    "width":0,
    "height":0,
    "type":type.folder,})

def open_file(path):
    p = path.split("/")
    f = tree
    for index,i in enumerate(p):
        for x in f:
            if i == x["name"]:
                if index == len(p)-1:
                    f = x
                else:
                    f = x["value"]
                    break
    opened.append({
    "name":f["name"],
    "value":f,
    "x":0,
    "y":0,
    "width":0,
    "height":0,
    "type":f["type"],})

def close_file(index):
    opened.pop(index)

def set_image(path,z):
    p = path.split("/")
    f = tree
    for index,i in enumerate(p):
        for x in f:
            if i == x["name"]:
                if index == len(p)-1:
                    f = x
                else:
                    f = x["value"]
                    break

    f["value"] = pygame.image.load(z)


def execute_system_app(index):
    if index == system["style"]:
        opened.append({
        "name":"Style Editor",
        "execute":[
            lambda x,y: text((x+5,y+21),"Background Color",sub((255,255,255),style['text']),True,False),
            lambda x,y: w.blit(icons['palette'],(x+5,y+21+14)),
            lambda x,y: w.blit(icons['palette3'],(x+126,y+21+14)),
            lambda x,y: w.blit(icons['palette2'],(x+186,y+21+14)),
            lambda x,y: text((x+5,y+45),"Panel Color",sub((255,255,255),style['text']),True,False),
            lambda x,y: w.blit(icons['palette'],(x+5,y+45+14)),
            lambda x,y: w.blit(icons['palette3'],(x+126,y+45+14)),
            lambda x,y: w.blit(icons['palette2'],(x+186,y+45+14)),
            lambda x,y: text((x+5,y+69),"Window Color",sub((255,255,255),style['text']),True,False),
            lambda x,y: w.blit(icons['palette'],(x+5,y+69+14)),
            lambda x,y: w.blit(icons['palette3'],(x+126,y+69+14)),
            lambda x,y: w.blit(icons['palette2'],(x+186,y+69+14)),
            lambda x,y: text((x+5,y+93),"Text Color",sub((255,255,255),style['text']),True,False),
            lambda x,y: w.blit(icons['palette'],(x+5,y+93+14)),
            lambda x,y: w.blit(icons['palette3'],(x+126,y+93+14)),
            lambda x,y: w.blit(icons['palette2'],(x+186,y+93+14)),
            lambda x,y: script(type._styleeditor,x,y)
        ],
        "x":50,
        "y":50,
        "width":246,
        "height":126,
        "type":type._styleeditor,})

def script(id,x,y):
    if id == type._styleeditor:
        rect((x+5 + 116*colorsys.rgb_to_hsv(style['bgcolor'][0],style['bgcolor'][1],style['bgcolor'][2])[0],y+21+12,1,14),sub((255,255,255),style['window']))
        rect((x+126 + 50*colorsys.rgb_to_hsv(style['bgcolor'][0],style['bgcolor'][1],style['bgcolor'][2])[1],y+21+12,1,14),sub((255,255,255),style['window']))
        rect((x+186 + 50*(colorsys.rgb_to_hsv(style['bgcolor'][0],style['bgcolor'][1],style['bgcolor'][2])[2]/255.0),y+21+12,1,14),sub((255,255,255),style['window']))
        rect((x+5 + 116*colorsys.rgb_to_hsv(style['panel'][0],style['panel'][1],style['panel'][2])[0],y+45+12,1,14),sub((255,255,255),style['window']))
        rect((x+126 + 50*colorsys.rgb_to_hsv(style['panel'][0],style['panel'][1],style['panel'][2])[1],y+45+12,1,14),sub((255,255,255),style['window']))
        rect((x+126 + 50*colorsys.rgb_to_hsv(style['panel'][0],style['panel'][1],style['panel'][2])[1],y+45+12,1,14),sub((255,255,255),style['window']))
        rect((x+186 + 50*(colorsys.rgb_to_hsv(style['panel'][0],style['panel'][1],style['panel'][2])[2]/255.0),y+45+12,1,14),sub((255,255,255),style['window']))
        rect((x+5 + 116*colorsys.rgb_to_hsv(style['window'][0],style['window'][1],style['window'][2])[0],y+69+12,1,14),sub((255,255,255),style['window']))
        rect((x+126 + 50*colorsys.rgb_to_hsv(style['window'][0],style['window'][1],style['window'][2])[1],y+69+12,1,14),sub((255,255,255),style['window']))
        rect((x+186 + 50*(colorsys.rgb_to_hsv(style['window'][0],style['window'][1],style['window'][2])[2]/255.0),y+69+12,1,14),sub((255,255,255),style['window']))
        rect((x+5 + 116*colorsys.rgb_to_hsv(style['text'][0],style['text'][1],style['text'][2])[0],y+93+12,1,14),sub((255,255,255),style['window']))
        rect((x+126 + 50*colorsys.rgb_to_hsv(style['text'][0],style['text'][1],style['text'][2])[1],y+93+12,1,14),sub((255,255,255),style['window']))
        rect((x+186 + 50*(colorsys.rgb_to_hsv(style['text'][0],style['text'][1],style['text'][2])[2]/255.0),y+93+12,1,14),sub((255,255,255),style['window']))
        if pygame.mouse.get_pressed()[0]:
            if hover(pygame.mouse.get_pos(),(x+5,y+21+12),(112,10)):
                value = (pygame.mouse.get_pos()[0] - (x+5)) / (112)
                hsv = colorsys.rgb_to_hsv(style['bgcolor'][0],style['bgcolor'][1],style['bgcolor'][2])
                style['bgcolor'] = colorsys.hsv_to_rgb(value,hsv[1],hsv[2])
            elif hover(pygame.mouse.get_pos(),(x+126,y+21+12),(50,10)):
                value = (pygame.mouse.get_pos()[0] - (x+126)) / (50)
                hsv = colorsys.rgb_to_hsv(style['bgcolor'][0],style['bgcolor'][1],style['bgcolor'][2])
                style['bgcolor'] = colorsys.hsv_to_rgb(hsv[0],value,hsv[2])
            elif hover(pygame.mouse.get_pos(),(x+186,y+21+12),(50,10)):
                value = (pygame.mouse.get_pos()[0] - (x+186)) / (50) *255
                hsv = colorsys.rgb_to_hsv(style['bgcolor'][0],style['bgcolor'][1],style['bgcolor'][2])
                style['bgcolor'] = colorsys.hsv_to_rgb(hsv[0],hsv[1],value)
            elif hover(pygame.mouse.get_pos(),(x+5,y+45+12),(112,10)):
                value = (pygame.mouse.get_pos()[0] - (x+5)) / (112)
                hsv = colorsys.rgb_to_hsv(style['panel'][0],style['panel'][1],style['panel'][2])
                style['panel'] = colorsys.hsv_to_rgb(value,hsv[1],hsv[2])
            elif hover(pygame.mouse.get_pos(),(x+126,y+45+12),(50,10)):
                value = (pygame.mouse.get_pos()[0] - (x+126)) / (50)
                hsv = colorsys.rgb_to_hsv(style['panel'][0],style['panel'][1],style['panel'][2])
                style['panel'] = colorsys.hsv_to_rgb(hsv[0],value,hsv[2])
            elif hover(pygame.mouse.get_pos(),(x+186,y+45+12),(50,10)):
                value = (pygame.mouse.get_pos()[0] - x-186) / (50) *255
                hsv = colorsys.rgb_to_hsv(style['panel'][0],style['panel'][1],style['panel'][2])
                style['panel'] = colorsys.hsv_to_rgb(hsv[0],hsv[1],value)
            elif hover(pygame.mouse.get_pos(),(x+5,y+69+12),(112,10)):
                value = (pygame.mouse.get_pos()[0] - x-5) / (112)
                hsv = colorsys.rgb_to_hsv(style['window'][0],style['window'][1],style['window'][2])
                style['window'] = colorsys.hsv_to_rgb(value,hsv[1],hsv[2])
            elif hover(pygame.mouse.get_pos(),(x+126,y+69+12),(50,10)):
                value = (pygame.mouse.get_pos()[0] - x-126) / (50)
                hsv = colorsys.rgb_to_hsv(style['window'][0],style['window'][1],style['window'][2])
                style['window'] = colorsys.hsv_to_rgb(hsv[0],value,hsv[2])
            elif hover(pygame.mouse.get_pos(),(x+186,y+69+12),(50,10)):
                value = (pygame.mouse.get_pos()[0] - x-186) / (50) *255
                hsv = colorsys.rgb_to_hsv(style['window'][0],style['window'][1],style['window'][2])
                style['window'] = colorsys.hsv_to_rgb(hsv[0],hsv[1],value)
            elif hover(pygame.mouse.get_pos(),(x+5,y+93+12),(112,10)):
                value = (pygame.mouse.get_pos()[0] - x-5) / (112)
                hsv = colorsys.rgb_to_hsv(style['text'][0],style['text'][1],style['text'][2])
                style['text'] = colorsys.hsv_to_rgb(value,hsv[1],hsv[2])
            elif hover(pygame.mouse.get_pos(),(x+126,y+93+12),(50,10)):
                value = (pygame.mouse.get_pos()[0] - x-126) / (50)
                hsv = colorsys.rgb_to_hsv(style['text'][0],style['text'][1],style['text'][2])
                style['text'] = colorsys.hsv_to_rgb(hsv[0],value,hsv[2])
            elif hover(pygame.mouse.get_pos(),(x+186,y+93+12),(50,10)):
                value = (pygame.mouse.get_pos()[0] - x-186) / (50) *255
                hsv = colorsys.rgb_to_hsv(style['text'][0],style['text'][1],style['text'][2])
                style['text'] = colorsys.hsv_to_rgb(hsv[0],hsv[1],value)
    elif id == type._mover:
        pass

def pop_textbox(r,func,tag=""):
    textbox['box'] = r
    textbox['func'] = func
    textbox['active'] = True
    textbox['tag'] = tag

def rename(path,newname):
    p = path.split("/")
    f = tree
    for index,i in enumerate(p):
        for x in f:
            if i == x["name"]:
                if index == len(p)-1:
                    f = x
                else:
                    f = x["value"]
                    break
    f['name'] = newname

#font#
deffont = pygame.font.SysFont('Arial', 12)
font = deffont
######

create_folder()
changed(1,pygame.mouse.get_pressed()[0])
changed(2,pygame.mouse.get_pressed()[2])

while run:
    pygame.time.delay(int(1000/fpslock))
    rect((0,0,snap(),snap()),style['bgcolor'])
    rect((0,snap(32),snap(),32),style['panel'])
    pctime = datetime.datetime.now()
    text((snap(16+c(1)),snap(16+6)),str(pctime.hour).zfill(2) + ":" + str(pctime.minute).zfill(2),style['text'])
    for index,desktopapps in enumerate(tree[0]["value"]):
        if desktopapps["x"] + desktopapps["y"] == 0:
            desktopapps["x"] = 20+65*(math.floor(index/7))
            desktopapps["y"] = 64*(index%7)
        if desktopapps["type"] == type.folder:
            w.blit(icons["folder"],(desktopapps["x"],desktopapps["y"]))
        elif desktopapps['type'] == type.image:
            w.blit(icons["picture"],(desktopapps["x"],desktopapps["y"]))
        text((desktopapps["x"]+c(2),desktopapps["y"]+c(5)),desktopapps["name"],style['text'])
        if hover(pygame.mouse.get_pos(),(desktopapps["x"]-c(2),desktopapps["y"]),(32+c(4),32+c(4))):
            if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
                if desktopapps["type"] == type.folder:
                    open_folder("Desktop/"+desktopapps["name"])
                else:
                    open_file("Desktop/"+desktopapps["name"])
            elif changed(2,pygame.mouse.get_pressed()[2]) and pygame.mouse.get_pressed()[2]:
                if desktopapps["type"] == type.image:
                    item = desktopapps
                    contextmenu = {
                    "pos":pygame.mouse.get_pos(),
                    "value":[
                        {
                            "str":"Rename",
                            "func":lambda:pop_textbox((item["x"]-16,item['y']+c(5),64,14),lambda x:rename("Desktop/"+item['name'],x),"rename")
                        },{
                            "str":"Set Image",
                            'func':lambda:pop_textbox((item["x"]-16,item['y']+56,64,14),lambda x:set_image("Desktop/"+item['name'],x),"img")
                        },{
                            "str":"Move to...",
                            'func':lambda:open_mover(item['name'],"Desktop/"+item['name'],"Desktop")
                        }
                    ]
                    }
                elif desktopapps["type"] == type.folder:
                    item = desktopapps
                    contextmenu = {
                    "pos":pygame.mouse.get_pos(),
                    "value":[
                        {
                            "str":"Rename",
                            "func":lambda:pop_textbox((item["x"]-16,item['y']+c(5),64,14),lambda x:rename("Desktop/"+item['name'],x),"rename")
                        }
                    ]
                    }
    for index,windows in enumerate(opened):
        if windows["x"] + windows["y"] + windows["width"] + windows["height"] == 0:
            windows["x"] = 128 + 32 * index
            windows["y"] = 128 + 32 * index
            windows["width"] = 128
            windows["height"] = 128
        if windows["type"] == type.folder:
            rect((windows["x"],windows["y"],windows["width"],windows["height"]),(style["window"]))
            rect((windows["x"],windows["y"],windows["width"],16),(style["panel"]))
            rect((windows["x"],windows["y"],windows["width"],16),(style["panel"]))
            text((windows["x"]+4+16,windows['y']),windows["name"],style['text'],True,False)
            ic = icons['folder']
            ic = pygame.transform.scale(ic,(16,16))
            w.blit(ic,(windows["x"]+2,windows['y']))
            w.blit(icons["cross"],(windows["x"]+windows["width"]-16,windows["y"]))
            if hover(pygame.mouse.get_pos(),(windows["x"]+windows["width"]-16,windows["y"]),(16,16)):
                if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
                    close_file(index)
        elif windows["type"] == type.image:
            rect((windows["x"],windows["y"],windows["width"],windows["height"]),(style["window"]))
            rect((windows["x"],windows["y"],windows["width"],16),(style["panel"]))
            rect((windows["x"],windows["y"],windows["width"],16),(style["panel"]))
            text((windows["x"]+4+16,windows['y']),windows["name"],style['text'],True,False)
            ic = icons['picture']
            ic = pygame.transform.scale(ic,(16,16))
            w.blit(ic,(windows["x"]+2,windows['y']))
            w.blit(icons["cross"],(windows["x"]+windows["width"]-16,windows["y"]))
            if windows['value']['value'] == "":
                text((windows['x']+64,windows['y']+48),"No image loaded in.",(0,0,0))
                text((windows['x']+64,windows['y']+80),"To set image click RMB on img file",(0,0,0))
                text((windows['x']+64,windows['y']+96),"and select 'set image' option.",(0,0,0))
            else:
                r = windows['value']['value'].get_rect()
                r.center = (windows['x']+64,windows['y']+64)
                img_rect = w.blit(windows['value']['value'],r)
                text((windows['x']+2,windows['y']+128-12),str(img_rect[2])+"x"+str(img_rect[3]),(0,0,0),True,False)
                try:
                    text((windows['x']+128-32,windows['y']+128-18),str(int(scale*100))+"%",(0,0,0))
                except NameError:
                    text((windows['x']+128-16,windows['y']+128-12),"100%",(0,0,0))
                except TypeError:
                    text((windows['x']+128-16,windows['y']+128-12),"100%",(0,0,0))
            if hover(pygame.mouse.get_pos(),(windows["x"]+windows["width"]-16,windows["y"]),(16,16)):
                if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
                    close_file(index)
        else:
            rect((windows["x"],windows["y"],windows["width"],windows["height"]),(style["window"]))
            rect((windows["x"],windows["y"],windows["width"],16),(style["panel"]))
            rect((windows["x"],windows["y"],windows["width"],16),(style["panel"]))
            text((windows["x"]+4+16,windows['y']),windows["name"],style['text'],True,False)
            ic = icons['terminal']
            ic = pygame.transform.scale(ic,(16,16))
            w.blit(ic,(windows["x"]+2,windows['y']))
            w.blit(icons["cross"],(windows["x"]+windows["width"]-16,windows["y"]))
            for i in windows['execute']:
                i(windows['x'],windows['y'])
            if hover(pygame.mouse.get_pos(),(windows["x"]+windows["width"]-16,windows["y"]),(16,16)):
                if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
                    close_file(index)
    if changed(2,pygame.mouse.get_pressed()[2]) and pygame.mouse.get_pressed()[2] and len(contextmenu['value']) == 0:
        contextmenu ={
        "pos": pygame.mouse.get_pos() + (2,2),
        "value":[{
            "str":"Create Folder",
            "func": lambda: create_folder()
            },{
            "str":"Create Image",
            "func": lambda: create_image()
            },{
            "str":"Style",
            "func": lambda: execute_system_app(system["style"])
            }
        ]}
    for index,column in enumerate(contextmenu["value"]):
        rect((contextmenu["pos"][0],contextmenu["pos"][1]+17*index,128,16),style["window"])
        text((contextmenu["pos"][0]+2,contextmenu["pos"][1]+2+17*index),column['str'],sub(style['window'],style['text']),True,False)
        if hover(pygame.mouse.get_pos(),(contextmenu["pos"][0],contextmenu["pos"][1]+17*index),(128,16)):
            if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
                column['func']()
                contextmenu = {'pos':pygame.mouse.get_pos(),'value':[]}
    if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
        contextmenu = {'pos':(0,0),'value':[]}
    if textbox['active'] == True:
        try:
            rect((textbox['box'][0],textbox['box'][1],max(textbox['box'][2],s+2),textbox['box'][3]),style['text'])
        except TypeError:
            rect((textbox['box'][0],textbox['box'][1],textbox['box'][2],textbox['box'][3]),style['text'])
        except NameError:
            rect((textbox['box'][0],textbox['box'][1],textbox['box'][2],textbox['box'][3]),style['text'])
        s = text((textbox['box'][0]+1,textbox['box'][1]+1),textbox['input'],sub(style['window'],style['text']),True,False).width
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if textbox['active'] == True:
                if event.key == pygame.K_BACKSPACE:
                    textbox['input'] = textbox['input'][:-1]
                elif event.key == pygame.K_KP_ENTER:
                    if textbox['input'] == "":
                        textbox['active'] = False
                        textbox['box'] = (0,0,0,0)
                        textbox['func'] = False
                        textbox['input'] = ""
                    else:
                        if textbox['tag'] == "img":
                            try:
                                with open(textbox['input']) as f:
                                    textbox['func'](textbox['input'])
                                    textbox['active'] = False
                                    textbox['box'] = (0,0,0,0)
                                    textbox['func'] = False
                                    textbox['input'] = ""
                            except IOError:
                                print("File not accessible")
                        else:
                            textbox['func'](textbox['input'])
                            textbox['active'] = False
                            textbox['box'] = (0,0,0,0)
                            textbox['func'] = False
                            textbox['input'] = ""
                else:
                    textbox['input'] += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hover(pygame.mouse.get_pos(),(textbox['box'][0],textbox['box'][1]),(textbox['box'][2],textbox['box'][3])) == False and textbox['active'] == True:
                textbox['active'] = False
                textbox['box'] = (0,0,0,0)
                textbox['func'] = False
                textbox['input'] = ""
