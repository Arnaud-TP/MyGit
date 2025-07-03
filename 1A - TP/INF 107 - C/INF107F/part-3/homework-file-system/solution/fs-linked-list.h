#include <stdlib.h>

typedef int32_t value_t;
typedef int index_t;

#define NONE -1 /* no next node */

typedef struct _node_t {
  value_t value;
  index_t next;
} node_t;

typedef struct _list_t list_t;

/* Allocated a node of attributes value and next in storage allocated to list.
 * Return its node index.
 */
index_t allocate_node(list_t *list, value_t value, index_t next);

/* Create a list head with a dummy node which only purpose is to provide the
 * index of the first node in its attribute next. If attribute next of this
 * dummy node is NONE the list is empty. If not, this next attribute refers to
 * the index of the very first node of the list.
 */
list_t *create_list();

void display_list(list_t *list);

/* Insert node of attributes value and next in sorted list. If a node of
 * attributes value already exists, ignore the new node.
 */
void insert_node(list_t *list, value_t value);

/* Lock node that is lock the chunk of storage allocated to the node.
 */
void lock_node(list_t *list, index_t index);

void open_list(list_t *list);

/* Read node of index, index, from the storage allocated to list
 */
node_t read_node(list_t *list, index_t index);

/* Unlock node that is lock the chunk of storage allocated to the node.
 */
void unlock_node(list_t *list, index_t index);

/* Update attributes value and next of node of index, index, in the storage
 * allocated to list.
 */
void write_node(list_t *list, index_t index, value_t value, index_t next);

