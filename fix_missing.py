import os
import re

slugs = [
    "timetable", "rules", "achievements", "career", "zhaz-2024", "self-assessment"
]

# 1. Update base.html
base_html_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\templates\base.html"
with open(base_html_path, "r", encoding="utf-8") as f:
    base_html = f.read()

for s in slugs:
    view_name = s.replace("-", "_")
    base_html = base_html.replace(f"{{% url 'app:static_page' '{s}' %}}", f"{{% url 'app:{view_name}' %}}")

with open(base_html_path, "w", encoding="utf-8") as f:
    f.write(base_html)

# 2. Update views.py
views_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\views.py"
with open(views_path, "r", encoding="utf-8") as f:
    views_content = f.read()

# Add the 6 missing views
views_addition = ""
for s in slugs:
    view_name = s.replace("-", "_")
    if f"def {view_name}(" not in views_content:
        views_addition += f"def {view_name}(request):\n    return render(request, 'pages/{s}.html')\n\n"
views_content += views_addition

# Also remove Page search logic
views_content = re.sub(r"page_results\s*=\s*\[\]", "", views_content)
views_content = re.sub(r"# Статикалық беттерден іздеу \(Page\).*?page_results.*?distinct\(\)", "", views_content, flags=re.DOTALL)
views_content = re.sub(r"'page_results': page_results,", "", views_content)
views_content = re.sub(r"\s+\+\s+len\(page_results\)", "", views_content)

with open(views_path, "w", encoding="utf-8") as f:
    f.write(views_content)

# 3. Update urls.py
urls_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\urls.py"
with open(urls_path, "r", encoding="utf-8") as f:
    urls_content = f.read()

urls_addition = ""
for s in slugs:
    view_name = s.replace("-", "_")
    if f"path('page/{s}/'" not in urls_content:
        urls_addition += f"    path('page/{s}/', views.{view_name}, name='{view_name}'),\n"

urls_content = re.sub(r"\]\s*$", urls_addition + "\n]", urls_content, flags=re.MULTILINE)

with open(urls_path, "w", encoding="utf-8") as f:
    f.write(urls_content)

# 4. Generate the 6 HTML files
template_dir = r"c:\Users\Asus Vivobook\Desktop\School\project\app\templates\pages"
for s in slugs:
    title = s.replace("-", " ").title()
    if "2024" in s: title = "Жаз - 2024"
    if s == "timetable": title = "Сабақ кестесі"
    if s == "rules": title = "Тәртіп ережесі"
    
    html = f"""{{% extends 'base.html' %}}

{{% block title %}}{title} | Талант №1{{% endblock %}}

{{% block content %}}
<div class="page-header py-5 bg-light border-bottom text-center">
  <div class="container">
    <h1 class="page-header-title text-uppercase fw-bold m-0" style="color: #1e293b;">{title}</h1>
  </div>
</div>
<div class="container py-5"><p>Бұл бет уақытша бос. Мәтінді <code>app/templates/pages/{s}.html</code> файлына жазыңыз.</p></div>
{{% endblock %}}
"""
    with open(os.path.join(template_dir, f"{s}.html"), "w", encoding="utf-8") as f:
        f.write(html)

# 5. Fix search_results.html
search_html_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\templates\search_results.html"
with open(search_html_path, "r", encoding="utf-8") as f:
    search_html = f.read()

# Remove the block that renders page_results
search_html = re.sub(r"{% if page_results %}.*?{% endif %}", "", search_html, flags=re.DOTALL)

with open(search_html_path, "w", encoding="utf-8") as f:
    f.write(search_html)

print("Fixed!")
