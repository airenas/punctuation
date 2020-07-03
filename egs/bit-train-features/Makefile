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
	pv $(INPUT_DIR)/final/lt.train.txt | python $(MAIN_DIR)/tensorflow/data/text-to-train.py > $(WORK_DIR)/data/train
	pv $(INPUT_DIR)/final/lt.dev.txt | python $(MAIN_DIR)/tensorflow/data/text-to-train.py > $(WORK_DIR)/data/dev
	cp $(INPUT_DIR)/config/features.txt $(WORK_DIR)/data
	touch $@

$(WORK_DIR)/model/.done: $(WORK_DIR)/data/.done | $(WORK_DIR)/model
	python $(MAIN_DIR)/tensorflow/train-features.py --data-dir $(WORK_DIR)/data --model-dir $(WORK_DIR)/model \
		--word-vec-size=$(WORD_VEC_SIZE) --hidden=$(HIDDEN) $(GPU_SETTING)
	touch $@

$(WORK_DIR)/predict/test.txt: $(WORK_DIR)/data/.done $(WORK_DIR)/model/.done | $(WORK_DIR)/predict
	python $(MAIN_DIR)/tensorflow/predict-features.py --test $(INPUT_DIR)/final/lt.test.txt --features $(WORK_DIR)/data/features.txt \
		--model $(WORK_DIR)/model/$(MODEL_PREFIX)_$(MODEL_TEST).h5 --out $(WORK_DIR)/predict/test.txt

$(WORK_DIR)/score.txt: $(WORK_DIR)/predict/test.txt | $(WORK_DIR)/predict
	python $(MAIN_DIR)/tensorflow/punctuator2/error_calculator.py $(INPUT_DIR)/final/lt.test.txt $(WORK_DIR)/predict/test.txt > $@
#################################################################################################
to-tf-format: $(WORK_DIR)/model/.done
	rm -rf $(WORK_DIR)/tf
	python $(MAIN_DIR)/tensorflow/saveAsTF.py $(WORK_DIR)/model/$(MODEL_PREFIX)_$(MODEL_TEST).h5 $(WORK_DIR)/tf
#################################################################################################
build: info $(WORK_DIR)/model/.done
predict: $(WORK_DIR)/score.txt
	cat $^
#################################################################################################
clean:
	rm -rf $(WORK_DIR)
#################################################################################################
.PHONY: info clean
#################################################################################################
