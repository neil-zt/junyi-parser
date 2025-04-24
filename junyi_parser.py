# contents_processor.py

import json

# Input and output file paths
INPUT_PATH = 'contents.json'
OUTPUT_PATH = 'contents_flat.json'

def load_json(path):
    """Load JSON data from a file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def prune_metadata(node):
    """
    Recursively remove 'id' and 'tags', rename 'hasContentChild' to 'isContent',
    and keep 'title', 'href', 'isContent', 'children'.
    """
    if isinstance(node, dict):
        new_node = {}
        for k, v in node.items():
            # Drop unwanted keys
            if k in ('id', 'tags'):
                continue
            # Rename hasContentChild
            if k == 'hasContentChild':
                new_node['isContent'] = prune_metadata(v)
            elif k == 'children':
                new_node['children'] = [prune_metadata(child) for child in v]
            else:
                new_node[k] = prune_metadata(v)
        return new_node
    elif isinstance(node, list):
        return [prune_metadata(item) for item in node]
    else:
        return node

def filter_subjects(data, subjects_to_keep):
    """
    Keep only top-level subjects with titles in subjects_to_keep.
    """
    top_children = data.get('data', {}).get('children', [])
    filtered = [child for child in top_children if child.get('title') in subjects_to_keep]
    data['data']['children'] = filtered
    return data

def gather_leaf_chapters(node):
    """
    Recursively gather leaf nodes (chapters) from a subtree.
    """
    if not node.get('children'):
        return [{
            'title': node['title'],
            'href': node.get('href', ''),
            'isContent': node.get('isContent', False)
        }]
    chapters = []
    for child in node['children']:
        chapters.extend(gather_leaf_chapters(child))
    return chapters

def flatten_structure(data):
    """
    Convert nested subjects → grades → chapters into a shallow mapping.
    Grades '國小', '國中', '高中' are grouped; others under '其他'.
    """
    subjects = {}
    grade_labels = ['國小', '國中', '高中']

    for subj in data['data']['children']:
        subj_title = subj['title']
        # Categorize children by grade label
        grade_map = {gl: [] for gl in grade_labels}
        misc = []

        for child in subj.get('children', []):
            assigned = False
            for gl in grade_labels:
                if gl in child.get('title', ''):
                    grade_map[gl].append(child)
                    assigned = True
                    break
            if not assigned:
                misc.append(child)

        subj_entries = []
        # Process each grade category
        for gl in grade_labels:
            groups = grade_map[gl]
            if not groups:
                continue
            chapters = []
            for group in groups:
                chapters.extend(gather_leaf_chapters(group))
            subj_entries.append({
                'grade': gl,
                'href': '',
                'isContent': False,
                'chapters': chapters
            })

        # Any remaining under '其他'
        if misc:
            chapters = []
            for group in misc:
                chapters.extend(gather_leaf_chapters(group))
            subj_entries.append({
                'grade': '其他',
                'href': '',
                'isContent': False,
                'chapters': chapters
            })

        subjects[subj_title] = subj_entries

    return subjects

def save_json(data, path):
    """Save JSON data to a file with pretty formatting."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    subjects_to_keep = {'數學', '英語文', '自然', '國語文', '社會', '跨域素養'}
    # Load, prune, filter, flatten, and save
    data = load_json(INPUT_PATH)
    pruned = prune_metadata(data)
    filtered = filter_subjects(pruned, subjects_to_keep)
    flattened = flatten_structure(filtered)
    save_json(flattened, OUTPUT_PATH)
    print(f"Processed curriculum saved to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
