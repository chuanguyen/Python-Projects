# # Define default action when "make" is run_logs by itself
# .DEFAULT_GOAL :=all
all: lint baseline

.PHONY: baseline
baseline:
	@echo "************ Starting profiling network baseline ************"
	@robot --outputdir robot/run_logs/ robot/cml_network_baseline.robot
	@echo "************ Completed profiling network baseline ************"

.PHONY: profile
profile:
	@echo "************ Starting profiling for network changes ************"
	@robot --outputdir robot/run_logs/ robot/cml_network_profile_changes.robot
	@echo "************ Completed profiling for network changes ************"

.PHONY: lint
lint:
	@echo "************ Starting lint tests ************"
	@echo "------------ Linting Testbed ------------"
	@pyats validate testbed -q cml_testbed.yml
	@echo "------------ Linting Robot Tests ------------"
	@rflint --ignore TooFewTestSteps -r robot
	@echo "************ Completed lint tests ************"
