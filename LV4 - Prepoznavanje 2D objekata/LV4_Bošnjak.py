import cv2
import numpy as np


def main():
    print("Odaberite sliku unošenjem broja između 1 i 3 za željeni objekt:")
    print("1 - Ampermetar")
    print("2 - Kalkulator")
    print("3 - Knjiga")
    odabir=int(input())
    #Učitavanje slika
    while(odabir>3 or odabir<1):
        print("Krivi unos, broj treba biti između 1 i 3")
        odabir=int(input())
    if(odabir==1):
        imageT0=cv2.imread("./LV/LV4/Ampermetar1.jpg")
        imageT2=cv2.imread("./LV/LV4/Ampermetar2.jpg")
    elif(odabir==2):
        imageT0=cv2.imread("./LV/LV4/Kalkulator1.jpg")
        imageT2=cv2.imread("./LV/LV4/Kalkulator2.jpg")
    elif(odabir==3):
        imageT0=cv2.imread("./LV/LV4/Knjiga1.jpg")
        imageT2=cv2.imread("./LV/LV4/Knjiga2.jpg")
    #Reshape-anje slike da bi stala na ekran
    if(imageT0.shape[0] != 480):     
        scale_percent = 50
        width = int(imageT0.shape[1] * scale_percent / 100)
        height = int(imageT0.shape[0] * scale_percent / 100)
        dim = (width, height)
        imageT0 = cv2.resize(imageT0, dim, interpolation = cv2.INTER_AREA)
        imageT2 = cv2.resize(imageT2, dim, interpolation = cv2.INTER_AREA)
    #Odabir ROI-a
    r = cv2.selectROI("Select the area", imageT0)
    #Odvajanje ROI-a
    ROI = imageT0[int(r[1]):int(r[1]+r[3]),
                            int(r[0]):int(r[0]+r[2])]
    #Konstruktor za sift
    sift = cv2.SIFT_create()
    #Pronalaženje keypoint-ova i deskriptora pomoću SIFT metode
    keypointsROI, descriptorsROI=sift.detectAndCompute(ROI, None)
    keypointsScene, descriptorsScene=sift.detectAndCompute(imageT2, None)
    #Prikaz svih slika
    cv2.imshow("ROI",ROI)
    cv2.waitKey()
    cv2.destroyAllWindows()
    keypoints_imageROI=cv2.drawKeypoints(ROI,keypointsROI,cv2.DRAW_MATCHES_FLAGS_DEFAULT)
    cv2.imshow("Keypoints",keypoints_imageROI)
    cv2.waitKey()
    cv2.destroyAllWindows()
    keypoints_imageScene=cv2.drawKeypoints(imageT2,keypointsScene,cv2.DRAW_MATCHES_FLAGS_DEFAULT)
    cv2.imshow("Keypoints_scene", keypoints_imageScene)
    cv2.waitKey()
    cv2.destroyAllWindows()
    #Konstruktor za brute force matcher
    bf=cv2.BFMatcher()
    #KNN matcher iz objekta brute force, za k=2 najbližih susjeda
    matches=bf.knnMatch(descriptorsROI,descriptorsScene,k=2)
    #Threshhold za odabir "dobrih" parova
    threshhold=0.75
    #Odabir "dobrih" parova, za svaki match
    good = []
    for m,n in matches:
        if m.distance < threshhold*n.distance:
            good.append([m])
    #Prikaz dobivenih parova
    matches_image = cv2.drawMatchesKnn(ROI,keypointsROI,imageT2,keypointsScene,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imshow("Matches",matches_image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    #Spremanje dobrih matcheva u listu kao posebni elementi, potrebno za m.queryIdx i m.trainIdx
    good = []
    for m,n in matches:
        if m.distance < threshhold*n.distance:
            good.append(m)
    MIN_MATCH_COUNT=5
    #Ako postoji barem 5 dobrih match-eva
    if len(good)>MIN_MATCH_COUNT:
        #Dohvaćanje koordinata keypoint-ova iz liste dobrih match-eva
        src_pts = np.float32([ keypointsROI[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ keypointsScene[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        #Pronalazak homografije RANSAC metodom, koja vraća matricu homografije M i samo inlier-e keypoint-ova
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,10.0)
        matchesMask = mask.ravel().tolist()
        h,w,d = ROI.shape
        #Određivanje koordinata pravokutnika oko ROI-a te transformacija tih točaka na sliku scene
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        imageT2 = cv2.polylines(imageT2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    else:
        print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
        matchesMask = None
    #Parametri za crtanje konačne slike, zajedno sa transformiranim pravokutnikom
    draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = None,
                   matchesMask = matchesMask,
                   flags = 2)
    Matches = cv2.drawMatches(ROI,keypointsROI,imageT2,keypointsScene,good,None,**draw_params)
    cv2.imshow("Matches", Matches)
    cv2.waitKey()
    cv2.destroyAllWindows()



if __name__=='__main__':
    main()