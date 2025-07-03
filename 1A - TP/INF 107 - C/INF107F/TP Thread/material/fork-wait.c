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
    /*
    *p = 42;
    int * p = NULL;
    */
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

    int wait_rv, status;
wait_rv = wait(&status);
    printf("[%8d/%8d] Resume after %8d completion\n", (int)getpid(),
           (int)getppid(), wait_rv);
    printf("[%8d/%8d] Child completed with status : 0x%04x\n", (int)getpid(),
           (int)getppid(), status);
  }
  return 0;
}

/* Le programme renvoie :
[ 571245/ 571110] Execute main process
[ 571245/ 571110] fork() returned value 571246
[ 571245/ 571110] Wait for child completion
[ 571246/ 571245] fork() returned value 0
[ 571246/ 571245] Sleep for a 2 seconds
[ 571246/ 571245] Wake up and exit 7
[ 571245/ 571110] Resume after 571246 completion
[ 571245/ 571110] Exit with status : 0x0700

On a bien le processus parent qui attend le processus enfant pour terminer
On a de plus l'exit status qui a les deux bits faibles en hexa qui valent 0 (exit status)
       -> Dans le cas =/= 0, alors le processus enfant s'est fait erminer par une erreur ou autre
On a aussi l'exit status qui vaut bien 7..Si on rajoute le code (ligne 22), on a alors l'exit status qui vaut quelque chose différent de 0
       -> Due à l'erreur d'un pointeur nul déréférencé
*/
