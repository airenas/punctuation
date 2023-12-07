-include Makefile.options
MAIN_DIR=${CURDIR}/../..
OUT_DIR=$(WORK_DIR)/punctuation
OUT_FILE=punctuation-$(VERSION).0.tar.gz
#################################################################################################
info:
	@echo "Input		: $(INPUT_DIR)"
	@echo "Model		: $(MODEL)"
	@echo "Output		: $(WORK_DIR)/$(OUT_FILE)"
#################################################################################################
$(WORK_DIR)/data:
	mkdir -p $@
$(OUT_DIR)/$(VERSION).0:
	mkdir -p $@
$(OUT_DIR)/models:
	mkdir -p $@
#################################################################################################
$(OUT_DIR)/$(VERSION).0/vocabulary: | $(OUT_DIR)/$(VERSION).0
	cp $(VOCAB) $@

$(OUT_DIR)/$(VERSION).0/settings.yml: $(OUT_DIR)/$(VERSION).0/vocabulary | $(OUT_DIR)/$(VERSION).0
	echo "info: \"hidden layers: 256, vocaburaly size: $$(wc -l $(WORK_DIR)/punctuation/$(VERSION).0/vocabulary \
		| awk '{print $$1}'), zip date: $$(date -Isec)\"" > $@
	echo "puctuationVocabulary: [' ', ',', '.', '?', '!',':',';','-']" >> $@
	echo "sentenceEnd: ['.', '?', '!']" >> $@
	echo "timesteps: 50" >> $@
	echo "unknownWord: <UNK>" >> $@
	echo "numWord: <NUM>" >> $@
	echo "sequenceEndWord: </S>" >> $@
	echo "model: punctuation dp" >> $@
	echo "version: $(VERSION)" >> $@

$(OUT_DIR)/models/punctuation/$(VERSION): $(MODEL) | $(OUT_DIR)/models
	rm -rf $@
	python $(SCRIPT_DIR)/save_as_tf.py $(MODEL) $@

$(OUT_DIR)/$(VERSION).0/info: | $(OUT_DIR)/$(VERSION).0
	python $(SCRIPT_DIR)/model_info.py $(MODEL) > $@

$(WORK_DIR)/$(OUT_FILE): $(OUT_DIR)/$(VERSION).0/settings.yml $(OUT_DIR)/$(VERSION).0/vocabulary \
	$(OUT_DIR)/models/punctuation/$(VERSION) $(OUT_DIR)/$(VERSION).0/info
	cd $(WORK_DIR) && tar -czvf $(OUT_FILE) punctuation
#################################################################################################
build: info $(WORK_DIR)/$(OUT_FILE)
#################################################################################################
clean:
	rm -rf $(WORK_DIR)
#################################################################################################
.PHONY: info clean
#################################################################################################
