from PIL import Image, ImageOps, ImageFilter
import numpy as np




vertical_filter = np.array(
                [[-1,-2,-1], 
                [ 0, 0, 0], 
                [ 1, 2, 1]])
horizontal_filter = np.array(
                [[-1,0,1], 
                    [-2,0,2], 
                    [-1,0,1]])

path = r"C:\Users\sebas\OneDrive - Technische Hochschule Nürnberg Georg Simon Ohm\Desktop\TH-Nürnberg\Sem3\Sim\Geradenerkennung\450x450_blcksqr.png" #



img = Image.open(path)                  #Bild öffnen
img = img.convert('L')                  #In Graubild ändern
map = np.asarray(img)                   #Grauwerte als 2D-Array
map = map/255.0                         #Werte durch 255 teilen, sodass 1 größtmöglicher Wert ist


print(map)

width, height = img.size

#path = "C:/Users/hilde/source/repos/Sobel_1/sw_Quadrat-voll.jpg"
#path = "C:/Users/hilde/source/repos/Sobel_1/5x10_l-shape.png"






    


def main():
    

    Sobelfilter()
    #Houghtrans()
    print("sers")
 



def Sobelfilter():



    
    
    #print("width" + str(width))
    #print("heigth" + str(height))


    sobelArrvert = np.zeros([height, width])
    sobelArrhor = np.zeros([height, width])


    z=1

    for r in range(1, height-1):              #überprüfen welche zahl (vordere oder hintere die breite/höhe ist) -> muss ich bei 1 oder 3 starten?
        for c in range(1, width-1):
            localArr = map[r-1:r+2, c-1:c+2]  #Ränder weglassen, von r-1 bis r+1 laufen (Endwert nicht drin)
            z = z+1

            tempVal = 0                       # jetzt gehts -> tempVal musste da vorne hin
            for i in range(0,3):              #evtl schöner zusammen schreiben`?
                for j in range(0,3):          #dauert sehr lange zum rechnen -> evtl eine integrierte Methode zum verrechnen?
                    
                    tempVal = tempVal + (vertical_filter[i][j] * localArr[i][j])
            sobelArrvert[r,c] = tempVal

            tempVal = 0
            for i in range(0,3):
                for j in range(0,3):
                    
                    tempVal = tempVal + (horizontal_filter[i][j] * localArr[i][j])
            sobelArrhor[r,c] = tempVal



    print(sobelArrhor)
    print(sobelArrvert)


    sobelArr = np.hypot(sobelArrvert, sobelArrhor)      #Hypothenuse -> Pythagoras ? zu vereinfacht?
        

    maxi = sobelArr.max()
    print(maxi)
    sobelArr=sobelArr / maxi                 #damit alle Werte unter 1 normiert werden -> sodass ich sie später wieder hochskalieren kann
    sobelArr=sobelArr*255
    print(sobelArr)


    sobelArrvert = abs(sobelArrvert)
    maxivert = sobelArrvert.max()
    sobelArrvert = sobelArrvert/maxivert
    sobelArrvert = sobelArrvert * 255
    Image.fromarray(sobelArrvert).show()


    sobelArrhor = abs(sobelArrhor)
    maxihor = sobelArrhor.max()
    sobelArrhor = sobelArrhor/maxihor
    sobelArrhor = sobelArrhor * 255
    Image.fromarray(sobelArrhor).show()




    endimage = Image.fromarray(sobelArr)
    endimage.show()

    Houghtrans(sobelArr)


def Houghtrans(Arr):                     #xcos(phi) + ysin(phi) = d
    inkr_phi = 10                     
    #phi = 360/inkr_phi

    d_max = np.hypot(height,width)     #x-Achse: d  |  y-Achse: phi
    inkr_d = int(np.ceil(d_max))            #unnötig aufzurunden? eig kann unten keine kante sein

    schwell =  150                      #!!!! eigentlich auf die nicht normierte Map zugreifen -> problem mit global variable


    hRoom = np.zeros((int(360/10),inkr_d))

    for y in range(1, height-1):              #Ränder werden ausgelassen -> enthalten "eh" keine kanten
        for x in range(1, width-1):
            if(Arr[y,x] >= schwell):

                phi=0
                s = 0                               #evtl Zähler als Math. Gleichung für den Zugriff auf 2d array umschreiben
                while(phi != 360.0):           
                    d = int( np.round( x*np.cos(phi) + y*np.sin(phi) ) )

                    hRoom[s][d]=  hRoom[s][d] + 1                   #Matrix-Indexer fragen?
                    s = s + 1

                    phi = phi+(360.0/inkr_phi)


    
    hRoom = hRoom/hRoom.max()
    hRoom = hRoom*255
    Image.fromarray(hRoom).show()

















if __name__ == '__main__':
     main()










#print(map)


#print(sobelArr)



#for r in range(3, height-1):              #überprüfen welche zahl (vordere oder hintere die breite/höhe ist) -> muss ich bei 2 oder 3 starten?
#    for c in range(3, width-1):

#        for i in range(0,2)
#        tempval
#        pxval







#px = img.load()





#for row in range(3, i-2):
#    for col in range(3, j-2):
#        local_pixels = img[row-1:row+2, col-1:col+2, 0]
#        transf_pixels = vertical_filter * local_pixels
#        vertival_score = (transf_pixels.sum()+4)/8
#        vertical_edges_img[row, col] = [vertical_score]*3