#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
  pid_t rv1, rv2;
  printf("[%8d/%8d] printf-1 Executing main process\n", (int)getpid(),
         (int)getppid());

  rv1 = fork();

  printf("[%8d/%8d] printf-2  First  fork(), returned value : %8d\n",
         (int)getpid(), (int)getppid(), rv1);

  rv2 = fork();
  if (rv2 == 0)
       sleep(1);
  printf("[%8d/%8d] printf-3  Second fork(), returned value : %8d\n",
         (int)getpid(), (int)getppid(), rv2);

  return 0;
}

/*

1-2]

[ 564682/ 556709] printf-1 Executing main process
[ 564682/ 556709] printf-2 First fork(), returned value : 564683
[ 564683/ 564682] printf-2 First fork(), returned value : 0
[ 564682/ 556709] printf-3 Second fork(), returned value : 0
[ 564684/ 564682] printf-3 Second fork(), returned value : 0
[ 564683/ 564682] printf-3 Second fork(), returned value : 0
[ 564685/ 564683] printf-3 Second fork(), returned value : 0

Shell : 556709
Enfant de shell : 564682
Enfants de 564682 : 564683 et 564684
Enfant de 564683 : 564685 (donc 564685 est le grandchild de 564682)

3]

Lorsque le processus grandchild execute la commande sleep(), tous les autres processus terminent, sauf les 2 processus enfants créés par la commande fork pour rv2
Conséquence : Ces deux processus sont orphelins et sont adoptés par le processus 1 avant de terminer
*/

