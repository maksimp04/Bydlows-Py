import pygame
import datetime
import math
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
rect = lambda pos,col: pygame.draw.rect(w,col,pos)
def text(pos,txt,clr=(255,255,255),antialias=True,centered=True):
    t = font.render(txt,antialias,clr)
    if centered == True:
        text_rect = t.get_rect()
        text_rect.midtop = pos
        w.blit(t,text_rect)
    else:
        w.blit(t,pos)
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
}
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

def create_folder(name="new_folder",path="Desktop"):
    for i in tree:
        if i["name"] == path:
            i["value"].append({
                "name":name,
                "type":type.folder,
                "value":[],
                "x":0,
                "y":0,
            })

def create_image(name="new_image",path="Desktop"):
    for i in tree:
        if i["name"] == path:
            i["value"].append({
                "name":name,
                "type":type.image,
                "value":'',
                "x":0,
                "y":0,
            })

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
        pass

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
    text((snap(16+c(1)),snap(c(3))),str(pctime.hour).zfill(2) + ":" + str(pctime.minute).zfill(2))
    for index,i in enumerate(tree[0]["value"]):
        if i["x"] + i["y"] == 0:
            i["x"] = 20+65*(math.floor(index/8))
            i["y"] = 55*(index%8)
        if i["type"] == type.folder:
            w.blit(icons["folder"],(i["x"],i["y"]))
        elif i['type'] == type.image:
            w.blit(icons["picture"],(i["x"],i["y"]))
        text((i["x"]+c(2),i["y"]+c(5)),i["name"])
        if hover(pygame.mouse.get_pos(),(i["x"]-c(2),i["y"]),(32+c(4),32+c(4))):
            if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
                if i["type"] == type.folder:
                    open_folder("Desktop/"+i["name"])
                else:
                    open_file("Desktop/"+i["name"])
            elif changed(2,pygame.mouse.get_pressed()[2]) and pygame.mouse.get_pressed()[2]:
                if i["type"] == type.image:
                    contextmenu = {
                    "pos":pygame.mouse.get_pos(),
                    "value":[
                        {
                            "str":"Set Image",
                            'func':lambda:set_image("Desktop/"+i["name"],input("image path: "))
                        }
                    ]
                    }
    for index,i in enumerate(opened):
        if i["x"] + i["y"] + i["width"] + i["height"] == 0:
            i["x"] = 128 + 32 * index
            i["y"] = 128 + 32 * index
            i["width"] = 128
            i["height"] = 128
        if i["type"] == type.folder:
            rect((i["x"],i["y"],i["width"],i["height"]),(style["window"]))
            rect((i["x"],i["y"],i["width"],16),(style["panel"]))
            rect((i["x"],i["y"],i["width"],16),(style["panel"]))
            text((i["x"]+2,i['y']),i["name"],(255,255,255),True,False)
            w.blit(icons["cross"],(i["x"]+i["width"]-16,i["y"]))
            if hover(pygame.mouse.get_pos(),(i["x"]+i["width"]-16,i["y"]),(16,16)):
                if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
                    close_file(index)
        elif i["type"] == type.image:
            rect((i["x"],i["y"],i["width"],i["height"]),(style["window"]))
            rect((i["x"],i["y"],i["width"],16),(style["panel"]))
            rect((i["x"],i["y"],i["width"],16),(style["panel"]))
            text((i["x"]+2,i['y']),i["name"],(255,255,255),True,False)
            w.blit(icons["cross"],(i["x"]+i["width"]-16,i["y"]))
            r = i['value']['value'].get_rect()
            r.center = (i['x']+64,i['y']+64)
            w.blit(i['value']['value'],r)
            if hover(pygame.mouse.get_pos(),(i["x"]+i["width"]-16,i["y"]),(16,16)):
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
        text((contextmenu["pos"][0]+2,contextmenu["pos"][1]+2+17*index),column['str'],(0,0,0),True,False)
        if hover(pygame.mouse.get_pos(),(contextmenu["pos"][0],contextmenu["pos"][1]+17*index),(128,16)):
            if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
                column['func']()
                contextmenu = {'pos':pygame.mouse.get_pos(),'value':[]}
    if changed(1,pygame.mouse.get_pressed()[0]) and pygame.mouse.get_pressed()[0]:
        contextmenu = {'pos':(0,0),'value':[]}
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
