#include <setjmp.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#ifndef Q
#define Q 0
#endif

#define NO_EXCEPTION           0
#define OUT_OF_RANGE_EXCEPTION 1001
#define NULL_POINTER_EXCEPTION 1002
#define USER_DEFINED_EXCEPTION 1003

typedef struct _exception_t {
  jmp_buf block;
  int id;
  struct sigaction sa;
} exception_t;

/* Function declarations */
void on_error(int sig);
#define exception_enter_try_block(e) (e)->id = sigsetjmp((e)->block, 1);
void exception_add_catch_block(exception_t *e, int exception_id);
void exception_leave_try_block(exception_t *e);
void exception_raise_exception(int exception_id);

/* Declare an array and an iterator on this array */
#define ARRAY_LENGTH 100

void exception_test_main(int exception_id);
long *array[ARRAY_LENGTH];
int array_index;

exception_t exception;

int main(int argc, char *argv[]) {
  int scanf_rv;
  int choice;

  for (array_index = 0; array_index < ARRAY_LENGTH; array_index++)
    array[array_index] = NULL;

#if (Q > 0)
  printf("Question %d\n", Q);
#endif

  while (1) {
    printf("\t[1] OUT_OF_RANGE_EXCEPTION\n");
    printf("\t[2] NULL_POINTER_EXCEPTION\n");
    printf("\t[3] USER_DEFINED_EXCEPTION\n");
    printf("Choice : ");

    scanf_rv = scanf("%d", &choice);
    choice = choice - 1 + OUT_OF_RANGE_EXCEPTION;
    if (scanf_rv != 1)
      exit(1);

    switch (choice) {
    case OUT_OF_RANGE_EXCEPTION:
      /* Test memory error */
      array_index = 1000000;
      break;

    case NULL_POINTER_EXCEPTION:
      array_index = 0;
      break;

    default:
      break;
    }

    /* Test with exception handler */
    printf("\n***Test with exception handler ***\n\n");

    exception_enter_try_block(&exception);
    printf("[ENTER TRY BLOCK] exception id = %d\n", exception.id);
    exception_add_catch_block(&exception, OUT_OF_RANGE_EXCEPTION);
    exception_add_catch_block(&exception, NULL_POINTER_EXCEPTION);
    exception_add_catch_block(&exception, USER_DEFINED_EXCEPTION);

    switch (exception.id) {
    default:
      exception_test_main(choice);
      break;

    case OUT_OF_RANGE_EXCEPTION:
      printf("Catch OUT_OF_RANGE_EXCEPTION\n");
      break;

    case NULL_POINTER_EXCEPTION:
      printf("Catch NULL_POINTER_EXCEPTION\n");
      break;

    case USER_DEFINED_EXCEPTION:
      printf("Catch USER_DEFINED_EXCEPTION\n");
      break;
    }
    exception_leave_try_block(&exception);
    printf("[LEAVE TRY BLOCK] exception id = %d\n", exception.id);

    printf("\n*** Test without exception handler ***\n\n");
    exception_test_main(choice);
  }
  exit(0);
}

void on_error(int sig) {

  switch (sig) {
  case SIGBUS:
    exception.id = OUT_OF_RANGE_EXCEPTION;
    break;

  case SIGSEGV:
    exception.id = NULL_POINTER_EXCEPTION;
    break;

  case SIGUSR1:
    exception.id = USER_DEFINED_EXCEPTION;
    break;

  default:
    exception.id = 0;
  }
  printf("[ON ERROR] Exception id = %d\n", exception.id);
#if (Q > 1)
  siglongjmp(exception.block, exception.id);
#endif
}

void exception_add_catch_block(exception_t *e, int exception_id) {
  if (e->id != 0)
    return;

#if (Q > 0)
  e->sa.sa_flags = 0;
  sigemptyset(&e->sa.sa_mask);
  e->sa.sa_handler = on_error;

  switch (exception_id) {
  case OUT_OF_RANGE_EXCEPTION:
    if (sigaction(SIGBUS, &e->sa, NULL) == -1) {
      perror("Failed to change handler for SIGBUS");
      exit(1);
    }
    break;

  case NULL_POINTER_EXCEPTION:
    if (sigaction(SIGSEGV, &e->sa, NULL) == -1) {
      perror("Failed to change handler for SIGSEGV");
      exit(1);
    }
    break;

  case USER_DEFINED_EXCEPTION:
    if (sigaction(SIGUSR1, &e->sa, NULL) == -1) {
      perror("Failed to change handler for SIGUSR1");
      exit(1);
    }
    break;

  default:
    printf("Exception %d not implemented\n", exception_id);
  }
#endif
}

void exception_leave_try_block(exception_t *e) {
#if (Q > 2)
  e->sa.sa_handler = SIG_DFL;
  if (sigaction(SIGBUS, &e->sa, NULL) == -1) {
    perror("Failed to change handler for SIGBUS");
    exit(1);
  }
  if (sigaction(SIGSEGV, &e->sa, NULL) == -1) {
    perror("Failed to change handler for SIGSEGV");
    exit(1);
  }
  if (sigaction(SIGUSR1, &e->sa, NULL) == -1) {
    perror("Failed to change handler for SIGUSR1");
    exit(1);
  }
#endif
}

void exception_raise_exception(int exception_id) {
#if (Q > 3)
  int kill_rv;
  switch (exception_id) {
  default:
    break;
  case OUT_OF_RANGE_EXCEPTION:
    kill_rv = kill(getpid(), SIGBUS);
    if (kill_rv != 0) {
      perror("Failed to raise SIGSEGV");
      exit(1);
    }
    break;

  case NULL_POINTER_EXCEPTION:
    kill_rv = kill(getpid(), SIGSEGV);
    if (kill_rv != 0) {
      perror("Failed to raise SIGSEGV");
      exit(1);
    }
    break;

  case USER_DEFINED_EXCEPTION:
    kill_rv = kill(getpid(), SIGUSR1);
    if (kill_rv != 0) {
      perror("Failed to raise SIGUSR1");
      exit(1);

      break;
    }
  }
#endif
}

void exception_test_main(int choice) {
  switch (choice) {
  case OUT_OF_RANGE_EXCEPTION:
  case NULL_POINTER_EXCEPTION:

    printf("Check access to content of array[%d]\n", array_index);
    printf("array[%d] = %ld\n", array_index, *array[array_index]);
    break;

  case USER_DEFINED_EXCEPTION:
    exception_raise_exception(USER_DEFINED_EXCEPTION);
    break;

  default:
    break;
  }
}
