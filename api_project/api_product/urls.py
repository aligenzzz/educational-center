from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('teacher-info', views.TeacherInfoViewSet, basename='teacher-info')
router.register('certificates', views.CertificateViewSet, basename='certificates')
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('course-categories', views.CourseCategoryViewSet, basename='course-categories')
router.register('courses', views.CourseViewSet, basename='courses')
router.register('discounts', views.DiscountViewSet, basename='discounts')
router.register('reviews', views.ReviewViewSet, basename='reviews')
router.register('faq-categories', views.FaqCategoryViewSet, basename='faq-categories')
router.register('faqs', views.FaqViewSet, basename='faqs')
router.register('applications', views.ApplicationViewSet, basename='applications')

urlpatterns = router.urls
