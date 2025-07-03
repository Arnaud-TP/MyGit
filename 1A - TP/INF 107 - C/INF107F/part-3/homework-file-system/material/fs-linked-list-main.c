#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "fs-linked-list.h"
#include "utils.h"

void execute_producer();

list_t *list;

int max_values, max_processes;

int main(int argc, char **argv) {
  if (argc != 3) {
    printf("Usage : %s <max_processes> <max_values>\n", argv[0]);
    exit(1);
  }

  max_processes = strtol(argv[1], NULL, 10);
  assert(max_processes != 0 || errno == EINVAL);

  max_values = strtol(argv[2], NULL, 10);
  assert(max_values != 0 || errno == EINVAL);

  list = create_list();

  for (int p = 1; p < max_processes; p++) {
    if (fork() == 0) {
      execute_producer();
      exit(0);
    }
  }
  execute_producer();
  while (wait(NULL) > 0)
    ;
}

void execute_producer() {
  init_random_value();
  open_list(list);
  for (int i = 0; i < max_values; i++) {
    value_t value = value_between(0, 2 * max_values);
    printf("Process %d insert node %d\n", getpid(), value);
    insert_node(list, value);
    display_list(list);
  }
}
