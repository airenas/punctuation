-include Makefile.options
PATH:=$(TOOLS_ROOT)/bin:$(PATH)
F_DIR=$(WORK_DIR)/final
#################################################################################################
info:
	@echo "Input     : $(INPUT_FILE)"
	@echo "Sentences : $(SENTENCES)"
	@echo "Vocab     : $(VOCAB)"
#################################################################################################
$(WORK_DIR):
	mkdir -p $@

$(F_DIR):
	mkdir -p $@
#################################################################################################
$(WORK_DIR)/text.input: | $(WORK_DIR)
	pv $(INPUT_FILE) | head -n $(SENTENCES) > $@
$(WORK_DIR)/text.a6: $(WORK_DIR)/text.input
	pv $^ | python local/fix_spaces.py | python local/fix_sym.py | python local/change_num.py | \
		python local/change_punct.py | python local/join_colon_sentence.py | python local/drop_period_sentence.py | \
		python local/add_period.py> $@

$(WORK_DIR)/text.counts: $(WORK_DIR)/text.a6
	pv $^ | python $(SCRIPT_DIR)/data/clean-punct.py | \
		python $(SCRIPT_DIR)/data/text-to-counts.py | sort -r -n -k 2 > $@

$(WORK_DIR)/vocab.txt: $(WORK_DIR)/text.counts
	echo '<UNK>' > $@
	echo '</S>' >> $@
	pv $^ | python $(SCRIPT_DIR)/data/counts_to_vocab.py --n $(VOCAB) --drop_unk --leave '<NUM>' >> $@

$(WORK_DIR)/text.a7: $(WORK_DIR)/text.a6 $(WORK_DIR)/vocab.txt
	pv $(WORK_DIR)/text.a6 | python local/drop_unk_sentence.py --vocab $(WORK_DIR)/vocab.txt > $@

$(F_DIR)/lt.train.txt: $(WORK_DIR)/text.a7 | $(F_DIR)
# hold out one in every 20 lines as dev data and as evaluation data.
# use 5 % for dev and 5% for test
	pv $^ | awk \
		'{if(NR%20 == 0) { print >"$(F_DIR)/lt.dev.txt"; } \
		else {if(NR%20 == 1) { print >"$(F_DIR)/lt.test.txt"; } \
		else {print;}}}' > $@
$(F_DIR)/vocab.txt: $(WORK_DIR)/vocab.txt | $(F_DIR)
	cp $^ $@
#################################################################################################
dev: $(WORK_DIR)/text.a7
build: info $(F_DIR)/lt.train.txt $(F_DIR)/vocab.txt
#################################################################################################
put-data:
	$(SSH_CMD) "mkdir -p $(REMOTE_DIR)"
	$(PUT_CMD) $(F_DIR)/*.txt $(PUT_DIR)/final/
#################################################################################################
clean:
	rm -rf $(WORK_DIR)
#################################################################################################
.PHONY: info clean
#################################################################################################
