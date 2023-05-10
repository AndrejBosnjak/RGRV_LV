import cv2
import numpy as np
import json
import math

points=np.zeros((0,2))
n_clicks=0

def onMouse(event, x, y, flags, Data):
    if event==cv2.EVENT_LBUTTONDOWN:
        global points
        global n_clicks
        points=np.concatenate((points,[(x,y)]),0)
        n_clicks+=1
        if(n_clicks>=4):
            cv2.destroyAllWindows()


def main():
    f=open("./LV/LV3/camera_params.json")
    dict=json.load(f)

    #Učitavanje dobivenih parametara kamere
    camera_matrix=np.array(dict["camera_matrix"])
    dist_coeffs=np.array(dict["dist_coeffs"])

    #Učitavanje slike
    image=cv2.imread("./LV/LV3/image.jpg")
    image=cv2.undistort(image,camera_matrix,dist_coeffs)

    print("Na slici označiti 4 točke, redom gore lijevo, gore desno, dolje lijevo i dolje denso")
    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", onMouse)
    cv2.waitKey()

    #Nakon označavanja 4 točke interesa, slika se cropp-a   
    roi = image[int(points[0][1]):int(points[3][1]), int(points[0][0]):int(points[3][0])]

    edges=cv2.Canny(roi,100,200)

    #Detektiranje linija
    line=cv2.HoughLines(edges, 1, np.pi/180,150)
    detectedLine=np.full(roi.shape, 0, dtype=np.uint8)

    if line is not None:
        rho=line[0][0][0]
        theta=line[0][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv2.line(detectedLine, pt1, pt2, (255,255,255), 3)
    else:
        print("Nisu detektirane linije")
        return

    cv2.imshow("ROI", roi)
    cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.imshow("Edges", edges)
    cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.imshow("Detected line", detectedLine)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
    #Označavanje vrhova pravokutnika koji predstavlja ROI
    imagePoints=np.zeros((0,2))
    x1=points[0][0]
    y1=points[0][1]
    x2=points[1][0]
    y2=points[1][1]
    x3=points[2][0]
    y3=points[2][1]
    x4=points[3][0]
    y4=points[3][1]

    imagePoints=np.concatenate((imagePoints,[(0,0)]),0)
    imagePoints=np.concatenate((imagePoints,[(x2-x1,0)]),0)
    imagePoints=np.concatenate((imagePoints,[(0,y3-y1)]),0)
    imagePoints=np.concatenate((imagePoints,[(x4-x1,y4-y1)]),0)

    #Udaljenosti ROI točaka na mm papiru
    objectPoints=np.array([ [0.0,0.0,0.0],
                            [130.0,0.0,0.0],
                            [0.0,110.0,0.0],
                            [130.0,110.0,0.0]])
    
    #Dohvaćanje rotacijske matrice i translacijskog vektora
    output=cv2.solvePnP(objectPoints,imagePoints,camera_matrix,dist_coeffs)
    R=cv2.Rodrigues(output[1])
    R=R[0]
    t=output[2]

    #Jednadžbe iz priloga
    A=camera_matrix@R
    B=camera_matrix@t
    lambdaX=A[0][0]*math.cos(theta)+A[1][0]*math.sin(theta)-rho*A[2][0]
    lambdaY=A[0][1]*math.cos(theta)+A[1][1]*math.sin(theta)-rho*A[2][1]
    lambdaP=B[2]*rho-B[0]*math.cos(theta)-B[1]*math.sin(theta)
    theta_real=math.atan2(lambdaY,lambdaX)
    rho_real=(lambdaP / (math.sqrt(lambdaX*lambdaX+lambdaY*lambdaY)))

    #Ispisivanje dobivenih vrijednosti
    paper_rho=55
    paper_theta=math.acos(50/90)
    print("Stvarni kut pravca na milimetarskom papiru: " + str(paper_theta) + " [rad]")
    print("Stvarna udaljenost pravca od ishodišta na milimetarskom papiru: " + str(paper_rho) + " [mm]")
    print("Izračunati kut: " + str(theta_real) + " [rad]")
    print("Izračunata udaljenost: " + str(rho_real[0]) + " [mm]")
    print("Podudaranje kuta: " + str(theta_real/paper_theta * 100) + " %")
    print("Podudaranje udaljenosti: " + str(rho_real[0]/paper_rho * 100) + " %")

if __name__=='__main__':
    main()
