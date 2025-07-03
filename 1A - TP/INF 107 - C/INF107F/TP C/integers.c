#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

_Bool isNegative(int n)
{
    _Bool result;
    n=n>>31;
    result = (n&1);
    return(result);
}


int main(int argc, char *argv[]) {
  printf("%d\n",isNegative(-2457));
}
