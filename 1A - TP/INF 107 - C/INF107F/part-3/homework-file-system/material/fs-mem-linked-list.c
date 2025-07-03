#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "fs-linked-list.h"
#include "utils.h"

typedef struct _list_t {
  node_t *nodes;
} list_t;

index_t allocate_node(list_t *list, value_t value, index_t next) {
  /* The length of array (nodes) is not stored. Compute it by going through the
   * list.
   */
  int size = 1;
  index_t index = 0;
  while (list->nodes[index].next != NONE) {
    index = list->nodes[index].next;
    size++;
  }
  /* Resize the array (nodes) once its length is computed.
   */
  list->nodes[size].value = value;
  list->nodes[size].next = next;
  return size;
}

list_t *create_list() {
  list_t *list;
  list = (list_t *)malloc(sizeof(list_t));
  list->nodes = (node_t *)malloc(sizeof(node_t));
  write_node(list, 0, -2147483648L, NONE);
  return list;
};

void lock_node(list_t *list, index_t index) { /* Not relevant here */
}

void open_list(list_t *list){
    /* Not relevant here */
};

node_t read_node(list_t *list, index_t index) { return list->nodes[index]; }

void unlock_node(list_t *list, index_t index) { /* Not relevant here */
}

void write_node(list_t *list, index_t index, value_t value, index_t next) {
  list->nodes[index].value = value;
  list->nodes[index].next = next;
}
