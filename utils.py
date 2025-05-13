import os

def build_readme(product_dir, topic, reason):
    content = f"# {topic}\n\n**Why this matters:** {reason}\n\nThis auto-generated tool solves a trending problem using automation.\n"
    with open(os.path.join(product_dir, "README.md"), "w") as f:
        f.write(content)

def build_faq(product_dir, topic):
    content = f"## Frequently Asked Questions\n\n**Q: What does this tool do?**\nA: It automates a solution for the trending topic: *{topic}*.\n"
    with open(os.path.join(product_dir, "FAQ.md"), "w") as f:
        f.write(content)

def build_sample_output(product_dir, topic):
    content = f"This is a sample output for the tool based on the topic: {topic}.\n\n[Sample output would go here]"
    with open(os.path.join(product_dir, "sample_output.txt"), "w") as f:
        f.write(content)
