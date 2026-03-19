import os
import re

# 1. Update views.py
views_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\views.py"
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = r"def static_page(request, slug):\s+.*?\s+page = get_object_or_404\(Page, slug=slug\)\s+return render\(request, 'static_page\.html', \{'page': page\}\)"
replacement = """def static_page(request, slug):
    \"\"\"Кез-келген статикалық бет\"\"\"
    page = get_object_or_404(Page, slug=slug)
    # Жүйе алдымен 'pages/<slug>.html' іздейді. Егер таба алмаса 'static_page.html' ашады
    return render(request, [f'pages/{slug}.html', 'static_page.html'], {'page': page})"""

new_content = re.sub(target, replacement, content, count=1, flags=re.DOTALL)
if new_content != content:
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("views.py updated successfully.")
else:
    print("Failed to replace text in views.py. Maybe already updated?")

# 2. Generate HTML templates
slugs = [
    "history", "administration", "kitapkhana", "askhana", 
    "magistr", "sanat", "zhetekshiler", "zhetistik",
    "parents-meeting", "school-rules", "med-kyzmet", "psikholog", 
    "kamqorshy", "logoped", "logoped-okushy", "defektolog", 
    "defektolog-okushy", "mad-a", "mad-ae", "mad-b", "mad-v", 
    "mad-g", "mad-f", "mad-d", "mad-e", "social-work", "ozin-ozi-bagalau"
]

template_dir = r"c:\Users\Asus Vivobook\Desktop\School\project\app\templates\pages"
os.makedirs(template_dir, exist_ok=True)

html_content = """{% extends 'base.html' %}
{% load static %}

{% block title %}{{ page.title }} | Талант №1{% endblock %}

{% block content %}
<!-- Басты тақырып бөлігі (Header) -->
<div class="page-header py-5 bg-light text-center border-bottom">
  <div class="container">
    <h1 class="page-header-title text-uppercase fw-bold text-dark mb-0">{{ page.title }}</h1>
  </div>
</div>

<!-- Негізгі контент -->
<div class="container py-5">
  <div class="row justify-content-center">
    <div class="col-lg-10">
      
      <!-- Егер админкадан сурет қосылған болса -->
      {% if page.image %}
      <div class="text-center mb-5">
        <img src="{{ page.image.url }}" alt="{{ page.title }}" class="img-fluid rounded shadow w-100" style="max-height: 500px; object-fit: cover;">
      </div>
      {% endif %}
      
      <!-- Админкадан толтырылған мәтін -->
      <div class="card shadow-sm border-0">
        <div class="card-body p-4 p-md-5 fs-5 text-secondary lh-lg" style="text-align: justify;">
          {{ page.content|safe }}
        </div>
      </div>
      
    </div>
  </div>
</div>
{% endblock %}
"""

for slug in slugs:
    file_path = os.path.join(template_dir, f"{slug}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

print(f"Created/Verified {len(slugs)} template files in {template_dir}")
