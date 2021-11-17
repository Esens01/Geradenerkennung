from PIL import Image, ImageOps, ImageFilter, ImageDraw
import PIL
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
path = r"C:\Users\Sebastian\OneDrive - Technische Hochschule Nürnberg Georg Simon Ohm\Desktop\TH-Nürnberg\Sem3\Sim\Geradenerkennung\100x100_blacktri.png"
#path = "C:/Users/hilde/source/repos/Sobel_1/sw_Quadrat-voll.jpg"
#path = "C:/Users/hilde/source/repos/Sobel_1/Ohm.png"



colImg = Image.open(path)                  #Bild öffnen
img = colImg.convert('L')                  #In Graubild ändern
map = np.asarray(img)                   #Grauwerte als 2D-Array
map = map/255.0                         #Werte durch 255 teilen, sodass 1 größtmöglicher Wert ist (zwischen 0(w) und 1(sw))


#print(map)

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
            localArr = map[r-1:r+2, c-1:c+2]  #Ränder weglassen, von r-1 bis r+1 laufen (Endwert nicht drin) -> indexer so richtig?

            tempVal = 0                       #tempVal muss hier stehen
            for i in range(0,3):              #evtl schöner zusammen schreiben?  0 li v akt Zelle?
                for j in range(0,3):          #dauert sehr lange zum rechnen -> evtl eine integrierte Methode zum verrechnen?
                    
                    tempVal = tempVal + (vertical_filter[i][j] * localArr[i][j])   #hier werden beide Sobel-F. angewendet
            sobelArr_vert[r][c] = tempVal

            tempVal = 0
            for i in range(0,3):
                for j in range(0,3):
                    
                    tempVal = tempVal + (horizontal_filter[i][j] * localArr[i][j])
            sobelArr_hor[r][c] = tempVal



    #print(sobelArr_hor)        #zwischenzeitliches Sobelarray ausgeben
    #print(sobelArr_vert)


    sobelArr = np.hypot(sobelArr_vert, sobelArr_hor)      #Hypothenuse!!!!! brauchen wir ned? -> Pythagoras, zu vereinfacht?  #python shorct punktweise op  hypot unnötig
        

    maxi = sobelArr.max()
#    print(maxi)
    sobelArr=sobelArr / maxi                 #damit alle Werte unter 1 normiert werden -> sodass ich sie später wieder hochskalieren kann
    sobelArr=sobelArr*255
