from django.contrib import admin
from .models import (
    NewsCategory, News, Teacher, GalleryAlbum, GalleryImage,
    DocumentCategory, Document, Page, Slider, ContactMessage, Club
)


# ── Жаңалықтар ──────────────────────────────────────────────

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'


# ── Мұғалімдер ──────────────────────────────────────────────

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'experience', 'order')
    list_filter = ('subject',)
    search_fields = ('name', 'subject')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)


# ── Галерея ─────────────────────────────────────────────────

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3
    fields = ('image', 'caption')


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_count', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryImageInline]

    @admin.display(description='Суреттер саны')
    def image_count(self, obj):
        return obj.images.count()


# ── Құжаттар ────────────────────────────────────────────────

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title',)


# ── Беттер ──────────────────────────────────────────────────

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')


# ── Слайдер ─────────────────────────────────────────────────

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)


# ── Хабарламалар ────────────────────────────────────────────

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')

    def has_add_permission(self, request):
        return False


# ── Үйірмелер ───────────────────────────────────────────────

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)
    search_fields = ('name', 'content')


# ── Админ-сайт баптаулары ───────────────────────────────────
admin.site.site_header = 'Talant №1 — Әкімшілік'
admin.site.site_title = 'Talant №1 Админ (Школа №1)'
admin.site.index_title = 'Басқару панелі'
