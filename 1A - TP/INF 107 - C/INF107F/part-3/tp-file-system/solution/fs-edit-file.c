#include <assert.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAXLEN 32

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("Usage : %s <file-to-edit>>\n", argv[0]);
    exit(1);
  }

#ifdef TEACHER
  int fd = open(argv[1], O_CREAT | O_RDWR, 0644);
  assert(0 <= fd);
#endif

  uint32_t value;
  int nbyte;
  int n;
  char answer[MAXLEN];

  int offset = 0;

  while (1) {
    /* Get the offset (index of the file) with lseek().
     */
#ifdef TEACHER
    offset = lseek(fd, 0, SEEK_CUR);
#endif
    /* Read a unsigned integer of 32 bits. Check the result.
     */
#ifdef TEACHER
    nbyte = read(fd, &value, sizeof(value));
    assert(0 <= nbyte);
#endif

    if (nbyte == sizeof(value))
      printf("[%08x] %08x\n", offset, value);
    else
      printf("[%08x] <EOF>\n", offset);
    printf("value to edit or RET to skip : ");

    /* The fgets() function shall read bytes from stream into the array pointed
     * to by s, until n-1 bytes are read, or a <newline> is read and transferred
     * to s, or an end-of-file condition is encountered. The string is then
     * terminated with a null byte.
     */
    fgets(answer, MAXLEN, stdin);

    /* Answer is just a newline.
     */
    if (strcmp(answer, "\n") == 0)
      continue;
    
    n = sscanf(answer, "%x", &value);
    /* If the answer is not an hexadecimal integer, leave editor.
     */
    if (n == 0)
      break;

    if (nbyte != 0) {
      /* We succeded to read a 32-bits unsigned integer. We are not at the end
       * of the file. We move the index back to modify the integer we read.
       */
#ifdef TEACHER
      lseek(fd, -sizeof(value), SEEK_CUR);
#endif
    }

    /* Update the current 32-bits unsigned integer.
     */
#ifdef TEACHER
    nbyte = write(fd, &value, sizeof(value));
    assert(nbyte == sizeof(value));
#endif

    /* We move the index back to modify the integer we wrote to allow the
     * program to read again.
     */
#ifdef TEACHER
    lseek(fd, -sizeof(value), SEEK_CUR);
#endif
  }

  /*  Build a name for a temporary file by adding ".tmp" to the original filename
   */
  char * tmp_name = (char *) malloc (strlen(argv[1]) + 5);
  strcpy(tmp_name, argv[1]);
  strcat(tmp_name, ".tmp");

  /* Reset the file index at its beginning.
   */
#ifdef TEACHER
  lseek(fd, 0, SEEK_SET);
#endif

/* Open the temporary file to write part of the original file
 */
#ifdef TEACHER
  int tmp_fd = open(tmp_name, O_CREAT|O_WRONLY, 0644);
#endif
  for (int i = 0; i < offset; i = i +sizeof(value)){
    /* Read 32-bits unsigned integer from original file and write it in the temporary file.
     */
#ifdef TEACHER
    nbyte = read(fd, &value, sizeof(value));
    assert (nbyte == sizeof(value));
    nbyte = write(tmp_fd, &value, sizeof(value));
    assert (nbyte == sizeof(value));
#endif
  }

  /* Remove original file and rename temporary one.
   */
#ifdef TEACHER
  unlink(argv[1]);
  rename(tmp_name, argv[1]);
#endif

  /* Close files.
   */
#ifdef TEACHER
  close(fd);
  close(tmp_fd);
#endif
}
