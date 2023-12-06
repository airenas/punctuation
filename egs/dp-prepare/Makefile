-include Makefile.options
ifeq ($(GPU), 1)
    GPU_SETTING=--use-gpu
endif
ifeq ($(PREFETCH_ON),)
else
    PREFETCH_SETTING=--prefetch-device $(PREFETCH_ON)
endif
PATH:=$(TOOLS_ROOT)/bin:$(PATH)
F_DIR=$(WORK_DIR)/final
#################################################################################################
info:
	@echo "Input     : $(INPUT_FILE)"
	@echo "Sentences : $(SENTENCES)"
	@echo "Vocab     : $(VOCAB)"
#################################################################################################
$(WORK_DIR) $(WORK_DIR)/predict $(WORK_DIR)/model $(WORK_DIR)/data:
	mkdir -p $@

$(F_DIR):
	mkdir -p $@
#################################################################################################
$(WORK_DIR)/.unzip: | $(WORK_DIR)
	unzip $(INPUT_FILE) -d $(WORK_DIR)/in
	touch $@
$(WORK_DIR)/text.input: $(WORK_DIR)/.unzip | $(WORK_DIR)
	cat $(WORK_DIR)/in/*.txt | head -n $(SENTENCES) > $@
$(WORK_DIR)/text.a6: $(WORK_DIR)/text.input
	pv $^ | python local/fix_text.py | \
	    python $(SCRIPT_L_DIR)/fix_spaces.py | python $(SCRIPT_L_DIR)/fix_sym.py | python $(SCRIPT_L_DIR)/change_num.py | \
		python $(SCRIPT_L_DIR)/change_punct.py | python $(SCRIPT_L_DIR)/join_colon_sentence.py | python $(SCRIPT_L_DIR)/drop_period_sentence.py | \
		python $(SCRIPT_L_DIR)/add_period.py> $@

$(WORK_DIR)/text.counts: $(WORK_DIR)/text.a6
	pv $^ | python $(SCRIPT_DIR)/data/clean-punct.py | \
		python $(SCRIPT_DIR)/data/text-to-counts.py | sort -r -n -k 2 > $@

$(WORK_DIR)/vocab.txt: $(WORK_DIR)/text.counts
	echo '<UNK>' > $@
	echo '</S>' >> $@
	pv $^ | python $(SCRIPT_DIR)/data/counts_to_vocab.py --n $(VOCAB) --drop_unk --leave '<NUM>' >> $@

$(WORK_DIR)/text.a7: $(WORK_DIR)/text.a6 $(WORK_DIR)/vocab.txt
	pv $(WORK_DIR)/text.a6 | python $(SCRIPT_L_DIR)/drop_unk_sentence.py --vocab $(WORK_DIR)/vocab.txt > $@

$(F_DIR)/lt.train.txt: $(WORK_DIR)/text.a7 | $(F_DIR)
# hold out one in every 20 lines as dev data and as evaluation data.
# use 5 % for dev and 5% for test
	pv $^ | awk \
		'{if(NR%20 == 0) { print >"$(F_DIR)/lt.dev.txt"; } \
		else {if(NR%20 == 1) { print >"$(F_DIR)/lt.test.txt"; } \
		else {print;}}}' > $@
$(F_DIR)/vocab.txt: $(WORK_DIR)/vocab.txt | $(F_DIR)
	cp $^ $@

calc/oov/%: $(F_DIR)/lt.%.txt
	cat $^ | python $(SCRIPT_DIR)/data/calc_oov.py --vocab $(MAIN_VOCAB_FILE)

#################################################################################################
$(WORK_DIR)/predict/test.txt: $(F_DIR)/lt.test.txt | $(WORK_DIR)/predict
	python $(SCRIPT_DIR)/predict.py $(F_DIR)/lt.test.txt $(MAIN_VOCAB_FILE) $(MAIN_MODEL_FILE) \
		$(WORK_DIR)/predict/test.txt
$(WORK_DIR)/score.txt: $(WORK_DIR)/predict/test.txt | $(WORK_DIR)/predict
	python $(SCRIPT_DIR)/punctuator2/error_calculator.py $(F_DIR)/lt.test.txt $(WORK_DIR)/predict/test.txt > $@

score: $(WORK_DIR)/score.txt
	cat $^
#################################################################################################
$(WORK_DIR)/predict/test_new.txt: $(F_DIR)/lt.test.txt | $(WORK_DIR)/predict
	python $(SCRIPT_DIR)/predict.py $(F_DIR)/lt.test.txt $(MAIN_VOCAB_FILE) $(WORK_DIR)/model/$(MODEL_PREFIX)_$(MODEL_TEST).h5 \
		$(WORK_DIR)/predict/test_new.txt
$(WORK_DIR)/score_new.txt: $(WORK_DIR)/predict/test_new.txt | $(WORK_DIR)/predict
	python $(SCRIPT_DIR)/punctuator2/error_calculator.py $(F_DIR)/lt.test.txt $(WORK_DIR)/predict/test_new.txt > $@

score/new: $(WORK_DIR)/score_new.txt
	cat $^
#################################################################################################
$(WORK_DIR)/predict/dev.txt: $(F_DIR)/lt.dev.txt | $(WORK_DIR)/predict
	python $(SCRIPT_DIR)/predict.py $(F_DIR)/lt.dev.txt $(MAIN_VOCAB_FILE) $(WORK_DIR)/model/$(MODEL_PREFIX)_$(MODEL_TEST).h5 \
		$(WORK_DIR)/predict/dev.txt
$(WORK_DIR)/score_dev.txt: $(WORK_DIR)/predict/dev.txt | $(WORK_DIR)/predict
	python $(SCRIPT_DIR)/punctuator2/error_calculator.py $(F_DIR)/lt.dev.txt $(WORK_DIR)/predict/dev.txt > $@

score/dev: $(WORK_DIR)/score_dev.txt
	cat $^	
#################################################################################################
$(WORK_DIR)/data/.done: $(WORK_DIR)/final/lt.train.txt | $(WORK_DIR)/data
	pv $(WORK_DIR)/final/lt.train.txt | python $(SCRIPT_DIR)/data/text_to_train.py --vocab $(MAIN_VOCAB_FILE) > $(WORK_DIR)/data/train
	pv $(WORK_DIR)/final/lt.dev.txt | python $(SCRIPT_DIR)/data/text_to_train.py --vocab $(MAIN_VOCAB_FILE) > $(WORK_DIR)/data/dev
	wc -l $(WORK_DIR)/data/train | awk '{print $$1}' > $(WORK_DIR)/data/train.counts
	wc -l $(WORK_DIR)/data/dev | awk '{print $$1}' > $(WORK_DIR)/data/dev.counts
	touch $@

$(WORK_DIR)/model/.done: $(WORK_DIR)/data/.done | $(WORK_DIR)/model
	rm -rf $(WORK_DIR)/tb
	python $(SCRIPT_DIR)/continue_train.py --data-dir $(WORK_DIR)/data --model-dir $(WORK_DIR)/model \
		--word-vec-size=$(WORD_VEC_SIZE) --hidden=$(HIDDEN) $(GPU_SETTING) \
		--shuffle $(SHUFFLE) --prefetch $(PREFETCH) $(PREFETCH_SETTING) \
		--batch-size $(BATCH_SIZE) --model-in $(MAIN_MODEL_FILE) $(TENSORBOARD_SETTING) 
	touch $@
#################################################################################################
build: info $(WORK_DIR)/model/.done
#################################################################################################
clean:
	rm -rf $(WORK_DIR)
#################################################################################################
.PHONY: info clean
#################################################################################################
