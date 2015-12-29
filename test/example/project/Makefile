EXEC = project

.PHONY:	all build clean

all: build

build:
	@cd src/ && $(MAKE)
	@cp -f src/$(EXEC) ./

clean:
	@cd src/ && $(MAKE) clean
	@rm -f $(EXEC)
