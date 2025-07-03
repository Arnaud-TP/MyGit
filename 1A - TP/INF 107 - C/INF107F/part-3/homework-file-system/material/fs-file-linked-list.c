#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "fs-linked-list.h"
#include "utils.h"

#define list_storage_name "storage.dat"

typedef struct _list_t {
  int file;
} list_t;

index_t allocate_node(list_t *list, value_t value, index_t next) {
  node_t node;
  int length = 0;

  node.value = value;
  node.next = next;

  /* Evaluate the last index of the node array. To do that, get the length of
   * the file. To do that, use wisely lseek.
   */
  /* The offset returned by lseek gives you a way tu compute the length of the
   * array
   */
  length = offset / sizeof(node_t);

  /* Keep this delay to cause race conditions
   */
  delay_milli_sec(value_between(0, 200));

  /* Resize the array (nodes) once its length is computed.
   */
  return length;
}

list_t *create_list() {
  list_t *list;
  list = (list_t *)malloc(sizeof(list_t));
  unlink(list_storage_name);
  list->file = open(list_storage_name, O_CREAT | O_RDWR, 0640);
  write_node(list, 0, -2147483648L, NONE);
  close(list->file);
  return list;
};

void lock_node(list_t *list, index_t index) {
}

void open_list(list_t *list) {
  list->file = open(list_storage_name, O_RDWR, 0640);
};

node_t read_node(list_t *list, index_t index) {
  node_t node = {0, NONE};
  /* Determine where to read in the file
   */

  /* Keep this delay to cause race conditions
   */
  delay_milli_sec(value_between(0, 200));

  /* Read node in the file
   */
  return node;
}

void unlock_node(list_t *list, index_t index) {
};

void write_node(list_t *list, index_t index, value_t value, index_t next) {
  node_t node;
  node.value = value;
  node.next = next;
  /* Determine where to write in the file
   */

  /* Keep this delay to cause race conditions
   */
  delay_milli_sec(value_between(0, 200));

  /* Write node in the file
   */
}
