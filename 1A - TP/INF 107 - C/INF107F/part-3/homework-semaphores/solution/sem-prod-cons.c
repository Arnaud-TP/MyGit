#include <assert.h>
#include <fcntl.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

// Declare the names of the semaphores used in the program
#ifdef TEACHER
#define full_slots_name "/full_slots.sem"
#define empty_slots_name "/empty_slots.sem"
#endif
#define buffer_mutex_name "/buffer_mutex.sem"
#define shared_variable_first_name "shared_variable_first.var"
#define shared_variable_last_name "shared_variable_last.var"
#define shared_variable_size_name "shared_variable_size.var"
#define shared_buffer_array_name "shared_buffer_array.var"

int max_producers, max_consumers;
int n_producers, n_consumers;

void execute_producer();
void execute_consumer();

// Generate a random integer value between first and last
int value_between(int first, int last);

// Read an integer from a file. This intends to simulate a read operation on a
// shared integer variable of name name.
int read_shared_var(char *name);

// Write an integer into a file. This intends to simulate a write operation on a
// shared integer variable of name name.
void write_shared_var(char *name, int value);

// Read an integer array from a file. This intends to simulate a read operation
// on a shared integer array of name name.
void read_shared_array(char *name, int *array, int size);

// Write an integer array into a file. This intends to simulate a write
// operation on a shared integer array of name name.
void write_shared_array(char *name, int *array, int size);

typedef struct _bounded_buffer_t {
  int first;
  int last;
  int size;
  int max_size;
  int *elements;
#ifdef TEACHER
  sem_t *full_slots;
  sem_t *empty_slots;
#endif
  sem_t *buffer_mutex;
} bounded_buffer_t;

bounded_buffer_t *buffer;

int main(int argc, char **argv) {
  int rv;
  int max_size;

  if (argc != 4) {
    printf("Usage : %s <max_consumers> <max_producers> <max_size>\n", argv[0]);
    exit(1);
  }
  max_consumers = strtol(argv[1], NULL, 10);
  max_producers = strtol(argv[2], NULL, 10);
  max_size = strtol(argv[3], NULL, 10);

  buffer = (bounded_buffer_t *)malloc(sizeof(bounded_buffer_t));
  assert(buffer != NULL);
  buffer->elements = (int *)malloc(max_size * sizeof(int));
  assert(buffer->elements != NULL);

  buffer->max_size = max_size;
  buffer->size = 0;
  buffer->first = 0;
  buffer->last = buffer->max_size - 1;
  for (int i = 0; i < max_size; i++)
    buffer->elements[i] = 0;

#ifdef TEACHER
  write_shared_var(shared_variable_first_name, buffer->first);
  write_shared_var(shared_variable_last_name, buffer->last);
  write_shared_var(shared_variable_size_name, buffer->size);
  write_shared_array(shared_buffer_array_name, buffer->elements,
                     buffer->max_size);

  sem_unlink(full_slots_name);
  buffer->full_slots = sem_open(full_slots_name, O_CREAT, 0644, 0);
  assert(buffer->full_slots >= 0);

  sem_unlink(empty_slots_name);
  buffer->empty_slots =
      sem_open(empty_slots_name, O_CREAT, 0644, buffer->max_size);
  assert(buffer->empty_slots >= 0);
#endif

  sem_unlink(buffer_mutex_name);
  buffer->buffer_mutex = sem_open(buffer_mutex_name, O_CREAT, 0644, 1);
  assert(buffer->buffer_mutex >= 0);

  for (n_producers = 0; n_producers < max_producers; n_producers++)
    if (fork() == 0)
      execute_producer();

  for (n_consumers = 0; n_consumers < max_consumers; n_consumers++)
    if (fork() == 0)
      execute_consumer();

  while (wait(NULL) > 0)
    ;
}

