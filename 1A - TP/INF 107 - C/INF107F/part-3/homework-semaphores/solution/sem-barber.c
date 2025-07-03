#include <assert.h>
#include <fcntl.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

// Declare the names of the semaphores used in the program
#ifdef TEACHER
#define barber_enter_brushing_name "/barber_enter_brushing.sem"
#define barber_leave_brushing_name "/barber_leave_brushing.sem"
#define client_enter_brushing_name "/client_enter_brushing.sem"
#define client_leave_brushing_name "/client_leave_brushing.sem"
#define waiting_room_name "/waiting_room.sem"
#endif
#define shared_variable_seats_name "shared_variable_seats.var"

int max_seats, n_seats;
int max_clients, n_clients;

#ifdef TEACHER
sem_t *barber_enter_brushing;
sem_t *client_enter_brushing;
sem_t *barber_leave_brushing;
sem_t *client_leave_brushing;
sem_t *waiting_room;
#endif

void execute_barber();
void execute_client();

// Generate a random integer value between first and last
int value_between(int first, int last);

// Read an integer from a file. This intends to simulate a read operation on a
// shared integer variable of name name.
int read_shared_var(char *name);

// Write an integer into a file. This intends to simulate a write operation on a
// shared integer variable of name name.
void write_shared_var(char *name, int value);

// Set up a handshake with two semaphores one assigned to the process itself the
// other to the partner.
void rendez_vous(sem_t *i_arrive, sem_t *u_arrive);

int main(int argc, char **argv) {

  if (argc != 2) {
    printf("Usage : %s <max_seats>\n", argv[0]);
    exit(1);
  }
  max_seats = strtol(argv[1], NULL, 10);
  max_clients = max_seats + 2;
  write_shared_var(shared_variable_seats_name, max_seats);

#ifdef TEACHER
  sem_unlink(barber_enter_brushing_name);
  barber_enter_brushing =
      sem_open(barber_enter_brushing_name, O_CREAT, 0644, 0);

  sem_unlink(barber_leave_brushing_name);
  barber_leave_brushing =
      sem_open(barber_leave_brushing_name, O_CREAT, 0644, 0);

  sem_unlink(client_enter_brushing_name);
  client_enter_brushing =
      sem_open(client_enter_brushing_name, O_CREAT, 0644, 0);

  sem_unlink(client_leave_brushing_name);
  client_leave_brushing =
      sem_open(client_leave_brushing_name, O_CREAT, 0644, 0);

  sem_unlink(waiting_room_name);
  waiting_room = sem_open(waiting_room_name, O_CREAT, 0644, 1);
#endif

  // Create more clients than there are seats to test that they leave
  // immediately when the waiting room is full
  for (n_clients = 0; n_clients < max_clients; n_clients++)
    if (fork() == 0)
      execute_client();

  execute_barber();
}

void execute_barber() {
  while (1) {
#ifdef TEACHER
    rendez_vous(barber_enter_brushing, client_enter_brushing);
#endif

    printf("Barber enters brushing process\n");
    sleep(value_between(1, 3));
    printf("Barber leaves brushing process\n");

#ifdef TEACHER
    rendez_vous(barber_leave_brushing, client_leave_brushing);
#endif
  }
}

void execute_client() {
#ifdef TEACHER
  sem_wait(waiting_room);
#endif

  n_seats = read_shared_var(shared_variable_seats_name);
  if (n_seats > 0) {
    n_seats--;
    write_shared_var(shared_variable_seats_name, n_seats);
    printf("Client %d sits in waiting room\n", n_clients);

#ifdef TEACHER
    sem_post(waiting_room);
#endif
  } else {
#ifdef TEACHER
    sem_post(waiting_room);
#endif

    printf("Client %d leaves immediately\n", n_clients);
    exit(0);
  }

#ifdef TEACHER
  rendez_vous(client_enter_brushing, barber_enter_brushing);
  sem_wait(waiting_room);
#endif

  n_seats = read_shared_var(shared_variable_seats_name);
  n_seats++;
  write_shared_var(shared_variable_seats_name, n_seats);

#ifdef TEACHER
  sem_post(waiting_room);
#endif

  printf("Client %d enters brushing process\n", n_clients);

#ifdef TEACHER
  rendez_vous(client_leave_brushing, barber_leave_brushing);
#endif

  printf("Client %d leaves brushing process\n", n_clients);
  exit(0);
}

// Set up a handshake with two semaphores one assigned to the process itself the
// other to the partner.
void rendez_vous(sem_t *i_arrive, sem_t *u_arrive) {
#ifdef TEACHER
  sem_post(i_arrive);
  sem_wait(u_arrive);
#endif
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