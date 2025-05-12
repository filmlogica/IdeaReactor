import os
import json
import shutil
import sys
from price_engine import calculate_price
from utils import build_readme, build_faq, build_sample_output
import py_compile
import subprocess

def build_product(product_name):
    print(f"\n🛠️ [Product Builder] Starting build for: {product_name}")

    # Load trend info
    with open("trend.json", "r") as f:
        trend = json.load(f)

    topic = trend['topic']
    reason = trend['reason']
    score = float(trend['score'])
    complexity = trend.get('complexity', 'moderate')

    # Calculate price
    print("\n🧮 [Pricing Engine] Calculating price...")
    price = calculate_price(score, complexity)
    print(f"💰 Final Price: ${price:.2f}")

    # Create product folder
    product_dir = os.path.join("products", product_name)
    os.makedirs(product_dir, exist_ok=True)
    print(f"📂 [Directory] Created at {product_dir}")

    # Create the Python script (core product)
    script_path = os.path.join(product_dir, f"{product_name}.py")
    with open(script_path, "w") as f:
        f.write(f"# Auto-generated script for: {topic}\n")
        f.write("# Summary:\n")
        f.write(f"# {reason}\n\n")
        f.write("print('This script addresses a trending market problem using automation.')\n")

    print(f"📜 [Script] Written to: {script_path}")

    # Compile to EXE using PyInstaller
    print("🔨 [Compile] Converting script to executable (.exe)...")
    subprocess.run([
        "pyinstaller", "--onefile", "--distpath", product_dir,
        "--workpath", "build", "--specpath", "build",
        script_path
    ], check=True)

    # Remove the raw script and spec
    os.remove(script_path)
    shutil.rmtree("build", ignore_errors=True)
    spec_file = f"{product_name}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
    print("🧹 [Cleanup] Raw files removed.")

    # Build supporting files
    build_readme(product_dir, topic, reason)
    build_faq(product_dir, topic)
    build_sample_output(product_dir, topic)

    # Save price info
    with open(os.path.join(product_dir, "price.txt"), "w") as f:
        f.write(str(price))

    # Zip the product folder
    zip_path = shutil.make_archive(product_dir, 'zip', product_dir)
    print(f"📦 [ZIP] Created: {zip_path}")

    # Display file sizes
    print("\n📊 [File Sizes]")
    for root, dirs, files in os.walk(product_dir):
        for file in files:
            file_path = os.path.join(root, file)
            size_kb = os.path.getsize(file_path) / 1024
            print(f" - {file}: {size_kb:.2f} KB")

    # Display product preview
    print("\n🖼️ [Product Preview]")
    readme_path = os.path.join(product_dir, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            preview = f.read(500)
            print(preview)
            if len(preview) == 500:
                print("... [truncated]")
    else:
        print("No README.md found.")

    print("\n✅ [Build Complete] Your digital product is ready!\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ [Error] Please provide a product name.")
        sys.exit(1)
    build_product(sys.argv[1])
