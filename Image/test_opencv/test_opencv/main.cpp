#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include "def.h"
#include "nrio.h"
#include "nrarith.h"
#include "nralloc.h"
#include "math.h"

#define TEST_MORPHOLOGIE 0
#define DETECTION_DE_MOUVEMENT_PAR_DIFFERENCE 0
#define EXTRACTION_IMAGE_DE_REFERENCE 0
#define DETECTION_DE_MOUVEMENT_IMG_REFERENCE 0
#define TEST_ETIQUETAGE_INTUITIF 0
#define POINTS_INTERET_HARRIS 0
#define POINTS_INTERET_GRADIENT 0
#define SUIVI_OBJET_SIMPLE 0
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
byte** detection_mouvement(rgb8** image1, rgb8** image2, long nrl, long nrh, long ncl, long nch, int seuil);
int comparaison_entiers(const void* a, const void* b);
void trier_tableau(int* tableau, int taille);
int trouver_mediane(int* tableau, size_t taille);
byte** extraction(int etiquette, byte** original, int** M, long nrl, long nrh, long ncl, long nch);
byte** etiquetage(byte** img, int no_etiquette, long nrl, long nrh, long ncl, long nch, BOOL affichage_liste_etiquette);
int cmp_etiquette_center_gravity(byte** img, int* centre, long nrl, long nrh, long ncl, long nch);
int cmp_etiquette_point_interet(byte** img_original, byte** img, int** points_interets, int nb_points_interets, int* position_ancienne_etiquette, int rectangle_englobant, long nrl, long nrh, long ncl, long nch);
byte** harris(byte** img, double lambda, long nrl, long nrh, long ncl, long nch);
int** gradient(byte** img, int nb_points, long nrl, long nrh, long ncl, long nch, long miniX, long maxiX, long miniY, long maxiY);
double** masque_gaussien(double sigma);
int* centre_gravite(byte** img, long nrl, long nrh, long ncl, long nch);
double** convolution(byte** img, double** filtre, double diviseur, long nrl, long nrh, long ncl, long nch);
double convolution_1_pixel(double** img, double** filtre, double diviseur, int i, int j);
rgb8** draw_box(rgb8** img, byte** img_b, long nrl, long nrh, long ncl, long nch);


