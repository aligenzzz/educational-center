from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('teacher_info', views.TeacherInfoViewSet)
router.register('certificate', views.CertificateViewSet)
router.register('article', views.ArticleViewSet)
router.register('course_category', views.CourseCategoryViewSet)
router.register('course', views.CourseViewSet)
router.register('discount', views.DiscountViewSet)
router.register('review', views.ReviewViewSet)
router.register('faq_category', views.FaqCategoryViewSet)
router.register('faq', views.FaqViewSet)
router.register('application', views.ApplicationViewSet)

urlpatterns = router.urls
