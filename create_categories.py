from tracker.models import Category
categories = ['Food', 'Travel', 'Rent', 'Utilities', 'Entertainment', 'Shopping', 'Health', 'Education']
for cat in categories:
    Category.objects.get_or_create(name=cat, is_predefined=True)
print("Categories created successfully!")