int couucouuuu(void) {

	int i, j, k;
	long nrl, nrh, ncl, nch;
	int nb_img = 965;


#if TEST_MORPHOLOGIE

	long nrl2, nrh2, ncl2, nch2;

	byte** Ibruit;
	byte** Itrou;


	Ibruit = LoadPGM_bmatrix("carreBruit.pgm", &nrl, &nrh, &ncl, &nch);
	Itrou = LoadPGM_bmatrix("carreTrou.pgm", &nrl2, &nrh2, &ncl2, &nch2);

	Ibruit = ouverture(Ibruit, nrl, nrh, ncl, nch, 10);
	Itrou = fermeture(Itrou, nrl2, nrh2, ncl2, nch2, 10);

	SavePGM_bmatrix(Ibruit, nrl, nrh, ncl, nch, "carreBruit_bis.pgm");
	SavePGM_bmatrix(Itrou, nrl2, nrh2, ncl2, nch2, "carreTrou_bis.pgm");

	free_bmatrix(Ibruit, nrl, nrh, ncl, nch);
	free_bmatrix(Itrou, nrl2, nrh2, ncl2, nch2);

#endif // TEST_MORPHOLOGIE

#if DETECTION_DE_MOUVEMENT_PAR_DIFFERENCE
	rgb8** newI;
	rgb8** I;
	byte** mouvement;

	i = 0;

	char folder_name[] = "fomd/";
	char file_name[100];
	struct dirent* entry;
	DIR* dir = opendir(folder_name);
	struct stat file_stat;


	if (dir == NULL) {
		perror("Erreur lors de l'ouverture du dossier");
		exit(EXIT_FAILURE);
	}
	int verif_2e_boucle = 0;
	int cpt = 1;

	while ((entry = readdir(dir)) != NULL) {
		// Vérifier que le nom de fichier commence par "fomd"
		if (strncmp(entry->d_name, "fomd", 4) == 0) {
			// Concat�ner le nom de dossier et le nom de fichier
			sprintf(file_name, "%s%s", folder_name, entry->d_name);
			// Vérifier si le fichier est un fichier régulier
			if (stat(file_name, &file_stat) == 0 && S_ISREG(file_stat.st_mode)) {

				if (verif_2e_boucle == 1)
					I = newI;

				// Charger l'image
				newI = LoadPPM_rgb8matrix(file_name, &nrl, &nrh, &ncl, &nch);

				if (verif_2e_boucle == 1)
				{
					//Comparaison image
					mouvement = detection_mouvement(I, newI, nrl, nrh, ncl, nch, 15);
					mouvement = ouverture(mouvement, nrl, nrh, ncl, nch, 1);
					mouvement = fermeture(mouvement, nrl, nrh, ncl, nch, 6);
					//printf("%d ", cpt);
					sprintf(file_name, "./ResultatsMorpho/fomd_mouvment%03d-%03d.pgm", cpt, cpt - 1);
					SavePGM_bmatrix(mouvement, nrl, nrh, ncl, nch, file_name);
				}
				cpt++;
				verif_2e_boucle = 1;
			}
		}
	}

	closedir(dir);

#endif // DETECTION_DE_MOUVEMENT_PAR_DIFFERENCE

#if EXTRACTION_IMAGE_DE_REFERENCE

	rgb8** I;
	rgb8** Imoy;

	//MOYENNE
	I = LoadPPM_rgb8matrix("./fomd/fomd001.ppm", &nrl, &nrh, &ncl, &nch); //Chargement dans le vide pour avoir la taille
	Imoy = rgb8matrix(nrl, nrh, ncl, nch);

	//Tableau pour stocker les valeurs moyenne (rgb8matrix ne permet pas d'aller au dela de 255)
	int tab_moy[300][400][3] = { 0 };

	//Lecture de toute les images
	char file_name[100];
	int compteur = 0;
	for (k = 1; k < 965; k++) {
		sprintf(file_name, "./fomd/fomd%03d.ppm", k);
		I = LoadPPM_rgb8matrix(file_name, &nrl, &nrh, &ncl, &nch);

		//Compteur pour diviser a la fin (moyenne)
		compteur++;
		for (i = nrl; i < nrh; i++) {
			for (j = ncl; j < nch; j++) {
				//Sommes
				tab_moy[i][j][0] += I[i][j].r;
				tab_moy[i][j][1] += I[i][j].g;
				tab_moy[i][j][2] += I[i][j].b;
			}
		}
	}

	//Division
	for (i = nrl; i < nrh; i++) {
		for (j = ncl; j < nch; j++) {
			tab_moy[i][j][0] /= compteur;
			tab_moy[i][j][1] /= compteur;
			tab_moy[i][j][2] /= compteur;
		}
	}

	//Image_moy = tab_moy
	for (i = nrl; i < nrh; i++) {
		for (j = ncl; j < nch; j++) {
			Imoy[i][j].r = tab_moy[i][j][0];
			Imoy[i][j].g = tab_moy[i][j][1];
			Imoy[i][j].b = tab_moy[i][j][2];
		}
	}
	SavePPM_rgb8matrix(Imoy, nrl, nrh, ncl, nch, "fomd_ref_moy.ppm");

	//MEDIANNE
	rgb8** Imed;
	Imed = rgb8matrix(nrl, nrh, ncl, nch);

	rgb8** img_load;
	int pixel_r[nb_img];
	int pixel_g[nb_img];
	int pixel_b[nb_img];
	//printf("nrh=%d\n", nrh);

	//Pour chaque pixels
	for (i = nrl; i < nrh; i++) {
		for (j = ncl; j < nch; j++) {
			//On charge toute les images
			for (k = 1; k < nb_img; k++) {
				sprintf(file_name, "./fomd/fomd%03d.ppm", k);
				img_load = LoadPPM_rgb8matrix(file_name, &nrl, &nrh, &ncl, &nch);
				pixel_r[k - 1] = img_load[i][j].r;
				pixel_g[k - 1] = img_load[i][j].g;
				pixel_b[k - 1] = img_load[i][j].b;
				free_rgb8matrix(img_load, nrl, nrh, ncl, nch);
			}
			//On tri les tableaux des valeurs du pixel k
			trier_tableau(pixel_r, nb_img);
			trier_tableau(pixel_g, nb_img);
			trier_tableau(pixel_b, nb_img);

			//On récupère la medianne
			Imed[i][j].r = trouver_mediane(pixel_r, nb_img);
			Imed[i][j].g = trouver_mediane(pixel_g, nb_img);
			Imed[i][j].b = trouver_mediane(pixel_b, nb_img);
		}
		//printf("%d ", i);
	}

	SavePPM_rgb8matrix(Imed, nrl, nrh, ncl, nch, "fomd_ref_med.ppm");

#endif // EXTRACTION_IMAGE_DE_REFERENCE

#if DETECTION_DE_MOUVEMENT_IMG_REFERENCE
	rgb8** Img;
	rgb8** Iref;
	char file_name[100];
	byte** difference;

	//Iref=LoadPPM_rgb8matrix("./fomd_ref_moy.ppm",&nrl,&nrh,&ncl,&nch);
	Iref = LoadPPM_rgb8matrix((char *)". / fomd_ref_med.ppm", &nrl, &nrh, &ncl, &nch);

	for (k = 0; k < 800; k++) {
		sprintf(file_name, "./fomd/fomd%03d.ppm", k + 1);
		Img = LoadPPM_rgb8matrix(file_name, &nrl, &nrh, &ncl, &nch);
		difference = detection_mouvement(Img, Iref, nrl, nrh, ncl, nch, 15);
		difference = n_erosion(difference, nrl, nrh, ncl, nch, 2);
		difference = n_dilatation(difference, nrl, nrh, ncl, nch, 3);
		difference = n_erosion(difference, nrl, nrh, ncl, nch, 3);
		difference = n_dilatation(difference, nrl, nrh, ncl, nch, 3);
		difference = n_erosion(difference, nrl, nrh, ncl, nch, 1);


		sprintf(file_name, "./ResultatsMorpho_Iref_Moy/fomd_mouvment%03d.pgm", k + 1);
		//sprintf(file_name,"./ResultatsMorpho_Iref_Med/fomd_mouvment%03d.pgm", k+1);
		SavePGM_bmatrix(difference, nrl, nrh, ncl, nch, file_name);
	}

#endif // DETECTION_DE_MOUVEMENT_IMG_REFERENCE

#if TEST_ETIQUETAGE_INTUITIF
	byte** Img;
	Img = LoadPGM_bmatrix("./rice.pgm", &nrl, &nrh, &ncl, &nch);
	for (i = nrl; i < nrh; i++) {
		for (j = ncl; j < nch; j++) {
			if (Img[i][j] < 125)
				Img[i][j] = 0;
			else
				Img[i][j] = 255;
		}
	}

	byte** Iett;
	Iett = bmatrix0(nrl, nrh, ncl, nch);
	Iett = etiquetage(Img, 10, nrl, nrh, ncl, nch, TRUE);
	SavePGM_bmatrix(Iett, nrl, nrh, ncl, nch, "./rice_etiquette.pgm");

	free_bmatrix(Img, nrl, nrh, ncl, nch);
	free_bmatrix(Iett, nrl, nrh, ncl, nch);

#endif // ETIQUETAGE_INTUITIF

#if POINTS_INTERET_HARRIS
	// rgb8** Img;
	// Img=LoadPPM_rgb8matrix("./fomd_ref_med.ppm",&nrl,&nrh,&ncl,&nch);

	// byte** Img_b;
	// Img_b=rgbtobyte(Img, nrl, nrh, ncl, nch);

	byte** Img_b;
	Img_b = LoadPGM_bmatrix("./carreTrou.pgm", &nrl, &nrh, &ncl, &nch);

	byte** img_point_interet;
	img_point_interet = harris(Img_b, 0.2, nrl, nrh, ncl, nch);

	SavePGM_bmatrix(img_point_interet, nrl, nrh, ncl, nch, "./carreTrou_points_interet.pgm");
	// SavePGM_bmatrix(img_point_interet,nrl,nrh,ncl,nch,"./img_mediane_points_interet.pgm");

	free_bmatrix(Img_b, nrl, nrh, ncl, nch);
	free_bmatrix(img_point_interet, nrl, nrh, ncl, nch);
	// free_rgb8matrix(Img, nrl, nrh, ncl, nch);

#endif // POINTS_INTERET_HARRIS

#if POINTS_INTERET_GRADIENT

	byte** Img_b;
	Img_b = LoadPGM_bmatrix("./carreTrou.pgm", &nrl, &nrh, &ncl, &nch);

	int** tab_point_interet;
	tab_point_interet = gradient(Img_b, 20, nrl, nrh, ncl, nch);

	printf("Points d'intérets :\n");
	for (j = 0; j < 20; j++) {
		printf("%d %d\n", tab_point_interet[0][j], tab_point_interet[1][j]);
	}

	free_bmatrix(Img_b, nrl, nrh, ncl, nch);
#endif // POINTS_INTERET_GRADIENT

#if SUIVI_OBJET_SIMPLE

	int etiquette = 28;

	rgb8** Img;
	rgb8** Iref;
	char file_name[100];
	byte** Img_b;
	byte** Img_etiqueteter;
	int* centre;

	Iref = LoadPPM_rgb8matrix("./fomd_ref_med.ppm", &nrl, &nrh, &ncl, &nch);

	for (k = 135; k < 695; k++) {
		//DETECTION DE MOUVEMENT
		sprintf(file_name, "./fomd/fomd%03d.ppm", k);
		Img = LoadPPM_rgb8matrix(file_name, &nrl, &nrh, &ncl, &nch);
		Img_b = detection_mouvement(Img, Iref, nrl, nrh, ncl, nch, 15);
		Img_b = n_erosion(Img_b, nrl, nrh, ncl, nch, 2);
		Img_b = n_dilatation(Img_b, nrl, nrh, ncl, nch, 3);
		Img_b = n_erosion(Img_b, nrl, nrh, ncl, nch, 3);
		Img_b = n_dilatation(Img_b, nrl, nrh, ncl, nch, 3);
		Img_b = n_erosion(Img_b, nrl, nrh, ncl, nch, 1);

		if (k == 135)
		{
			Img_etiqueteter = etiquetage(Img_b, etiquette, nrl, nrh, ncl, nch, TRUE);
			centre = centre_gravite(Img_b, nrl, nrh, ncl, nch);
		}
		else
		{
			etiquette = cmp_etiquette_center_gravity(Img_b, centre, nrl, nrh, ncl, nch);

			Img_etiqueteter = etiquetage(Img_b, etiquette, nrl, nrh, ncl, nch, FALSE);
			centre = centre_gravite(Img_b, nrl, nrh, ncl, nch);

			Img = draw_box(Img, Img_etiqueteter, nrl, nrh, ncl, nch);

			sprintf(file_name, "./Resultats_simple_tracking/fomd%03d.ppm", k);
			SavePPM_rgb8matrix(Img, nrl, nrh, ncl, nch, file_name);
		}
	}

	free_rgb8matrix(Img, nrl, nrh, ncl, nch);
	free_rgb8matrix(Iref, nrl, nrh, ncl, nch);
	free_bmatrix(Img_b, nrl, nrh, ncl, nch);
	free_bmatrix(Img_etiqueteter, nrl, nrh, ncl, nch);
	free(centre);

#endif // SUIVI_OBJET_SIMPLE

#if SUIVI_OBJET_SELECTION_VIGNETTE
	int etiquette = 14;
	int nb_points_interets = 20;

	rgb8** Img;
	rgb8** Iref;
	char file_name[100];
	byte** Img_b;
	byte** Img_etiqueteter;
	int* pos_etiquette = new int[2];;
	int** points_interets; //[0][-] et [1][-] : coordonnées; 	[2][-] : NDG
	points_interets=imatrix0(0, 2, 0, nb_points_interets - 1);

	Iref = LoadPPM_rgb8matrix((char *)"fomd_ref_med.ppm", &nrl, &nrh, &ncl, &nch);

	for (k = 135; k < 300; k++) {
		//DETECTION DE MOUVEMENT
		sprintf(file_name, "fomd%03d.ppm", k);
		Img = LoadPPM_rgb8matrix(file_name, &nrl, &nrh, &ncl, &nch);

		Img_b = detection_mouvement(Img, Iref, nrl, nrh, ncl, nch, 15);
		Img_b = n_erosion(Img_b, nrl, nrh, ncl, nch, 2);
		Img_b = n_dilatation(Img_b, nrl, nrh, ncl, nch, 3);
		Img_b = n_erosion(Img_b, nrl, nrh, ncl, nch, 3);
		Img_b = n_dilatation(Img_b, nrl, nrh, ncl, nch, 3);
		Img_b = n_erosion(Img_b, nrl, nrh, ncl, nch, 1);

		if (k > 135) {
			printf("%d : debut #########\n", k);
			etiquette = cmp_etiquette_point_interet(rgbtobyte(Img, nrl, nrh, ncl, nch), Img_b, points_interets, nb_points_interets, pos_etiquette, 30, nrl, nrh, ncl, nch);
			printf("k : %d\n", k);
			//ETIQUETAGE
			
			Img_etiqueteter = etiquetage(Img_b, etiquette, nrl, nrh, ncl, nch, FALSE);
			printf("%d : fin etiquetage", k);
		}
		else
			Img_etiqueteter = etiquetage(Img_b, etiquette, nrl, nrh, ncl, nch, TRUE);

		//Bounding box
		int min_x = nch, min_y = nrh, max_x = 0, max_y = 0;
		for (i = nrl; i <= nrh; i++) {
			for (j = ncl; j <= nch; j++) {
				if (Img_etiqueteter[i][j] != 0) {
					if (j < min_x) {
						min_x = j;
					}
					if (j > max_x) {
						max_x = j;
					}
					if (i < min_y) {
						min_y = i;
					}
					if (i > max_y) {
						max_y = i;
					}
				}
			}
		}
		printf("%d : debut centre g\n", k);
		//Centre de gravité
		pos_etiquette = centre_gravite(Img_etiqueteter, nrl, nrh, ncl, nch);

		//POINTS INTERETS dans la bouding box
		points_interets = gradient(rgbtobyte(Img, nrl, nrh, ncl, nch), nb_points_interets, nrl, nrh, ncl, nch, min_x, max_x, min_y, max_y);

		//Affichage
		printf("%d : debut draw box\n", k);
		Img = draw_box(Img, Img_etiqueteter, nrl, nrh, ncl, nch);
		sprintf(file_name, "./Resultats_tracking_points_interets/fomd%03d.ppm", k);
		printf("%d : debut save\n", k);

		SavePPM_rgb8matrix(Img, nrl, nrh, ncl, nch, file_name);
		free_rgb8matrix(Img, nrl, nrh, ncl, nch);
		printf("%d : fin save\n", k);
	}

	free_bmatrix(Img_b, nrl, nrh, ncl, nch);
	free_rgb8matrix(Img, nrl, nrh, ncl, nch);
	free_rgb8matrix(Iref, nrl, nrh, ncl, nch);
	free_bmatrix(Img_etiqueteter, nrl, nrh, ncl, nch);
	delete[] pos_etiquette;
	free_imatrix(points_interets, 0, 2, 0, nb_points_interets - 1);

#endif //SUIVI_OBJET_SELECTION_VIGNETTE

	return 1;
}

