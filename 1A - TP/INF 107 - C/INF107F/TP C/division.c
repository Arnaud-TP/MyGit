#include <stdio.h>
#include <stdlib.h>

unsigned int division(unsigned int dividend, unsigned int divisor) {
  unsigned int result = 0;
  for(unsigned int rest = dividend; rest >= divisor; result++)
    rest = rest - divisor;
  return result;
}

const char message[] = "Hello World";
short n = 48;
int division_result;

int main(int argc, char *argv[]) {
  division_result = division(n, 9);
  printf("%s\n", message);
  printf("%d\n", division_result);
  printf("%d\n", n);
  return EXIT_SUCCESS;
}
