#include <stdlib.h>
#include <stdio.h>
#include <math.h>

const unsigned int n = 10000;
_Bool array[10000];

void sieve(void)
{
    for(int i=1; i<n; i++)
        array[i] = 1;
    for(int i=2; i <= 100 +1; i++)
        if (array[i]) for(int j=i; j<=n; j+=i) array[j]=0;
}


int main(int argc, char *argv[]) {
    sieve();
    int cpt = 0;
    for(int i=1; i<n;i++) if(array[i]) {
        printf("%d \t",i);
        cpt++;
        if (cpt == 3) {
            printf("\n");
            cpt = cpt - 3;
            }
    }
}