//*********************************************************************************************************************************************
//*********************************************************************************************************************************************
//*********************************************************************************************************************************************
//*********************************************************************************************************************************************
//*********************************************************************************************************************************************


/**
 * Cette fonction fait la dilatation d'une image avec un élement structurant 3x3.
 *
 * @param img L'image à dilater.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return L'image dilatée
 */
byte** dilatation(byte** img, long nrl, long nrh, long ncl, long nch)
{
	byte** new_img;
	new_img = bmatrix0(nrl, nrh, ncl, nch);

	int i; int j;
	for (i = nrl + 1; i < nrh - 1; i++) {
		for (j = ncl + 1; j < nch - 1; j++) {
			if (img[i - 1][j - 1] == BLANC || img[i - 1][j] == BLANC || img[i - 1][j + 1] == BLANC || img[i][j - 1] == BLANC || img[i][j + 1] == BLANC || img[i + 1][j - 1] == BLANC || img[i + 1][j] == BLANC || img[i + 1][j + 1] == BLANC) {
				new_img[i][j] = BLANC;
			}
			else {
				new_img[i][j] = NOIR;
			}
		}
	}
	return new_img;
}

/**
 * Cette fonction fait plusieurs dilatations d'une image avec un élement structurant 3x3.
 *
 * @param img L'image à dilater.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 * @param iterations Le nombre de dilatations.
 *
 * @return L'image dilatée plusieurs fois.
 */
