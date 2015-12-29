#include "module.h"

#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>

#define MSG "Hello World!\n"

void
hello (int n)
{
  if (n < 1)
    {
      fputs (MSG, stdout);
      return;
    }

  for (int i = 0; i < n; i++)
    fputs (MSG, stdout);

  return;
}

void
print_message ()
{
  char *line = NULL;
  size_t line_size = 0;

  /* Get the number of time to print the line */
  fputs ("Give the number of times you want to write the line: ", stdout);
  if (!getline (&line, &line_size, stdin))
    {
      fputs ("error: failed to read the number\n", stderr);
      exit (EXIT_FAILURE);
    }

  int n = atoi (line);

  /* Get the line to print */
  fputs ("Write the line to print: ", stdout);
  if (!getline (&line, &line_size, stdin))
    {
      fputs ("error: failed to read the message\n", stderr);
      exit (EXIT_FAILURE);
    }

  /* Print the line */
  for (int i = 0; i < n; i++)
    fprintf (stdout, "%s", line);

  /* Cleaning */
  free (line);
}
