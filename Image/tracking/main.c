#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <dirent.h>

#include "def.h"
#include "nrio.h"
#include "nrarith.h"
#include "nralloc.h"
#include "math.h"

#define TEST_MORPHOLOGIE 0
#define DETECTION_DE_MOUVEMENT_PAR_DIFFERENCE 0
#define EXTRACTION_IMAGE_DE_REFERENCE 0
#define DETECTION_DE_MOUVEMENT_IMG_REFERENCE 0
#define ETIQUETAGE_INTUITIF 0
#define POINTS_INTERET_HARRIS 0
#define POINTS_INTERET_GRADIENT 0
#define SUIVI_OBJET_SELECTION_VIGNETTE 1

#define NOIR 0
#define BLANC 255

byte** dilatation(byte** img, long nrl, long nrh, long ncl, long nch);
byte** n_dilatation(byte** img, long nrl, long nrh, long ncl, long nch, int iterations);
byte** erosion(byte** img, long nrl, long nrh, long ncl, long nch);
byte** n_erosion(byte** img, long nrl, long nrh, long ncl, long nch, int iterations);
byte** ouverture(byte** img, long nrl, long nrh, long ncl, long nch, int iterations);
byte** fermeture(byte** img, long nrl, long nrh, long ncl, long nch, int iterations);
byte** rgbtobyte(rgb8** img, long nrl, long nrh, long ncl, long nch);
byte** detection_mouvement(rgb8** image, rgb8** new_image, long nrl, long nrh, long ncl, long nch, int seuil);
int comparaison_entiers(const void* a, const void* b);
void trier_tableau(int* tableau, int taille);
int trouver_mediane(int* tableau, size_t taille);
byte** extraction(int etiquette, byte** original, int** M, long nrl, long nrh, long ncl, long nch);
byte** etiquetage(byte** img, int no_etiquette, long nrl, long nrh, long ncl, long nch);
byte** harris(byte** img, double lambda, long nrl, long nrh, long ncl, long nch);
int** gradient(byte** img, int nb_points, long nrl, long nrh, long ncl, long nch);
double** masque_gaussien(double sigma);
double** convolution(byte** img, double** filtre, double diviseur, long nrl, long nrh, long ncl, long nch);
double convolution_1_pixel(double** img, double** filtre, double diviseur, int i, int j);


