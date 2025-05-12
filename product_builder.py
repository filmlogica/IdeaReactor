import os
import zipfile
import json
import subprocess
import sys
from price_engine import calculate_price

def build_product_folder(product_name, script_file, description, faq_content, sample_output, final_price):
    base_path = os.path.join("products", product_name)
    os.makedirs(os.path.join(base_path, "screenshots"), exist_ok=True)

    print(f"📂 [Build] Creating folder: {base_path}")

    # Write the script file
    script_path = os.path.join(base_path, f"{product_name}.py")
    with open(script_path, "w") as f:
        f.write(script_file)
    print(f"📜 [Script] Written to: {script_path}")

    # Create README
    with open(os.path.join(base_path, "README.md"), "w") as f:
        f.write(f"# {product_name}\n\n{description}\n\n## How to Use\n- Double-click the .exe\n- Follow prompts")
    print("📝 [README] Created")

    # Create FAQ
    with open(os.path.join(base_path, "FAQ.md"), "w") as f:
        f.write(faq_content)
    print("❓ [FAQ] Created")

    # Create sample output
    with open(os.path.join(base_path, "output_sample.txt"), "w") as f:
        f.write(sample_output)
    print("📄 [Sample Output] Created")

    # Save price
    with open(os.path.join(base_path, "price.txt"), "w") as f:
        f.write(f"${final_price}")
    print(f"💰 [Price] Saved: ${final_price}")

    # Compile the script into a .exe
    print("🔨 [Compile] Converting script to .exe...")
    subprocess.run([
        "pyinstaller", "--onefile", "--distpath", base_path,
        "--workpath", "build", "--specpath", "build", script_path
    ], check=True)
    print("✅ [Compile] .exe created")

    # Clean up spec file if it exists
    spec_path = os.path.join("build", f"{product_name}.spec")
    if os.path.exists(spec_path):
        os.remove(spec_path)
        print("🧹 [Clean] .spec file removed")

    # Remove original .py script
    if os.path.exists(script_path):
        os.remove(script_path)
        print("🧹 [Clean] Original .py file removed")

    # Zip the folder
    zip_name = os.path.join("products", f"{product_name}.zip")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(base_path):
            for file in files:
                full_path = os.path.join(root, file)
                zipf.write(full_path, os.path.relpath(full_path, base_path))
    print(f"📦 [ZIP] Product archived: {zip_name}")

    return zip_name

# --- Script Entry ---
if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Generate a product"
    product_name = sys.argv[2] if len(sys.argv) > 2 else "AI_Product"

    print("🛠️ [Product Builder] Starting build process...")

    with open("trend.json", "r") as f:
        trend = json.load(f)

    complexity = "moderate"
    price = calculate_price(trend["score"], complexity)

    script = f"print('This script is based on the trend: {trend['topic']}')"
    desc = f"This script was generated based on the trending topic: {trend['topic']}.\nReason: {trend['reason']}"
    faq = f"# FAQ\n\n**Q: What is this?**\nA: A script auto-generated based on \"{trend['topic']}\".\n\n**Q: How do I run it?**\nA: Just double-click the .exe inside the ZIP."
    sample_output = f"This tool is based on {trend['topic']}. It performs X functionality and can be customized easily."

    zipfile = build_product_folder(product_name, script, desc, faq, sample_output, price)

    print(f"🚀 [Build Complete] Product ready and zipped at: {zipfile}")