#    print(sobelArr)



    
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
    inkr_phi = 1200         
    inkr_phi_distance = (180/inkr_phi) 
    phi_Vektor= np.zeros((inkr_phi))
    phi = -90

    for i in range(inkr_phi):
        phi_Vektor[i] = phi * (np.pi/180)
        phi = phi + inkr_phi_distance
    
    #phi_testvekt = np.linspace(0,  180/inkr_phi, num = inkr_phi)

    inkr_d = 600
    d_max = np.hypot(height,width)       #x-Achse: d  |  y-Achse: phi  ???muss hier height -1 und width -1 gewählt werden?
    inkr_distance = d_max/ inkr_d


    

    schwell =  150                       #!!!! eigentlich auf die nicht normierte Map zugreifen -> problem mit global variable


    hRoom = np.zeros((inkr_phi, inkr_d * 2 ))    #nicht inkr_phi statt 10?  #doppelte Länge, sodass alle negativen und positiven d werte erfasst werden 

    for y in range(1, height-1):              #Ränder werden ausgelassen -> enthalten "eh" keine kanten
        for x in range(1, width-1):
            if(Arr[y][x] >= schwell):

                # phi=-90
                s = 0                         #evtl Zähler als Math. Gleichung für den Zugriff auf 2d array umschreiben
                
                while(s!=inkr_phi-1):          #Aufgrund der kleinen Abstände ergeben sich Rundungsfehler -> der exakte Wert 360 wird nie erreicht 
                    
                    phi = phi_Vektor[s]
                    
                    #d =x*np.cos(phi * (np.pi/180) ) + y*np.sin( phi  * (np.pi/180)  ) #noch vorher ohne phi-vektor
                    d =x*np.cos(phi ) + y*np.sin( phi  )

                    if(d == d_max):
                        print()

                    d=int(np.round(  d/inkr_distance  +  inkr_d   ))            #x-Verschiebung mit +inkr_d
                    
                    #d = int( np.round( (x*np.cos(phi) + y*np.sin(phi)) / inkr_distance ) )
                    

                    hRoom[s][d]=  hRoom[s][d] + 1               #das + wird benötigt um den x-0 punkt auf die mitte der x-Achse des HRaums zu verschieben             #Matrix-Indexer fragen? 


                    # phi = phi+inkr_phi_distance                 #phis und d in Vektoren übertragen

                    s = s + 1



    
    hRoom = hRoom / hRoom.max()
    hRoom = hRoom*255
    

    #testcode
    # for y in range(0, inkr_phi-1):              #Ränder werden ausgelassen -> enthalten "eh" keine kanten
    #     for x in range(0, inkr_d-1):
    #         if(hRoom[y][x] > 0 ):
    #             hRoom[y][x] = 255

    

    #testcode
    #hRoom = np.swapaxes(hRoom,0,1)              #y-Achse d   |   x-Achse phi


    himage = Image.fromarray(hRoom)
    himage.show()
    himage = himage.convert("RGB")
    himage.save(r"C:\Users\Sebastian\OneDrive - Technische Hochschule Nürnberg Georg Simon Ohm\Desktop\TH-Nürnberg\Sem3\Sim\Geradenerkennung\hRoom.jpg")




    #find local maxima


    peaks = []
    realPeaks = []

    for phi in range(0,inkr_phi):
        for d in range(0,(inkr_d*2)):
            if(hRoom[phi][d] >= 65):
                peakval = hRoom[phi][d]
                peaks = peaks + [[phi,d,peakval]]
                



    suchradius = 6
    localmax = [-1,-1]
    localmaxVal = -1
    for r in range(0,len(peaks)):

        if(peaks[r] ==[-1,-1,-1] ):
            continue

        phi,d,val = peaks[r]
        #peaks[r] = [-1,-1,-1]



        localmax = [phi,d]
        localmaxVal = val

        

        for t in range(0,len(peaks)):                       #hier die Funktion, bei der direkt zum nächsthöheren Wert als Arbeitspunkt gesprungen wird.
            phitemp,dtemp,valtemp = peaks[t]

            # if(phitemp == -1 and dtemp == -1 and valtemp == -1):
            #     continue

            
            distance = np.sqrt( (dtemp-localmax[1])**2 + (phitemp-localmax[0])**2 )

            if(distance < suchradius and valtemp >= localmaxVal):
                localmax = [phitemp,dtemp]
                localmaxVal = valtemp 
                #peaks[t] = [-1,-1,-1]
            
        if(localmax in realPeaks):
            pass
        else:
            realPeaks = realPeaks + [localmax]

    print("ende")
    showLines(realPeaks, inkr_d, inkr_distance, d_max, phi_Vektor, inkr_phi)