int main(void){

    int i,j, k;
	long nrl,nrh,ncl,nch;
	int nb_img=965;


	#if TEST_MORPHOLOGIE

	long nrl2,nrh2,ncl2,nch2;

	byte **Ibruit;
    byte **Itrou;


	Ibruit=LoadPGM_bmatrix("carreBruit.pgm",&nrl,&nrh,&ncl,&nch);
	Itrou=LoadPGM_bmatrix("carreTrou.pgm",&nrl2,&nrh2,&ncl2,&nch2);

    Ibruit=ouverture(Ibruit,nrl,nrh,ncl,nch, 10);
    Itrou=fermeture(Itrou,nrl2,nrh2,ncl2,nch2, 10);

	SavePGM_bmatrix(Ibruit,nrl,nrh,ncl,nch,"carreBruit_bis.pgm");
	SavePGM_bmatrix(Itrou,nrl,nrh,ncl,nch,"carreTrou_bis.pgm");

	free_bmatrix(Ibruit,nrl,nrh,ncl,nch);
    free_bmatrix(Itrou,nrl2,nrh2,ncl2,nch2);

	#endif // TEST_MORPHOLOGIE

	#if DETECTION_DE_MOUVEMENT_PAR_DIFFERENCE
	rgb8** newI;
	rgb8** I;
	byte** mouvement;

    i=0;

    char folder_name[] = "fomd/";
    char file_name[100];
    struct dirent *entry;
    DIR *dir = opendir(folder_name);
    struct stat file_stat;


    if (dir == NULL) {
        perror("Erreur lors de l'ouverture du dossier");
        exit(EXIT_FAILURE);
    }
    int verif_2e_boucle=0;
    int cpt=1;

    while ((entry = readdir(dir)) != NULL) {
        // Vérifier que le nom de fichier commence par "fomd"
        if(strncmp(entry->d_name, "fomd", 4) == 0) {
            // Concat�ner le nom de dossier et le nom de fichier
            sprintf(file_name, "%s%s", folder_name, entry->d_name);
            // Vérifier si le fichier est un fichier régulier
            if (stat(file_name, &file_stat) == 0 && S_ISREG(file_stat.st_mode)) {

				if(verif_2e_boucle==1)
					I=newI;

				// Charger l'image
				newI = LoadPPM_rgb8matrix(file_name,&nrl,&nrh,&ncl,&nch);

				if(verif_2e_boucle==1)
				{
					//Comparaison image
					mouvement=detection_mouvement(I,newI,nrl,nrh,ncl,nch,15);
					mouvement=ouverture(mouvement,nrl,nrh,ncl,nch,1);
					mouvement=fermeture(mouvement,nrl,nrh,ncl,nch,6);
					//printf("%d ", cpt);
					sprintf(file_name,"./ResultatsMorpho/fomd_mouvment%03d-%03d.pgm",cpt, cpt-1);
					SavePGM_bmatrix(mouvement,nrl,nrh,ncl,nch,file_name);
				}
                cpt++;
				verif_2e_boucle=1;
			}
        }
    }

    closedir(dir);

    #endif // DETECTION_DE_MOUVEMENT_PAR_DIFFERENCE

    #if EXTRACTION_IMAGE_DE_REFERENCE

	rgb8** I;
	rgb8** Imoy;

	//MOYENNE
	I = LoadPPM_rgb8matrix("./fomd/fomd001.ppm",&nrl,&nrh,&ncl,&nch); //Chargement dans le vide pour avoir la taille
	Imoy=rgb8matrix(nrl,nrh,ncl,nch);

    //Tableau pour stocker les valeurs moyenne (rgb8matrix ne permet pas d'aller au dela de 255)
	int tab_moy[300][400][3]={0};

	//Lecture de toute les images
    char file_name[100];
    int compteur=0;
    for(k=1; k<965; k++){
        sprintf(file_name,"./fomd/fomd%03d.ppm",k);
        I = LoadPPM_rgb8matrix(file_name,&nrl,&nrh,&ncl,&nch);

        //Compteur pour diviser a la fin (moyenne)
        compteur++;
        for(i=nrl; i<nrh; i++){
            for(j=ncl; j<nch; j++){
                //Sommes
                tab_moy[i][j][0] += I[i][j].r;
                tab_moy[i][j][1] += I[i][j].g;
                tab_moy[i][j][2] += I[i][j].b;
            }
        }
    }

    //Division
	for(i=nrl; i<nrh; i++){
		for(j=ncl; j<nch; j++){
			tab_moy[i][j][0] /= compteur;
			tab_moy[i][j][1] /= compteur;
            tab_moy[i][j][2] /= compteur;
		}
	}

    //Image_moy = tab_moy
    for(i=nrl; i<nrh; i++){
		for(j=ncl; j<nch; j++){
            Imoy[i][j].r=tab_moy[i][j][0];
            Imoy[i][j].g=tab_moy[i][j][1];
            Imoy[i][j].b=tab_moy[i][j][2];
		}
    }
	SavePPM_rgb8matrix(Imoy,nrl, nrh, ncl, nch,"fomd_ref_moy.ppm");

	//MEDIANNE
    rgb8** Imed;
    Imed=rgb8matrix(nrl,nrh,ncl,nch);

    rgb8** img_load;
	int pixel_r[nb_img];
	int pixel_g[nb_img];
	int pixel_b[nb_img];
    printf("nrh=%d\n", nrh);
	for(i=nrl; i<nrh; i++){
		for(j=ncl; j<nch; j++){
		    for(k=1;k<nb_img;k++){
				sprintf(file_name,"./fomd/fomd%03d.ppm",k);
				img_load = LoadPPM_rgb8matrix(file_name,&nrl,&nrh,&ncl,&nch);
				pixel_r[k-1]=img_load[i][j].r;
				pixel_g[k-1]=img_load[i][j].g;
				pixel_b[k-1]=img_load[i][j].b;
				free_rgb8matrix(img_load, nrl,nrh,ncl,nch);
			}
			trier_tableau(pixel_r, nb_img);
			trier_tableau(pixel_g, nb_img);
			trier_tableau(pixel_b, nb_img);

			Imed[i][j].r=trouver_mediane(pixel_r, nb_img);
			Imed[i][j].g=trouver_mediane(pixel_g, nb_img);
			Imed[i][j].b=trouver_mediane(pixel_b, nb_img);
		}
		printf("%d ", i);
	}

	SavePPM_rgb8matrix(Imed,nrl, nrh, ncl, nch,"fomd_ref_med.ppm");

	#endif // EXTRACTION_IMAGE_DE_REFERENCE

	#if DETECTION_DE_MOUVEMENT_IMG_REFERENCE
	rgb8** Img;
	rgb8** Iref;
    char file_name[100];
	byte** difference;


	Iref=LoadPPM_rgb8matrix("./fomd_ref_med.ppm",&nrl,&nrh,&ncl,&nch);

	for(k=0; k<800; k++){
		sprintf(file_name,"./fomd/fomd%03d.ppm",k+1);
		Img=LoadPPM_rgb8matrix(file_name,&nrl,&nrh,&ncl,&nch);
		difference = detection_mouvement(Img, Iref, nrl, nrh, ncl, nch, 15);
		difference = n_erosion(difference, nrl, nrh, ncl, nch, 2);
		difference = n_dilatation(difference, nrl, nrh, ncl, nch, 3);
        difference = n_erosion(difference, nrl, nrh, ncl, nch, 3);
        difference = n_dilatation(difference, nrl, nrh, ncl, nch, 3);
        difference = n_erosion(difference, nrl, nrh, ncl, nch, 1);


		sprintf(file_name,"./ResultatsMorpho_Iref_Med/fomd_mouvment%03d.pgm", k+1);
		SavePGM_bmatrix(difference,nrl,nrh,ncl,nch,file_name);
	}

    #endif // DETECTION_DE_MOUVEMENT_IMG_REFERENCE

	#if ETIQUETAGE_INTUITIF
	byte** Ibin;
	Ibin=LoadPGM_bmatrix("./ResultatsMorpho_Iref_Med/fomd_mouvment005.pgm",&nrl,&nrh,&ncl,&nch);
	etiquetage(Ibin, nrl, nrh, ncl, nch);

	#endif // ETIQUETAGE_INTUITIF

	#if POINTS_INTERET_HARRIS
	// rgb8** Img;
	// Img=LoadPPM_rgb8matrix("./fomd_ref_med.ppm",&nrl,&nrh,&ncl,&nch);

	// byte** Img_b;
	// Img_b=rgbtobyte(Img, nrl, nrh, ncl, nch);

	byte** Img_b;
	Img_b=LoadPGM_bmatrix("./carreTrou.pgm",&nrl,&nrh,&ncl,&nch);

	byte** img_point_interet;
	img_point_interet = harris(Img_b, 0.2, nrl, nrh, ncl, nch);

	SavePGM_bmatrix(img_point_interet,nrl,nrh,ncl,nch,"./carreTrou_points_interet.pgm");
	// SavePGM_bmatrix(img_point_interet,nrl,nrh,ncl,nch,"./im_mediane_points_interet.pgm");

	free_bmatrix(Img_b, nrl, nrh, ncl, nch);
	free_bmatrix(img_point_interet, nrl, nrh, ncl, nch);
	// free_rgb8matrix(Img, nrl, nrh, ncl, nch);

	#endif // POINTS_INTERET_HARRIS

	#if POINTS_INTERET_GRADIENT

	byte** Img_b;
	Img_b=LoadPGM_bmatrix("./carreTrou.pgm",&nrl,&nrh,&ncl,&nch);

	int** tab_point_interet;
	tab_point_interet=gradient(Img_b, 20, nrl, nrh, ncl, nch);

	printf("Points d'intérets :\n");
	for(j=0; j<20; j++){
		printf("%d %d\n", tab_point_interet[0][j], tab_point_interet[1][j]);
	}

	free_bmatrix(Img_b, nrl, nrh, ncl, nch);
	#endif // POINTS_INTERET_GRADIENT

	#if SUIVI_OBJET_SELECTION_VIGNETTE
	int etiquette=17;

	rgb8** Img;
	rgb8** Iref;
    char file_name[100];
	byte** Img_b;
	byte** Img_etiqueteter;
	int** points_interets;

	Iref=LoadPPM_rgb8matrix("./fomd_ref_med.ppm",&nrl,&nrh,&ncl,&nch);

	for(k=0; k<800; k++){
		//DETECTION DE MOUVEMENT
		sprintf(file_name,"./fomd/fomd%03d.ppm",k+1);
		Img=LoadPPM_rgb8matrix(file_name,&nrl,&nrh,&ncl,&nch);
		Img_b = detection_mouvement(Img, Iref, nrl, nrh, ncl, nch, 15);
		Img_b = n_erosion(Img_b, nrl, nrh, ncl, nch, 2);
		Img_b = n_dilatation(Img_b, nrl, nrh, ncl, nch, 3);
        Img_b = n_erosion(Img_b, nrl, nrh, ncl, nch, 3);
        Img_b = n_dilatation(Img_b, nrl, nrh, ncl, nch, 3);
        Img_b = n_erosion(Img_b, nrl, nrh, ncl, nch, 1);

		//ETIQUETAGE
		Img_etiqueteter=etiquetage(Img_b, 5, nrl, nrh, ncl, nch);

		//POINTS INTERETS ( a changer : points d'interet dans une region ).
		points_interets=gradient(rgbtobyte(Img, nrl, nrh, ncl, nch), 20, nrl, nrh, ncl, nch);

		//



		// sprintf(file_name,"./ResultatsMorpho_Iref_Med/fomd_mouvment%03d.pgm", k+1);
		// SavePGM_bmatrix(difference,nrl,nrh,ncl,nch,file_name);
	}

	// char file_name[100];
	// sprintf(file_name,"./Img_extraite/Img_extraite_etiquette_%03d.pgm", etiquette);
    // SavePGM_bmatrix(img_extraite,nrl,nrh,ncl,nch,file_name);

	free_bmatrix(Img_b, nrl, nrh, ncl, nch);
	free_rgb8matrix(Img, nrl, nrh, ncl, nch);
	free_rgb8matrix(Iref,  nrl, nrh, ncl, nch);

	#endif //SUIVI_OBJET_SELECTION_VIGNETTE
	
	return 1;
}

