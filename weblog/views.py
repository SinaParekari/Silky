from django.shortcuts import render, get_object_or_404
from .models import Weblog,WeblogCategory,WeblogLike,WeblogReview,WeblogText
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import Http404
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.utils.text import slugify
from .forms import WeblogReviewForm
# Create your views here.

def weblog(request):

    weblogs = (Weblog.objects.get_active_weblogs().annotate(likes_count=Count("likes", distinct=True),reviews_count=Count("reviews", distinct=True),).order_by("-created_at"))

    categories = (WeblogCategory.objects.annotate(weblogs_count=Count("weblogs",filter=Q(weblogs__is_active=True))))

    category = request.GET.get("category")

    sort = request.GET.get("sort", "newest")

    if sort == "newest":
        weblogs = weblogs.order_by("-created_at")

    elif sort == "oldest":
        weblogs = weblogs.order_by("created_at")

    elif sort == "views":
        weblogs = weblogs.order_by("-views")

    elif sort == "likes":
        weblogs = weblogs.order_by("-likes_count")

    if category:
        weblogs = weblogs.filter(category_id=category)

    paginator = Paginator(weblogs, 9)  # 9 weblogs per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj" : page_obj,
        "categories": categories,
    }

    return render(request,'weblog.html', context)

def single_post(request, slug):
    weblog = get_object_or_404(
        Weblog.objects.select_related("user").prefetch_related(
            "category",
            "tags",
            "texts",
            "likes",
        ),
        slug=slug,
    )

    liked = False

    if request.user.is_authenticated:
        liked = weblog.likes.filter(user=request.user).exists()

    previous_weblog = (
        Weblog.objects.filter(
            is_active=True,
            created_at__lt=weblog.created_at
        )
        .order_by("-created_at")
        .first()
    )

    next_weblog = (
        Weblog.objects.filter(
            is_active=True,
            created_at__gt=weblog.created_at
        )
        .order_by("created_at")
        .first()
    )

    weblog.views += 1

    post = {
        "title": weblog.title,
        "slug":weblog.slug,
        "excerpt": weblog.excerpt,
        "category": weblog.category.title,
        "date": weblog.created_at.strftime("%Y-%m-%d"),
        "updated": weblog.updated_at.strftime("%Y-%m-%d"),
        "readTime": weblog.readTime,
        "views": weblog.views,
        "likes": weblog.likes.count(),
        "image": weblog.image.url if weblog.image else "",
        "imageCredit": "تصویر از Unsplash",
        "summary": weblog.summary,
        "tags": [tag.title for tag in weblog.tags.all()],
        "author": {
            "name": f"{weblog.user.first_name} {weblog.user.last_name}",
            "role": "نویسنده ارشد",
            "avatar": weblog.user.avatar.url if weblog.user.avatar else "",
            "bio": "علی با بیش از ۱۰ سال تجربه در حوزه بررسی و تحلیل تجهیزات دیجیتال، تلاش می‌کند بهترین انتخاب‌ها را به کاربران معرفی کند.",
            "socials": [],
        },
    }

    toc = [
        {
            "id": slugify(text.header),
            "title": text.header,
            "level": 2,
        }
        for text in weblog.texts.all()
        if text.header and text.template in ["simple", "simple_ul"]
    ]

    related_posts = []

    for item in Weblog.objects.get_weblog_by_category(weblog.category).exclude(id=weblog.id):
        related_posts.append(
            {
                "id": item.id,
                "slug" : item.slug,
                "title": item.title,
                "category": item.category.title,
                "image": item.image.url if item.image else "",
                "date": item.created_at.strftime("%Y-%m-%d"),
                "readTime": item.readTime,
            }
        )


    comments = [
        {
            "id": review.id,
            "name": f"{review.user.first_name} {review.user.last_name}".strip(),
            "avatar": review.user.avatar.url if hasattr(review.user, "avatar") and review.user.avatar else None,
            "text": review.comment,
            "rating": review.rating,
            "date": review.created_at,
            "likes": 0,      # اگر مدل لایک برای کامنت نداری
            "liked": False,  # اگر سیستم لایک کامنت نداری
        }
        for review in weblog.reviews.filter(is_approved=True).select_related("user")
    ]

    inline_products = [
        {
            "id": item.product.id,
            "name": item.product.name,
            "slug": item.product.slug,
            "price": item.product.default_variant.price if item.product.default_variant else None,
            "image": (
                item.product.main_image.image.url
                if item.product.main_image
                else ""
            ),
            "rating": 0,
            "reviews": 0,
        }
        for item in weblog.related_products.select_related("product").prefetch_related(
            "product__images",
            "product__variants",
        )[:2]
    ]

    texts = weblog.texts.all()

    for text in texts:
        if text.template == WeblogText.Choices.simple_ul:
            text.lines = text.text.splitlines() if text.text else []

    context = {
        "post": post,
        "toc": toc,
        "texts": texts,
        "relatedPosts": related_posts,
        "comments" : comments ,
        "next_weblog" : next_weblog,
        "previos_weblog" : previous_weblog,
        "inlineProducts" : inline_products,
        "liked" : liked
    }

    return render(request, "post.html", context)

@login_required
def toggle_weblog_like(request, slug):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    weblog = Weblog.objects.get(slug=slug, is_active=True)

    like = WeblogLike.objects.filter(
        weblog=weblog,
        user=request.user,
    )

    if like.exists():
        like.delete()
        liked = False
    else:
        WeblogLike.objects.create(
            weblog=weblog,
            user=request.user,
        )
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": weblog.likes.count(),
    })

@login_required
def submit_review(request, slug):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Method not allowed."},
            status=405,
        )

    weblog = get_object_or_404(
        Weblog,
        slug=slug,
        is_active=True,
    )

    if WeblogReview.objects.filter(
        weblog=weblog,
        user=request.user,
    ).exists():
        return JsonResponse(
            {
                "success": False,
                "message": "You have already submitted a review.",
            },
            status=400,
        )

    form = WeblogReviewForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors,
            },
            status=400,
        )

    review = form.save(commit=False)
    review.weblog = weblog
    review.user = request.user
    review.is_approved = False
    review.save()

    return JsonResponse(
        {
            "success": True,
            "message": "Your review has been submitted and is awaiting approval.",
        }
    )