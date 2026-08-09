# Step-by-Step Execution GuideEnvironment Activation: Open a terminal and source your Python virtual environment

source ~/env/edge_ai_venv/bin/activate

# Initialize Calibration Cache: Create a local cache folder to store a representative sample of real meltpool camera images used to calibrate the integer boundary scales:

mkdir -p ~/am_workspace/calibration_data

# Run Quantization Engine Script: Save the compilation logic script below as compress_model.py and run it to convert the baseline model structures:

python3 compress_model.py

# Verify Asset Footprint Reduction: Measure file sizes to confirm that your new model is roughly 75% smaller than the original:

ls -lh models/fp32_meltpool_net/saved_model.pb models/int8_meltpool_net.tflite