//*********************************************************************************************************************************************
//*********************************************************************************************************************************************
//*********************************************************************************************************************************************
//*********************************************************************************************************************************************
//*********************************************************************************************************************************************

byte** dilatation(byte** img, long nrl, long nrh, long ncl, long nch)
{
	byte** new_img;
	new_img=bmatrix0(nrl,nrh,ncl,nch);

	int i; int j;
	for(i=nrl+1; i<nrh-1; i++){
		for(j=ncl+1; j<nch-1; j++){
			if(img[i-1][j-1]==BLANC || img[i-1][j]==BLANC || img[i-1][j+1]==BLANC || img[i][j-1]==BLANC || img[i][j+1]==BLANC || img[i+1][j-1]==BLANC || img[i+1][j]==BLANC || img[i+1][j+1]==BLANC){
				new_img[i][j]=BLANC;
			}
			else{
				new_img[i][j]=NOIR;
			}
		}
	}
	return new_img;
}

byte** n_dilatation(byte** img, long nrl, long nrh, long ncl, long nch, int iterations)
{
    int i;
	for(i=0; i<iterations; i++)
		img=dilatation(img, nrl, nrh, ncl, nch);
    return img;
}

byte** erosion(byte** img, long nrl, long nrh, long ncl, long nch)
{
	byte** new_img;
	new_img=bmatrix(nrl,nrh,ncl,nch);

	int i; int j;
	for(i=nrl+1; i<nrh-1; i++){
		for(j=ncl+1; j<nch-1; j++){
			if(img[i-1][j-1]==BLANC && img[i-1][j]==BLANC && img[i-1][j+1]==BLANC && img[i][j-1]==BLANC && img[i][j+1]==BLANC && img[i+1][j-1]==BLANC && img[i+1][j]==BLANC && img[i+1][j+1]==BLANC){
				new_img[i][j]=BLANC;
			}
			else{
				new_img[i][j]=NOIR;
			}
		}
	}
	return new_img;
}

