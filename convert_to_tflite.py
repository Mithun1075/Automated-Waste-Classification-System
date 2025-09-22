import tensorflow as tf

# 1. Load your trained Keras model (.h5 file)
# Make sure you already trained & saved waste_cnn.h5
model = tf.keras.models.load_model("models/waste_cnn.h5")

# 2. Create a TFLiteConverter object from the Keras model
# This will allow converting the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# 3. Apply default optimization (quantization)
# This reduces model size & speeds up inference
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# 4. Convert the model → produces a TFLite (quantized) model
tflite_model = converter.convert()

# 5. Save the converted model to disk
# You will use this .tflite file inside your Django app
with open("models/waste_cnn_quant.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Quantized model saved as models/waste_cnn_quant.tflite")