byte** n_dilatation(byte** img, long nrl, long nrh, long ncl, long nch, int iterations)
{
	int i;
	for (i = 0; i < iterations; i++)
		img = dilatation(img, nrl, nrh, ncl, nch);
	return img;
}

/**
 * Cette fonction fait l'erosion d'une image avec un élement structurant 3x3.
 *
 * @param img L'image à éroder.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return L'image érodée
 */
byte** erosion(byte** img, long nrl, long nrh, long ncl, long nch)
{
	byte** new_img;
	new_img = bmatrix(nrl, nrh, ncl, nch);

	int i; int j;
	for (i = nrl + 1; i < nrh - 1; i++) {
		for (j = ncl + 1; j < nch - 1; j++) {
			if (img[i - 1][j - 1] == BLANC && img[i - 1][j] == BLANC && img[i - 1][j + 1] == BLANC && img[i][j - 1] == BLANC && img[i][j + 1] == BLANC && img[i + 1][j - 1] == BLANC && img[i + 1][j] == BLANC && img[i + 1][j + 1] == BLANC) {
				new_img[i][j] = BLANC;
			}
			else {
				new_img[i][j] = NOIR;
			}
		}
	}
	return new_img;
}

/**
 * Cette fonction fait plusieurs érosions d'une image avec un élement structurant 3x3.
 *
 * @param img L'image à éroder.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 * @param iterations Le nombre de dilatations.
 *
 * @return L'image érodée plusieurs fois.
 */
byte** n_erosion(byte** img, long nrl, long nrh, long ncl, long nch, int iterations)
{
	int i;
	for (i = 0; i < iterations; i++)
		img = erosion(img, nrl, nrh, ncl, nch);
	return img;
}

/**
 * Cette fonction fait l'ouverture d'une image.
 *
 * @param img L'image sur laquelle faire l'ouverture.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 * @param iterations Le nombre d'érosions et de dilatations.
 *
 * @return L'image après ouverture.
 */
byte** ouverture(byte** img, long nrl, long nrh, long ncl, long nch, int iterations)
{
	int i;
	for (i = 0; i < iterations; i++)
		img = erosion(img, nrl, nrh, ncl, nch);
	for (i = 0; i < iterations; i++)
		img = dilatation(img, nrl, nrh, ncl, nch);

	return img;
}

/**
 * Cette fonction fait la fermeture d'une image.
 *
 * @param img L'image sur laquelle faire la fermeture.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 * @param iterations Le nombre de dilatations et d'érosions.
 *
 * @return L'image après fermeture.
 */
byte** fermeture(byte** img, long nrl, long nrh, long ncl, long nch, int iterations)
{
	int i;
	for (i = 0; i < iterations; i++)
		img = dilatation(img, nrl, nrh, ncl, nch);
	for (i = 0; i < iterations; i++)
		img = erosion(img, nrl, nrh, ncl, nch);

	return img;
}

/**
 * Cette fonction converti une image rgb8 en image byte.
 *
 * @param img L'image en rgb8.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return L'image en byte.
 */
byte** rgbtobyte(rgb8** img, long nrl, long nrh, long ncl, long nch)
{
	int i, j;
	byte** result;
	result = bmatrix0(nrl, nrh, ncl, nch);

	for (i = nrl; i < nrh; i++) {
		for (j = ncl; j < nch; j++) {
			result[i][j] = 0.2989 * img[i][j].r + 0.5870 * img[i][j].g + 0.1140 * img[i][j].b;
		}
	}
	return result;
}

/**
 * Cette fonction fait la différence entre 2 images (image2 - image1) pixel à pixel.
 *
 * @param image1 L'image en rgb8 que l'on soustrait.
 * @param image2 L'image en rgb8 à laquelle on soustrait.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 * @param seuil La valeur qui définie si on détecte ou non un mouvement.
 *
 * @return L'image des mouvements détectés en byte.
 */
byte** detection_mouvement(rgb8** image1, rgb8** image2, long nrl, long nrh, long ncl, long nch, int seuil)
{
	int i, j;
	int diff;
	byte** mouvement;
	mouvement = bmatrix(nrl, nrh, ncl, nch);

	for (i = nrl; i < nrh; i++) {
		for (j = ncl; j < nch; j++) {
			diff = (image2[i][j].r - image1[i][j].r) + (image2[i][j].g - image1[i][j].g) + (image2[i][j].b - image1[i][j].b);
			if (diff < seuil)
				mouvement[i][j] = 0;
			else
				mouvement[i][j] = 255;
		}
	}
	return mouvement;
}

/**
 * Cette fonction est utilisée pour comparer deux entiers qui sont des pointeurs void.
 * Elle est utilisée comme fonction de comparaison dans la fonction de tri qsort.
 *
 * @param a Pointeur vers le premier entier à comparer.
 * @param b Pointeur vers le deuxième entier à comparer.
 *
 * @return Un entier négatif, zéro ou positif si a est inférieur à, égal à, ou supérieur à b.
 */
int comparaison_entiers(const void* a, const void* b) {
	// Convertir les pointeurs void en entiers
	int int_a = *((int*)a);
	int int_b = *((int*)b);
	// Comparer les entiers et renvoyer le résultat
	return (int_a > int_b) - (int_a < int_b);
}

/**
 * Cette fonction trie un tableau d'entiers en utilisant la fonction de comparaison
 * 'comparaison_entiers' qui est passée à la fonction qsort.
 *
 * @param tableau Le tableau à trier.
 * @param taille La taille du tableau.
 */
void trier_tableau(int* tableau, int taille) {
	// Utiliser la fonction qsort pour trier le tableau
	qsort(tableau, taille, sizeof(int), comparaison_entiers);
}

/**
 * Cette fonction trouve la médiane d'un tableau d'entiers (ne tri pas le tableau).
 *
 * @param tableau Le tableau d'entiers à analyser.
 * @param taille La taille du tableau.
 *
 * @return La médiane du tableau.
 */
int trouver_mediane(int* tableau, size_t taille) {
	if (taille % 2 == 0) {
		// Si le tableau a un nombre pair d'éléments, la médiane est la moyenne des deux éléments du milieu
		return (tableau[taille / 2 - 1] + tableau[taille / 2]) / 2;
	}
	else {
		// Si le tableau a un nombre impair d'éléments, la médiane est l'élément du milieu
		return tableau[taille / 2];
	}
}

