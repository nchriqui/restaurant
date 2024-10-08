#include "contour.h"

int main(void) {
	// Initialisation de la graine du générateur aléatoire
	

	long nrh, nrl, nch, ncl;
	rgb8** Image = LoadPPM_rgb8matrix((char*)"fraises.ppm", &nrl, &nrh, &ncl, &nch);;
	byte** Image_pgm = PpmToPgm(Image, nrl, nrh, ncl, nch);

	byte** Image_contour = detectionContour (Image_pgm, nrl, nrh, ncl, nch);
	//byte** Image_etiquetage = etiquetage(Image_contour, nrl, nrh, ncl, nch);

	SavePGM_bmatrix(Image_contour, nrl, nrh, ncl, nch,(char *) "faises_contour.pgm");
	//SavePGM_bmatrix(Image_etiquetage, nrl, nrh, ncl, nch, (char*)"kids_e.pgm");

	/* ###############################################################################################################"" */
	free_bmatrix(Image_contour, nrl, nrh, ncl, nch);
	//free_bmatrix(Image_etiquetage, nrl, nrh, ncl, nch);
	free_bmatrix(Image_pgm, nrl, nrh, ncl, nch);
	free_rgb8matrix(Image, nrl, nrh, ncl, nch);

	//rgb8** Image_ppm = LoadPPM_rgb8matrix((char*)"banane2.ppm", &nrl, &nrh, &ncl, &nch);
	//auto start = std::chrono::high_resolution_clock::now();

	//rgb8** Image_etiquetage = etiquetage_evolue(Image_ppm, nrl, nrh, ncl, nch);
	//
	//
	//auto end = std::chrono::high_resolution_clock::now();
	//// Calcul de la durée écoulée en nanosecondes
	//auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);

	//// Affichage du temps d'exécution en secondes
	//std::cout << "Temps d'execution: " << duration.count() / 1e9 << " secondes" << std::endl;

	//
	
	//byte** Image_pgm = PpmToPgm(Image_ppm, nrl, nrh, ncl, nch);
	//SavePGM_bmatrix(Image_pgm, nrl, nrh, ncl, nch, (char*)"kids.pgm");
	
	//free_bmatrix(Image_pgm, nrl, nrh, ncl, nch);
	//free_rgb8matrix(Image_ppm, nrl, nrh, ncl, nch);
	//SavePPM_rgb8matrix(Image_etiquetage, nrl, nrh, ncl, nch,(char *)"banane_2.ppm");
	//free_rgb8matrix(Image_etiquetage, nrl, nrh, ncl, nch);
	//PpmToPgm((char *)"jaune");


	return 1;
}
rgb8** PgmToPpm(rgb8** Image_ppm, byte** Image_pgm, long nrl, long nrh, long ncl, long nch) {
}
int min(int a, int b) {
	return (a < b) ? a : b;
}
int max(int a, int b) {
	return (a > b) ? a : b;
}
rgb8** etiquetage_evolue(rgb8** Image_ppm, long nrl, long nrh, long ncl, long nch) {
	const int taille = 100000; // Taille du tableau
	int T[taille];

	for (int i = 0; i < taille; ++i) {
		T[i] = i;
	}


	byte** Image_pgm = PpmToPgm(Image_ppm, nrl, nrh, ncl, nch);
	Image_pgm = detectionContour(Image_pgm, nrl, nrh, ncl, nch);

	int** E = imatrix0(nrl, nrh, ncl, nch);
	int tmp = 0;

	int maxOccurrences = 0;
	int valueWithMaxOccurrences = 0;

	int retourimage = 0;

	for (long i = 0; i < nrh; i++)
	{
		for (long j = 0; j < nch; j++)
		{
			int att_a;
			int att_b;
			int att_c = Image_pgm[i][j];

			int E_c = E[i][j];
			int E_a;
			int E_b;


			if (i != 0 && j != 0) {
				att_a = Image_pgm[i][j - 1];
				att_b = Image_pgm[i - 1][j];
				E_a = E[i][j - 1];
				E_b = E[i - 1][j];
			}
			else if (i != 0 && j == 0) {
				att_a = -10;
				att_b = Image_pgm[i - 1][j];
				E_a = -10;
				E_b = E[i - 1][j];
			}
			else  if (i == 0 && j != 0) {
				att_a = Image_pgm[i][j - 1];
				att_b = 20;
				E_a = E[i][j - 1];
				E_b = 20;
			}
			else {
				att_a = -45;
				att_b = -22;
				E_a = -54;
				E_b = -10;
			}




			if (att_c == att_a && att_c != att_b) {
				E[i][j] = E_a; //E(c) = E(a)
			}
			else if (att_c == att_b && att_c != att_a) {
				E[i][j] = E_b; //E(c) = E(b)
			}
			else if (att_c != att_b && att_c != att_a) {
				E[i][j] = tmp;
				tmp++;
			}
			else if (att_c == att_b && att_c == att_a && E_a == E_b) {
				E[i][j] = E_b;
			}
			else if (att_c == att_b && att_c == att_a && E_a != E_b) {
				E[i][j] = min(T[E_b], E_a);
				T[E[i][j]] = E[i][j];
				T[E_a] = E[i][j];
				int mx = max(T[E_b], E_a);
				T[mx] = E[i][j];
			}
		}

			for (int r = 0; r < nrh; r++)
			{
				for (int c = 0; c < nch; c++)
				{	
					E[r][c] = T[E[r][c]];
				}
			}

	}


	rgb8** Image_resultat = rgb8matrix0(nrl, nrh, ncl, nch);
	std::unordered_map<int, int> occurrences;

	// Parcours du tableau et comptage des occurrences


	for (int i = 0; i < nrh; ++i) {
		for (int j = 0; j < nch; ++j) {
			int value = E[i][j];
			occurrences[value]++;
			if (occurrences[value] > maxOccurrences) {
				maxOccurrences = occurrences[value];
				valueWithMaxOccurrences = value;
			}
		}
	}
	//std::cout << "Valeur qui se répète le plus : " << valueWithMaxOccurrences << " nobre d'occurance :" << maxOccurrences << std::endl;

	for (int i = 0; i < nrh; ++i) {
		for (int j = 0; j < nch; ++j) {
			if (E[i][j] != valueWithMaxOccurrences) {
				Image_resultat[i][j] = Image_ppm[i][j];
			}
		}
	}
	printf("retour image %d:\n", retourimage);
	return Image_resultat;
}