byte** n_erosion(byte** img, long nrl, long nrh, long ncl, long nch, int iterations)
{
    int i;
	for(i=0; i<iterations; i++)
		img=erosion(img, nrl, nrh, ncl, nch);
    return img;
}

byte** ouverture(byte** img, long nrl, long nrh, long ncl, long nch, int iterations)
{
	int i;
	for(i=0; i<iterations; i++)
		img=erosion(img, nrl, nrh, ncl, nch);
	for(i=0; i<iterations; i++)
        img=dilatation(img, nrl, nrh, ncl, nch);

    return img;
}

byte** fermeture(byte** img, long nrl, long nrh, long ncl, long nch, int iterations)
{
    int i;
	for(i=0; i<iterations; i++)
		img=dilatation(img, nrl, nrh, ncl, nch);
	for(i=0; i<iterations; i++)
        img=erosion(img, nrl, nrh, ncl, nch);

    return img;
}

byte** rgbtobyte(rgb8** img, long nrl, long nrh, long ncl, long nch)
{
	int i, j;
	byte** result;
	result = bmatrix0(nrl, nrh, ncl, nch);

	for(i=nrl; i<nrh; i++){
		for(j=ncl; j<nch; j++){
			result[i][j] = 0.2989*img[i][j].r + 0.5870*img[i][j].g + 0.1140*img[i][j].b;
		}
	}
	return result;
}

