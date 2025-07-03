#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define LINE_SIZE 64

int main() {
  char cmd_line[LINE_SIZE];
  char sep[] = " \t\n";

  while (1) {
    printf("$ ");
    fflush(stdout);

    if (read(0, cmd_line, LINE_SIZE) <= 1)
      continue;

    int do_wait = 1;
    int argc = 0;
    char **argv = NULL;

    /* strtok() splits the command line into tokens separated by delimiters from
     * sep (close to what splitPrefix does). It breaks a string into a sequence
     * of zero or more nonempty tokens.  On the first call to strtok(), the
     * string to be parsed is specified in str.  In each subsequent call that
     * should parse the same string, str must be NULL.
     */

    char *token = strtok(cmd_line, sep);
    while (1) {
      argv = (char **)realloc(argv, (argc + 1) * sizeof(char *));
      argv[argc] = token;
      if (token == NULL)
        break;
      argc++;
      token = strtok(NULL, sep);
    };

    /* At this point, argv and argc are ready to use for execlp. "prog x y" is
     * splitted such that argc = 3 and argv = {"prog", "x", "y", (char *)0}).
     * Note that argv[argc] is NULL.
     *
     * We have parsed the command line, in particular the command itself, its
     * argument and a possible '&' character. All we have to do is handled
     * detached processes, built-in (exit, exec) and normal commands.
     */

    /* First check whether we have to detach or to wait for command completion.
     * Initialize do_wait.
     */

    /* Second, execute built-ins in the current process except if we have
     * detached the command. Try to handle "exit", "exec" and "echo".
     */
    if (do_wait) {
    }

    /* At last, create a process to execute the command and wait for its
     * completion
     */

    /* Output the command we should have executed (except built-in commands)
     */
    int i = 0;
    printf("{\"%s\"", argv[i]);
    i++;
    while (argv[i]) {
      printf(", \"%s\"", argv[i]);
      i++;
    }
    printf("}\n");
    free(argv);
  }
  return 0;
}
