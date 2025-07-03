#include <assert.h>
#include <fcntl.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define fork_generic_name "/fork%02d"
char fork_specific_name[] = "/fork00";

int n_philosophers, max_philosophers;

sem_t **forks;

void execute_philosopher();

// Generate a random integer value between first and last
int value_between(int first, int last);

int main(int argc, char **argv) {
  int rv;
  int filename_len = strlen(fork_specific_name);

  if (argc != 2) {
    printf("Usage : %s <max_philosophers>\n", argv[0]);
    exit(1);
  }
  max_philosophers = strtol(argv[1], NULL, 10);

  forks = (sem_t **)malloc(sizeof(sem_t *) * max_philosophers);
  assert(forks != NULL);

  for (n_philosophers = 0; n_philosophers < max_philosophers;
       n_philosophers++) {
    rv = sprintf(fork_specific_name, fork_generic_name, n_philosophers);
    assert(rv == filename_len);

  }
  for (n_philosophers = 0; n_philosophers < max_philosophers;
       n_philosophers++) {
    rv = fork();
    assert(0 <= rv);
    if (rv == 0)
      execute_philosopher();
  }
  while (wait(NULL) > 0)
    ;
}

void execute_philosopher() {
  int id = n_philosophers;
  int first_fork;
  int last_fork;

  if (id == max_philosophers - 1) {
    first_fork = 0;
    last_fork = id;
  } else {
    first_fork = id;
    last_fork = id + 1;
  }

  for (int i = 0; i < 4; i++) {
    printf("Philosopher %d get forks %d + %d (round %d)\n", id, first_fork,
           last_fork, i + 1);
    printf("Philosopher %d start eating\n", id);
    sleep(value_between(1, 3));
    printf("Philosopher %d drops forks %d and %d\n", id, first_fork, last_fork);
    printf("Philosopher %d start sleeping\n", id);
    sleep(value_between(1, 3));
  }
  exit(0);
}

// Generate a random integer value between first and last
int value_between(int first, int last) {
  int length = last - first + 1;
  return first + (int)(random() % length);
}