byte** detection_mouvement(rgb8** image, rgb8** new_image, long nrl, long nrh, long ncl, long nch, int seuil)
{
	int i,j;
	int diff;
	byte** mouvement;
	mouvement=bmatrix(nrl,nrh,ncl,nch);

	for(i=nrl; i<nrh; i++){
		for(j=ncl; j<nch; j++){
			diff=(new_image[i][j].r - image[i][j].r) + (new_image[i][j].g - image[i][j].g) + (new_image[i][j].b - image[i][j].b);
			if(diff < seuil)
				mouvement[i][j]=0;
			else
				mouvement[i][j]=255;
		}
	}
	return mouvement;
}

int comparaison_entiers(const void* a, const void* b) {
    int int_a = *((int*)a);
    int int_b = *((int*)b);
    return (int_a > int_b) - (int_a < int_b);
}

void trier_tableau(int* tableau, int taille) {
    qsort(tableau, taille, sizeof(int), comparaison_entiers);
}

int trouver_mediane(int* tableau, size_t taille) {
    if (taille % 2 == 0) {
        // Si le tableau a un nombre pair d'éléments, la médiane est la moyenne des deux éléments du milieu
        return (tableau[taille/2 - 1] + tableau[taille/2]) / 2;
    } else {
        // Si le tableau a un nombre impair d'éléments, la médiane est l'élément du milieu
        return tableau[taille/2];
    }
}


byte** extraction(int etiquette, byte** original, int** M, long nrl, long nrh, long ncl, long nch){
    byte** sortie=bmatrix(nrl,nrh,ncl,nch);
    for(int i=nrl; i<nrh; i++){
        for(int j=ncl; j<nch; j++){
            if(M[i][j]==etiquette){
                sortie[i][j]=original[i][j];
            }
            else
                sortie[i][j]=0;
        }
    }

	return sortie;
}

