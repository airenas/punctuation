-include Makefile.options
MAIN_DIR=${CURDIR}/../..
ifeq ($(GPU), 1)
    GPU_SETTING=--use-gpu
endif
#################################################################################################
info:
	@echo "Input	: $(INPUT_DIR)"
	@echo "GPU		: $(GPU)"
	@echo "Hidden	: $(HIDDEN)"
	@echo "Word vec	: $(WORD_VEC_SIZE)"
#################################################################################################
$(WORK_DIR)/data:
	mkdir -p $@
$(WORK_DIR)/model:
	mkdir -p $@
$(WORK_DIR)/predict:
	mkdir -p $@
#################################################################################################
$(WORK_DIR)/data/.done: | $(WORK_DIR)/data
	pv $(INPUT_DIR)/final/lt.train.txt | python $(SCRIPT_DIR)/data/text-to-train.py > $(WORK_DIR)/data/train
	pv $(INPUT_DIR)/final/lt.dev.txt | python $(SCRIPT_DIR)/data/text-to-train.py > $(WORK_DIR)/data/dev
	cp $(INPUT_DIR)/config/features.txt $(WORK_DIR)/data
	wc -l $(WORK_DIR)/data/train | awk '{print $$1}' > $(WORK_DIR)/data/train.counts
	wc -l $(WORK_DIR)/data/dev | awk '{print $$1}' > $(WORK_DIR)/data/dev.counts
	touch $@

$(WORK_DIR)/model/.done: $(WORK_DIR)/data/.done | $(WORK_DIR)/model
	python $(SCRIPT_DIR)/train-features.py --data-dir $(WORK_DIR)/data --model-dir $(WORK_DIR)/model \
		--word-vec-size=$(WORD_VEC_SIZE) --hidden=$(HIDDEN) $(GPU_SETTING)
	touch $@

$(WORK_DIR)/predict/test.txt: $(WORK_DIR)/data/.done $(WORK_DIR)/model/.done | $(WORK_DIR)/predict
	python $(SCRIPT_DIR)/predict-features.py --test $(INPUT_DIR)/final/lt.test.txt --features $(WORK_DIR)/data/features.txt \
		--model $(WORK_DIR)/model/$(MODEL_PREFIX)_$(MODEL_TEST).h5 --out $(WORK_DIR)/predict/test.txt

$(WORK_DIR)/score.txt: $(WORK_DIR)/predict/test.txt | $(WORK_DIR)/predict
	python $(SCRIPT_DIR)/punctuator2/error_calculator.py $(INPUT_DIR)/final/lt.test.txt $(WORK_DIR)/predict/test.txt > $@
#################################################################################################
to-tf-format: $(WORK_DIR)/model/.done
	rm -rf $(WORK_DIR)/tf
	python $(SCRIPT_DIR)/saveAsTF.py $(WORK_DIR)/model/$(MODEL_PREFIX)_$(MODEL_TEST).h5 $(WORK_DIR)/tf
#################################################################################################
prepare-data: info $(WORK_DIR)/data/.done
build: info $(WORK_DIR)/model/.done
predict: $(WORK_DIR)/score.txt
	cat $^
#################################################################################################
clean:
	rm -rf $(WORK_DIR)
#################################################################################################
.PHONY: info clean
#################################################################################################
