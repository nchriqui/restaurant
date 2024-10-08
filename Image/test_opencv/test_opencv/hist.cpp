#include "contour.h"


int testtest(void) 
{
	long nrh, nrl, nch, ncl;
	int size = 256;

	cv::VideoCapture cap(0);


	if (!cap.isOpened()) {
		std::cerr << "Impossible d'ouvrir le flux de la caméra." << std::endl;
		return -1;
	}

	// Créer une fenêtre pour afficher les images capturées
	cv::namedWindow("Camera", cv::WINDOW_NORMAL);

	int img_width = cap.get(cv::CAP_PROP_FRAME_WIDTH);
	int img_height = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
	int img_size = img_width * img_height;


	char filenameimage[20];
	bool isFirstIteration = true; // Indicateur pour savoir si c'est la première itération


	//calculeHistogramme();
	int tmp = 0;

	while (true) {
		// Capturer l'image
		cv::Mat frame;
		cap.read(frame);
		if (frame.empty()) {
			std::cerr << "Aucune image capturée." << std::endl;
			break;
		}
		if (!isFirstIteration) {
			std::string previousFilename = "img.ppm";
			remove(previousFilename.c_str());
		}
		sprintf(filenameimage, "fomd%03d.ppm",tmp);
		FILE* file = fopen(filenameimage, "wb");
		if (!file)
		{
			fprintf(stderr, "Impossible de créer le fichier %s\n", filenameimage);
			return 1;
		}

		fprintf(file, "P6\n%d %d\n255\n", img_width, img_height);
		cv::cvtColor(frame, frame, cv::COLOR_BGR2RGB);
		fwrite(frame.data, 1, img_size * 3, file);

		fclose(file);
		isFirstIteration = false;

		cv::cvtColor(frame, frame, cv::COLOR_RGB2BGR);
		// Afficher l'image capturée
		cv::imshow("Camera", frame);

		// Attendre pendant 10 ms
		std::this_thread::sleep_for(std::chrono::milliseconds(100));
		//tauxDeRecemblance();
	

		//tauxDeRecemblance();
		// Vérifier si l'utilisateur a appuyé sur la touche 'q' pour quitter
		if (cv::waitKey(1) == 'q') {
			break;
		}
		tmp++;
	}

	// Fermer la fenêtre et libérer les ressources
	cv::destroyAllWindows();
	cap.release();

	return 0;


}
/*
*calculer la distance de Bhattacharyya
* @param hist1 histogramme de l'image 1
* @param hist2 histogramme de l'image 2
* @param size la taille des images
* @return distance: la distance de Bhattacharyya
*
*/
double computeBhattacharyyaDistance(image_histogram image, image_histogram image_actuel, int size) {
	double distance = 0.0;
	double distance_red = 0.0;
	double distance_green = 0.0;
	double distance_blue = 0.0;
	double sum1 = 0.0;
	double sum2 = 0.0;
	//red distance 
	for (int i = 0; i < size; i++) {
		distance_red += sqrt(image.red_histogram[i] * image_actuel.red_histogram[i]);
		sum1 += image.red_histogram[i];
		sum2 += image_actuel.red_histogram[i];
	}
	distance_red = sqrt(1.0 - (distance_red / sqrt(sum1 * sum2)));


	//green distance 
	sum1 = 0.0;
	sum2 = 0.0;
	for (int i = 0; i < size; i++) {
		distance_green += sqrt(image.green_histogram[i] * image_actuel.green_histogram[i]);
		sum1 += image.green_histogram[i];
		sum2 += image_actuel.green_histogram[i];
	}
	distance_green = sqrt(1.0 - (distance_green / sqrt(sum1 * sum2)));
	

	//blue distance 
	sum1 = 0.0;
	sum2 = 0.0;
	for (int i = 0; i < size; i++) {
		distance_blue += sqrt(image.blue_histogram[i] * image_actuel.blue_histogram[i]);
		sum1 += image.blue_histogram[i];
		sum2 += image_actuel.blue_histogram[i];

	}
	distance_blue = sqrt(1.0 - (distance_blue / sqrt(sum1 * sum2)));

	distance = (distance_red + distance_green + distance_blue) / 3.0;
	return distance;
}
/*
*calculer la distance de Bhattacharyya, méthode 2
* @param hist1 histogramme de l'image 1
* @param hist2 histogramme de l'image 2
* @param size la taille des images
* @return distance: la distance de Bhattacharyya
* 
*/
double computeBhattacharyyaDistance2(int* hist1, int* hist2, int size) {
	double distance = 0.0;
//	double BhattacharyyaCoefficient=0.0;

	double sum1 = 0.0;
	double sum2 = 0.0;
	double* hist1d = new double[size];
	double* hist2d = new double[size];

	// Calcul des sommes des valeurs dans hist1 et hist2
	for (int i = 0; i < size; i++) {
		sum1 += hist1[i];
		sum2 += hist2[i];	
	}

	// Normalisation des histogrammes
	for (int i = 0; i < size; i++) {
		hist1d[i] = hist1[i]/sum1;
		hist2d[i] = hist2[i] / sum2;
	}


	// Calcul de la distance de Bhattacharyya
	for (int i = 0; i < size; i++) {
		distance += sqrt(hist1d[i] * hist2d[i]);
	}

	distance = sqrt(1.0 - distance);


	return distance;
}

