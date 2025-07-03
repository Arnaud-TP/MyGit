#include <stdio.h>
#include <unistd.h>

#include "fs-linked-list.h"
#include "utils.h"

void display_list(list_t *list) {
  node_t node;
  index_t index = read_node(list, 0).next;
  printf("Process %d [", getpid());
  while (index != NONE) {
    node = read_node(list, index);
    printf(" %d", node.value);
    index = node.next;
  }
  printf("]\n");
}

void insert_node(list_t *list, value_t value) {
  index_t previous = 0;
  node_t prev_node;
  node_t next_node;

  lock_node(list, previous);
  prev_node = read_node(list, previous);
  sleep(value_between(0, 1));

  /* Loop to find the two nodes between which the new value is to be inserted
   */
  while (prev_node.next != NONE) {
    /* At this point, the previous node is locked */
    lock_node(list, prev_node.next);
    sleep(value_between(0, 1));

    /* At this point, the next node is locked */
    next_node = read_node(list, prev_node.next);

    if (next_node.value == value) {
      /* This node already exists. Unlock previous and next nodes */
      unlock_node(list, prev_node.next);
      unlock_node(list, previous);
      return;
    }
    if (next_node.value > value)
      break;

    /* The exploration goes one step forward, so we unlock the previous node */
    unlock_node(list, previous);
    previous = prev_node.next;
    prev_node = read_node(list, previous);
  }

  /* At this point, the new node has to be added after the previous node. Note
   * that this previous node always exists since the dummy node holds MIN_INT.
   * Previous node is locked. Next node is either equal to NONE or locked.
   */

  index_t new_node = allocate_node(list, value, prev_node.next);
  write_node(list, previous, prev_node.value, new_node);

  if (prev_node.next != NONE)
    unlock_node(list, prev_node.next);
  unlock_node(list, previous);
}