/**
 * Cette fonction extrait une région d'intérêt d'une image binaire en utilisant l'étiquette fournie.
 * Les valeurs des pixels de l'image originale correspondant à l'étiquette sont copiées dans la région d'intérêt de sortie.
 * Les pixels qui ne correspondent pas à l'étiquette sont définis à zéro.
 *
 * @param etiquette L'étiquette à utiliser pour extraire la région d'intérêt.
 * @param original L'image originale.
 * @param M Le tableau d'étiquettes.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return Une image contenant uniquement la région d'intérêt.
 */
byte** extraction(int etiquette, byte** original, int** M, long nrl, long nrh, long ncl, long nch) {
	byte** sortie = bmatrix(nrl, nrh, ncl, nch);
	for (int i = nrl; i < nrh; i++) {
		for (int j = ncl; j < nch; j++) {
			if (M[i][j] == etiquette) {
				sortie[i][j] = original[i][j];
			}
			else
				sortie[i][j] = 0;
		}
	}

	return sortie;
}

/**
 * Cette fonction permet de trouver l'étiquette la plus proche du centre de gravité de la zone étiqueté précedente.
 *
 * @param img L'image dans laquelle on cherche l'étiquette.
 * @param centre Les coordonnées du centre de gravité de l'étiquette.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return L'étiquette de la zone correspondante à la zone précedente.
 */
int cmp_etiquette_center_gravity(byte** img, int* centre, long nrl, long nrh, long ncl, long nch) {

	int** M;
	byte** R;

	M = imatrix0(nrl, nrh, ncl, nch);
	R = bmatrix0(nrl, nrh, ncl, nch);

	int i, j;
	int A = 0, B = 0, C = 0;
	int EA = 0, EB = 0, EC = 0;
	int etiquette = 0;
	for (i = nrl + 1; i < nrh; i++) {
		for (j = ncl + 1; j < nch; j++) {
			A = img[i][j - 1];
			B = img[i - 1][j];
			C = img[i][j];
			EA = M[i][j - 1];
			EB = M[i - 1][j];
			EC = M[i][j];
			// printf("%d, %d, %d, %d, %d, %d\n", A, B, C, EA, EB, EC);
			if (C == A && C != B)
				EC = EA;
			else if (C == B && C != A)
				EC = EB;
			else if (C != B && C != A) {
				etiquette++;
				EC = etiquette;
			}
			else if (C == B && C == A && EA == EB)
				EC = EB;
			else if (C == B && C == A && EA != EB) {
				EC = EB;
				for (int k = nrl; k <= i; k++) {
					for (int l = ncl; l < nch; l++) {
						if (M[k][l] == EA)
							M[k][l] = EB;
					}
				}
			}
			else
				printf("Ya un truc bizarre :( \n");

			M[i][j] = EC;
		}
	}

	//printf("Nb etiquette = %d\n", etiquette);

	for (i = 0; i < nrh; i++) {
		for (j = 0; j < nch; j++) {
			R[i][j] = (M[i][j] * 255) / etiquette;
		}
	}
	//SavePGM_bmatrix(R,nrl,nrh,ncl,nch,"Img_etiquette.pgm");


	int * tab= new int[etiquette];
	for (i = 0; i < etiquette; i++) tab[i] = 0;

	int* new_centre;
	float dist = nrh * nch;
	float new_dist;
	int etiquette_plus_proche = M[0][0];

	for (i = nrl; i < nrh; i++) {
		for (j = ncl; j < nch; j++) {
			if (tab[M[i][j]] != 1) {
				tab[M[i][j]] = 1;
				new_centre = centre_gravite(extraction(M[i][j], img, M, nrl, nrh, ncl, nch), nrl, nrh, ncl, nch);
				new_dist = sqrt(abs((new_centre[0] - centre[0]) * (new_centre[0] - centre[0])) + abs((new_centre[1] - centre[1]) * (new_centre[1] - centre[1])));
				if (dist > new_dist) {
					dist = new_dist;
					etiquette_plus_proche = M[i][j];
				}
				delete[] new_centre;
			}
		}
	}
	delete[] tab;
	return etiquette_plus_proche;
}

/**
 * Cette fonction permet de trouver l'étiquette la plus proche des points d'intêrets de la zone étiqueté précedente.
 *
 * @param img_original L'image original en nuance de gris.
 * @param img L'image dans laquelle on cherche l'étiquette.
 * @param points_interets Les coordonnées des points d'intêrets de la zone précedente.
 * @param position_ancienne_etiquette La position précedente du centre de gravité de la zone que l'on suit.
 * @param rectangle_englobant La taille du rectangle dans lequel on va chercher une nouvelle étiquette.
 * @param nb_points_interets Le nombre de points d'interets
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return L'étiquette de la zone correspondante à la zone précedente.
 */
