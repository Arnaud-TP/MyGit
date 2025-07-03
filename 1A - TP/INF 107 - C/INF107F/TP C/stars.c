#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

struct star_structure 
{ 
    long ns_id; // Numerical Star Identifier
    char name[21]; // Name of the star
    char short_cons[4]; // 3 letters acronym of the star's constellation
    int dist; // Distance from Earth to star in Parsec (3,086e+16 m)
    double magn; // Absolute star magnitude
};
typedef struct star_structure star_t;
star_t mon_etoile1 = {30365,"Canopus","Car", 94,-0.62};

void starInit(star_t *star)
{
    //(*star).ns_id = 0; // Déréférencement puis attribution
    star->ns_id = 0; // Effectue la même opération 
    star-> dist = 0;
    star -> magn = 0;
    for (int i = 0;i<21;i++) star -> name[i] = '\0';
    for (int i = 0;i<4;i++) star -> short_cons[i] = '\0';
}

void printStar(FILE *stream, const star_t *star)
{
    if (fprintf(stream, "\nNumeric ID : %6ld \nConstellation's acronym : %3s \nDistance from Earth to Star in Parsec (3,086e+16 m) : %3d \nAbsolute Star Magnitude : %+5.2f \nStar Name : %s \n", star->ns_id, star->short_cons,star->dist,star->magn,star->name) < 0) {
        perror("fprintf");
        exit(EXIT_FAILURE);
    }
    exit(EXIT_SUCCESS);
}


char *splitPrefix(char *s, char delimiter)
{
    for (char *ptr = s; *ptr != '\0'; ++ptr)
    {
        if (*ptr == delimiter)
            {
                *ptr = '\0';
                return(ptr+1);
            } 
    }
    return(NULL);
}

_Bool readStar(FILE *fptr, star_t *sptr)
{
    char* stri = NULL;
    long id;
    float distance;
    float magnitude;
    if (fscanf(fptr, "%ld , %21s , %f , %f", &id, stri, &distance, &magnitude))
    {
        perror("fscanf");
        exit(EXIT_FAILURE);
    }
    if (fscanf(fptr, "%ld , %21s , %f , %f", &id, stri, &distance, &magnitude) == EOF)
    {
        starInit(sptr);
        return(1);
    }
    fscanf(fptr, "%ld , %21s , %f , %f", &id, stri, &distance, &magnitude);
    starInit(sptr);
    sptr -> ns_id = id;
    sptr-> dist = (int)distance;
    sptr -> magn = magnitude;
    char* in1 = stri;
    char* out1 = splitPrefix(in1, ':');
    strncpy(sptr -> short_cons, in1, sizeof(sptr -> short_cons));
    strncpy(sptr -> name , out1, sizeof(sptr -> name));
    return(0);
}

void openFile(const char* filename)
{
    FILE *fileptr;
    star_t* star_data[312];
    if (fopen(filename, "r") == NULL)
    {
        perror("fopen");
        exit(EXIT_FAILURE);
    }
    fileptr = fopen(filename, "r");
    int i=0;
    while (readStar(fileptr, star_data[i]))
    {
        printStar(stdout, star_data[i]);
        i++;
    }
    if (fclose(fileptr))
    {
        perror("fclose");
        exit(EXIT_FAILURE);
    }
    exit(EXIT_SUCCESS);
}

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        fprintf(stderr,"Error : Program takes 2 arguments");
        exit(EXIT_FAILURE);
    }
    openFile(argv[1]);
    exit(EXIT_SUCCESS);
}

/*

2.2.2) printStar(stdout, &mon_etoile1); Ligne de test

2.2.3) wc --line stars.csv   nous donne 311 lignes
fscanf(f, "%d", ,&id); 

fscanf reçoit une COPIE de ses arguments, 
on a besoin d'une fonction qui puisse modifier un de ses arguments, 
donc de récupérer l'adresse de id et non sa valeur 
*/


//Principe de liste chaînée pour créer un tableau de taille dynamique, n'est pas constitutif en mémoire
// Avantages : Facile d'ajouter / supprimer des éléments

// A l'examen : quand on crée un pointeur, on alloue de la mémoire au pointeur lui-même, pas à l'objet, et on ne peut pas l'utiliser (pointe aléatoirement dans la mémoire) -> On peut utiliser malloc ou attribué directement le pointeur pour pouvoir l'utiliser

