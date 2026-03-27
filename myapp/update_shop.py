import codecs

path = r"c:\Users\rajja\OneDrive\Desktop\PYTHON\Project\myenv\myproject\myapp\templates\shop.html"
with codecs.open(path, 'r', 'utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_tab5 = False
skip_tab6 = False

tab5_replacement = """                                {% for i in product %}
                                <div class="col-lg-4">
                                    <div class="product-item rounded wow fadeInUp" data-wow-delay="0.1s">
                                        <div class="product-item-inner border rounded">
                                            <div class="product-item-inner-item">
                                                <a href="{% url 'b_single' pk=i.id %}"><img src="{{ i.pimage.url }}" class="img-fluid w-100 rounded-top" alt=""></a>
                                                <div class="product-new">New</div>
                                                <div class="product-details">
                                                    <a href="{% url 'b_single' pk=i.id %}"><i class="fa fa-eye fa-1x"></i></a>
                                                </div>
                                            </div>
                                            <div class="text-center rounded-bottom p-4">
                                                <a href="{% url 'b_single' pk=i.id %}" class="d-block mb-2">{{ i.pcategory }}</a>
                                                <a href="{% url 'b_single' pk=i.id %}" class="d-block h4">{{ i.pname }}</a>
                                                <del class="me-2 fs-5">₹{{ i.pprice }}</del>
                                                <span class="text-primary fs-5">₹{{ i.pprice }}</span>
                                            </div>
                                        </div>
                                        <div class="product-item-add border border-top-0 rounded-bottom text-center p-4 pt-0">
                                            <a href="{% url 'cart' %}" class="btn btn-primary border-secondary rounded-pill py-2 px-4 mb-4"><i class="fas fa-shopping-cart me-2"></i> Add To Cart</a>
                                            <div class="d-flex justify-content-between align-items-center">
                                                <div class="d-flex">
                                                    <i class="fas fa-star text-primary"></i><i class="fas fa-star text-primary"></i><i class="fas fa-star text-primary"></i><i class="fas fa-star text-primary"></i><i class="fas fa-star"></i>
                                                </div>
                                                <div class="d-flex">
                                                    <a href="#" class="text-primary d-flex align-items-center justify-content-center me-3"><span class="rounded-circle btn-sm-square border"><i class="fas fa-random"></i></span></a>
                                                    <a href="#" class="text-primary d-flex align-items-center justify-content-center me-0"><span class="rounded-circle btn-sm-square border"><i class="fas fa-heart"></i></span></a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                {% endfor %}
"""

tab6_replacement = """                                {% for i in product %}
                                <div class="col-lg-6">
                                    <div class="products-mini-item border">
                                        <div class="row g-0">
                                            <div class="col-5">
                                                <div class="products-mini-img border-end h-100">
                                                    <a href="{% url 'b_single' pk=i.id %}"><img src="{{ i.pimage.url }}" class="img-fluid w-100 h-100" alt="Image"></a>
                                                    <div class="products-mini-icon rounded-circle bg-primary">
                                                        <a href="{% url 'b_single' pk=i.id %}"><i class="fa fa-eye fa-1x text-white"></i></a>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="col-7">
                                                <div class="products-mini-content p-3">
                                                    <a href="{% url 'b_single' pk=i.id %}" class="d-block mb-2">{{ i.pcategory }}</a>
                                                    <a href="{% url 'b_single' pk=i.id %}" class="d-block h4">{{ i.pname }}</a>
                                                    <del class="me-2 fs-5">₹{{ i.pprice }}</del>
                                                    <span class="text-primary fs-5">₹{{ i.pprice }}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="products-mini-add border p-3">
                                            <a href="{% url 'cart' %}" class="btn btn-primary border-secondary rounded-pill py-2 px-4"><i class="fas fa-shopping-cart me-2"></i> Add To Cart</a>
                                            <div class="d-flex">
                                                <a href="#" class="text-primary d-flex align-items-center justify-content-center me-3"><span class="rounded-circle btn-sm-square border"><i class="fas fa-random"></i></span></a>
                                                <a href="#" class="text-primary d-flex align-items-center justify-content-center me-0"><span class="rounded-circle btn-sm-square border"><i class="fas fa-heart"></i></span></a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                {% endfor %}
"""

for i, line in enumerate(lines):
    if '<div class="row g-4 product">' in line and not skip_tab5 and not skip_tab6:
        new_lines.append(line)
        new_lines.append(tab5_replacement)
        skip_tab5 = True
        continue
        
    if skip_tab5 and '<div class="col-12 wow fadeInUp"' in line and i+1 < len(lines) and '"pagination' in lines[i+1]:
        skip_tab5 = False
        new_lines.append(line)
        continue
        
    if skip_tab5:
        continue

    if '<div class="row g-4 products-mini">' in line and not skip_tab5 and not skip_tab6:
        new_lines.append(line)
        new_lines.append(tab6_replacement)
        skip_tab6 = True
        continue
        
    if skip_tab6 and '<div class="col-12 wow fadeInUp"' in line and i+1 < len(lines) and '"pagination' in lines[i+1]:
        skip_tab6 = False
        new_lines.append(line)
        continue
        
    if skip_tab6:
        continue
        
    new_lines.append(line)

with codecs.open(path, 'w', 'utf-8') as f:
    f.writelines(new_lines)
print("Updated successfully")