void execute_producer() {
  for (int i = 0; i < max_consumers; i++) {
    sleep(value_between(1, 3));

#ifdef TEACHER
    sem_wait(buffer->empty_slots);
    sem_wait(buffer->buffer_mutex);
#endif

    buffer->size = read_shared_var(shared_variable_size_name);
    buffer->first = read_shared_var(shared_variable_first_name);
    buffer->last = read_shared_var(shared_variable_last_name);
    read_shared_array(shared_buffer_array_name, buffer->elements,
                      buffer->max_size);

    buffer->size++;
    buffer->last = (buffer->last + 1) % buffer->max_size;
    buffer->elements[buffer->last] = 100 + n_producers;

    printf("Producer %d produces slot %d (%d)\n", n_producers, buffer->last,
           buffer->elements[buffer->last]);

    printf("[");
    for (int i = 0; i < buffer->size; i++)
      printf(" %d", buffer->elements[(buffer->first + i) % buffer->max_size]);
    printf("]\n");

    write_shared_array(shared_buffer_array_name, buffer->elements,
                       buffer->max_size);
    write_shared_var(shared_variable_size_name, buffer->size);
    write_shared_var(shared_variable_first_name, buffer->first);
    write_shared_var(shared_variable_last_name, buffer->last);

#ifdef TEACHER
    sem_post(buffer->buffer_mutex);
    sem_post(buffer->full_slots);
#endif
  }
  printf("Producer %d completed\n", n_producers);
  exit(0);
}

void execute_consumer() {
  for (int i = 0; i < max_producers; i++) {
    sleep(value_between(1, 3));

#ifdef TEACHER
    sem_wait(buffer->full_slots);
    sem_wait(buffer->buffer_mutex);
#endif

    buffer->size = read_shared_var(shared_variable_size_name);
    buffer->first = read_shared_var(shared_variable_first_name);
    buffer->last = read_shared_var(shared_variable_last_name);
    read_shared_array(shared_buffer_array_name, buffer->elements,
                      buffer->max_size);

    printf("Consumer %d consumes slot %d (%d)\n", n_consumers, buffer->first,
           buffer->elements[buffer->first]);
    buffer->size--;
    buffer->first = (buffer->first + 1) % buffer->max_size;

    printf("[");
    for (int i = 0; i < buffer->size; i++)
      printf(" %d", buffer->elements[(buffer->first + i) % buffer->max_size]);
    printf("]\n");

    write_shared_array(shared_buffer_array_name, buffer->elements,
                       buffer->max_size);
    write_shared_var(shared_variable_size_name, buffer->size);
    write_shared_var(shared_variable_first_name, buffer->first);
    write_shared_var(shared_variable_last_name, buffer->last);

#ifdef TEACHER
    sem_post(buffer->buffer_mutex);
    sem_post(buffer->empty_slots);
#endif
  }
  printf("Consumer %d completed\n", n_consumers);
  exit(0);
}

// Generate a random integer value between first and last
int value_between(int first, int last) {
  int length = last - first + 1;
  return first + (int)(random() % length);
}

// Read an integer from a file. This intends to simulate a read operation on a
// shared integer variable of name name.
int read_shared_var(char *name) {
  int value;
  int fd = open(name, O_RDWR);
  int rv;
  assert(fd > 0);
  rv = read(fd, &value, sizeof(int));
  assert(rv == sizeof(int));
  close(fd);
  return value;
}

// Write an integer into a file. This intends to simulate a write operation on a
// shared integer variable of name name.
void write_shared_var(char *name, int value) {
  int fd = open(name, O_CREAT | O_RDWR, 0644);
  int rv;
  assert(fd > 0);
  rv = write(fd, &value, sizeof(int));
  assert(rv == sizeof(int));
  close(fd);
}

// Read an integer array from a file. This intends to simulate a read operation
// on a shared integer array of name name.
void read_shared_array(char *name, int *array, int size) {
  int fd = open(name, O_RDWR);
  int rv;
  assert(fd > 0);
  rv = read(fd, array, size * sizeof(int));
  assert(rv == size * sizeof(int));
  close(fd);
};

// Write an integer array into a file. This intends to simulate a write
// operation on a shared integer array of name name.
void write_shared_array(char *name, int *array, int size) {
  int fd = open(name, O_CREAT | O_RDWR, 0644);
  int rv;
  assert(fd > 0);
  rv = write(fd, array, size * sizeof(int));
  assert(rv == size * sizeof(int));
  close(fd);
};