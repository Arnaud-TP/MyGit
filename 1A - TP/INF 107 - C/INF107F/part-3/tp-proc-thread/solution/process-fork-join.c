#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

void child_function(int index);
void parent_function();

int main(int argc, char *argv[]) {
  int nb_of_processes, child_index, child_pid;

  /* Check that one parameter was provided */
  if (argc != 2) {
    printf(" Wrong usage : %s number_of_processes\n", argv[0]);
    exit(1);
  }

  /* conversion ascii -> decimal integer */
  nb_of_processes = strtol(argv[1], NULL, 10);
  if (errno == EINVAL) {
    perror("Invalid decimal argument");
    exit(2);
  }

  if (nb_of_processes <= 0) {
    printf(" Wrong usage : %s number_of_processes (>0)\n", argv[0]);
    exit(3);
  }

  for (child_index = 1; child_index <= nb_of_processes; child_index++) {
    /* Implement the fork part of the fork-join model and create processes.
     */
#ifdef TEACHER
    child_pid = fork();
#endif
    switch (child_pid) {
    case 0:
      child_function(child_index);
    case -1:
      printf("[%8d/%8d] Fork failed\n", (int)getpid(), (int)getppid());
      exit(2); /* exit in case an error occurred */
    }
  }
  parent_function();
}

void child_function(int index) {
  printf("[%8d/%8d] Execute child of index %d\n", (int)getpid(), (int)getppid(),
         index);
  printf("[%8d/%8d] Child of index %d works or sleeps for %d seconds\n",
         (int)getpid(), (int)getppid(), index, 2 * index);
  sleep(2 * index);
  /* insert code : should all processes complete successfully ?
   */
#ifdef TEACHER
  int div_zero = 1 / (1 - index);
  printf("%d\n", div_zero);
#endif
  exit(index);
}

void parent_function() {
  int rv, status;
  while (1) {
    printf("[%8d/%8d] Wait for child completion\n", (int)getpid(),
           (int)getppid());
    /* Implement the join part of the fork-join model and wait for process
     * completion.
     */

#ifdef TEACHER
    rv = wait(&status);
#endif
    if (rv == -1) break;
    printf("[%8d/%8d] Child %8d completed with status 0x%04x\n",
           (int)getpid(), (int)getppid(), rv, status);
  }
  printf("[%8d/%8d] No child to wait for\n", (int)getpid(), (int)getppid());
}
