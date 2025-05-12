from django.apps import apps

def get_model_by_name(app_label, model_name):
    return apps.get_model(app_label, model_name)
