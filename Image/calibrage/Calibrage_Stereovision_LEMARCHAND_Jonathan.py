import numpy as np
import cv2
import matplotlib.pyplot as plt


def calibrage(matrice_reel, matrice_image):
    '''
    Calibrage d'une caméra
    Paramètres :
        matrice_reel : matrice 3*24 contenant les coordonnées réels (x,y,z)
        matrice_image : matrice 2*24 contenant les coordonnées du pointage (u,v)

    Retourne : 
        Une matrice 4*4, qui est la matrice de calibrage
    '''
    # GENERER LA MATRICE A
    A=np.zeros((2*len(matrice_reel), 12))

    for i in range(int(len(matrice_reel))):
        #Lignes paires
        A[i*2][0]=matrice_reel[i][0] #x
        A[i*2][1]=matrice_reel[i][1] #y
        A[i*2][2]=matrice_reel[i][2] #z
        A[i*2][3]=1

        A[i*2][8]=(-1*matrice_image[i][0]*matrice_reel[i][0])
        A[i*2][9]=(-1*matrice_image[i][0]*matrice_reel[i][1])
        A[i*2][10]=(-1*matrice_image[i][0]*matrice_reel[i][2])
        A[i*2][11]=(-1*matrice_image[i][0])

        #Lignes impaires
        A[i*2+1][4]=matrice_reel[i][0]
        A[i*2+1][5]=matrice_reel[i][1]
        A[i*2+1][6]=matrice_reel[i][2]
        A[i*2+1][7]=1

        A[i*2+1][8]=(-1*matrice_image[i][1]*matrice_reel[i][0])
        A[i*2+1][9]=(-1*matrice_image[i][1]*matrice_reel[i][1])
        A[i*2+1][10]=(-1*matrice_image[i][1]*matrice_reel[i][2])
        A[i*2+1][11]=(-1*matrice_image[i][1])

    # B=transposer(A)*A
    B=np.dot(np.transpose(A) ,A)

    # Calculer les valeurs et vecteurs propres de B
    w, v = np.linalg.eig(B)

    # Trouver l'indice k de la plus petite valeur propre non nulle de B
    k = np.argmin(np.abs(w[np.nonzero(w)]))

    # Récupérer le vecteur propre correspondant à l'indice k
    M = v[:, k]

    return M



def test_calibrage(M, point):
    '''
    Fonction de test du calibrage
    Paramètres : 
        M : matrice de calibrage
        point : un point 3D

    Affiche : Le point 2D de l'image correspondant au point 3D donnée en entrée 
    '''
    # Nuérateur de U
    U_num = point[0]*M[0] + point[1]*M[1] + point[2]*M[2] + M[3]
    # Numérateur de V
    V_num = point[0]*M[4] + point[1]*M[5] + point[2]*M[6] + M[7]
    # Dénominateur (commun à U et V)
    den = point[0]*M[8] + point[1]*M[9] + point[2]*M[10] + M[11]
    
    # Calcul de u et v
    Uf=U_num / den
    Vf=V_num / den

    print("Caibrage :")
    print("Uf = ", Uf)
    print("Vf = ", Vf)
    print()


def vecteur_propre(M):
    '''
    Vecteur propre
    Paramètre : 
        M : matrice de calibrage
    Affiche :
        Le vecteur propre de l'image
    Retourne :
        Le vecteur propre de l'image
    '''
    # Calcul de U0
    U0 = (M[0]*M[8] + M[1]*M[9] + M[2]*M[10]) / (M[8]**2 + M[9]**2 + M[10]**2)
    # Calcul de V0
    V0 = (M[4]*M[8] + M[5]*M[9] + M[6]*M[10]) / (M[8]**2 + M[9]**2 + M[10]**2)

    print("Vecteur propre :")
    print("U0 = ", U0)
    print( "V0 = ", V0)
    print()
    return U0, V0


