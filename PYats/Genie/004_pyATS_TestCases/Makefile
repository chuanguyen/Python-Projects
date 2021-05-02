# # Define default action when "make" is run_logs by itself
# .DEFAULT_GOAL :=all
all: lint baseTests

.PHONY: baseTests
baseTests:
	@echo "************ Starting base network tests ************"
	@pyats run job jobfile.py --testbed-file testbed.yml
	@echo "************ Completed base network tests ************"

.PHONY: lint
lint:
	@echo "************ Starting lint tests ************"
	@echo "------------ Linting Testbed ------------"
	@pyats validate testbed -q testbed.yml
	@echo "************ Completed lint tests ************"
