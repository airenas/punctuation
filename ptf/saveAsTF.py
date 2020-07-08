import tensorflow as tf
from tensorflow import keras
import model.model as model
import sys

if len(sys.argv) > 1:
    in_file = sys.argv[1]
else:
    sys.exit("Input file path argument missing")

if len(sys.argv) > 2:
    out_dir = sys.argv[2]
else:
    sys.exit("Output dir argument missing")

print('Loading')
m = model.load(in_file)
m.summary(150)

print('Saving tf')
inputsd = {"in": m.input }
outputsd = {"out": m.output }
print('================ THESE ARE IMPORTANT:===================')
print('Input name  :', m.input.name )
print('Output name :', m.output.name )
print('========================================================')

keras.experimental.export_saved_model(m, out_dir)
print('==============DONE =====================================')
print('========================================================')