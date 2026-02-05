from celery import shared_task
import time
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_book_created_mail(book_id,book_title,author_name):
    print(f"task stated for the book{book_title}")
    
     # Simulate slow email sending (3 seconds)
    time.sleep(3)
    
    # In real world, you'd actually send email here:
    # send_mail(
    #     subject=f'New Book Added: {book_title}',
    #     message=f'Book "{book_title}" by {author_name} has been added.',
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=['admin@library.com'],
    # )
    
    print(f"Task completed: Email sent for book {book_title}")
    return f"Email sent for {book_title}"