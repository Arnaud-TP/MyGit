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
#ifdef TEACHER
    if (strcmp(argv[argc - 1], "&") == 0) {
      do_wait = 0;
      argv[argc - 1] = NULL;
    } else {
      do_wait = 1;
    }
#endif

    /* Second, execute built-ins in the current process except if we have
     * detached the command. Try to handle "exit", "exec" and "echo".
     */
    if (do_wait) {
#ifdef TEACHER
      if (strcmp(argv[0], "exit") == 0) {
        exit(0);
      } else if (strcmp(argv[0], "exec") == 0) {
        if (argc > 0) {
          argv = &argv[1];
          execvp(argv[0], argv);
          perror("execv:");
          exit(2);
        }
      } else if (strcmp(argv[0], "echo") == 0) {
        for (int i = 1; argv[i]; i++)
          printf("%s ", argv[i]);
        printf("\n");
        free(argv);
        continue;
      }
#endif
    }

    /* At last, create a process to execute the command and wait for its
     * completion
     */
#ifdef TEACHER
    int fork_rv = fork();
    switch (fork_rv) {
    case 0:
      execvp(argv[0], argv);
      perror("execv:");
      exit(2);
    case -1:
      perror("fork:");
      exit(3);
    default:
      if (do_wait) {
        wait(NULL);
      }
    }
#endif

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