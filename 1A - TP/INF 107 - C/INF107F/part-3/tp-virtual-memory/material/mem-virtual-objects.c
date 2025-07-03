#include <assert.h>
#include <fcntl.h>
#include <setjmp.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define max_vir_obj 8 // Number of virtual objects in swap file
#define max_phy_obj 4 // Number of physical objects in memory
#define max_unsigned_int -1

typedef struct {
  int x;
  int y;
} object_t;

typedef unsigned int phy_obj_id_t;
typedef unsigned int vir_obj_id_t;
typedef unsigned int access_time_t;

#define NO_OBJ_ID -1

/* Table of pointers to virtual objects posibly in memory. If the virtual object
 * is really stored in memory, the pointer refers to a physical object from
 * table phy_obj_tab (see below). If the pointer is NULL, the virtual object is
 * not available in memory.
 */
object_t *vir_obj_tab[max_vir_obj];

/* Table of physical objects in memory.
 */
object_t phy_obj_tab[max_phy_obj];

/* Current virtual object id.
 */
vir_obj_id_t vir_obj_id;

access_time_t last_tab_access_time = 0;

/* Mapping table to associate physical objects to virtual objects. For each
 * virtual object we store its possible equivalent physical object and its last
 * access time.
 */

typedef struct {
  phy_obj_id_t phy_obj_id;
  access_time_t last_obj_access_time;
} vir_to_phy_t;
vir_to_phy_t vir_to_phy_map[max_vir_obj];

/* Descriptor of the file used to store virtual objects (swap file)
 */
int vir_obj_file;

void init_obj_tab();
void dump_vir_obj_tab();

/* Define and set handler to catch virtual object fault ie access to virtual
 * object that are not physically in memory.
 */
void handle_obj_fault(int sig);
void set_obj_fault_handler();
jmp_buf recover_from_obj_fault;

void modify_object(vir_obj_id_t id);

int main(int argc, char *argv[]) {

  init_obj_tab();

  set_obj_fault_handler();

  while (1) {
    dump_vir_obj_tab();

    printf("vir obj id> ");
    if (scanf("%d", &vir_obj_id) <= 0)
      exit(0);

    modify_object(vir_obj_id);
  }
}

void init_obj_tab() {
  object_t initial_obj = {0, 0};
  vir_obj_id_t vir_obj_id;
  phy_obj_id_t phy_obj_id;
  int rv;

  unlink("vir_obj_file"); // Supprime le fichier vir_obj_file
  /* Create vir_obj_file used to store virtual objects in a file. Initialize
   * them with the initial object value (see above).
   * vvvvv
   */
  int fd = open("vir_obj_file", O_RDWR | O_CREAT, 0644); //Mode du fichier (3e paramètre) -> Accorde les permissions
  if (fd < 0)
  {
    perror("open");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i > max_vir_obj; i++)
  {
    int res = write(fd, &initial_obj, sizeof(initial_obj));
    if (res != sizeof(initial_obj))
      {
        perror("open");
        exit(EXIT_FAILURE);
      } 
  }
  /* Create vir_obj_tab used to store virtual objects in memory. At the
   * beginning, no virtual object is stored in memory.
   */
  for (vir_obj_id = 0; vir_obj_id < max_vir_obj; vir_obj_id++) {
    /* At the beginning, no virtual object is stored in memory
     */
    vir_obj_tab[vir_obj_id] = NULL;

    /* At the beginning, no virtual object is mapped to a physical object
     */
    vir_to_phy_map[vir_obj_id].phy_obj_id = NO_OBJ_ID;
    vir_to_phy_map[vir_obj_id].last_obj_access_time = 0;

    /* Map the first virtual objects as physical objects. Initialize the
     * physical object with their value. Update the different data structures.
     */
  }
  for (vir_obj_id = 0; vir_obj_id < max_phy_obj; vir_obj_id++) 
  {
    phy_obj_tab[vir_obj_id] = initial_obj;
    vir_obj_tab[vir_obj_id] = &phy_obj_tab[vir_obj_id];
    vir_to_phy_map[vir_obj_id].phy_obj_id = vir_obj_id;
  }
}

void handle_obj_fault(int sig) {
  phy_obj_id_t phy_obj_id;
  vir_obj_id_t replaced_obj_id = NO_OBJ_ID;
  vir_obj_id_t obj_id;
  int rv;

  dump_vir_obj_tab();

  /* Find the least recently used object to replace and store it in
   * replaced_obj_id.
   */

  if (replaced_obj_id == NO_OBJ_ID) {
    printf("no replaced object\n");
    exit(1);
  }

  phy_obj_id = vir_to_phy_map[replaced_obj_id].phy_obj_id;
  vir_to_phy_map[replaced_obj_id].phy_obj_id = NO_OBJ_ID;
  vir_to_phy_map[replaced_obj_id].last_obj_access_time = 0;

  printf("Replace vir obj %d (phy obj %d) to store vir obj %d\n",
         replaced_obj_id, phy_obj_id, vir_obj_id);

  /* Save replaced physical object (find its location in memory) in swap file
   * (find its location in file)
   */

  /* Update the mapping table.
   */
  vir_to_phy_map[vir_obj_id].phy_obj_id = phy_obj_id;
  vir_to_phy_map[vir_obj_id].last_obj_access_time = last_tab_access_time;

  /* Update the virtual object table for the replaced object.
   */
  vir_obj_tab[replaced_obj_id] = NULL;

  /* Update the virtual object table for the virtual object.
   */
  vir_obj_tab[vir_obj_id] = &phy_obj_tab[phy_obj_id];

  /* Load virtual object (find its location in file) from swap file in the
   * physical object (find its location in memory).
   */
  dump_vir_obj_tab();

  /* Object fault has been handled. Recover from fault and try again
   */
  printf("not yet ready\n");
  exit(1);
}

void modify_object(vir_obj_id_t id) {
  printf("vir_obj_tab[%d] = (%d, %d)\n", id, vir_obj_tab[id]->x,
         vir_obj_tab[id]->y);
  printf("x = ");
  scanf("%d", &(vir_obj_tab[id]->x));
  printf("y = ");
  scanf("%d", &(vir_obj_tab[id]->y));
  printf("vir_obj_tab[%d] = (%d, %d)\n", id, vir_obj_tab[id]->x,
         vir_obj_tab[id]->y);

  // Update
  last_tab_access_time++;
  vir_to_phy_map[id].last_obj_access_time = last_tab_access_time;
}

void dump_vir_obj_tab() {
  for (vir_obj_id = 0; vir_obj_id < max_vir_obj; vir_obj_id++) 
  {
    printf("[%02d][%d%d] ",vir_to_phy_map[vir_obj_id].phy_obj_id, vir_obj_tab[vir_obj_id]->x,
         vir_obj_tab[vir_obj_id]->y);
  }
}
  /* Display virtual objects such as we get [<phy obj id> <acc time>] for each of them.
  */

/* Handling a memory fault has already been presented in a previous homework.
*/
void set_obj_fault_handler() {
}