byte** etiquetage(byte** img, int no_etiquette, long nrl, long nrh, long ncl, long nch){

	int** M;
	byte** R;

	M = imatrix0(nrl,nrh,ncl,nch);
    R=bmatrix0(nrl,nrh,ncl,nch);

	int i, j;
	int A=0, B=0, C=0;
	int EA=0, EB=0, EC=0;
	int etiquette=0;
    for(i=nrl+1; i<nrh; i++){
        for(j=ncl+1; j<nch; j++){
            A=img[i][j-1];
            B=img[i-1][j];
            C=img[i][j];
            EA=M[i][j-1];
            EB=M[i-1][j];
            EC=M[i][j];
            // printf("%d, %d, %d, %d, %d, %d\n", A, B, C, EA, EB, EC);
            if(C==A && C!=B)
                EC=EA;
            else if(C==B && C!=A)
                EC=EB;
            else if(C!=B && C!=A){
                etiquette++;
                EC=etiquette;
            }
            else if(C==B && C==A && EA==EB)
                EC=EB;
            else if(C==B && C==A && EA!=EB){
                EC=EB;
                for(int k=nrl; k<=i; k++){
                    for(int l=ncl; l<nch; l++){
                        if(M[k][l]==EA)
                            M[k][l]=EB;
                    }
                }
            }
            else
                printf("Ya un truc bizarre :( \n");

            M[i][j]=EC;
        }
    }

    printf("Nb etiquette = %d\n", etiquette);

    for(i=0; i<nrh; i++){
        for(j=0; j<nch; j++){
            R[i][j]=(M[i][j]*255)/etiquette;
        }
    }
    //SavePGM_bmatrix(R,nrl,nrh,ncl,nch,"Img_etiquette.pgm");


    int tab[etiquette];
    for(i=0; i<etiquette; i++) tab[i]=0;

    for(i=0; i<nrh; i++){
        for(j=0; j<nch; j++){
            if(tab[M[i][j]]!=1){
                printf("%d\n", M[i][j]);
                tab[M[i][j]]=1;
            }
        }
    }

	return extraction(no_etiquette, img, M, nrl, nrh, ncl, nch);
}

double** masque_gaussien(double sigma){
	double** G;
	G=dmatrix0(-1, 1, -1, 1);
	int x, y;
	for(y=-1; y<=1; y++){
        for(x=-1; x<=1; x++){
			G[y][x]=(1/(2*PI*(sigma*sigma))) * exp((-1)*(((double)(y*y) + (double)(x*x))/(2*(sigma*sigma))));
		}
	}
	return G;
}

double** convolution(byte** img, double** filtre, double diviseur, long nrl, long nrh, long ncl, long nch){
	double** resultat;
	resultat=dmatrix0(nrl, nrh, ncl, nch);
	int i, j;

	for(i=nrl+1; i<nrh-1; i++){
        for(j=ncl+1; j<nch-1; j++){
			resultat[i][j] = (	(double)(img[i-1][j-1]) 	* filtre[-1][-1] 	+ (double)(img[i][j-1]) 	* filtre[0][-1] 	+ (double)(img[i+1][j-1]) 	* filtre[1][-1] +
								(double)(img[i-1][j]) 		* filtre[-1][0] 	+ (double)(img[i][j]) 		* filtre[0][0] 		+ (double)(img[i+1][j]) 	* filtre[1][0] 	+
								(double)(img[i-1][j+1]) 	* filtre[-1][1] 	+ (double)(img[i][j+1]) 	* filtre[0][1] 		+ (double)(img[i+1][j+1]) 	* filtre[1][1]	) / diviseur;
		}
	}
	return resultat;
}

double convolution_1_pixel(double** img, double** filtre, double diviseur, int i, int j){
	double resultat;
	resultat = (img[i-1][j-1] 	* filtre[-1][-1] + img[i][j-1] 	* filtre[0][-1] + img[i+1][j-1] * filtre[1][-1] +
				img[i-1][j]		* filtre[-1][0]  + img[i][j]	* filtre[0][0] 	+ img[i+1][j] 	* filtre[1][0] 	+
				img[i-1][j+1] 	* filtre[-1][1]  + img[i][j+1] 	* filtre[0][1] 	+ img[i+1][j+1] * filtre[1][1]	) / diviseur;

	return resultat;
}

