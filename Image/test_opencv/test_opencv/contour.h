#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<stdlib.h>
#include <opencv2/opencv.hpp>
#include "lib/def.h"
#include "lib/nrio.h"
#include "lib/nrarith.h"
#include "lib/nralloc.h"
#include <math.h>
#include <unordered_map>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <ctime>
#include <chrono>

#include <thread>


#include <sstream>
#include <string>
#include <vector>

struct ImageHistogram {
	std::string imageName;
	int red_histogram[256] = { 0 };
	int green_histogram[256] = { 0 };
	int blue_histogram[256] = { 0 };
};

typedef ImageHistogram image_histogram;

void saveHistogramToFile(image_histogram histogeram, int size);
double computeBhattacharyyaDistance2(int* hist1, int* hist2, int size);
double computeBhattacharyyaDistance(image_histogram image, image_histogram image_actuel, int size);
std::vector<image_histogram> readHistogramsFromFile(const std::string& filename);

double tauxDeRecemblance();

void calculeHistogramme();
int min(int a, int b);
int max(int a, int b);

byte** PpmToPgm(rgb8** Image_ppm, long nrl, long nrh, long ncl, long nch);
rgb8** etiquetage(rgb8** Image_ppm, long nrl, long nrh, long ncl, long nch);
byte** detectionContour(byte** Image_pgm, long nrl, long nrh, long ncl, long nch);
rgb8** PgmToPpm(rgb8** Image_ppm, byte** Image_pgm, long nrl, long nrh, long ncl, long nch);
rgb8** etiquetage_evolue(rgb8** Image_ppm, long nrl, long nrh, long ncl, long nch);
