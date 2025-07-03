#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
  pid_t rv;
  printf("[%8d/%8d] printf-0 Before fork()\n", (int)getpid(), (int)getppid());
  /* Create a new process
   */
#ifdef TEACHER
  rv = fork();
#endif
  printf("[%8d/%8d] printf-1 After fork()\n", (int)getpid(), (int)getppid());
  printf("[%8d/%8d] printf-2 returned value : %d\n", (int)getpid(),
         (int)getppid(), rv);
  return 0;
}