byte** harris(byte** img, double lambda, long nrl, long nrh, long ncl, long nch){
	int i, j;

	double** dx_img;
	double** dy_img;
	double** dx2_img;
	double** dy2_img;
	double** dxy_img;

	dx_img=dmatrix0(nrl, nrh, ncl, nch);
	dy_img=dmatrix0(nrl, nrh, ncl, nch);
	dx2_img=dmatrix0(nrl, nrh, ncl, nch);
	dy2_img=dmatrix0(nrl, nrh, ncl, nch);
	dxy_img=dmatrix0(nrl, nrh, ncl, nch);

	double** SobelX;
	SobelX=dmatrix0(-1, 1, -1, 1);
	double** SobelY;
	SobelY=dmatrix0(-1, 1, -1, 1);

	SobelX[-1][-1] = -1; SobelX[-1][0] = 0; SobelX[-1][1] = 1;
	SobelX[0][-1] = -2;	 SobelX[0][0] = 0;  SobelX[0][1] = 2;
	SobelX[1][-1] = -1;  SobelX[1][0] = 0;  SobelX[1][1] = 1;

	SobelY[-1][-1] = -1; SobelY[-1][0] = -2; SobelY[-1][1] = -1;
	SobelY[0][-1] = 0;	 SobelY[0][0] = 0;  SobelY[0][1] = 0;
	SobelY[1][-1] = 1;  SobelY[1][0] = 2;  SobelY[1][1] = 1;

	dx_img = convolution(img, SobelX, 4, nrl, nrh, ncl, nch);
	dy_img = convolution(img, SobelY, 4, nrl, nrh, ncl, nch);

	//Ix^2 et Iy^2
	for(i=nrl; i<=nrh; i++){
		for(j=ncl; j<=nch; j++){
			dx2_img[i][j] = dx_img[i][j]*dx_img[i][j];
			dy2_img[i][j] = dy_img[i][j]*dy_img[i][j];
		}
	}

	//Ix*Iy
	for(i=nrl; i<=nrh; i++){
		for(j=ncl; j<=nch; j++){
			dxy_img[i][j] = dx_img[i][j]*dy_img[i][j];
		}
	}

	double** Gaussian;
	Gaussian=masque_gaussien(1);

	double** C;
	C=dmatrix0(nrl, nrh, ncl, nch);

	double dx2_conv;
	double dy2_conv;
	double dxy_conv;

	for(i=nrl+1; i<=nrh-1; i++){
	    for(j=ncl+1; j<=nch-1; j++){
			dx2_conv=convolution_1_pixel(dx2_img, Gaussian, 1, i, j);
			dy2_conv=convolution_1_pixel(dy2_img, Gaussian, 1, i, j);
			dxy_conv=convolution_1_pixel(dxy_img, Gaussian, 1, i, j);

			C[i][j] = (dx2_conv * dy2_conv) - (dxy_conv) - (lambda * (dx2_conv + dy2_conv) * (dx2_conv + dy2_conv));
		}
	}

	// AFFICHAGE !!!
	double max = C[0][0];
	double min = C[0][0];
	for(i=nrl; i<=nrh; i++){
	    for(j=ncl; j<=nch; j++){
			if(C[i][j]>max)
				max=C[i][j];
			if(C[i][j]<min)
				min=C[i][j];
		}
	}

	printf("MAX = %f\nMIN = %f\n", max, min);

	byte** C_byte;
	C_byte=bmatrix0(nrl, nrh, ncl, nch);

	for(i=nrl; i<=nrh; i++){
	    for(j=ncl; j<=nch; j++){
			/*C[i][j] = ((C[i][j]-min) / (max-min)) * 255.0;
			C_byte[i][j] = (byte) C[i][j];*/
			int tmp=0;
			if(C[i][j]<0)
				C_byte[i][j]=0;
			else{
				tmp=(C[i][j]*255)/max;
				C_byte[i][j]=(byte)tmp;
			}
		}
	}
	return C_byte;
}

