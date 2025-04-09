import json
import os

def txt_to_json(folder_short_desc, folder_long_desc, output_folder):
    files = [f for f in os.listdir(folder_short_desc) if f.endswith('.txt')]

    for file in files:
        category = file.replace('.txt', '')
        desc_file = os.path.join(folder_short_desc, f"{category}.txt")
        long_desc_file = os.path.join(folder_long_desc, f"{category}_longer.txt")
        output_file = os.path.join(output_folder, f"{category}.json")

        with open(desc_file, 'r', encoding='utf-8') as f1, open(long_desc_file, 'r', encoding='utf-8') as f2:
            descriptions = f1.readlines()
            long_descriptions = f2.readlines()

        if len(descriptions) != len(long_descriptions):
            raise ValueError(f"The number of lines in {category} files must be the same.")

        data = []
        for idx, (desc, long_desc) in enumerate(zip(descriptions, long_descriptions), start=1):
            entry = {
                "id": f"{idx:03d}",
                "description": desc.strip(),
                "long_description": long_desc.strip(),
                "category": [category]
            }
            data.append(entry)

        os.makedirs(output_folder, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f_out:
            json.dump(data, f_out, indent=4, ensure_ascii=False)

        print(f"JSON file successfully created: {output_file}")

if __name__ == "__main__":
    folder_short_desc = "VBench/prompts/prompts_per_category"
    folder_long_desc = "VBench/prompts/gpt_enhanced_prompts/prompts_per_category_longer"
    output_folder = "Vbench-Lite/category_output"

    txt_to_json(folder_short_desc, folder_long_desc, output_folder)