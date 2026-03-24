import os
import re

files = [
    r'myapp\templates\index.html',
    r'myapp\templates\sindex.html',
    r'myapp\templates\shop.html',
    r'myapp\templates\single.html',
    r'myapp\templates\bestseller.html',
    r'myapp\templates\cart.html'
]

updates = {
    'Patthar.png': ('Stone & Rock', 'Premium Stone Patthar <br> For Construction'),
    'Concrete_Blocks.jpg': ('Bricks & Blocks', 'Heavy Duty Concrete Blocks <br> Construction Grade'),
    'Concrete_Bricks.jpg': ('Bricks & Blocks', 'Solid Concrete Bricks <br> Premium Grade'),
    'Soil.png': ('Earth & Soil', 'Rich Organic Soil <br> Village Origin'),
    'Cement.jpg': ('Cement & Concrete', 'Premium Portland Cement <br> 50kg Bag'),
    'Rebars.jpg': ('Steel & Rebars', 'High Strength TMT Rebars <br> For Construction')
}

for fp in files:
    if not os.path.exists(fp): 
        print(f"Skipping {fp}")
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig = content
    for img, (cat, title) in updates.items():
        # Match from img tag to the h4 title tag
        # We find the specific blocks containing the images.
        def rep_func(m):
            t = m.group(0)
            t = re.sub(r'class="d-block mb-2">[^<]*</a>', f'class="d-block mb-2">{cat}</a>', t)
            t = re.sub(r'class="d-block h4">.*?</a>', f'class="d-block h4">{title}</a>', t, flags=re.DOTALL)
            return t
        
        # Regex to find the product card section starting with the image and ending with the title.
        pattern = rf'img/{img}.*?class="d-block mb-2">.*?class="d-block h4">.*?</a>'
        content = re.sub(pattern, rep_func, content, flags=re.DOTALL)

    if content != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated text mapping in {os.path.basename(fp)}')

print('Done')
