from PIL import Image, ImageDraw
from collections import defaultdict
import json

def drawGridLines(draw,W,H):
    for x in range(500, W+1, 500):
        draw.line((x, 0, x, H), fill=(0, 0, 0), width=10)
    for y in range(500, H+1, 500):
        draw.line((0, y, W, y), fill=(0, 0, 0), width=10)

def drawDots(draw,W,H):
    #draw dots
    r=15
    for x in range(100,W+1,100):
        for y in range(100,H+1,100):
            draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0), outline=(0,0,0,0) )

def drawValidDots(draw,valid,color=(255,255,0),r=15):
    for x,y in valid:
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color, outline=(0,0,0,0) )

def drawLines(draw,lines,color=(0,0,0),thickness=10):
    for u,v in lines:
        draw.line( (u[0],u[1],v[0],v[1]), fill=color, width=thickness)

def addRect(inpSet,xlow,ylow,xmax,ymax,jump=100):
    for x in range(xlow,xmax+1,jump):
        for y in range(ylow,ymax+1,jump):
            inpSet.add( (x,y) )

def addDiagLine(inpSet,x1,y1,x2,y2,jump=100):
    L = abs(x2-x1)//jump
    for i in range(L+1):
        inpSet.add( (x1+i*(x2-x1)//L, y1+i*(y2-y1)//L) )

def generateMap():
    doors = set()
    vents = set()
    stairs= set()

    valid = set()
    invalid = set()
    
    #cockpit
    addRect(valid,500,2400,1400,2400)
    addRect(valid,300,2500,1400,3000)

    #communications
    addRect(valid,1700,2100,2100,2400)
    addRect(invalid,1900,2100,1900,2200)

    #coco hall
    addRect(valid,1600,2600,2400,2700)
    addRect(valid,2200,2800,2200,2800)

    #vault
    addRect(valid,1900,900,3100,1600)
    addRect(valid,2100,700,2900,800)
    addRect(valid,2100,1700,2900,1800)

    #viewing deck
    addRect(valid,1400,4100,2400,4400)

    #armory
    addRect(valid,1700,3000,2400,3900)
    addRect(invalid,1700,3300,2100,3500)
    addDiagLine(invalid,2100,3300,1900,3100)
    addDiagLine(invalid,2100,3500,1900,3700)

    #kitchen
    addRect(valid,2600,3400,2800,4900)
    addRect(valid,2900,3800,3400,4900)

    #art hall
    addRect(valid,3600,4200,4400,4400)

    #security
    addRect(valid,4500,4000,5100,4400)

    #brigg
    addRect(valid,3300,1200,4100,1400)

    #left gap room
    addRect(valid,4300,1200,4600,1500)
    addRect(valid,4300,1200,4400,1400)

    #right gap room
    addRect(valid,5200,1200,6000,1400)
    addRect(valid,5300,1600,5800,1700)

    #records
    addRect(valid,6200,1000,7100,1400)
    addRect(valid,6500,800,6700,1700)
    addRect(valid,6400,1600,6800,1600)
    addRect(invalid,7100,1000,7100,1000)
    addRect(invalid,6500,1200,6800,1200)
    
    #showers
    addRect(valid,6200,1800,6500,2000)
    addRect(valid,6600,2400,6700,2600)
    addRect(valid,6800,2400,7300,2900)
    addRect(valid,6700,2100,7300,2200)
    addRect(valid,7200,2300,7300,2300)
    addRect(valid,7400,2400,7600,2600)
    addRect(invalid,6400,1900,6400,1900) #bench
    addRect(invalid,6500,1800,6500,1800) #connector
    addRect(valid,6400,2000,6500,2700)
    addRect(valid,6600,1900,6700,1900)
    addRect(invalid,6700,2500,7100,2500)
    addRect(invalid,6900,2700,7100,2800)

    #meeting room
    addRect(valid,4300,200,6300,500)
    addRect(invalid,5000,300,5600,400)

    #lounge
    addRect(valid,7300,1100,7700,1800)
    addRect(valid,7900,1400,8700,1800)
    addRect(valid,7800,1700,7800,1800)
    addRect(valid,8600,1900,8600,1900)
    

    #cargo bay
    addRect(valid,8400,2000,8800,2000)
    addRect(valid,8500,2100,8700,2200)
    addRect(valid,8100,2300,9500,3100)
    addRect(invalid,8100,2400,8400,2600)
    addRect(invalid,8800,2400,9000,2600)
    addRect(invalid,8700,2800,9200,2900)
    addRect(invalid,8600,3000,9000,3100)
    addRect(invalid,8400,2700,8400,2900)
    addRect(invalid,8200,2800,8200,2900)
    addRect(invalid,8100,2900,8200,2900)
    addRect(valid,7800,1700,8000,1800)

    #medical
    addRect(valid,6900,3300,8500,3400)
    addRect(valid,6900,3500,7100,4000)
    addRect(valid,6900,3900,7500,4000)
    addRect(valid,7400,3700,7400,3900)

    #electrical
    addRect(valid,5200,3400,6700,3500)
    addRect(valid,5200,3700,6700,3800)
    addRect(valid,5600,4000,6700,4200)
    addRect(valid,5200,3400,5300,4100)
    addRect(valid,5700,3400,5700,4200)
    addRect(valid,6100,3400,6100,4200)
    addRect(valid,6500,3000,6600,4200)
    addRect(valid,6300,3000,6700,3100)
    
    #main hall
    addRect(valid,4500,2500,6200,2600) #main
    addRect(valid,4600,2100,4700,2600) #empty n room
    addRect(valid,5100,2100,5200,2600) #trash+vent
    addRect(valid,5500,2200,5600,2600) #darkroom

    addRect(valid,5900,2100,5900,2400)#wires/decontam
    addRect(valid,6000,2200,6000,2400)
    addRect(valid,6100,2200,6100,2300)
    
    addRect(valid,4600,2700,4700,3000)#divert/vent
    addRect(valid,4800,2800,4800,3000)

    addRect(valid,5500,2700,5700,3100)#electric entr
    addRect(invalid,5700,2700,5700,2700)

    #engines
    addRect(valid,2600,2300,4300,2900)
    addRect(invalid,3300,2300,3500,2300)
    addRect(invalid,2800,2400,3500,2600)
    addRect(invalid,2600,2800,3600,2900)
    addRect(invalid,4000,2800,4400,2900)
    addRect(invalid,3900,2300,4000,2500)
    addRect(invalid,4100,2300,4300,2400)
    addRect(invalid,4000,2600,4000,2600)
    addRect(invalid,4200,2600,4200,2700)
    addRect(valid,3600,1600,3800,2500)
    addRect(valid,3500,1600,3500,1600)


    addRect(doors,1500,2600,1500,2700) #cockpit
    addRect(doors,2500,2600,2500,2700) #engine(west)
    addRect(doors,1800,2500,1900,2500) #comms
    addRect(doors,2200,2900,2200,2900) #armory(north)
    addRect(doors,2500,3500,2500,3600) #armory(east)
    addRect(doors,2500,4200,2500,4300) #kitchen(southwest)
    addRect(doors,3500,4200,3500,4300) #kitchen(east)
    addRect(doors,5500,3400,5500,3500) #electric(vert) nw
    addRect(doors,6000,3400,6000,3500) #electric(vert) n
    addRect(doors,6300,3400,6300,3500) #electric(vert) ne
    addRect(doors,5500,3700,5500,3800) #electric(vert) w
    addRect(doors,6000,3700,6000,3800) #electric(vert) center
    addRect(doors,6300,3700,6300,3800) #electric(vert) e
    addRect(doors,6000,4000,6000,4200) #electric(vert) s
    addRect(doors,6300,4000,6300,4200) #electric(vert) se
    addRect(doors,5700,3600,5700,3600) #electric(horz) nw
    addRect(doors,6100,3600,6100,3600) #electric(horz) n
    addRect(doors,6500,3600,6600,3600) #electric(horz) ne
    addRect(doors,6100,3900,6100,3900) #electric(horz) s
    addRect(doors,6500,3900,6600,3900) #electric(horz) se
    addRect(doors,6800,3700,6800,3800) #medbay(west)
    addRect(doors,8400,3200,8500,3200) #medbay(north)
    addRect(doors,7200,1100,7200,1300) #records(east)
    addRect(doors,6600,1800,6700,1800) #records(south)
    addRect(doors,6100,1100,6100,1300) #records(west)
    addRect(doors,3200,1200,3200,1400) #brig(west)
    addRect(doors,4200,1200,4200,1400) #brig(east)
    addRect(doors,3600,1500,3700,1500) #brig(south)
    addRect(doors,4400,2500,4400,2600) #main hall(west)
    addRect(doors,6300,2500,6300,2600) #main hall(east)
    
    vent_cockpit=(600,2700)
    vent_vault=(2000,1300)
    vent_viewing=(1600,4200)
    vent_kitchen=(3400,3900)
    vent_engine=(3800,2900)
    vent_main_south=(4800,3000)
    vent_main_north=(5200,2100)
    vent_gap_left=(4300,1500)
    vent_gap_right=(5600,1700)
    vent_records=(7100,1300)
    vent_showers=(7200,2700)
    vent_cargo=(8100,3000)
    vents.add( (vent_cockpit,vent_vault) )
    vents.add( (vent_cockpit,vent_viewing) )
    vents.add( (vent_kitchen,vent_engine) )
    vents.add( (vent_kitchen,vent_main_south) )
    vents.add( (vent_engine,vent_main_south) )
    vents.add( (vent_gap_left,vent_gap_right) )
    vents.add( (vent_gap_left,vent_main_north) )
    vents.add( (vent_gap_right,vent_main_north) )
    vents.add( (vent_showers,vent_records) )
    vents.add( (vent_showers,vent_cargo) )
    vents.add( (vent_records,vent_cargo) )

    stairs_meeting_l = (4400,500)
    stairs_meeting_r = (4500,500)
    stairs_gap_l = (4400,1200)
    stairs_gap_r = (4500,1200)
    stairs_gap_r_top = (5300,1400)
    stairs_gap_r_bot = (5300,1600)
    stairs_gap_left = (4600,1300)
    stairs_gap_right= (5200,1300)
    stairs.add( (stairs_meeting_l,stairs_gap_l) )
    stairs.add( (stairs_meeting_r,stairs_gap_r) )
    stairs.add( (stairs_gap_r_top,stairs_gap_r_bot) )
    stairs.add( (stairs_gap_left,stairs_gap_right) )

    walkablePoints = valid.difference(invalid).union(doors)

    return (walkablePoints,doors,vents,stairs)


def displayImage():
    with Image.open("airship_cropped.png") as im:
        H = im.height
        W = im.width
        draw = ImageDraw.Draw(im)

        drawGridLines(draw,W,H)
        drawDots(draw,W,H)

        walkablePoints, doors, vents, stairs = generateMap()

        drawValidDots(draw,walkablePoints)
        drawValidDots(draw,doors,color=(0,255,0),r=20)
        drawLines(draw,vents,color=(0,0,0))
        drawLines(draw,stairs,color=(0,0,0))
                
        im.show()

def saveToJson(fname):
    walkablePoints, doors, vents, stairs = generateMap()
    data={}
    data["walkable"] = [w for w in walkablePoints]
    data["doors"] = [d for d in doors]
    data["vents"] = [v for v in vents]
    data["stairs"] = [s for s in stairs]

    with open(fname, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    

"""
def findNeighbors(node,allNodes,specialEdges,allowDiag=True):
    ans = []
    x, y = node

    for i,(dx,dy) in enumerate([(-100,0),(0,-100),(100,0),(0,100),(-100,-100),(-100,100),(100,100),(100,-100)]):
        newNode = (x+dx,y+dy)
        if newNode not in allNodes:
            continue
        if (node,newNode) in specialEdges:
            continue
        else:
            ans.append( (node,newNode, 1 if i<4 else 2**0.5) )
    return neighbors
"""

if __name__ == "__main__":
    #displayImage()
    saveToJson("mapData.txt")
