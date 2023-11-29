-include Makefile.options
PATH:=$(TOOLS_ROOT)/bin:$(PATH)
F_DIR=$(WORK_DIR)/final
#################################################################################################
info:
	@echo "Input dir : $(INPUT_DIR)"
	@echo "Top words : $(TOP_WORDS)"
	@echo "Work Dir	 : $(WORK_DIR)"
#################################################################################################
$(WORK_DIR):
	mkdir -p $@
$(WORK_DIR)/config:
	mkdir -p $@
$(WORK_DIR)/text:
	mkdir -p $@
$(WORK_DIR)/final:
	mkdir -p $@
#################################################################################################
$(WORK_DIR)/config/oov.txt: | $(WORK_DIR)/config
	echo "<UNK>" > $(WORK_DIR)/config/oov.txt
#################################################################################################
$(WORK_DIR)/config/data_weights.txt: | $(WORK_DIR)/config
	echo train 1 1.0 > $(WORK_DIR)/config/data_weights.txt

$(WORK_DIR)/text/train.txt: $(INPUT_DIR)/lt.train.txt | $(WORK_DIR)/text
	pv $^ | python $(SCRIPT_DIR)/data/clean-punct.py | python local/change_unk.py > $@

$(WORK_DIR)/text/train.counts: $(WORK_DIR)/text/train.txt
	pv $^ | python $(SCRIPT_DIR)/data/text-to-counts.py > $@

$(WORK_DIR)/config/words.txt: $(WORK_DIR)/text/train.txt | $(WORK_DIR)/config
	pv $^ | python $(SCRIPT_DIR)/data/text-to-vocab.py --add-eps '<eps>' --add-unk '<UNK>' > $@
	$(eval n=`cat $@ | wc -l`)
	echo "<brk> $(n)" >> $@
	$(eval n=`cat $@ | wc -l`)
	echo "<s> $(n)" >> $@
	$(eval n=`cat $@ | wc -l`)
	echo "</S> $(n)" >> $@

$(WORK_DIR)/config/unigram_probs.txt: $(WORK_DIR)/config/words.txt $(WORK_DIR)/config/data_weights.txt $(WORK_DIR)/text/train.counts
	python $(KALDI_ROOT)/scripts/rnnlm/get_unigram_probs.py --vocab-file=$(WORK_DIR)/config/words.txt \
                              --unk-word="<UNK>" \
                              --data-weights-file=$(WORK_DIR)/config/data_weights.txt \
                              $(WORK_DIR)/text | awk 'NF==2' > $@

$(WORK_DIR)/config/features.txt: $(WORK_DIR)/config/unigram_probs.txt
	python $(KALDI_ROOT)/scripts/rnnlm/choose_features.py --unigram-probs=$(WORK_DIR)/config/unigram_probs.txt \
                            --use-constant-feature=true \
                            --special-words='<s>,<brk>,<UNK>,<NUM>,</S>' \
                            --top-word-features=$(TOP_WORDS) \
                            --include-unigram-feature=false \
                            --max-ngram-order=3 \
                            $(WORK_DIR)/config/words.txt > $@
$(WORK_DIR)/config/word_feats.txt: $(WORK_DIR)/config/features.txt
	python $(KALDI_ROOT)/scripts/rnnlm/get_word_features.py --unigram-probs=$(WORK_DIR)/config/unigram_probs.txt \
		$(WORK_DIR)/config/words.txt $(WORK_DIR)/config/features.txt > $@

$(WORK_DIR)/final/.done: $(WORK_DIR)/final
	ln -s $(INPUT_DIR)/lt.train.txt $(WORK_DIR)/final/lt.train.txt
	ln -s $(INPUT_DIR)/lt.test.txt $(WORK_DIR)/final/lt.test.txt
	ln -s $(INPUT_DIR)/lt.dev.txt $(WORK_DIR)/final/lt.dev.txt
	touch $@

#################################################################################################
dev: $(WORK_DIR)/text/train.counts
build: info $(WORK_DIR)/config/word_feats.txt $(WORK_DIR)/final/.done
#################################################################################################
put-data:
	$(SSH_CMD) "mkdir -p $(REMOTE_DIR)"
	$(PUT_CMD) $(INPUT_DIR)/*.txt $(PUT_DIR)/final/
	$(PUT_CMD) $(WORK_DIR)/config/features.txt $(PUT_DIR)/config/
#################################################################################################
clean:
	rm -rf $(WORK_DIR)
#################################################################################################
.PHONY: info clean
#################################################################################################
