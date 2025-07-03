#include <signal.h>
#include <stdio.h>
#include <unistd.h>
/* See https://pubs.opengroup.org/onlinepubs/009695399/functions/sigaction.html
 * for a full description of sigaction */

int main(int argc, char *argv[]) {
  int sig;
  struct sigaction sa;
  for (sig = 1; sig < NSIG; sig++) {
    /* For now, we do not use any option. By default, the signal handler
     * sa_handler is used */
    sa.sa_flags = 0;

    /* sa.sa_sigaction is the pointer to a signal-catching function */
    sa.sa_handler = SIG_IGN;

    /* For now, we do not use any mask. By default, the signal received is
     * included in mask */
    sigemptyset(&sa.sa_mask);

    if (sigaction(sig, &sa, NULL) == -1)
      printf("Failed to change handler for signal %d\n", sig);
  }

  /* Wait for receiving signals */
  int delay = 30;
  while (delay != 0)
    delay = sleep(delay);

  return 0;
}
