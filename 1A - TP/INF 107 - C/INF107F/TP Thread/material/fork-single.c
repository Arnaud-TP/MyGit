#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
  pid_t rv;
  printf("[%8d/%8d] printf-0 Before fork()\n", (int)getpid(), (int)getppid());
  rv = fork();
  if (rv==0) // Si on est le processus enfant
  {
    sleep(1);
  }
  printf("[%8d/%8d] printf-1 After fork()\n", (int)getpid(), (int)getppid());
  printf("[%8d/%8d] printf-2 returned value : %d\n", (int)getpid(),
         (int)getppid(), rv);
  return 0;
}

/*
1]     (int)getppid() processus parent, correspond au shell -> se vérifie avec la commande ps sur le terminal
        Si on a 5 lignes qui s'affichent, c'est que lors de la commande du processus fork(), on a deux
        processus qui vont chacun faire printf de leur côté (2 premières par le processus parent, 2 dernières par le processus enfant)
        Le processus enfant est un clône du processus parent

        Chaque processus a un processus parent, et celui-ci DOIT ETRE VIVANT
        Ici avec la commande sleep(), on a terminé le processus parent tant que le processus enfant était en pause
          -> Conséquence, le processus orphelin doit être accepté par un processus parent (par défaut processus 1 accepte tout le monde)
*/
