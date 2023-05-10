import numpy as np
import random
import cv2

nPts=20
mapSize=400
boundarySize=20
imgSize = mapSize + 2 * boundarySize

def drawTriangles(triangleList, img):

    ##Za svaki trokut u listi trokuta pokupi sve točke i nacrtaj linije između njih
    for i in range(len(triangleList)):

        point1x=int(triangleList[i][0])
        point1y=int(triangleList[i][1])
        point2x=int(triangleList[i][2])
        point2y=int(triangleList[i][3])
        point3x=int(triangleList[i][4])
        point3y=int(triangleList[i][5])

        cv2.line(img,(point1x,point1y),(point2x,point2y),(0,0,0))
        cv2.line(img,(point2x,point2y),(point3x,point3y),(0,0,0))
        cv2.line(img,(point1x,point1y),(point3x,point3y),(0,0,0))


def fillTriangle(edgeVertex,subdiv,img,color):
    
    currentEdge=edgeVertex
    points=np.zeros((0,2),dtype=np.uint8)

    ##Prolazak preko edge-ova i skupljanje koordinata svakog vrha
    for i in range(3):
        nextEdge=subdiv.getEdge(currentEdge,0x13)
        point1x=int(subdiv.edgeOrg(currentEdge)[1][0])
        point1y=int(subdiv.edgeOrg(currentEdge)[1][1])
        points=np.concatenate((points,[(point1x,point1y)]),0)
        currentEdge=nextEdge
    
    ##Ako se neka točka nalazi van boundary-a, nemoj bojati trokut i vrati boolean False
    for point in points:
        if ((point[0] > boundarySize+mapSize or point[0] < boundarySize or point[1] > boundarySize+mapSize or point[1] < boundarySize)):
            return False
    cv2.fillConvexPoly(img,points,color)
    cv2.imshow("Window", img)


def clearAllColors(img):
    ##Stvara pravokutnik i ispunjava ga bijelom bojom
    cv2.rectangle(img,(0,0),(imgSize,imgSize),(255,255,255),-1)


def onMouse(event, x, y, flags, Data):
    if event==cv2.EVENT_LBUTTONDOWN:

        ##Brisanje prošlih obojanih trokuta
        clearAllColors(Data[1])
        drawTriangles(Data[0].getTriangleList(),Data[1])

        ##Ako se klikne van boundary-a, izađi iz funkcije
        if (x < boundarySize or x > boundarySize+mapSize or y < boundarySize or y > boundarySize+mapSize):
            return

        ##Dohvaćanje edge-a trokuta unutar koordinata mouse click-a
        currentEdge=Data[0].locate((x,y))[1]

        ##Popunjavanje odabranog trokuta, ako nije uspio, izlazi iz funkcije
        if(fillTriangle(currentEdge,Data[0],Data[1],(0,0,255))==False):
            return
        
        ##Popunjavanje susjednih trokuta
        for i in range(3):
            rotatedEdge=Data[0].rotateEdge(currentEdge,2)
            fillTriangle(rotatedEdge,Data[0],Data[1],(255,0,0))
            currentEdge=Data[0].getEdge(currentEdge,0x13)

        cv2.imshow("Window",Data[1])
        cv2.waitKey()


def main():

    img = np.full((imgSize, imgSize, 3), 255, dtype=np.uint8)

    subdiv = cv2.Subdiv2D((0,0,imgSize,imgSize))

    ##Insert boundary točke
    subdiv.insert((boundarySize,boundarySize))
    subdiv.insert((boundarySize,boundarySize + mapSize))
    subdiv.insert((boundarySize + mapSize,boundarySize))
    subdiv.insert((boundarySize + mapSize,boundarySize + mapSize))

    ##Insert random točke
    for i in range(nPts):
        subdiv.insert((random.randint(boundarySize,boundarySize+mapSize),random.randint(boundarySize,boundarySize+mapSize)))

    ##Crtanje svih trokuta
    drawTriangles(subdiv.getTriangleList(), img)

    ##Prikazivanje slike i definiranje mouse callback funkcije
    cv2.imshow("Window", img)

    cv2.setMouseCallback("Window",onMouse,[subdiv,img])

    cv2.waitKey()


if __name__=='__main__':
    main()

