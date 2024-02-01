from modeltranslation.translator import translator, TranslationOptions

from .models import Promotion


class PromotionTranslationOptions(TranslationOptions):
    fields = ['name', 'description']


translator.register(Promotion, PromotionTranslationOptions)
