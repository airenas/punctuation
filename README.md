# Punctuation
Punctuation restoration using TensorFlow

## Introduction
The repository was inspired by **[github.com/ottokart/punctuator2](https://github.com/ottokart/punctuator2)**. I did not want to use *phyton* in serving the model. So I tried to change *Theano* to *TensorFlow*. **Attention** and **Late Fusion** layers were the big challanges for me, I'm not sure they are 100% correct. I compared the results with **punctuator2** and they looked very similar.

## NEW: Feature representation of words
Added support of [Kaldi](https://github.com/kaldi-asr/kaldi) like word features. Word hashing was originally described in [Learning deep structured semantic models for web search using clickthrough data - by Po-Sen Huang et al. 2013](https://posenhuang.github.io/papers/cikm2013_DSSM_fullversion.pdf). It allows to use nearly unlimited vocabulary instead of a shortlist for NN training.
Samples added for [data prepareation](egs/bit-prepare-features) and [training](egs/bit-train-features). 

## Requirements
Implementation was tested with *python* 3.7.3. The training code uses modules: 
```bash
pip install tensorflow # or tensorflow-gpu, tested with tensorflow==2.2.0
pip install tqdm
```
The optimization of hyper parameters:
```bash
pip install parameter-sherpa
pip install keras
```

## Data preparation
For the initial data requirements see **[github.com/ottokart/punctuator2](https://github.com/ottokart/punctuator2)**. You can configure punctuation and vocabulary size in the [ptf/data/data.py](ptf/data/data.py). To prepare the data for the training:
```bash
python ptf/punctuator2/data.py <initialDataDir> <dataDir>
```
Or see the [egs](egs) for sample scripts 

## Training
To train one model, you can configure model parameters in [ptf/train.py](ptf/train.py). The taining can be performed by:
```bash
mkdir model1 && cd model1
python ../ptf/train.py <dataDir> <modelPrefix>
```
The trained model is saved as *keras* hd5 format in the working folder *model1*. 

## Optimization
There is the python script to optimize hyperparameters of a model using *sherpa* tool. See  [optimize/optimize.py](optimize/optimize.py). The sample to start an optimization:
```bash
mkdir optim1 && cd optim1
python ../optimize/optimize.py <dataDir> 
```
All models are saved in in the working folder *optim1*.


## Prediction, error calculation
To predict punctuation for a test text:
```bash
python ptf/predict.py <testTextFile> <vocaburaly> <hd5ModelFile> <predictedOutputFile>
```
To evaluate error scores of the prediction:
```bash
python ptf/punctuator2/error_calculator.py <testTextFile> <predictedOutputFile>
```

## Saving as a pure *tensorflow* model
During the training all models are saved in *keras* format. To save a model in a pure *tensorflow* format there is a script:
```bash
python ptf/save_as_tf.py <hd5ModelFile> <tfModelOutputDir>
```
## Loading model with *go*
Sample *go* code on how to load the trained tensorflow model: [examples/goload/loadtf.go](examples/goload/loadtf.go). To compile the sample *go* code you need to install *tensorflow* library and configure *LD_LIBRARY_PATH*. See [https://www.tensorflow.org/install/lang_go](https://www.tensorflow.org/install/lang_go)

---
### Author

**Airenas Vaičiūnas**
 
* [bitbucket.org/airenas](https://bitbucket.org/airenas)
* [github.com/airenas](https://github.com/airenas/)
* [linkedin.com/in/airenas](https://www.linkedin.com/in/airenas/)


---
### License

Copyright © 2020, [Airenas Vaičiūnas](https://github.com/airenas).
Released under the [The 3-Clause BSD License](LICENSE).

Also, please, see the [License Ottokar Tilk](Licenses/).

---