def showLines(peakArr, inkr_d, inkr_distance, d_max, phi_Vektor, inkr_phi):

    origImg = Image.new("RGB", (inkr_d*2,inkr_phi))
    origImg = Image.new("RGB", (width,height))
    redImg = ImageDraw.Draw(colImg)

    for phitemp,dtemp in peakArr:               #

        x0 = (dtemp-inkr_d)*inkr_distance  * np.cos(phi_Vektor[phitemp])
        y0 = (dtemp-inkr_d)*inkr_distance  * np.sin(phi_Vektor[phitemp])


        x1 = np.round( x0 + d_max*np.sin(phi_Vektor[phitemp]))
        y1 = np.round( y0 + d_max*np.cos(phi_Vektor[phitemp]))

        x2 = np.round( x0 - d_max*np.sin(phi_Vektor[phitemp]))
        y2 = np.round( y0 - d_max*np.cos(phi_Vektor[phitemp]))



        


        
        redImg.line(((x1,y1),(x2,y2)), fill="red", width = 4 )
        #origImg.show()

    #colImg.paste(origImg , (0,0))
    colImg.show()

    


    # for s in range(0, inkr_phi-1):              #s = phi    |  d =
    #     for d in range(0,(inkr_d*2)-1):             # bei 0 starten oder bei 1

    #         if(hRoom[s][d] >= 40 ):

    #             dere = hRoom[s][d]

                

    #             i = 0
    #             tempval = 0
    #             dir = 0


    #             stemp = s
    #             dtemp = d

    #             while(dir != 4):        #hört erst auf die lokale Maximumsmatrix zu verändern, wenn das Maximum in der Mitte der Matrix ist.
                    
                    

    #                 if(stemp == 0 or stemp == (len(hRoom[0])-1) or dtemp == 0 or dtemp == (len(hRoom[1])-1)):

    #                     localmax = np.zeros((3,3))

    #                     if(stemp==0 and dtemp == 0):                                                # links oben
    #                         localmax[1:3,1:3] = hRoom[stemp:stemp+2, dtemp:dtemp+2]

    #                     elif(stemp==0 and dtemp == (len(hRoom[1])-1)):                              # rechts oben
    #                         localmax[1:3,0:2] = hRoom[stemp:stemp+2, dtemp-1:dtemp+1]                        

    #                     elif(dtemp==0 and stemp == (len(hRoom[0])-1) ):                             #links unten
    #                         localmax[0:2,1:3] = hRoom[stemp-1:stemp+1, dtemp:dtemp+2 ]                        

    #                     elif(stemp == (len(hRoom[0])-1) and dtemp == (len(hRoom[1])-1)):            #rechts unten
    #                         localmax[0:2, 0:2] = hRoom[stemp-1:stemp+1, dtemp-1:dtemp+1]

    #                     elif(dtemp == 0):
    #                         localmax[0:3,1:3] = hRoom[stemp-1:stemp+2, dtemp:dtemp+2]       #links

    #                     elif(stemp==0):
    #                         localmax[1:3, 0:3] = hRoom[stemp:stemp+2, dtemp-1:dtemp+2]      #oben
                            
    #                     elif(stemp == (len(hRoom[0])-1)):
    #                         localmax[0:2,0:3] = hRoom[stemp-1:stemp+1, dtemp-1:dtemp+2]     #unten

    #                     elif(dtemp == (len(hRoom[1])-1)):
    #                         localmax[0:3,0:2] = hRoom[stemp-1:stemp+2, dtemp-1:dtemp+1]     #rechts

                        

    #                 else:

    #                     localmax = hRoom[stemp-1:stemp+2, dtemp-1:dtemp+2]

    #                 for r in range(0,len(localmax[0])):
    #                     for c in range (0, len(localmax[1])):

    #                         if(tempval == 0 or localmax[r,c] > tempval ):
    #                             tempval = localmax[r,c]
    #                             dir = i

    #                         i =i + 1

    #                 i = 0
    #                 tempval = 0
    #                 if(dir == 0):
    #                     stemp += -1
    #                     dtemp += -1

    #                 elif(dir == 1):
    #                     stemp += -1

    #                 elif (dir == 2):
    #                     stemp += -1
    #                     dtemp += 1

    #                 elif ( dir == 3):
    #                     dtemp += -1

    #                 elif (dir == 5):
    #                     dtemp += 1

    #                 elif (dir == 6):
    #                     stemp += 1
    #                     dtemp += -1

    #                 elif (dir == 7):
    #                     stemp += 1

    #                 elif (dir == 8):
    #                     stemp += 1
    #                     dtemp += 1

                

    #             if( (len(peaks)==0) or not ([stemp,dtemp] in peaks) ):

    #                 breakstate = False
    #                 for yprev,xprev in peaks:
                        
    #                     vectY = yprev - stemp
    #                     vectX =xprev - dtemp
    #                     if( np.hypot(vectY,vectX) < (inkr_phi/10) ):
    #                         breakstate = True

    #                 if(breakstate):
    #                     break
    #                 peaks = peaks + [[stemp,dtemp]]






 
            
    #print("swew")

                

                


                

                    




                

                        








   
    

    # for s in range(1, inkr_phi-1):              #s = phi    |  d =
    #     for d in range(0,inkr_d-1):           

    #         if(hRoom[s][d] >= 125):


    #             x0 = (d-inkr_d)*inkr_distance  * np.cos(phi_Vektor[s])
    #             y0 = (d-inkr_d)*inkr_distance  * np.sin(phi_Vektor[s])


    #             x1 = np.round( x0 + d_max*np.sin(phi_Vektor[s]))
    #             y1 = np.round( y0 + d_max*np.cos(phi_Vektor[s]))

    #             x2 = np.round( x0 - d_max*np.sin(phi_Vektor[s]))
    #             y2 = np.round( y0 - d_max*np.cos(phi_Vektor[s]))



    #             origImg = Image.new("RGB", (inkr_d*2,inkr_phi))
    #             origImg = Image.new("RGB", (width,height))


    #             redImg = ImageDraw.Draw(origImg)
    #             redImg.line(((x1,y1),(x2,y2)), fill="red", width = 4 )
    #             origImg.show()












    



if __name__ == '__main__':
     main()