int cmp_etiquette_point_interet(byte** img_original, byte** img, int** points_interets, int nb_points_interets, int* position_ancienne_etiquette, int rectangle_englobant, long nrl, long nrh, long ncl, long nch) {

	int** M = imatrix0(nrl, nrh, ncl, nch);;
	byte** R = bmatrix0(nrl, nrh, ncl, nch);;


	int i, j, k;
	int A = 0, B = 0, C = 0;
	int EA = 0, EB = 0, EC = 0;
	int etiquette = 0;
	for (i = nrl + 1; i < nrh; i++) {
		for (j = ncl + 1; j < nch; j++) {
			A = img[i][j - 1];
			B = img[i - 1][j];
			C = img[i][j];
			EA = M[i][j - 1];
			EB = M[i - 1][j];
			EC = M[i][j];
			// printf("%d, %d, %d, %d, %d, %d\n", A, B, C, EA, EB, EC);
			if (C == A && C != B)
				EC = EA;
			else if (C == B && C != A)
				EC = EB;
			else if (C != B && C != A) {
				etiquette++;
				EC = etiquette;
			}
			else if (C == B && C == A && EA == EB)
				EC = EB;
			else if (C == B && C == A && EA != EB) {
				EC = EB;
				for (int k = nrl; k <= i; k++) {
					for (int l = ncl; l < nch; l++) {
						if (M[k][l] == EA)
							M[k][l] = EB;
					}
				}
			}
			else
				printf("Ya un truc bizarre :( \n");

			M[i][j] = EC;
		}
	}

	//printf("Nb etiquette = %d\n", etiquette);

	for (i = 0; i < nrh; i++) {
		for (j = 0; j < nch; j++) {
			R[i][j] = (M[i][j] * 255) / etiquette;
		}
	}
	//SavePGM_bmatrix(R,nrl,nrh,ncl,nch,"Img_etiquette.pgm");


	int* tab = new int[etiquette];
	for (i = 0; i < etiquette; i++) tab[i] = 0;

	int** new_points_interets;
	new_points_interets=imatrix0(0, 1, 0, nb_points_interets - 1);
	byte** img_extraite;
	img_extraite=bmatrix0(nrl,nrh,ncl,nch);
	float dist = nrh * nch;
	float sum_diff = INFINITY;
	int etiquette_plus_proche = M[0][0];

	//Rectangle englobant (zone de recherche)
	int debut_I = position_ancienne_etiquette[1] - rectangle_englobant;
	int fin_I = position_ancienne_etiquette[1] + rectangle_englobant;
	int debut_J = position_ancienne_etiquette[0] - rectangle_englobant;
	int fin_J = position_ancienne_etiquette[0] + rectangle_englobant;

	//Verif depassement
	if (debut_I < nrl)
		debut_I = nrl;
	if (fin_I > nrh)
		fin_I = nrh;
	if (debut_J < ncl)
		debut_J = ncl;
	if (fin_J > nch)
		fin_J = nch;

	//Parcours de la zone de recherche
	for (i = debut_I; i < fin_I; i++) {
		for (j = debut_J; j < fin_J; j++) {
			if (tab[M[i][j]] != 1) {
				tab[M[i][j]] = 1;

				//Extraction de l'etiquette
				img_extraite = extraction(M[i][j], img, M, nrl, nrh, ncl, nch);
				//Bounding box
				int ii, jj;
				int min_x = nch, min_y = nrh, max_x = 0, max_y = 0;
				for (ii = nrl; ii <= nrh; ii++) {
					for (jj = ncl; jj <= nch; jj++) {
						if (img_extraite[ii][jj] != 0) {
							if (jj < min_x) {
								min_x = jj;
							}
							if (jj > max_x) {
								max_x = jj;
							}
							if (ii < min_y) {
								min_y = ii;
							}
							if (ii > max_y) {
								max_y = ii;
							}
						}
					}
				}
				//Calcul nouveaux points interets
				new_points_interets = gradient(img_original, nb_points_interets, nrl, nrh, ncl, nch, min_x, max_x, min_y, max_y);

				//Comparaison
				float new_sum_diff = 0;/*TODO*/
				for (k = 0; k < nb_points_interets; k++) {
					new_sum_diff += abs(new_points_interets[2][k] - points_interets[2][k]);
				}

				if (sum_diff > new_sum_diff) {
					sum_diff = new_sum_diff;
					etiquette_plus_proche = M[i][j];
				}
			}
		}
	}
	delete[] tab;
	free_imatrix(M, nrl, nrh, ncl, nch);
	free_bmatrix(R, nrl, nrh, ncl, nch);
	free_imatrix(new_points_interets, 0, 2, 0, nb_points_interets - 1);
	free_bmatrix(img_extraite, nrl, nrh, ncl, nch);

	return etiquette_plus_proche;
}

/**
 * Cette fonction fait l'étiquetage d'une image et extrait la zone de l'étiquette donné en entrée.
 *
 * @param img L'image que l'on veut etiquetter.
 * @param no_etiquette Le numéro de l'étiquette que l'on veut extraire.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 * @param affichage_liste_etiquette Si VRAI alors on affiche sur la console la liste des étiquettes.
 *
 * @return L'image extraite correspondante à l'étiquette que l'on cherche.
 */
byte** etiquetage(byte** img, int no_etiquette, long nrl, long nrh, long ncl, long nch, BOOL affichage_liste_etiquette) {

	int** M;
	byte** R;

	M = imatrix0(nrl, nrh, ncl, nch);
	R = bmatrix0(nrl, nrh, ncl, nch);

	int i, j;
	int A = 0, B = 0, C = 0;
	int EA = 0, EB = 0, EC = 0;
	int etiquette = 0;
	for (i = nrl + 1; i < nrh; i++) {
		for (j = ncl + 1; j < nch; j++) {
			A = img[i][j - 1];
			B = img[i - 1][j];
			C = img[i][j];
			EA = M[i][j - 1];
			EB = M[i - 1][j];
			EC = M[i][j];
			// printf("%d, %d, %d, %d, %d, %d\n", A, B, C, EA, EB, EC);
			if (C == A && C != B)
				EC = EA;
			else if (C == B && C != A)
				EC = EB;
			else if (C != B && C != A) {
				etiquette++;
				EC = etiquette;
			}
			else if (C == B && C == A && EA == EB)
				EC = EB;
			else if (C == B && C == A && EA != EB) {
				EC = EB;
				for (int k = nrl; k <= i; k++) {
					for (int l = ncl; l < nch; l++) {
						if (M[k][l] == EA)
							M[k][l] = EB;
					}
				}
			}
			else
				printf("Ya un truc bizarre :( \n");

			M[i][j] = EC;
		}
	}

	// if(affichage_liste_etiquette)
	//     printf("Nb etiquette = %d\n", etiquette);

	for (i = 0; i < nrh; i++) {
		for (j = 0; j < nch; j++) {
			R[i][j] = (M[i][j] * 255) / etiquette;
		}
	}
	SavePGM_bmatrix(R, nrl, nrh, ncl, nch, (char *)"Img_etiquette.pgm");


	int* tab = new int[etiquette];;
	for (i = 0; i < etiquette; i++) tab[i] = 0;

	for (i = 0; i < nrh; i++) {
		for (j = 0; j < nch; j++) {
			if (tab[M[i][j]] != 1) {
				if (affichage_liste_etiquette)
					printf("%d\n", M[i][j]);

				tab[M[i][j]] = 1;
			}
		}
	}

	free_bmatrix(R, nrl, nrh, ncl, nch);
	delete[] tab;
	return extraction(no_etiquette, img, M, nrl, nrh, ncl, nch);
}

/**
 * Cette fonction calcul les coordonnées du centre de gravité d'une zone d'une image en noir et blanc.
 * (Le centre de gravité de la zone blanche)
 *
 * @param img L'image en noir et blanc.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return Un tableau d'entier de taille 2 contenant les coordonnées du centre de gravité(0:x 1:y).
 */
int* centre_gravite(byte** img, long nrl, long nrh, long ncl, long nch) {
	int i, j;
	float centre_x = 0;
	float centre_y = 0;
	float n_pixel = 0;
	for (i = nrl; i < nrh; i++) {
		for (j = ncl; j < nch; j++) {
			if (img[i][j] != 0) {
				centre_x += j;
				centre_y += i;
				n_pixel += 1;
			}
		}
	}

	int* centre = new int[2];

	centre[0] = (int)(centre_x / n_pixel);
	centre[1] = (int)(centre_y / n_pixel);

	return centre;
}

/**
 * Cette fonction crée un masque Gaussien.
 *
 * @param sigma L'écart-type du masque gaussien.
 *
 * @return Une matrice représentant le masque Gaussien (de taille 3x3 avec des indices allant de -1 à 1).
 */
double** masque_gaussien(double sigma) {
	double** G;
	G = dmatrix0(-1, 1, -1, 1);
	int x, y;
	for (y = -1; y <= 1; y++) {
		for (x = -1; x <= 1; x++) {
			G[y][x] = (1 / (2 * PI * (sigma * sigma))) * exp((-1) * (((double)(y * y) + (double)(x * x)) / (2 * (sigma * sigma))));
		}
	}
	return G;
}

