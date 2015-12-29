#include "project.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <getopt.h>

#include <module.h>

/* global variables */
static bool interactive = false;

static void
usage (int status)
{
  if (status != EXIT_SUCCESS)
    fprintf (stderr, "Try `%s --help' for more information.\n", PROG_NAME);
  else
    {
      fprintf (stdout, "Usage: %s [OPTION] [N]\n", PROG_NAME);

      fputs ("Print 'Hello World' N times.\n"
	     "\n"
	     "  -i, --interactive\t\tenter interactive mode\n"
	     "  -v, --version\t\tdisplay version and exit\n"
	     "  -h, --help\t\tdisplay this help and exit\n", stdout);
    }

  exit (status);
}

static void
version ()
{
  fprintf (stdout, "%s %s", PROG_NAME, VERSION);
  fputs ("\n"
	 "This program is public domain, it is only intended for testing "
	 "purpose.\nFeel free to use it, read the source and modify it.\n",
	 stdout);

  exit (EXIT_SUCCESS);
}

static void
option_parser (int argc, char *argv[])
{
  /* getopt.h variables */
  extern int optind;
  int optc;

  /* Short options string */
  char *const optstring = "hiv";

  /* Long options struct */
  struct option const long_opts[] = {
    {"interactive", no_argument, NULL, 'i'},
    {"version", no_argument, NULL, 'v'},
    {"help", no_argument, NULL, 'h'},
    {NULL, 0, NULL, 0}
  };

  /* Parsing options */
  while ((optc = getopt_long (argc, argv, optstring, long_opts, NULL)) != -1)
    switch (optc)
      {
      case 'i':		/* Enter interactive mode */
	interactive = true;
	break;

      case 'v':		/* Display version number and exit */
	version ();
	break;

      case 'h':		/* Display usage and exit */
	usage (EXIT_SUCCESS);
	break;

      default:
	usage (EXIT_FAILURE);
      }
}

int
main (int argc, char *argv[])
{
  /* Parsing command line options */
  option_parser (argc, argv);

  /* Main function */
  if (!interactive)
    /* Non-interactive mode */
    hello (((argc > 1) ? atoi (argv[1]) : 0));
  else
    /* Interactive mode */
    print_message ();


  return EXIT_SUCCESS;
}
