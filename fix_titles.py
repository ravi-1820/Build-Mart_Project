import os
import re

files = [
    r'myapp\templates\index.html',
    r'myapp\templates\sindex.html',
    r'myapp\templates\shop.html',
    r'myapp\templates\bestseller.html',
    r'myapp\templates\single.html',
    r'myapp\templates\cart.html'
]

# (image_name, old_cat, old_name, new_cat, new_name)
updates = [
    ('Patthar.png', 'Cement & Concrete', r'Premium Portland Cement (?:\s*<br>\s*)? 50kg Bag', 'Stone & Rock', 'Premium Stone Patthar <br> For Construction'),
    ('Concrete_Bricks.jpg', 'Steel & Rebars', r'High Strength TMT Rebars (?:\s*<br>\s*)? For Construction', 'Bricks & Blocks', 'Solid Concrete Bricks <br> Premium Grade'),
    ('Concrete_Blocks.jpg', 'Bricks & Blocks', r'Red Clay Solid Bricks (?:\s*<br>\s*)? Premium Grade', 'Bricks & Blocks', 'Heavy Duty Concrete Blocks <br> Construction Grade'),
    ('Soil.png', 'Steel & Rebars', r'High Strength TMT Rebars (?:\s*<br>\s*)? For Construction', 'Earth & Soil', 'Rich Organic Soil <br> Village Origin'),
    ('Rebars.jpg', 'Bricks & Blocks', r'Red Clay Solid Bricks (?:\s*<br>\s*)? Premium Grade', 'Steel & Rebars', 'High Strength TMT Rebars <br> For Construction'),
]

for fp in files:
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig = content
        for img, old_cat, old_name_pattern, new_cat, new_name in updates:
            # We want to replace the FIRST occurrence of old_cat and old_name AFTER the mg
            # Since regex with .*? can be greedy or miss, we split by image name.
            parts = content.split(img)
            if len(parts) > 1:
                # Reconstruct content, modifying each part after the first (which means it's after the image)
                new_parts = [parts[0]]
                for i in range(1, len(parts)):
                    part = parts[i]
                    # We only want to replace within the first ~2000 chars of the part (the product card)
                    target_chunk = part[:2000]
                    rest = part[2000:]
                    
                    # Replace category specifically in class="d-block mb-2" or similar
                    target_chunk = re.sub(
                        r'(<a[^>]*class="[^"]*mb-2[^"]*"[^>]*>\s*)' + re.escape(old_cat) + r'(\s*</a>)',
                        r'\g<1>' + new_cat + r'\g<2>',
                        target_chunk,
                        count=1
                    )
                    
                    target_chunk = re.sub(
                        r'(<a[^>]*class="[^"]*h4[^"]*"[^>]*>\s*)' + old_name_pattern + r'(\s*</a>)',
                        r'\g<1>' + new_name + r'\g<2>',
                        target_chunk,
                        count=1
                    )
                    
                    new_parts.append(target_chunk + rest)
                content = img.join(new_parts)
                
        if content != orig:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated {fp}')

print('Done')
