#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#include "utils.h"

int value_between(int first, int last) {
  int length = last - first + 1;
  return first + (int)(rand() % length);
}

void init_random_value() { srand(getpid()); }

void delay_milli_sec(int ms){
  struct timespec t = {0, ms * 1000};
  nanosleep(&t, NULL);
}
