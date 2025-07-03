#include <assert.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("Usage : %s <file-to-dump>>\n", argv[0]);
    exit(1);
  }
  int myfile = open(argv[1], O_RDONLY);
  uint32_t value;
  int nbyte;
  int offset = 0;
  while (1) {
    printf("%08x :", offset); // Print offset in the file
    for (int i = 0; i < 4; i++) { //Print 4 unsigned integers of 32 bits.
      nbyte = read(myfile, &value, sizeof(value));//Exit when we reach end of file or cannot read a value.
      printf("\t%08x", value); 
      if (nbyte != sizeof(value))
        exit(EXIT_FAILURE);
    }
    printf("\n");
    offset = offset + sizeof(value);
    if (nbyte != sizeof(value))
        break;
  }
  close(myfile);
  /* Close file before terminating. Done by default.
   */
}