def calcul_pose(M, U0, V0):
    '''
    Calcul de la pose
    Paramètres :
        M : matrice de calibrage
        U0, V0 : Le vecteur propre de l'image
    Affiche : La position 3D de la pose
    '''
    print("Pose :")
    Lambda=(1)/(np.sqrt(M[8]**2 + M[9]**2 + M[10]**2))

    tz=Lambda*M[11]

    tmp1=(M[0]**2 + M[1]**2 + M[2]**2)/(M[8]**2 + M[9]**2 + M[10]**2)
    tmp2=((M[0]*M[8] + M[1]*M[9] + M[2]*M[10]) / (M[8]**2 + M[9]**2 + M[10]**2))**2
    au=1*np.sqrt(tmp1 - tmp2)
    tx=(Lambda*M[3] - (-U0)*tz) / au
    print("tx = ", tx)

    tmp3=(M[4]**2 + M[5]**2 + M[6]**2)/(M[8]**2 + M[9]**2 + M[10]**2)
    tmp4=((M[4]*M[8] + M[5]*M[9] + M[6]*M[10]) / (M[8]**2 + M[9]**2 + M[10]**2))**2
    av=1*np.sqrt(tmp3 - tmp4)
    ty=(Lambda*M[7] - V0*tz) / av
    print("ty = ", ty)

    print("tz = ", tz)
    print()



def stereoVision(M1, M2, u1, v1, u2, v2):
    '''
    StéreoVision
    Paramètres :
        M1 : Matrice de calibrage de la 1ère image
        M2 : Matrice de calibrage de la 2ème image
        u1, v1 : Points 2D de la première image
        u2, v2 : Points 2D de la seconde image (correspondant au point (u1,v1))
    Affiche :
        Le vecteur x,y,z qui correspond a la position 3D du point (u1,v1) de l'image 1 et (u2,v2) de l'image 2
    '''
    A=np.zeros(4)
    B=np.zeros(4)
    C=np.zeros(4)
    D=np.zeros(4)
    for i in range(4):
        A[i]=M1[i] - u1*M1[8+i]
        B[i]=M1[4+i] - v1*M1[8+i]
        C[i]=M2[i] - u2*M2[8+i]
        D[i]=M2[4+i] - v2*M2[8+i]
    
    E=np.array([[A[0], A[1], A[2]],[B[0], B[1], B[2]],[C[0], C[1], C[2]],[D[0], D[1], D[2]]])
    Vec4=np.array([[-A[3]],[-B[3]],[-C[3]],[-D[3]]])

    E_plus = np.linalg.pinv(E) #pseudo inverse

    xyz = np.dot(E_plus, Vec4)

    print("Stereo-vision :")

    print("x = ", xyz[0][0])
    print("y = ", xyz[1][0])
    print("z = ", xyz[2][0])
    
    print()



def droite_epipolaire(image1, image2, u1, v1, chemin_image1, chemin_image2):
    '''
    Droite épipolaire
    Paramètres :
        image1 : matrice 2*24 contenant les coordonnées du pointage (u,v) de la 1ère image
        image2 : matrice 2*24 contenant les coordonnées du pointage (u,v) de la 2ème image
        u1,v1 : le point de la 1ère image par lequel passera la droite épipolaire sur la 2ème image
    Affiche :
        L'image 1 et le point (u1,v1)
        L'image 2 et la droite épipolaire
    '''
    # Charger l'image1
    img1 = cv2.imread(chemin_image1)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)  # Convertir l'image de BGR à RGB pour Matplotlib
    
    # Tracer une croix sur le point (u1,v1) (pour vérifier le bon fonctionnement de la droite épipolaire)
    cv2.line(img1, (v1-50, u1-50), (v1+50, u1+50), (0, 0, 255), 8)
    cv2.line(img1, (v1-50, u1+50), (v1+50, u1-50), (0, 0, 255), 8)

    # Calculer G
    G=np.zeros((24,9))
    for i in range(24):
        G[i] = np.array([image1[i][0]*image2[i][0], image1[i][0]*image2[i][1], image1[i][0], \
                          image1[i][1]*image2[i][0], image1[i][1]*image2[i][1], image1[i][1], \
                            image2[i][0], image2[i][1], 1])

    # H=transposer(G)*G
    H=np.dot(np.transpose(G) ,G)

    # Calculer les valeurs et vecteurs propres de H
    w, v = np.linalg.eig(H)

    # Trouver l'indice k de la plus petite valeur propre non nulle de B
    k = np.argmin(np.abs(w[np.nonzero(w)]))

    # Récupérer le vecteur propre correspondant à l'indice k
    F = v[:, k]

    #(u1. f11+v1.f21+f31)
    A = u1*F[0] + v1*F[3] + F[6]
    #(u1. f12+v1.f22+f32)
    B = u1*F[1] + v1*F[4] + F[7]
    #u1.f13+v1.f23+f33
    C = u1*F[2] + v1*F[5] + F[8]
    
    # Charger l'image2
    img2 = cv2.imread(chemin_image2)  # Remplacez le chemin vers l'image2
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)  # Convertir l'image de BGR à RGB pour Matplotlib

    # Tracer les droites épipolaires
    v2=0
    hauteur, largeur, canaux = img2.shape
    for v2 in range(largeur):
        u2 = int((-(C+B*v2)) / A)
        cv2.circle(img2, (v2, u2), 3, (255,0,0), -1)

    # Afficher les 2 images
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(img1)
    plt.axis('off')
    plt.title('Image 1')

    plt.subplot(1, 2, 2)
    plt.imshow(img2)
    plt.axis('off')
    plt.title('Image 2')

    plt.show()



