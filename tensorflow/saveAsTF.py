import tensorflow as tf
import numpy
from tensorflow import keras
from tensorflow.keras import backend
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import signature_def_utils
from tensorflow.python.saved_model import tag_constants
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

with tf.Session() as sess:
    backend.set_session(sess)  
    print('Loading')
    m = model.load(in_file)

    print('Saving tf')
    inputsd = {"in": m.input }
    outputsd = {"out": m.output }
    print('================ THESE ARE IMPORTANT:===================')
    print('Input name  :', m.input.name )
    print('Output name :', m.output.name )
    print('==============+++++++===================================')

    signature_def_map = {
      signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY:
          signature_def_utils.predict_signature_def(inputsd, outputsd)}
      
    builder = tf.saved_model.builder.SavedModelBuilder(out_dir)  
    # Tag the model, required for Go
    builder.add_meta_graph_and_variables(sess, 
        tags=[tag_constants.SERVING], 
        signature_def_map=signature_def_map, 
        strip_default_attrs=True)
    builder.save()  