/**
 * Cette fonction fait la convolution d'une image par un masque de taille 3x3.
 *
 * @param img L'image à convoluer.
 * @param filtre Le filtre que l'on applique.
 * @param diviseur Le diviseur par lequel on divise l'image.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return L'image convoluée.
 */
double** convolution(byte** img, double** filtre, double diviseur, long nrl, long nrh, long ncl, long nch) {
	double** resultat;
	resultat = dmatrix0(nrl, nrh, ncl, nch);
	int i, j;

	for (i = nrl + 1; i < nrh - 1; i++) {
		for (j = ncl + 1; j < nch - 1; j++) {
			resultat[i][j] = ((double)(img[i - 1][j - 1]) * filtre[-1][-1] + (double)(img[i][j - 1]) * filtre[0][-1] + (double)(img[i + 1][j - 1]) * filtre[1][-1] +
				(double)(img[i - 1][j]) * filtre[-1][0] + (double)(img[i][j]) * filtre[0][0] + (double)(img[i + 1][j]) * filtre[1][0] +
				(double)(img[i - 1][j + 1]) * filtre[-1][1] + (double)(img[i][j + 1]) * filtre[0][1] + (double)(img[i + 1][j + 1]) * filtre[1][1]) / diviseur;
		}
	}
	return resultat;
}

/**
 * Cette fonction fait l'opération de convolution sur un seul pixel d'une image par un masque de taille 3x3.
 *
 * @param img L'image à convoluer.
 * @param filtre Le filtre que l'on applique.
 * @param diviseur Le diviseur par lequel on divise l'image.
 * @param i L'indice en y du pixel à convoluer.
 * @param j L'indice en x du pixel à convoluer.
 *
 * @return Le pixel après la convolution.
 */
double convolution_1_pixel(double** img, double** filtre, double diviseur, int i, int j) {
	double resultat;
	resultat = (img[i - 1][j - 1] * filtre[-1][-1] + img[i][j - 1] * filtre[0][-1] + img[i + 1][j - 1] * filtre[1][-1] +
		img[i - 1][j] * filtre[-1][0] + img[i][j] * filtre[0][0] + img[i + 1][j] * filtre[1][0] +
		img[i - 1][j + 1] * filtre[-1][1] + img[i][j + 1] * filtre[0][1] + img[i + 1][j + 1] * filtre[1][1]) / diviseur;

	return resultat;
}

/**
 * Cette fonction fait la détection des points d'intérêts avec la méthode de Harris.
 *
 * @param img L'image dont on veut les points d'intérêts.
 * @param lambda Le paramètre lambda de la méthode.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return L'image avec les points d'intérêts.
 */
byte** harris(byte** img, double lambda, long nrl, long nrh, long ncl, long nch) {
	int i, j;

	double** dx_img;
	double** dy_img;
	double** dx2_img;
	double** dy2_img;
	double** dxy_img;

	dx_img = dmatrix0(nrl, nrh, ncl, nch);
	dy_img = dmatrix0(nrl, nrh, ncl, nch);
	dx2_img = dmatrix0(nrl, nrh, ncl, nch);
	dy2_img = dmatrix0(nrl, nrh, ncl, nch);
	dxy_img = dmatrix0(nrl, nrh, ncl, nch);

	double** SobelX;
	SobelX = dmatrix0(-1, 1, -1, 1);
	double** SobelY;
	SobelY = dmatrix0(-1, 1, -1, 1);

	SobelX[-1][-1] = -1; SobelX[-1][0] = 0; SobelX[-1][1] = 1;
	SobelX[0][-1] = -2;	 SobelX[0][0] = 0;  SobelX[0][1] = 2;
	SobelX[1][-1] = -1;  SobelX[1][0] = 0;  SobelX[1][1] = 1;

	SobelY[-1][-1] = -1; SobelY[-1][0] = -2; SobelY[-1][1] = -1;
	SobelY[0][-1] = 0;	 SobelY[0][0] = 0;  SobelY[0][1] = 0;
	SobelY[1][-1] = 1;  SobelY[1][0] = 2;  SobelY[1][1] = 1;

	dx_img = convolution(img, SobelX, 4, nrl, nrh, ncl, nch);
	dy_img = convolution(img, SobelY, 4, nrl, nrh, ncl, nch);

	//Ix^2 et Iy^2
	for (i = nrl; i <= nrh; i++) {
		for (j = ncl; j <= nch; j++) {
			dx2_img[i][j] = dx_img[i][j] * dx_img[i][j];
			dy2_img[i][j] = dy_img[i][j] * dy_img[i][j];
		}
	}

	//Ix*Iy
	for (i = nrl; i <= nrh; i++) {
		for (j = ncl; j <= nch; j++) {
			dxy_img[i][j] = dx_img[i][j] * dy_img[i][j];
		}
	}

	double** Gaussian;
	Gaussian = masque_gaussien(1);

	double** C;
	C = dmatrix0(nrl, nrh, ncl, nch);

	double dx2_conv;
	double dy2_conv;
	double dxy_conv;

	for (i = nrl + 1; i <= nrh - 1; i++) {
		for (j = ncl + 1; j <= nch - 1; j++) {
			dx2_conv = convolution_1_pixel(dx2_img, Gaussian, 1, i, j);
			dy2_conv = convolution_1_pixel(dy2_img, Gaussian, 1, i, j);
			dxy_conv = convolution_1_pixel(dxy_img, Gaussian, 1, i, j);

			C[i][j] = (dx2_conv * dy2_conv) - (dxy_conv)-(lambda * (dx2_conv + dy2_conv) * (dx2_conv + dy2_conv));
		}
	}

	// AFFICHAGE !!!
	double max = C[0][0];
	double min = C[0][0];
	for (i = nrl; i <= nrh; i++) {
		for (j = ncl; j <= nch; j++) {
			if (C[i][j] > max)
				max = C[i][j];
			if (C[i][j] < min)
				min = C[i][j];
		}
	}

	//printf("MAX = %f\nMIN = %f\n", max, min);

	byte** C_byte;
	C_byte = bmatrix0(nrl, nrh, ncl, nch);

	for (i = nrl; i <= nrh; i++) {
		for (j = ncl; j <= nch; j++) {
			/*C[i][j] = ((C[i][j]-min) / (max-min)) * 255.0;
			C_byte[i][j] = (byte) C[i][j];*/
			int tmp = 0;
			if (C[i][j] < 0)
				C_byte[i][j] = 0;
			else {
				tmp = (C[i][j] * 255) / max;
				C_byte[i][j] = (byte)tmp;
			}
		}
	}
	return C_byte;
}

/**
 * Cette fonction fait la détection des points d'intérêts avec la méthode des gradients dans une zone au choix.
 *
 * @param img L'image dont on veut les points d'intérêts
 * @param nb_points Le nombre de points d'intérêt que l'on veut.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 * @param miniX La coordonnée X de la gauche de la zone de recherche.
 * @param maxiX La coordonnée X de la droite de la zone de recherche.
 * @param miniY La coordonnée Y du haut de la zone de recherche.
 * @param maxiY La coordonnée Y du bas de la zone de recherche.
 *
 * @return Un tableau de 3 lignes contenant en [0][-]:y  en [1][-]:x   en [2][x]:le NDG
 */