'''
Main --------------------------------------------------------------------
'''

## DONNEES REEL (Xi,Yi,Zi)
# Ouvrir le fichier en mode lecture
with open('donnees_reel.txt', 'r') as f:
    # Lire le contenu du fichier
    content = f.readlines()

# Initialiser la matrice numpy
matrice_reel = np.zeros((len(content), 3))

# Parcourir les lignes du fichier et stocker les valeurs dans la matrice
for i, line in enumerate(content):
    x, y, z = line.replace(',','.').split(';')
    matrice_reel[i] = [float(x), float(y), float(z)]

## DONNEES IMAGES (u,v)
## IMAGE FACE
# Ouvrir le fichier en mode lecture
with open('mire_face_data.txt', 'r') as f:
    # Lire le contenu du fichier
    content = f.readlines()

# Initialiser la matrice numpy
matrice_image_face = np.zeros((len(content), 2))

# Parcourir les lignes du fichier et stocker les valeurs dans la matrice
for i, line in enumerate(content):
    x, y = line.replace(',','.').split(';')
    matrice_image_face[i] = [float(x), float(y)]

## IMAGE DROITE 
# Ouvrir le fichier en mode lecture
with open('mire_droite_data.txt', 'r') as f:
    # Lire le contenu du fichier
    content = f.readlines()

# Initialiser la matrice numpy
matrice_image_droite = np.zeros((len(content), 2))

# Parcourir les lignes du fichier et stocker les valeurs dans la matrice
for i, line in enumerate(content):
    x, y = line.replace(',','.').split(';')
    matrice_image_droite[i] = [float(x), float(y)]


'''
Test des fonctions ------------------------------------------------------------
'''

# CALIBRAGE -------------------------------------------------------------------
P11=np.array([30, 39, 139.5]) #Face : U=1385 V=1345 #Coté : U=1515 V=1700
P31=np.array([64, 110,104.5]) #Face : U=1591 V=1644 #Coté : U=1750 V=1835

M1 = calibrage(matrice_reel, matrice_image_face)

test_calibrage(M1, P11)

M2 = calibrage(matrice_reel, matrice_image_droite)
test_calibrage(M2, P31)

# Calcul vecteur propre (Centre de l'image)
u0,v0 = vecteur_propre(M1)

#Calcul Tx, Ty, Tz (Position de l'appareil photo)
calcul_pose(M1, u0, v0)

# STEREOVISION -----------------------------------------------------------------
# Point P11 (30, 39, 139.5)
# Image face
U1=1384
V1=1350
# Image coté droite
U2=1516
V2=1702
stereoVision(M1,M2, U1, V1, U2, V2)

droite_epipolaire(matrice_image_face, matrice_image_droite, U1, V1, './mire_face.jpg', './mire_cote_droite.jpg')