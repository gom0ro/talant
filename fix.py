import os

# 1. Update views.py safely
views_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\views.py"
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "Page.DoesNotExist" not in content:
    content = content.replace(
        "page = get_object_or_404(Page, slug=slug)",
        "try:\n        page = Page.objects.get(slug=slug)\n    except Page.DoesNotExist:\n        page = Page.objects.create(title=slug.replace('-', ' ').title(), slug=slug, content='Бұл бет әзірге бос. <br> Админкадан толтырыңыз.')"
    )
    content = content.replace(
        "return render(request, 'static_page.html', {'page': page})",
        "return render(request, [f'pages/{slug}.html', 'static_page.html'], {'page': page})"
    )
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("views.py updated successfully to handle 404s!")

# 2. Create HTML files
slugs = [
    "history", "administration", "kitapkhana", "askhana", "magistr", "sanat", 
    "zhetekshiler", "zhetistik", "parents-meeting", "school-rules", "med-kyzmet", 
    "psikholog", "kamqorshy", "logoped", "logoped-okushy", "defektolog", 
    "defektolog-okushy", "mad-a", "mad-ae", "mad-b", "mad-v", "mad-g", "mad-f", 
    "mad-d", "mad-e", "social-work", "ozin-ozi-bagalau"
]

template_dir = r"c:\Users\Asus Vivobook\Desktop\School\project\app\templates\pages"
os.makedirs(template_dir, exist_ok=True)

html_content = """{% extends 'base.html' %}

{% block title %}{{ page.title }} | Талант №1{% endblock %}

{% block content %}
<div class="page-header py-5 bg-light border-bottom text-center">
  <div class="container">
    <h1 class="page-header-title text-uppercase fw-bold m-0" style="color: #1e293b;">{{ page.title }}</h1>
  </div>
</div>

<div class="container py-5">
  <div class="row justify-content-center">
    <div class="col-lg-10">
      {% if page.image %}
      <div class="text-center mb-5">
        <img src="{{ page.image.url }}" alt="{{ page.title }}" class="img-fluid rounded shadow-sm w-100" style="max-height: 400px; object-fit: cover;">
      </div>
      {% endif %}
      
      <div class="card shadow-sm border-0">
        <div class="card-body p-4 p-md-5 fs-5 lh-lg text-secondary">
          {{ page.content|safe }}
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
"""

for slug in slugs:
    with open(os.path.join(template_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

print("All individual HTML files created in app/templates/pages/")
