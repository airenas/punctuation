-include Makefile.options
PATH:=$(TOOLS_ROOT)/bin:$(PATH)
F_DIR=$(WORK_DIR)/final
#################################################################################################
info:
	@echo "Input: $(INPUT_FILE)"
	@echo "Sentences: $(SENTENCES)"
#################################################################################################
$(WORK_DIR):
	mkdir -p $@

$(F_DIR):
	mkdir -p $@
#################################################################################################
$(WORK_DIR)/text.input: | $(WORK_DIR)
	pv $(INPUT_FILE) | head -n $(SENTENCES) > $@
$(WORK_DIR)/text.a1: $(WORK_DIR)/text.input
	pv $^ | drop.file | clear.symbols | change.numbers > $@
$(WORK_DIR)/text.a2: $(WORK_DIR)/text.a1
	pv $^ | to.sentences > $@
$(WORK_DIR)/text.a3: $(WORK_DIR)/text.a2
	pv $^ | drop.sentences > $@
$(WORK_DIR)/text.a4: $(WORK_DIR)/text.a3
	pv $^ | lc.sentences > $@
$(WORK_DIR)/text.a5: $(WORK_DIR)/text.a4
	pv $^ | make.data > $@
$(F_DIR)/lt.train.txt: $(WORK_DIR)/text.a5 | $(F_DIR)
	all=$$(wc -l $^ | awk '{print $$1;}'); \
	train=$$(($$all * 8 / 10)); \
	dev2=$$(($$all * 2 / 10 )); \
	dev1=$$(($$all * 1 / 10 )); \
	echo "$$all $$train $$dev2 $$dev1"; \
	head -n $$train $^ > $@; \
	tail -n $$dev2 $^ | head -n $$dev1 > $(F_DIR)/lt.dev.txt; \
	tail -n $$dev1 $^ > $(F_DIR)/lt.test.txt
#################################################################################################
build: info $(F_DIR)/lt.train.txt
#################################################################################################
clean:
	rm -rf $(WORK_DIR)
#################################################################################################
.PHONY: info clean
#################################################################################################
