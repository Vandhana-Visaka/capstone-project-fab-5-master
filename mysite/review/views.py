from django.shortcuts import render, redirect
from account.models import Account
from books.models import Books
from review.models import Review
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger("django")
logger.info("Whatever to log")

@csrf_exempt
def add_review(request):
    '''
    allows users to add review and provide rating
    date created is recorded
    Displayed on book page
    '''
    logger.info("print add_review")
    context = {}
    user = request.user
    if user.is_authenticated:
        rating = int(request.POST.get("rating"))
        review_text = request.POST.get("review")
        isbn = request.POST.get("isbn")
        account = Account.objects.get(username=user.username)
        book = Books.objects.get(ISBN=isbn)
        try:
            findreview = Review.objects.filter(UID=account, BID=book)
            if findreview.exists():
                findreview.all().delete()

            review = Review(UID=account, BID=book, rating=rating, review=review_text)
            review.save()
            review_data = {
                "id": review.id,
                "created_at": review.createdDate,
                "error": False,
                "errorMessage": "Add a review successfully!"
            }
            return JsonResponse(review_data, safe=False)
        except Exception as e:
            logger.info(e)
            print("cannot save review")
            review_data = {
                "error": True,
                "errorMessage": "Cannot add a review"
            }
            return JsonResponse(review_data, safe=False)
