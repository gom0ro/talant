import os
import re

slugs = [
    "history", "administration", "kitapkhana", "askhana", "magistr", "sanat", 
    "zhetekshiler", "zhetistik", "parents-meeting", "school-rules", "med-kyzmet", 
    "psikholog", "kamqorshy", "logoped", "logoped-okushy", "defektolog", 
    "defektolog-okushy", "mad-a", "mad-ae", "mad-b", "mad-v", "mad-g", "mad-f", 
    "mad-d", "mad-e", "social-work", "ozin-ozi-bagalau"
]

# 1. Update base.html
# Replace {% url 'app:static_page' 'slug-name' %} with {% url 'app:slug_name' %}
base_html_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\templates\base.html"
with open(base_html_path, "r", encoding="utf-8") as f:
    base_html = f.read()

for s in slugs:
    view_name = s.replace("-", "_")
    old_code = f"{{% url 'app:static_page' '{s}' %}}"
    new_code = f"{{% url 'app:{view_name}' %}}"
    base_html = base_html.replace(old_code, new_code)

with open(base_html_path, "w", encoding="utf-8") as f:
    f.write(base_html)

# 2. Update views.py
views_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\views.py"
with open(views_path, "r", encoding="utf-8") as f:
    views_content = f.read()

# Remove the old static_page view completely
old_static_page_regex = r"def static_page.*?return render\(request, \[f'pages/.*?\]\)"
views_content = re.sub(old_static_page_regex, "", views_content, flags=re.DOTALL)

# Let's generate all 27 views
views_addition = "\n# ── СТАТИКАЛЫҚ БЕТТЕР (ХАРДКОД) ──\n\n"
for s in slugs:
    view_name = s.replace("-", "_")
    views_addition += f"def {view_name}(request):\n    return render(request, 'pages/{s}.html')\n\n"

views_content += views_addition

with open(views_path, "w", encoding="utf-8") as f:
    f.write(views_content)

# 3. Update urls.py
urls_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\urls.py"
with open(urls_path, "r", encoding="utf-8") as f:
    urls_content = f.read()

# Remove old static path
urls_content = re.sub(r"path\('page/<slug:slug>/', views\.static_page, name='static_page'\),", "", urls_content)

# Add new paths
urls_addition = ""
for s in slugs:
    view_name = s.replace("-", "_")
    urls_addition += f"    path('page/{s}/', views.{view_name}, name='{view_name}'),\n"

# Insert them before the closing bracket of urlpatterns
urls_content = re.sub(r"\]\s*$", urls_addition + "\n]", urls_content, flags=re.MULTILINE)

with open(urls_path, "w", encoding="utf-8") as f:
    f.write(urls_content)

# 4. Modify all the pages templates to be standard hardcoded templates
template_dir = r"c:\Users\Asus Vivobook\Desktop\School\project\app\templates\pages"
os.makedirs(template_dir, exist_ok=True)

for s in slugs:
    title = s.replace("-", " ").title()
    if s == "med-kyzmet": title = "Медициналық қызмет"
    if s == "askhana": title = "Мектеп асханасы"
    if s == "psikholog": title = "Психолог қызметі"
    
    html = f"""{{% extends 'base.html' %}}

{{% block title %}}{title} | Талант №1{{% endblock %}}

{{% block content %}}
<div class="page-header py-5 bg-light border-bottom text-center">
  <div class="container">
    <h1 class="page-header-title text-uppercase fw-bold m-0" style="color: #1e293b;">{title}</h1>
  </div>
</div>

<div class="container py-5">
  <div class="row justify-content-center">
    <div class="col-lg-10">
      <div class="card shadow-sm border-0">
        <div class="card-body p-4 p-md-5 fs-5 lh-lg text-secondary">
          <p>Бұл бет уақытша бос. Мәтінді <code>app/templates/pages/{s}.html</code> файлына жазыңыз.</p>
        </div>
      </div>
    </div>
  </div>
</div>
{{% endblock %}}
"""
    with open(os.path.join(template_dir, f"{s}.html"), "w", encoding="utf-8") as f:
        f.write(html)

print("Migration completed: All pages are now explicitly hardcoded in views.py, urls.py, base.html, and pages/*.html")