int** gradient(byte** img, int nb_points, long nrl, long nrh, long ncl, long nch, long miniX, long maxiX, long miniY, long maxiY) {
	int i, j;

	double** dx_img;
	double** dy_img;
	double** dx2_img;
	double** dy2_img;
	double** dxy_img;

	//dx_img=dmatrix0(nrl, nrh, ncl, nch);
	//dy_img=dmatrix0(nrl, nrh, ncl, nch);
	dx2_img = dmatrix0(nrl, nrh, ncl, nch);
	dy2_img = dmatrix0(nrl, nrh, ncl, nch);
	dxy_img = dmatrix0(nrl, nrh, ncl, nch);

	double** SobelX;
	SobelX = dmatrix0(-1, 1, -1, 1);
	double** SobelY;
	SobelY = dmatrix0(-1, 1, -1, 1);

	SobelX[-1][-1] = -1; SobelX[-1][0] = 0; SobelX[-1][1] = 1;
	SobelX[0][-1] = -2;	 SobelX[0][0] = 0;  SobelX[0][1] = 2;
	SobelX[1][-1] = -1;  SobelX[1][0] = 0;  SobelX[1][1] = 1;

	SobelY[-1][-1] = -1; SobelY[-1][0] = -2; SobelY[-1][1] = -1;
	SobelY[0][-1] = 0;	 SobelY[0][0] = 0;  SobelY[0][1] = 0;
	SobelY[1][-1] = 1;  SobelY[1][0] = 2;  SobelY[1][1] = 1;

	dx_img = convolution(img, SobelX, 4, nrl, nrh, ncl, nch);
	dy_img = convolution(img, SobelY, 4, nrl, nrh, ncl, nch);

	//Ix^2 et Iy^2
	for (i = nrl; i <= nrh; i++) {
		for (j = ncl; j <= nch; j++) {
			dx2_img[i][j] = dx_img[i][j] * dx_img[i][j];
			dy2_img[i][j] = dy_img[i][j] * dy_img[i][j];
		}
	}

	//Ix*Iy
	for (i = nrl; i <= nrh; i++) {
		for (j = ncl; j <= nch; j++) {
			dxy_img[i][j] = dx_img[i][j] * dy_img[i][j];
		}
	}

	double** masque;
	masque = dmatrix0(-1, 1, -1, 1);

	masque[-1][-1] = 1; masque[-1][0] = 1; masque[-1][1] = 1;
	masque[0][-1] = 1;	 masque[0][0] = 0;  masque[0][1] = 1;
	masque[1][-1] = 1;  masque[1][0] = 1;  masque[1][1] = 1;

	double** K;
	K = dmatrix0(nrl, nrh, ncl, nch);

	double dx2_conv;
	double dy2_conv;
	double dxy_conv;

	for (i = nrl + 1; i <= nrh - 1; i++) {
		for (j = ncl + 1; j <= nch - 1; j++) {
			dx2_conv = convolution_1_pixel(dx2_img, masque, 1, i, j);
			dy2_conv = convolution_1_pixel(dy2_img, masque, 1, i, j);
			dxy_conv = convolution_1_pixel(dxy_img, masque, 1, i, j);

			K[i][j] = (dx2_img[i][j] * dy2_conv) + (dy2_img[i][j] * dx2_conv) - (2 * dxy_img[i][j] * dxy_conv);

			//Normalisation norme du gradient
			K[i][j] = K[i][j] / (dx2_conv + dy2_conv);
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

	int** tab_points_interet;
	tab_points_interet = imatrix0(0, 2, 0, nb_points - 1);
	double max;
	int i_ind_max;
	int j_ind_max;
	for (int point = 0; point < nb_points; point++) {
		max = K[0][0];
		i_ind_max = 0;
		j_ind_max = 0;
		for (i = miniY; i <= maxiY; i++) {
			for (j = miniX; j <= maxiX; j++) {
				if (K[i][j] > max) {
					max = K[i][j];
					i_ind_max = i;
					j_ind_max = j;
				}
			}
		}
		tab_points_interet[0][point] = i_ind_max;
		tab_points_interet[1][point] = j_ind_max;
		tab_points_interet[2][point] = K[i_ind_max][j_ind_max];
		K[i_ind_max][j_ind_max] = -INFINITY;

	}

	free_dmatrix(dx_img, nrl, nrh, ncl, nch);
	free_dmatrix(dy_img, nrl, nrh, ncl, nch);
	free_dmatrix(dx2_img, nrl, nrh, ncl, nch);
	free_dmatrix(dy2_img, nrl, nrh, ncl, nch);
	free_dmatrix(dxy_img, nrl, nrh, ncl, nch);
	free_dmatrix(SobelX, -1, 1, -1, 1);
	free_dmatrix(SobelY, -1, 1, -1, 1);
	free_dmatrix(masque, -1, 1, -1, 1);
	free_dmatrix(K, nrl, nrh, ncl, nch);

	return tab_points_interet;
}

/**
 * Cette fonction dessine un carré autour de la zone blanche de l'image binaire sur l'image d'origine.
 *
 * @param img L'image d'origine.
 * @param img_b L'image binaire.
 * @param nrl L'indice minimum des lignes.
 * @param nrh L'indice maximum des lignes.
 * @param ncl L'indice minimum des colonnes.
 * @param nch L'indice maximum des colonnes.
 *
 * @return L'image d'origine modifiée.
 */
rgb8** draw_box(rgb8** img, byte** img_b, long nrl, long nrh, long ncl, long nch) {
	int i, j;
	int min_x = nch, min_y = nrh, max_x = 0, max_y = 0;
	for (i = nrl; i <= nrh; i++) {
		for (j = ncl; j <= nch; j++) {
			if (img_b[i][j] != 0) {
				if (j < min_x) {
					min_x = j;
				}
				if (j > max_x) {
					max_x = j;
				}
				if (i < min_y) {
					min_y = i;
				}
				if (i > max_y) {
					max_y = i;
				}
			}
		}
	}
	// dessiner la boîte sur l'image "img"
	for (i = min_y; i <= max_y; i++) {
		img[i][min_x].r = 255; // ligne verticale gauche
		img[i][min_x].g = 0;
		img[i][min_x].b = 0;
		img[i][max_x].r = 255; // ligne verticale droite
		img[i][max_x].g = 0;
		img[i][max_x].b = 0;
	}
	for (j = min_x; j <= max_x; j++) {
		img[min_y][j].r = 255; // ligne horizontale supérieure
		img[min_y][j].g = 0;
		img[min_y][j].b = 0;
		img[max_y][j].r = 255; // ligne horizontale inférieure
		img[max_y][j].g = 0;
		img[max_y][j].b = 0;
	}

	return img;
}
