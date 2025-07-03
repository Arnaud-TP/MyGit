#include <assert.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

#define MAXLEN 32

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("Usage : %s <file-to-edit>>\n", argv[0]);
    exit(1);
  }
  int myfile = open(argv[1], O_RDWR);
  uint32_t value;
  int nbyte;
  int n;
  char answer[MAXLEN];
  int offset = 0;

  while (1) {
    offset = lseek(myfile, 0, SEEK_CUR); // Get the offset (index of the file) with lseek().
    nbyte = read(myfile, &value, sizeof(value)); //Read a unsigned integer of 32 bits. Check the result.
    if (nbyte == sizeof(value))
      printf("[%08x] %08x\n", offset, value);
    else
    {
      printf("[%08x] <EOF>\n", offset);
    }
    printf("value to edit or RET to skip : ");

    /* The fgets() function shall read bytes from stream into the array pointed
     * to by s, until n-1 bytes are read, or a <newline> is read and transferred
     * to s, or an end-of-file condition is encountered. The string is then
     * terminated with a null byte.
     */
    fgets(answer, MAXLEN, stdin); //Answer is just a new line
    if (strcmp(answer, "\n") == 0)
      continue;
    n = sscanf(answer, "%x", &value);
    if (n == 0)
      break;

    if (nbyte != 0) {
      /* We succeded to read a 32-bits unsigned integer. We are not at the end
       * of the file. We move the index back to modify the integer we read.
       */
    }
    
    nbyte = write(myfile, &value, sizeof(value));
    if (nbyte != sizeof(value))
    offset = lseek(myfile, offset, SEEK_SET);
      exit(EXIT_FAILURE); //Update the current 32-bits unsigned integer.
  

  /* We move the index back to modify the integer we wrote to allow the
  * program to read again.
  */
  }

  /*  Build a name for a temporary file by adding ".tmp" to the original filename
   */
  char * tmp_name = (char *) malloc (strlen(argv[1]) + 5);
  strcpy(tmp_name, argv[1]);
  strcat(tmp_name, ".tmp");

  /* Reset the file index at its beginning.
   */

/* Open the temporary file to write part of the original file
 */
  for (int i = 0; i < offset; i = i +sizeof(value)){
    /* Read 32-bits unsigned integer from original file and write it in the temporary file.
     */
  }

  /* Remove original file and rename temporary one.
   */

  /* Close files.
   */
}
