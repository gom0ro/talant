import os
import re

slugs = [
    "history", "administration", "kitapkhana", "askhana", "magistr", "sanat", 
    "zhetekshiler", "zhetistik", "parents-meeting", "school-rules", "med-kyzmet", 
    "psikholog", "kamqorshy", "logoped", "logoped-okushy", "defektolog", 
    "defektolog-okushy", "mad-a", "mad-ae", "mad-b", "mad-v", "mad-g", "mad-f", 
    "mad-d", "mad-e", "social-work", "ozin-ozi-bagalau",
    "timetable", "rules", "achievements", "career", "zhaz-2024", "self-assessment"
]

# 1. Revert base.html back to using app:static_page
base_html_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\templates\base.html"
with open(base_html_path, "r", encoding="utf-8") as f:
    base_html = f.read()

for s in slugs:
    view_name = s.replace("-", "_")
    base_html = base_html.replace(f"{{% url 'app:{view_name}' %}}", f"{{% url 'app:static_page' '{s}' %}}")

with open(base_html_path, "w", encoding="utf-8") as f:
    f.write(base_html)

# 2. Revert urls.py back to static_page and remove hardcoded ones
urls_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\urls.py"
with open(urls_path, "r", encoding="utf-8") as f:
    urls_content = f.read()

for s in slugs:
    view_name = s.replace("-", "_")
    urls_content = re.sub(rf"\s*path\('page/{s}/', views\.{view_name}, name='{view_name}'\),", "", urls_content)

# Add static_page back to urls.py
if "views.static_page" not in urls_content:
    urls_content = re.sub(r"\]\s*$", "    path('page/<slug:slug>/', views.static_page, name='static_page'),\n]", urls_content, flags=re.MULTILINE)

with open(urls_path, "w", encoding="utf-8") as f:
    f.write(urls_content)

# 3. Clean views.py
views_path = r"c:\Users\Asus Vivobook\Desktop\School\project\app\views.py"
with open(views_path, "r", encoding="utf-8") as f:
    views_content = f.read()

# Remove all hardcoded views
hardcoded_block_regex = r"# ── СТАТИКАЛЫҚ БЕТТЕР \(ХАРДКОД\) ──.*"
views_content = re.sub(hardcoded_block_regex, "", views_content, flags=re.DOTALL)

# Re-inject the static_page view safely
if "def static_page(" not in views_content:
    static_page_func = """
# ── Статикалық беттер ──
def static_page(request, slug):
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = Page.objects.create(title=slug.replace('-', ' ').title(), slug=slug, content='Бұл бет уақытша бос. Ақпаратты Админ-панельден қосыңыз.')
        
    templates = [f'pages/{slug}.html', 'static_page.html']
    return render(request, templates, {'page': page})
"""
    views_content += static_page_func

with open(views_path, "w", encoding="utf-8") as f:
    f.write(views_content)

# 4. Update HTML pages
template_dir = r"c:\Users\Asus Vivobook\Desktop\School\project\app\templates\pages"
for s in slugs:
    title = s.replace("-", " ").title()
    filepath = os.path.join(template_dir, f"{s}.html")
    
    html = "{% extends 'base.html' %}\n{% load static %}\n\n"
    html += "{% block title %}{{ page.title }} | Талант №1{% endblock %}\n\n"
    html += "{% block content %}\n"
    html += '<div class="page-header py-5 bg-light border-bottom text-center">\n'
    html += '  <div class="container">\n'
    html += '    <h1 class="page-header-title text-uppercase fw-bold m-0" style="color: #1e293b;">{{ page.title }}</h1>\n'
    html += '  </div>\n</div>\n\n'
    html += '<div class="container py-5">\n'
    html += '  <div class="row justify-content-center">\n'
    html += '    <div class="col-lg-10">\n'
    html += '      {% if page.image %}\n'
    html += '      <div class="text-center mb-5">\n'
    html += '        <img src="{{ page.image.url }}" alt="{{ page.title }}" class="img-fluid rounded shadow w-100" style="max-height: 400px; object-fit: cover;">\n'
    html += '      </div>\n'
    html += '      {% endif %}\n'
    html += '      <div class="card shadow-sm border-0">\n'
    html += '        <div class="card-body p-4 p-md-5 fs-5 lh-lg text-secondary" style="text-align: justify;">\n'
    html += '          {{ page.content|safe }}\n'
    html += '        </div>\n'
    html += '      </div>\n'
    html += '    </div>\n'
    html += '  </div>\n</div>\n'
    html += '{% endblock %}\n'

    if os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

print("SUCCESS: System reverted to pure dynamic Pages with Admin DB connectivity, and Reverse URLs restored!")
