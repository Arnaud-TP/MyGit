#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define OFFSET "\t\t\t\t\t\t\t"

int main() {
  printf("[%8d/%8d] Execute main process\n", (int)getpid(), (int)getppid());
  int fork_rv = fork();
  switch (fork_rv) {
  case 0:
    printf(OFFSET);
    printf("[%8d/%8d] fork() returned value %d\n", (int)getpid(),
           (int)getppid(), fork_rv);

    printf(OFFSET);
    printf("[%8d/%8d] Sleep for a 2 secondes\n", (int)getpid(), (int)getppid());

    sleep(2);

    printf(OFFSET);
    printf("[%8d/%8d] Wake up and exit 7\n", (int)getpid(), (int)getppid());

    exit(7);

  case -1:
    printf("[%8d/%8d] Fork failed\n", (int)getpid(), (int)getppid());
    exit(2);
  default:
    printf("[%8d/%8d] fork() returned value %d\n", (int)getpid(),
           (int)getppid(), fork_rv);
    printf("[%8d/%8d] Wait for child completion\n", (int)getpid(),
           (int)getppid());

    /* Wait for child completion
     */
    int wait_rv, status;
#ifdef TEACHER
    wait_rv = wait(&status);
#endif

    printf("[%8d/%8d] Resume after %8d completion\n", (int)getpid(),
           (int)getppid(), wait_rv);
    printf("[%8d/%8d] Child completed with status : 0x%04x\n", (int)getpid(),
           (int)getppid(), status);
  }
  return 0;
}
