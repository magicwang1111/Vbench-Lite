import json
import matplotlib.pyplot as plt
import os

def count_ids(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return len([item['id'] for item in data if 'id' in item])

def generate_dimension_pie_chart(dimension_name, original_count, filtered_count, output_path):
    removed = original_count - filtered_count

    labels = ['Remaining (Filtered)', 'Removed']
    sizes = [filtered_count, removed]
    colors = ['#66b3ff', '#ff9999']

    def autopct_format(pct):
        total = sum(sizes)
        count = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n({count})'

    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes,
        labels=labels,
        autopct=autopct_format,
        startangle=140,
        colors=colors,
        textprops={'fontsize': 12}
    )
    plt.title(f'Filtered {dimension_name.replace("_", " ").title()} Dimension Proportion')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def generate_overall_pie_chart(total_original, total_filtered, output_path):
    unselected = total_original - total_filtered
    labels = ['Filtered Prompts', 'Unselected Prompts']
    sizes = [total_filtered, unselected]
    colors = ['#8fd9b6', '#ffcc99']

    def autopct_format(pct):
        total = sum(sizes)
        count = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n({count})'

    plt.figure(figsize=(8, 8))
    plt.pie(
        sizes,
        labels=labels,
        autopct=autopct_format,
        startangle=140,
        colors=colors,
        textprops={'fontsize': 12}
    )
    plt.title(f'Overall Filtered Proportion\nTotal Prompts: {total_original}')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

    print(f"📊 Overall pie chart saved to: {output_path}")

def batch_generate_all(original_dir, filtered_dir, output_dir):
    total_original = 0
    total_filtered = 0

    for filename in os.listdir(original_dir):
        if filename.endswith('.json'):
            dimension_name = os.path.splitext(filename)[0]
            original_path = os.path.join(original_dir, filename)
            filtered_path = os.path.join(filtered_dir, filename)

            if not os.path.exists(filtered_path):
                print(f"⚠️ Skipping: {filename} (no filtered match)")
                continue

            original_count = count_ids(original_path)
            filtered_count = count_ids(filtered_path)

            total_original += original_count
            total_filtered += filtered_count

            chart_path = os.path.join(output_dir, f"{dimension_name}.png")
            generate_dimension_pie_chart(dimension_name, original_count, filtered_count, chart_path)
            print(f"✅ Saved: {chart_path} ({filtered_count}/{original_count})")

    
    overall_chart_path = os.path.join(output_dir, 'overall_filtered_distribution.png')
    generate_overall_pie_chart(total_original, total_filtered, overall_chart_path)


original_json_dir = '/Vbench-Lite/vbench_lite_t2v/dimension_original'
filtered_json_dir = '/Vbench-Lite/vbench_lite_t2v/dimension_filtered'
output_chart_dir = 'pie_img'


batch_generate_all(original_json_dir, filtered_json_dir, output_chart_dir)
