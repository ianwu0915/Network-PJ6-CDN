# Makefile to chmod scripts

# Define scripts
SCRIPTS = deployCDN.sh runCDN.sh stopCDN.sh

# Default target
all: make_executable

# Target to make scripts executable
make_executable:
	@chmod +x $(SCRIPTS)
	@echo "Scripts are now executable."

# Phony target to prevent make from getting confused by any files named "make_executable"
.PHONY: make_executable all
