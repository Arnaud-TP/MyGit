#include <stdio.h>
#include <unistd.h>

int main() {
  printf("\nsleeping ...\n");
  while (1) {
    printf("...\n");
    sleep(1);
  }
}
