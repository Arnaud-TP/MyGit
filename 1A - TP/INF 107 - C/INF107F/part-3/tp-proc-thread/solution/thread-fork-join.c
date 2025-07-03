#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void *thread_main(void *arg);

pthread_t main_thread;

int main(int argc, char *argv[]) {
  int n_threads, thread_index;
  pthread_t *threads;

  /* Check that one parameter was provided */
  if (argc != 2) {
    printf(" Wrong usage : %s n_threads\n", argv[0]);
    exit(1);
  }

  /* conversion ascii -> decimal integer */
  n_threads = strtol(argv[1], NULL, 10);
  if (errno == EINVAL) {
    perror("Invalid decimal argument");
    exit(2);
  }

  if (n_threads <= 0) {
    printf(" Wrong usage : %s n_threads (>0)\n", argv[0]);
    exit(3);
  }

  main_thread = pthread_self();

  /*
   *  creation of N threads
   */
  threads = (pthread_t *)(malloc(n_threads * sizeof(pthread_t)));
  for (thread_index = 1; thread_index <= n_threads; thread_index++) {
    int *thread_arg = (int *)malloc(sizeof(int));
    *thread_arg = thread_index;
#ifdef TEACHER
    pthread_create(&threads[thread_index], NULL, thread_main,
                   (void *)thread_arg);
#endif
  }
  for (thread_index = 1; thread_index <= n_threads; thread_index++) {
    int *exit_rv;
    int join_rv;
    printf("[%8ld/%8ld] Wait for thread completion\n", (long)main_thread,
           (long)main_thread);
#ifdef TEACHER
    join_rv = pthread_join(threads[thread_index], (void **)&exit_rv);
#endif
    if (join_rv != 0)
      printf("[%8ld/%8ld] Thread %8ld failed with returned value %d\n",
             (long)main_thread, (long)main_thread, (long)threads[thread_index],
             join_rv);
    else
      printf("[%8ld/%8ld] Thread %8ld completed with exit %d\n",
             (long)main_thread, (long)main_thread, (long)threads[thread_index],
             (int)*exit_rv);
  }
}

void *thread_main(void *arg) {
  int *thread_index = (int *)arg;
  pthread_t current_thread = pthread_self();
  printf("[%8ld/%8ld] Execute thread of index %d\n", (long)current_thread,
         (long)main_thread, *thread_index);
  printf("[%8ld/%8ld] Thread of index %d works or sleeps for %d secondsd\n",
         (long)current_thread, (long)main_thread, *thread_index,
         2 * (int)*thread_index);
  sleep(2 * (int)*thread_index);
#ifdef TEACHER
  int div_zero = 1 / (1 - *thread_index);
  printf("%d\n", div_zero);
#endif
  pthread_exit((void *)thread_index);
}