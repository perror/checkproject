CFLAGS = -Wall -Wextra -std=c99 -O2
CPPFLAGS = -I../include
LDFLAGS = -lm

.PHONY:	clean

all: project

project: project.o module.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

project.o: project.c project.h
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $@ -c $<

module.o: module.c ../include/module.h
	$(CC) $(CFLAGS) $(CPPFLAGS) -o $@ -c $<

clean:
	@rm -f project *.o *~
