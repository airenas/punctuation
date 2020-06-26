-include Makefile.options
PATH:=$(TOOLS_ROOT)/bin:$(PATH)
F_DIR=$(WORK_DIR)/final
#################################################################################################
info:
	@echo "Input:     $(INPUT_FILE)"
	@echo "Sentences: $(SENTENCES)"
	@echo "Top words: $(TOP_WORDS)"
#################################################################################################
$(WORK_DIR):
	mkdir -p $@
$(F_DIR):
	mkdir -p $@
$(WORK_DIR)/config:
	mkdir -p $@
$(WORK_DIR)/text:
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
$(WORK_DIR)/config/oov.txt: | $(WORK_DIR)/config
	echo "<UNK>" > $(WORK_DIR)/config/oov.txt
#################################################################################################
$(WORK_DIR)/config/data_weights.txt: | $(WORK_DIR)/config
	echo train 1 1.0 > $(WORK_DIR)/config/data_weights.txt

$(WORK_DIR)/text/train.txt: $(F_DIR)/lt.train.txt | $(WORK_DIR)/text
	pv $^ | python ../../tensorflow/data/clean-punct.py > $@

$(WORK_DIR)/text/train.counts: $(WORK_DIR)/text/train.txt
	pv $^ | python ../../tensorflow/data/text-to-counts.py > $@

$(WORK_DIR)/config/words.txt: $(WORK_DIR)/text/train.txt | $(WORK_DIR)/config
	pv $^ | python ../../tensorflow/data/text-to-vocab.py --add-eps '<eps>' --add-unk '<UNK>' > $@
	$(eval n=`cat $@ | wc -l`)
	echo "<brk> $(n)" >> $@
	$(eval n=`cat $@ | wc -l`)
	echo "<s> $(n)" >> $@

$(WORK_DIR)/config/unigram_probs.txt: $(WORK_DIR)/config/words.txt $(WORK_DIR)/config/data_weights.txt $(WORK_DIR)/text/train.counts
	python $(KALDI_ROOT)/scripts/rnnlm/get_unigram_probs.py --vocab-file=$(WORK_DIR)/config/words.txt \
                              --unk-word="<UNK>" \
                              --data-weights-file=$(WORK_DIR)/config/data_weights.txt \
                              $(WORK_DIR)/text | awk 'NF==2' > $@

$(WORK_DIR)/config/features.txt: $(WORK_DIR)/config/unigram_probs.txt
	python $(KALDI_ROOT)/scripts/rnnlm/choose_features.py --unigram-probs=$(WORK_DIR)/config/unigram_probs.txt \
                            --use-constant-feature=true \
                            --special-words='<s>,<brk>,<UNK>' \
                            --top-word-features=$(TOP_WORDS) \
                            --max-ngram-order=3 \
                            $(WORK_DIR)/config/words.txt > $@
$(WORK_DIR)/config/word_feats.txt: $(WORK_DIR)/config/features.txt
	python $(KALDI_ROOT)/scripts/rnnlm/get_word_features.py --unigram-probs=$(WORK_DIR)/config/unigram_probs.txt \
		$(WORK_DIR)/config/words.txt $(WORK_DIR)/config/features.txt > $@

build: info $(WORK_DIR)/config/word_feats.txt
#################################################################################################
clean:
	rm -rf $(WORK_DIR)
#################################################################################################
.PHONY: info clean
#################################################################################################
