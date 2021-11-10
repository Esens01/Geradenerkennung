from PIL import Image, ImageOps, ImageFilter
import numpy as np



vertical_filter = np.array(
                [[-1,-2,-1], 
                [ 0, 0, 0], 
                [ 1, 2, 1]])
horizontal_filter = np.array(
                [[-1, 0, 1], 
                 [-2, 0, 2], 
                 [-1, 0, 1]])


#path = "C:/Users/hilde/source/repos/Sobel_1/5x10_l-shape.png"
#path = r"C:\Users\sebas\OneDrive - Technische Hochschule Nürnberg Georg Simon Ohm\Desktop\TH-Nürnberg\Sem3\Sim\Geradenerkennung\100x100_blacksq.png" 
path = r"C:\Users\Sebastian\OneDrive - Technische Hochschule Nürnberg Georg Simon Ohm\Desktop\TH-Nürnberg\Sem3\Sim\Geradenerkennung\rgb.png"
#path = "C:/Users/hilde/source/repos/Sobel_1/sw_Quadrat-voll.jpg"
#path = "C:/Users/hilde/source/repos/Sobel_1/Ohm.png"



img = Image.open(path)                  #Bild öffnen
img = img.convert('L')                  #In Graubild ändern
map = np.asarray(img)                   #Grauwerte als 2D-Array
map = map/255.0                         #Werte durch 255 teilen, sodass 1 größtmöglicher Wert ist (zwischen 0(w) und 1(sw))


print(map)

width, height = img.size


    


def main():
    

    Sobelfilter()
    #Houghtrans()
    #print("sers")
 


def Sobelfilter():

    #print("width" + str(width))
    #print("heigth" + str(height))


    sobelArr_vert = np.zeros([height, width])
    sobelArr_hor = np.zeros([height, width])



    for r in range(1, height-1):              #überprüfen welche Zahl (vordere oder hintere die breite/höhe ist) -> muss ich bei 1 oder 3 starten?
        for c in range(1, width-1):           #r:Zeilen, c:Spalten          #evtl Rand mit anderem Filter mit einbringen
            localArr = map[r-1:r+2, c-1:c+2]  #Ränder weglassen, von r-1 bis r+1 laufen (Endwert nicht drin)

            tempVal = 0                       #tempVal muss hier stehen
            for i in range(0,3):              #evtl schöner zusammen schreiben?  0 li v akt Zelle?
                for j in range(0,3):          #dauert sehr lange zum rechnen -> evtl eine integrierte Methode zum verrechnen?
                    
                    tempVal = tempVal + (vertical_filter[i][j] * localArr[i][j])   #hier werden beide Sobel-F. angewendet
            sobelArr_vert[r,c] = tempVal

            tempVal = 0
            for i in range(0,3):
                for j in range(0,3):
                    
                    tempVal = tempVal + (horizontal_filter[i][j] * localArr[i][j])
            sobelArr_hor[r,c] = tempVal



    print(sobelArr_hor)
    print(sobelArr_vert)


    sobelArr = np.hypot(sobelArr_vert, sobelArr_hor)      #Hypothenuse!!!!! brauchen wir ned? -> Pythagoras, zu vereinfacht?  #python shorct punktweise op  hypot unnötig
        

    maxi = sobelArr.max()
    print(maxi)
    sobelArr=sobelArr / maxi                 #damit alle Werte unter 1 normiert werden -> sodass ich sie später wieder hochskalieren kann
    sobelArr=sobelArr*255
    print(sobelArr)



    
    # sobelArr_vert = abs(sobelArr_vert)
    # maxivert = sobelArr_vert.max()
    # sobelArr_vert = sobelArr_vert/maxivert
    # sobelArr_vert = sobelArr_vert * 255
    # Image.fromarray(sobelArr_vert).show()


    # sobelArr_hor = abs(sobelArr_hor)
    # maxihor = sobelArr_hor.max()
    # sobelArr_hor = sobelArr_hor/maxihor
    # sobelArr_hor = sobelArr_hor * 255
    # Image.fromarray(sobelArr_hor).show()


    endimage = Image.fromarray(sobelArr)
    endimage.show()

    Houghtrans(sobelArr)