void saveHistogramToFile( image_histogram histogram,  int size) {
	std::ofstream file("histogram.csv", std::ios::app); // Ouvre le fichier en mode ajout (append)

	if (!file.is_open()) {
		std::cout << "Erreur lors de l'ouverture du fichier." << std::endl;
		return;
	}

	// Écriture des valeurs de l'histogramme dans le fichier CSV
	file << histogram.imageName << ";"; // Nom de l'image dans la deuxième colonne

	for (int i = 0; i < size; i++) {
		file << histogram.red_histogram[i]<<",";
	}
	file <<";";
	for (int i = 0; i < size; i++) {
		file << histogram.green_histogram[i] << ",";
	}
	file << ";";
	for (int i = 0; i < size; i++) {
		file << histogram.blue_histogram[i] << ",";
	}
	file << ";";

	file << std::endl; // Nouvelle ligne pour l'entrée suivante

	file.close(); // Ferme le fichier
}


std::vector<image_histogram> readHistogramsFromFile(const std::string& filename)
{
	std::ifstream file(filename);
	std::vector<image_histogram> histograms;

	if (!file.is_open()) {
		std::cout << "Impossible d'ouvrir le fichier " << filename << std::endl;
		return histograms;
	}

	std::string line;
	while (std::getline(file, line)) {
		std::istringstream iss(line);
		std::string token;
		image_histogram histogram;

		// Lire le nom de l'image dans la deuxième colonne
		std::getline(iss, histogram.imageName, ';');
		
		// Lire les valeurs de l'histogramme rouge
		std::getline(iss, token, ';');
		std::istringstream redIss(token);
		int i = 0;
		while (std::getline(redIss, token, ',')) {
			histogram.red_histogram[i] = std::stoi(token);
			i++;
		}

		// Lire les valeurs de l'histogramme vert
		std::getline(iss, token, ';');
		std::istringstream greenIss(token);
		i = 0;
		while (std::getline(greenIss, token, ',')) {
			histogram.green_histogram[i] = std::stoi(token);
			i++;
		}

		// Lire les valeurs de l'histogramme bleu
		std::getline(iss, token, ';');
		std::istringstream blueIss(token);
		i = 0;
		while (std::getline(blueIss, token, ',')) {
			histogram.blue_histogram[i] = std::stoi(token);
			i++;
		}

		histograms.push_back(histogram);
	}

	file.close();
	return histograms;
}


double tauxDeRecemblance() {
	long nrh, nrl, nch, ncl;
	int size = 256;
	rgb8** Image_actuelle = LoadPPM_rgb8matrix((char *)"img.ppm", &nrl, &nrh, &ncl, &nch);
	rgb8** Image_etiquetage = etiquetage_evolue(Image_actuelle, nrl, nrh, ncl, nch);

	image_histogram image_act;
	
	image_act.imageName = "image actuelle";


	for (size_t i = 0; i < nrh; i++) {
		for (size_t j = 0; j < nch; j++) {
			rgb8 pixel = Image_etiquetage[i][j];
			image_act.red_histogram[pixel.r]++;
			image_act.green_histogram[pixel.g]++;
			image_act.blue_histogram[pixel.b]++;
		}
	}
	image_act.red_histogram[0] = 1;
	image_act.green_histogram[0] = 1;
	image_act.blue_histogram[0]=1;

	std::string filename = "histogram.csv";
	std::vector<image_histogram> histograms = readHistogramsFromFile(filename);

	// Utiliser le tableau d'histogrammes
	for (const auto& histogram : histograms) {
		// Faire quelque chose avec chaque histogramme

		double distance = computeBhattacharyyaDistance(histogram, image_act, size);
		std::cout << "taux de ressemblance avec l'image : " << histogram.imageName << "  est:" << distance << std::endl;
	}
}


void calculeHistogramme() {
	long nrh, nrl, nch, ncl;
	char* file = (char*)"banane_0.ppm";
	rgb8** Image_jaune = LoadPPM_rgb8matrix(file, &nrl, &nrh, &ncl, &nch);


	image_histogram jaune;
	jaune.imageName = "banane étiquetage_0";
	//vert.imageName = "vert";


	for (size_t i = 0; i < nrh; i++) {
		for (size_t j = 0; j < nch; j++) {
			rgb8 pixel = Image_jaune[i][j];
			jaune.red_histogram[pixel.r]++;
			jaune.green_histogram[pixel.g]++;
			jaune.blue_histogram[pixel.b]++;
		}
	}
	jaune.red_histogram[0]=1;
	jaune.green_histogram[0]=1;
	jaune.blue_histogram[0]=1;

	int size = 256;

	saveHistogramToFile(jaune, size);
}