int** gradient(byte** img, int nb_points, long nrl, long nrh, long ncl, long nch){
	int i, j;

	double** dx_img;
	double** dy_img;
	double** dx2_img;
	double** dy2_img;
	double** dxy_img;

	dx_img=dmatrix0(nrl, nrh, ncl, nch);
	dy_img=dmatrix0(nrl, nrh, ncl, nch);
	dx2_img=dmatrix0(nrl, nrh, ncl, nch);
	dy2_img=dmatrix0(nrl, nrh, ncl, nch);
	dxy_img=dmatrix0(nrl, nrh, ncl, nch);

	double** SobelX;
	SobelX=dmatrix0(-1, 1, -1, 1);
	double** SobelY;
	SobelY=dmatrix0(-1, 1, -1, 1);

	SobelX[-1][-1] = -1; SobelX[-1][0] = 0; SobelX[-1][1] = 1;
	SobelX[0][-1] = -2;	 SobelX[0][0] = 0;  SobelX[0][1] = 2;
	SobelX[1][-1] = -1;  SobelX[1][0] = 0;  SobelX[1][1] = 1;

	SobelY[-1][-1] = -1; SobelY[-1][0] = -2; SobelY[-1][1] = -1;
	SobelY[0][-1] = 0;	 SobelY[0][0] = 0;  SobelY[0][1] = 0;
	SobelY[1][-1] = 1;  SobelY[1][0] = 2;  SobelY[1][1] = 1;

	dx_img = convolution(img, SobelX, 4, nrl, nrh, ncl, nch);
	dy_img = convolution(img, SobelY, 4, nrl, nrh, ncl, nch);

	//Ix^2 et Iy^2
	for(i=nrl; i<=nrh; i++){
		for(j=ncl; j<=nch; j++){
			dx2_img[i][j] = dx_img[i][j]*dx_img[i][j];
			dy2_img[i][j] = dy_img[i][j]*dy_img[i][j];
		}
	}

	//Ix*Iy
	for(i=nrl; i<=nrh; i++){
		for(j=ncl; j<=nch; j++){
			dxy_img[i][j] = dx_img[i][j]*dy_img[i][j];
		}
	}
	
	double** masque;
	masque=dmatrix0(-1, 1, -1, 1);

	masque[-1][-1] = 1; masque[-1][0] = 1; masque[-1][1] = 1;
	masque[0][-1] = 1;	 masque[0][0] = 0;  masque[0][1] = 1;
	masque[1][-1] = 1;  masque[1][0] = 1;  masque[1][1] = 1;

	double** K;
	K=dmatrix0(nrl, nrh, ncl, nch);

	double dx2_conv;
	double dy2_conv;
	double dxy_conv;

	for(i=nrl+1; i<=nrh-1; i++){
	    for(j=ncl+1; j<=nch-1; j++){
			dx2_conv=convolution_1_pixel(dx2_img, masque, 1, i, j);
			dy2_conv=convolution_1_pixel(dy2_img, masque, 1, i, j);
			dxy_conv=convolution_1_pixel(dxy_img, masque, 1, i, j);

			K[i][j]=(dx2_img[i][j]*dy2_conv) + (dy2_img[i][j]*dx2_conv) - (2*dxy_img[i][j]*dxy_conv);

			//Normalisation norme du gradient
			K[i][j]=K[i][j] / (dx2_conv + dy2_conv);
		}
	}

// AFFICHAGE !!!
	/*
	double max = K[0][0];
	double min = K[0][0];
	for(i=nrl; i<=nrh; i++){
	    for(j=ncl; j<=nch; j++){
			if(K[i][j]>max)
				max=K[i][j];
			if(K[i][j]<min)
				min=K[i][j];
		}
	}

	// printf("MAX = %f\nMIN = %f\n", max, min);

	byte** K_byte;
	K_byte=bmatrix0(nrl, nrh, ncl, nch);

	for(i=nrl; i<=nrh; i++){
	    for(j=ncl; j<=nch; j++){
			int tmp=0;

			tmp = ((K[i][j]-min) / (max-min)) * 255.0;
			K_byte[i][j] = (byte)tmp;
		}
	}
	SavePGM_bmatrix(img_point_interet,nrl,nrh,ncl,nch,"./carreTrou_points_interet_2.pgm");
	*/

	int **tab_points_interet;
	tab_points_interet=imatrix0(0, 1, 0, nb_points-1);
	double max;
	int i_ind_max;
	int j_ind_max;
	for(int point=0; point<nb_points; point++){
		max = K[0][0];
		i_ind_max=0;
		j_ind_max=0;
		for(i=nrl; i<=nrh; i++){
		    for(j=ncl; j<=nch; j++){
				if(K[i][j]>max){
					max=K[i][j];
					i_ind_max=i;
					j_ind_max=j;
				}
			}
		}
		K[i_ind_max][j_ind_max]=-INFINITY;
		tab_points_interet[0][point]=i_ind_max;
		tab_points_interet[1][point]=j_ind_max;
	}

	return tab_points_interet;

}