rgb8 ** etiquetage(rgb8** Image_ppm, long nrl, long nrh, long ncl, long nch) {

	byte** masque = bmatrix0(0, 1, 0, 1);
	byte** Image_pgm = PpmToPgm(Image_ppm,nrl, nrh, ncl, nch);
	Image_pgm = detectionContour(Image_pgm , nrl, nrh, ncl, nch);

	int** E = imatrix0(nrl, nrh, ncl, nch);
	int tmp = 0; 

	int maxOccurrences = 0;
	int valueWithMaxOccurrences = 0;

	int retourimage = 0;

	for (long i = 0; i < nrh; i++)
	{
		for (long j = 0; j < nch; j++)
		{
			int att_a;
			int att_b;
			int att_c = Image_pgm[i][j];

			int E_c = E[i][j];
			int E_a;
			int E_b;


			if (i!=0 && j!=0 ) {
				att_a = Image_pgm[i][j - 1];
				att_b = Image_pgm[i - 1][j];
				E_a = E[i][j - 1];
				E_b = E[i - 1][j];
			}
			else if (i != 0 && j ==0 ) {
				att_a = -10;
				att_b = Image_pgm[i - 1][j];
				E_a =  -10;
				E_b = E[i - 1][j];
			}
			else  if (i == 0 && j != 0) {
				att_a = Image_pgm[i][j - 1];
				att_b =20;
				E_a = E[i][j - 1];
				E_b = 20;
			}
			else {
				att_a = -45;
				att_b = -22;
				E_a = -54;
				E_b = -10;
			}




			if (att_c == att_a && att_c != att_b) {
				E[i][j] = E_a; //E(c) = E(a)
			}
			else if (att_c == att_b && att_c != att_a) {
				E[i][j] = E_b; //E(c) = E(b)
			}
			else if (att_c != att_b && att_c != att_a) {
				E[i][j] = tmp;
				tmp++;
			}
			else if (att_c == att_b && att_c == att_a && E_a == E_b) {
				E[i][j] = E_b;
			}
			else if (att_c == att_b && att_c == att_a && E_a != E_b) {
				E[i][j] = E_b;
				for (long r = 0; r < nrh; r++)
				{
					for (long c= 0; c < nch; c++){
						if (E[r][c] == E_a) {
							E[r][c] = E_b;
							retourimage++;
						}
					}

				}
			}
		}

	}


	rgb8 ** Image_resultat = rgb8matrix0(nrl, nrh, ncl, nch);
	std::unordered_map<int, int> occurrences;

	// Parcours du tableau et comptage des occurrences


	for (int i = 0; i < nrh; ++i) {
		for (int j = 0; j < nch; ++j) {
			int value = E[i][j];
			occurrences[value]++;
			if (occurrences[value] > maxOccurrences) {
				maxOccurrences = occurrences[value];
				valueWithMaxOccurrences = value;
			}
		}
	}
	//std::cout << "Valeur qui se répète le plus : " << valueWithMaxOccurrences << " nobre d'occurance :" << maxOccurrences << std::endl;

	for (int i = 0; i < nrh; ++i) {
		for (int j = 0; j < nch; ++j) {
			if (E[i][j] != valueWithMaxOccurrences) {
				Image_resultat[i][j] = Image_ppm[i][j];
			}
		}
	}
	printf("retour image %d:\n", retourimage);
	return Image_resultat;
}
byte** PpmToPgm(rgb8** Image_ppm, long nrl, long nrh, long ncl, long nch){
	byte** Image_pgm;
	Image_pgm = bmatrix0(nrl, nrh, ncl, nch);
	for (long i = 0; i < nrh; i++)
	{
		for (long j = 0; j < nch; j++)
		{
			rgb8 pixel = Image_ppm[i][j];
			Image_pgm[i][j] = (pixel.b + pixel.g + pixel.r) / 3;
		}

	}
	return Image_pgm;
		
}
byte** detectionContour(byte** Image_pgm, long nrl, long nrh, long ncl, long nch) {

	/* -- Filtre moyenneur #############################################F##################################################################"" */

	//byte** moy = bmatrix0(nrl, nrh, ncl, nch);
	//byte** M = bmatrix0(0, 2, 0, 2);
	//for (int i = 0; i <= 2; i++)
	//{
	//	for (int j = 0; j < 2; j++)
	//	{
	//		M[i][j] = 1;
	//	}
	//}
	//for (long i = 1; i < nrh; i++)
	//{
	//	for (long j = 1; j < nch; j++)
	//	{
	//		moy[i][j] = (M[0][0] * Image_pgm[i - 1][j - 1] + M[0][1] * Image_pgm[i - 1][j] + M[0][2] * Image_pgm[i - 1][j + 1]
	//			+ M[1][0] * Image_pgm[i][j - 1] + M[1][1] * Image_pgm[i][j] + M[1][2] * Image_pgm[i][j + 1]
	//			+ M[2][0] * Image_pgm[i + 1][j - 1] + M[2][1] * Image_pgm[i + 1][j] + M[2][2] * Image_pgm[i + 1][j + 1]) / 9;
	//	}

	//}

	// SavePGM_bmatrix(moy, nrl, nrh, ncl, nch, (char*)"moy_1.pgm");
	/* Gradient_vertical ###############################################################################################################"" */
	
	byte** Gradient_vertical = bmatrix0(nrl, nrh, ncl, nch);
	int k = 0;
	for (long i = 1; i < nrh; i++)
	{
		for (long j = 1; j < nch; j++)
		{
			k = ((-Image_pgm[i - 1][j - 1] - (2 * Image_pgm[i - 1][j]) - Image_pgm[i - 1][j + 1] + Image_pgm[i + 1][j - 1] + (2 * Image_pgm[i + 1][j]) + Image_pgm[i + 1][j + 1]) / 4);
			Gradient_vertical[i][j] = abs(k);
		}

	}

	//SavePGM_bmatrix(Gradient_vertical, nrl, nrh, ncl, nch, (char*)"Gradient_vertical.pgm");
	
	
	/*  Gradient_horizental  ###############################################################################################################"" */

	byte** Gradient_horizental = bmatrix0(nrl, nrh, ncl, nch);

	for (long i = 1; i < nrh; i++)
	{
		for (long j = 1; j < nch; j++)
		{
			k = (-Image_pgm[i - 1][j - 1] + Image_pgm[i - 1][j + 1]
				- (2 * Image_pgm[i][j - 1]) + (2 * Image_pgm[i][j + 1])
				- Image_pgm[i + 1][j - 1] + Image_pgm[i + 1][j + 1]) / 4;
			Gradient_horizental[i][j] = abs(k);
		}
	}

	//SavePGM_bmatrix(Gradient_horizental, nrl, nrh, ncl, nch, (char*)"Gradient_horizental.pgm");
	 
	/* Norme_du_gradient ###############################################################################################################"" */
	byte** Norme_du_gradient = bmatrix0(nrl, nrh, ncl, nch);
	double tmp;
	for (long i = 1; i < nrh; i++)
	{
		for (long j = 1; j < nch; j++)
		{

			tmp = sqrt((Gradient_vertical[i][j] * Gradient_vertical[i][j]) + (Gradient_horizental[i][j] * Gradient_horizental[i][j]));
			Norme_du_gradient[i][j] = (byte)tmp;
		}
	}
	// SavePGM_bmatrix(Norme_du_gradient, nrl, nrh, ncl, nch, (char*)"Norme_du_gradient.pgm");
	/* ###############################################################################################################"" */

	byte** contour = bmatrix0(nrl, nrh, ncl, nch);

	for (long i = 0; i <= nrh; i++)
	{
		for (long j = 0; j <= nch; j++)
		{
			if (Norme_du_gradient[i][j] < 15)
			{
				contour[i][j] = 255;
			}
		}

	}
	//SavePGM_bmatrix(contour, nrl, nrh, ncl, nch, (char*)"cubes_Contour.pgm");
	free_bmatrix(Norme_du_gradient, nrl, nrh, ncl, nch);
	free_bmatrix(Gradient_horizental, nrl, nrh, ncl, nch);
	free_bmatrix(Gradient_vertical, nrl, nrh, ncl, nch);
	/*free_bmatrix(moy, nrl, nrh, ncl, nch);*/
	return contour;


}