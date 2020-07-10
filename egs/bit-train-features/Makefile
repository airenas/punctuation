-include Makefile.options
MAIN_DIR=${CURDIR}/../..
ifeq ($(GPU),1)
    GPU_SETTING=--use-gpu
endif
ifeq ($(PREFETCH_ON),)
else
    PREFETCH_SETTING=--prefetch-device $(PREFETCH_ON)
endif
ifeq ($(PROFILE),1)
    TENSORBOARD_SETTING=--tensorboard-dir $(WORK_DIR)/tb
endif
#################################################################################################
info:
	@echo "Input		: $(INPUT_DIR)"
	@echo "GP			: $(GPU)"
	@echo "Hidden		: $(HIDDEN)"
	@echo "Word vec		: $(WORD_VEC_SIZE)"
	@echo "Prefetch on	: $(PREFETCH_SETTINGs)"
#################################################################################################
$(WORK_DIR)/data:
	mkdir -p $@
$(WORK_DIR)/model:
	mkdir -p $@
$(WORK_DIR)/predict:
	mkdir -p $@
#################################################################################################
$(WORK_DIR)/data/.done: | $(WORK_DIR)/data
	pv $(INPUT_DIR)/final/lt.train.txt | python $(SCRIPT_DIR)/data/text_to_train.py --change-unk > $(WORK_DIR)/data/train
	pv $(INPUT_DIR)/final/lt.dev.txt | python $(SCRIPT_DIR)/data/text_to_train.py --change-unk > $(WORK_DIR)/data/dev
	cp $(INPUT_DIR)/config/features.txt $(WORK_DIR)/data
	wc -l $(WORK_DIR)/data/train | awk '{print $$1}' > $(WORK_DIR)/data/train.counts
	wc -l $(WORK_DIR)/data/dev | awk '{print $$1}' > $(WORK_DIR)/data/dev.counts
	touch $@

$(WORK_DIR)/model/.done: $(WORK_DIR)/data/.done | $(WORK_DIR)/model
	rm -rf $(WORK_DIR)/tb
	python $(SCRIPT_DIR)/train-features.py --data-dir $(WORK_DIR)/data --model-dir $(WORK_DIR)/model \
		--word-vec-size=$(WORD_VEC_SIZE) --hidden=$(HIDDEN) $(GPU_SETTING) \
		--shuffle $(SHUFFLE) --prefetch $(PREFETCH) $(PREFETCH_SETTING) \
		--batch-size $(BATCH_SIZE) $(TENSORBOARD_SETTING)
	touch $@

$(WORK_DIR)/predict/test.txt: $(WORK_DIR)/data/.done $(WORK_DIR)/model/.done | $(WORK_DIR)/predict
	python $(SCRIPT_DIR)/predict-features.py --test $(INPUT_DIR)/final/lt.test.txt --features $(WORK_DIR)/data/features.txt \
		--model $(WORK_DIR)/model/$(MODEL_PREFIX)_$(MODEL_TEST).h5 --out $(WORK_DIR)/predict/test.txt \
		--change-unk

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
tensorboard:
	tensorboard --logdir $(WORK_DIR)/tb
#################################################################################################
clean:
	rm -rf $(WORK_DIR)
#################################################################################################
.PHONY: info clean
#################################################################################################
