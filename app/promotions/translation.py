from modeltranslation.translator import translator, TranslationOptions

from .models import Promotion


class PromotionTranslationOptions(TranslationOptions):
    fields = ['description']


translator.register(Promotion, PromotionTranslationOptions)