def Houghtrans(Arr):                     #xcos(phi) + ysin(phi) = d
    inkr_phi = 400            
    inkr_phi_distance = 180/inkr_phi
    phi_Vektor= np.zeros((inkr_phi))

    inkr_d = 500
    #d_Vektor = 

    d_max = np.hypot(height,width)       #x-Achse: d  |  y-Achse: phi
    inkr_distance = d_max/inkr_d
    #inkr_d = int(np.ceil(d_max))         #unnötig aufzurunden? eig kann unten keine kante sein

    schwell =  150                       #!!!! eigentlich auf die nicht normierte Map zugreifen -> problem mit global variable


    hRoom = np.zeros((inkr_phi,inkr_d))    #nicht inkr_phi statt 10?

    for y in range(1, height-1):              #Ränder werden ausgelassen -> enthalten "eh" keine kanten
        for x in range(1, width-1):
            if(Arr[y,x] >= schwell):

                phi=0
                s = 0                         #evtl Zähler als Math. Gleichung für den Zugriff auf 2d array umschreiben
                
                while(s!=inkr_phi-1):          #Aufgrund der kleinen Abstände ergeben sich Rundungsfehler -> der exakte Wert 360 wird nie erreicht 

                    d = int( np.round( (x*np.cos(phi) + y*np.sin(phi)) / inkr_distance ) )
                    

                    hRoom[s][d]=  hRoom[s][d] + 1               #Matrix-Indexer fragen?
                    
                    phi_Vektor[s] = phi                         #???

                    phi = phi+inkr_phi_distance                 #phis und d in Vektoren übertragen

                    s = s + 1


    
    hRoom = hRoom/hRoom.max()
    hRoom = hRoom*255

    Image.fromarray(hRoom).show()
    RedLine(hRoom, inkr_d, inkr_phi)


def RedLine(hRoom, inkr_d, inkr_phi):
    for s in range(0, inkr_phi-1):
        for d in range(0,inkr_d-1):
            if(hRoom[s][d] >= 150):
                redArr = np.zeros((height,width))           #hier irgendwie Linien eintragen.



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









#    ALTER CODE   *

#square1 = img(sw_Quadrat-voll.jpg)

#from IPython.display import Image
#Image('sample.jpeg')

#pygame.draw.rect(screen, black, [10, 20, 100, 100], 1)

#square_1 = pygame.image.load("C:/Users/hilde/source/repos/Sobel_1/sw_Quadrat-voll.jpg")

#path = "C:/Users/hilde/source/repos/Sobel_1/sw_Quadrat-voll.jpg"
#path = "C:/Users/hilde/source/repos/Sobel_1/5x10_l-shape.png"
#path = "C:/Users/hilde/source/repos/Sobel_1/5x10_col.png"

#img = Image.open(path)
#img = img.convert('L')

#map = np.array(img)     #darf man das mit ner externen bib machen?
#print(map)



#width, height = img.size
#print("width" + str(width))
#print("heigth" + str(height))

#sobelArr = np.zeros([height, width])

#z=1

#for r in range(1, height-1):              #überprüfen welche zahl (vordere oder hintere die breite/höhe ist) -> muss ich bei 1 oder 3 starten?
#    for c in range(1, width-1):
#        localArr = map[r-1:r+2, c-1:c+2]  #Ränder weglassen, von r-1 bis r+1 laufen (Endwert nicht drin)
#        #print("cluster"+str(z))
#        z = z+1

#        #tempVal = 0
#        #tempVal = tempVal + (vertical_filter * localArr)

#        for i in range(0,3):
#            for j in range(0,3):
#                tempVal = 0
#                tempVal = tempVal + (vertical_filter[i][j] * localArr[i][j])

#        sobelArr[r][c] = tempVal

#    #print(localArr)
    

#print(map)
#print(sobelArr)


##for r in range(3, height-1):              #überprüfen welche zahl (vordere oder hintere die breite/höhe ist) -> muss ich bei 2 oder 3 starten?
##    for c in range(3, width-1):

##        for i in range(0,2)
##        tempval
##        pxval


##img.show() 

#px = img.load()

##img = ImageOps.grayscale(img)
##img.show() 

##len(img[1][1])

##A = array(img)


#fertig=img.filter(ImageFilter.FIND_EDGES)


#fertig.show()


#greyval = img.getchannel(0)
#print(img[4,7])

#list = []

#for i in range(img.height):
#    for j in range(img.width):
#        img.getpixel


#for row in range(3, i-2):
#    for col in range(3, j-2):
#        local_pixels = img[row-1:row+2, col-1:col+2, 0]
#        transf_pixels = vertical_filter * local_pixels
#        vertival_score = (transf_pixels.sum()+4)/8
#        vertical_edges_img[row, col] = [vertical_score]*3




