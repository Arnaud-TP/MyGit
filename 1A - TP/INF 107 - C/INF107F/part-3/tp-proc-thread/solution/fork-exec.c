#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  if (argc < 2) {
    printf("Usage : %s command line\n", argv[0]);
    exit(1);
  }

  printf("[%8d/%8d] Execute main process\n", (int)getpid(), (int)getppid());
  int fork_rv = fork();

  switch (fork_rv) {
  case 0:
    printf("[%8d/%8d] After first fork()\n", (int)getpid(), (int)getppid());
    printf("[%8d/%8d] Replace my program by %s\n", (int)getpid(),
           (int)getppid(), argv[1]);

    /* Replace program */
#ifdef TEACHER
    execvp(argv[1], &argv[1]);
#endif

    printf("[%8d/%8d] Program %s does not exist (exit 2)\n", (int)getpid(),
           (int)getppid(), argv[1]);
    exit(2);

  case -1:
    printf("[%8d/%8d] Fork failed (exit 3)\n", (int)getpid(), (int)getppid());
    exit(3);

  default:
    /* Parent waiting for a child... */
    printf("[%8d/%8d] Wait for a child\n", (int)getpid(), (int)getppid());

    int wait_rv, status;
#ifdef TEACHER
    wait_rv = wait(&status);
#endif

    printf("[%8d/%8d] Wait resumed with returned value %d\n", (int)getpid(),
           (int)getppid(), wait_rv);
    printf("[%8d/%8d] ............. and status : 0x%04x (hexa)\n",
           (int)getpid(), (int)getppid(), status);
    exit(0);
  }
  return 0;
}
