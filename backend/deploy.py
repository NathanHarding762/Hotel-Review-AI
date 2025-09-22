# deploy.py
import os
import shutil
import subprocess

# Paths
project_root = os.getcwd()
train_script = os.path.join(project_root, "train.py")  # your training script
backend_path = os.path.join(project_root, "backend")

# 1️⃣ Run the training script
print("Running train.py...")
subprocess.run(["python", train_script], check=True)

# 2️⃣ Copy model and tokenizer to backend
model_src = os.path.join(project_root, "hotel_model.h5")
tokenizer_src = os.path.join(project_root, "tokenizer.pkl")

model_dst = os.path.join(backend_path, "hotel_model.h5")
tokenizer_dst = os.path.join(backend_path, "tokenizer.pkl")

shutil.copy2(model_src, model_dst)
shutil.copy2(tokenizer_src, tokenizer_dst)

print("✅ Deployment complete: model and tokenizer updated in backend!")
