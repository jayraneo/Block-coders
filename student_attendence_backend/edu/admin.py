from django.contrib import admin
from django.apps import apps

# Get all models from the 'edu' app
models = apps.get_app_config('edu').get_models()

# Register each model
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass  # Skip already registered models
