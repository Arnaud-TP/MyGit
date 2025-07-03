#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void child_function(int index);
void parent_function();

int main(int argc, char *argv[]) {
  int nb_of_processes, child_index, child_pid;

  /* Check that one parameter was provided */
  if (argc != 2) {
    printf(" Wrong usage, expected : %s number_of_processes ! \n", argv[0]);
    exit(2);
  }

  nb_of_processes = strtol(argv[1], NULL, 10); /* conversion ascii -> decimal integer */
  if (errno == EINVAL) {
    perror("Invalid decimal argument");
    exit(1);
  }

  /* ----------------------------------------
   *  creation of children processes
   * ----------------------------------------
   */
  for (child_index = 1; child_index <= nb_of_processes; child_index++) {
    child_pid = fork();
    switch (child_pid) {
    case 0:
      child_function(child_index); /* You have to write this function ... */
      break;
    case -1:
      perror("Fork just failed !!!");
      exit(2); /* exit in case an error occurred */
    }
  }
  parent_function();
}

void child_function(int index) {
  printf("executing child %d; child process %d, parent process %d\n", index, getpid(), getppid());
  printf("going to wait...\n");
  sleep(2 * index);
  int div_zero = 1 / (1 - index);
  exit(index);
}

void parent_function() {
  int rv = 0, state;
  while (rv != -1) {
    rv = wait(&state);
    if (rv != -1)
      printf("Child finished its exectuion, pid: %d,\nIts state was : %04x\n", rv, state);
  }
}
