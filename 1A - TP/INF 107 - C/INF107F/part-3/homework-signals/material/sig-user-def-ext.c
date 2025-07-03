#include <signal.h>
#include <stdio.h>
#include <unistd.h>
/* See https://pubs.opengroup.org/onlinepubs/009695399/functions/sigaction.html
 * for a full description of sigaction */

void my_sigaction(int sig, siginfo_t *info, void *context);

int main(int argc, char *argv[]) {
  int sig;
  struct sigaction sa;

  for (sig = 1; sig < NSIG; sig++) {
    /*
     * sa.sa_flags provides special flags to change default behavior of signal.
     * With SA_NODEFER, sig will not be added to the thread's signal mask on
     * entry to the signal handler
     */
    sa.sa_flags = SA_SIGINFO;

    /* sa.sa_sigaction is the pointer to a signal-catching function */
    sa.sa_sigaction = my_sigaction;

    /*
     * By default, on entry to the signal handler, the signal is always added to
     * the thread's signal mask. sa.sa_mask provides additional set of signals
     * to be blocked during execution of signal-catching function.
     */
    sigemptyset(&sa.sa_mask);

    if (sigaction(sig, &sa, NULL) == -1)
      printf("Failed to change handler for signal %d\n", sig);
  }

  /* Wait for signals */
  int delay = 30;
  while (delay != 0)
    delay = sleep(delay);
  return 0;
}

void my_sigaction(int sig, siginfo_t *info, void *context) {
  printf("Receive signal from %d\n", info->si_pid);
  printf("Enter signal handler %d\n", sig);
  sleep(3);
  printf("Leave signal handler %d\n", sig);
}
