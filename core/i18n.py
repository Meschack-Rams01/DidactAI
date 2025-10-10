"""
Internationalization (i18n) Configuration and Utilities for DidactAI

This module provides comprehensive internationalization support including
language detection, translation management, and localized content handling.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _, gettext_lazy as _lazy, ngettext
from django.core.management.base import BaseCommand
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LanguageManager:
    """Manage language preferences and translations"""
    
    # Supported languages with display names
    SUPPORTED_LANGUAGES = {
        'en': {'name': 'English', 'native_name': 'English', 'rtl': False},
        'fr': {'name': 'French', 'native_name': 'Français', 'rtl': False},
        'es': {'name': 'Spanish', 'native_name': 'Español', 'rtl': False},
        'de': {'name': 'German', 'native_name': 'Deutsch', 'rtl': False},
        'pt': {'name': 'Portuguese', 'native_name': 'PortuguÃªs', 'rtl': False},
        'it': {'name': 'Italian', 'native_name': 'Italiano', 'rtl': False},
        'ru': {'name': 'Russian', 'native_name': 'ƒ', 'rtl': False},
        'zh': {'name': 'Chinese', 'native_name': '–‡', 'rtl': False},
        'ja': {'name': 'Japanese', 'native_name': 'æ—¥æœž', 'rtl': False},
        'ar': {'name': 'Arabic', 'native_name': '„ŠØ©', 'rtl': True},
        'he': {'name': 'Hebrew', 'native_name': '‘™×ª', 'rtl': True},
    }
    
    def __init__(self):
        self.default_language = getattr(settings, 'LANGUAGE_CODE', 'en')
        self.fallback_language = 'en'
    
    def get_supported_languages(self) -> Dict[str, Dict[str, Any]]:
        """Get all supported languages"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def is_supported_language(self, lang_code: str) -> bool:
        """Check if a language code is supported"""
        return lang_code in self.SUPPORTED_LANGUAGES
    
    def get_language_info(self, lang_code: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific language"""
        return self.SUPPORTED_LANGUAGES.get(lang_code)
    
    def get_user_language(self, user) -> str:
        """Get user's preferred language"""
        if hasattr(user, 'profile') and user.profile.language:
            return user.profile.language
        return self.default_language
    
    def set_user_language(self, user, lang_code: str) -> bool:
        """Set user's preferred language"""
        if not self.is_supported_language(lang_code):
            return False
        
        # Update user profile language preference
        if hasattr(user, 'profile'):
            user.profile.language = lang_code
            user.profile.save()
            return True
        
        return False
    
    def detect_language_from_request(self, request) -> str:
        """Detect language from HTTP request"""
        # Check for explicit language parameter
        if 'lang' in request.GET:
            lang = request.GET['lang']
            if self.is_supported_language(lang):
                return lang
        
        # Check for user preference
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_lang = self.get_user_language(request.user)
            if user_lang:
                return user_lang
        
        # Check session
        if hasattr(request, 'session') and 'django_language' in request.session:
            session_lang = request.session['django_language']
            if self.is_supported_language(session_lang):
                return session_lang
        
        # Check Accept-Language header
        if hasattr(request, 'META') and 'HTTP_ACCEPT_LANGUAGE' in request.META:
            accept_lang = request.META['HTTP_ACCEPT_LANGUAGE']
            for lang in accept_lang.split(','):
                lang_code = lang.strip().split(';')[0].split('-')[0].lower()
                if self.is_supported_language(lang_code):
                    return lang_code
        
        return self.default_language


class TranslationManager:
    """Manage translations and localized content"""
    
    def __init__(self):
        self.language_manager = LanguageManager()
        self.translation_cache = {}
    
    def get_translated_content(self, content_object, field_name: str, language: str = None) -> str:
        """Get translated content for a specific field"""
        if not language:
            language = translation.get_language()
        
        # Check if object has translation support
        if hasattr(content_object, 'translations'):
            translation_obj = content_object.translations.filter(language=language).first()
            if translation_obj and hasattr(translation_obj, field_name):
                translated_content = getattr(translation_obj, field_name)
                if translated_content:
                    return translated_content
        
        # Fallback to original content
        if hasattr(content_object, field_name):
            return getattr(content_object, field_name)
        
        return ""
    
    def set_translated_content(self, content_object, field_name: str, content: str, language: str) -> bool:
        """Set translated content for a specific field"""
        try:
            from .models import ContentTranslation
            
            # Get or create translation object
            translation_obj, created = ContentTranslation.objects.get_or_create(
                content_type=content_object.__class__.__name__.lower(),
                object_id=content_object.id,
                language=language,
                defaults={'translations': {}}
            )
            
            # Update translation data
            translation_obj.translations[field_name] = content
            translation_obj.save()
            
            return True
            
        except Exception as e:
            print(f"Translation error: {e}")
            return False
    
    def get_available_translations(self, content_object) -> List[str]:
        """Get list of available languages for content object"""
        try:
            from .models import ContentTranslation
            
            translations = ContentTranslation.objects.filter(
                content_type=content_object.__class__.__name__.lower(),
                object_id=content_object.id
            )
            
            return [t.language for t in translations]
            
        except Exception:
            return []
    
    def translate_ai_content(self, content: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """Translate AI-generated content to target language"""
        # This would integrate with translation services like Google Translate
        # For now, we'll return a placeholder implementation
        
        translated_content = content.copy()
        
        # Add translation metadata
        translated_content['translation_info'] = {
            'target_language': target_language,
            'translated_at': datetime.now().isoformat(),
            'translation_method': 'ai_translation'
        }
        
        # In a real implementation, you would:
        # 1. Extract translatable text from content
        # 2. Call translation API (Google Translate, DeepL, etc.)
        # 3. Replace original text with translated text
        # 4. Preserve formatting and structure
        
        return translated_content
    
    def batch_translate_content(self, content_objects: List[Any], target_languages: List[str]) -> Dict[str, Any]:
        """Batch translate multiple content objects"""
        results = {
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        for content_obj in content_objects:
            for language in target_languages:
                try:
                    # Get translatable fields
                    translatable_fields = self._get_translatable_fields(content_obj)
                    
                    for field_name in translatable_fields:
                        original_text = getattr(content_obj, field_name, '')
                        if original_text:
                            # Translate text (placeholder implementation)
                            translated_text = f"[{language.upper()}] {original_text}"
                            
                            # Save translation
                            success = self.set_translated_content(
                                content_obj, 
                                field_name, 
                                translated_text, 
                                language
                            )
                            
                            if success:
                                results['successful'] += 1
                            else:
                                results['failed'] += 1
                                
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append(str(e))
        
        return results
    
    def _get_translatable_fields(self, content_object) -> List[str]:
        """Get list of translatable fields for a content object"""
        translatable_fields = []
        
        # Common translatable fields
        common_fields = ['title', 'description', 'content', 'name', 'summary']
        
        for field in common_fields:
            if hasattr(content_object, field):
                field_value = getattr(content_object, field)
                if isinstance(field_value, str) and field_value.strip():
                    translatable_fields.append(field)
        
        return translatable_fields


class LocalizationUtils:
    """Utilities for localization tasks"""
    
    @staticmethod
    def format_date(date_obj: datetime, language: str = None) -> str:
        """Format date according to locale"""
        if not language:
            language = translation.get_language()
        
        # Activate the target language temporarily
        with translation.override(language):
            # Use Django's date formatting
            from django.utils.formats import date_format
            return date_format(date_obj, 'DATE_FORMAT')
    
    @staticmethod
    def format_number(number: float, language: str = None) -> str:
        """Format number according to locale"""
        if not language:
            language = translation.get_language()
        
        # Basic number formatting based on language
        if language in ['en', 'zh', 'ja']:
            return f"{number:,.2f}"
        elif language in ['fr', 'de', 'it']:
            return f"{number:,.2f}".replace(',', ' ').replace('.', ',')
        elif language in ['es', 'pt']:
            return f"{number:,.2f}".replace(',', '.')
        else:
            return str(number)
    
    @staticmethod
    def format_currency(amount: float, currency: str = 'USD', language: str = None) -> str:
        """Format currency according to locale"""
        if not language:
            language = translation.get_language()
        
        formatted_amount = LocalizationUtils.format_number(amount, language)
        
        # Currency symbols and positioning
        currency_formats = {
            'USD': {'en': f'${formatted_amount}', 'default': f'{formatted_amount} USD'},
            'EUR': {'fr': f'{formatted_amount} â‚¬', 'de': f'{formatted_amount} â‚¬', 'default': f'â‚¬{formatted_amount}'},
            'GBP': {'en': f'£{formatted_amount}', 'default': f'{formatted_amount} GBP'},
        }
        
        if currency in currency_formats:
            if language in currency_formats[currency]:
                return currency_formats[currency][language]
            else:
                return currency_formats[currency]['default']
        
        return f'{formatted_amount} {currency}'
    
    @staticmethod
    def get_plural_form(count: int, singular: str, plural: str = None, language: str = None) -> str:
        """Get correct plural form based on language rules"""
        if not language:
            language = translation.get_language()
        
        if not plural:
            plural = f"{singular}s"  # Simple English pluralization
        
        # Language-specific plural rules (simplified)
        if language == 'en':
            return singular if count == 1 else plural
        elif language in ['fr', 'es', 'pt', 'it']:
            return singular if count <= 1 else plural
        elif language == 'ru':
            # Russian has complex plural rules
            if count % 10 == 1 and count % 100 != 11:
                return singular
            elif 2 <= count % 10 <= 4 and not (12 <= count % 100 <= 14):
                return plural  # Would need special form in real implementation
            else:
                return plural
        else:
            return singular if count == 1 else plural
    
    @staticmethod
    def get_rtl_languages() -> List[str]:
        """Get list of right-to-left languages"""
        return [lang for lang, info in LanguageManager.SUPPORTED_LANGUAGES.items() if info.get('rtl', False)]
    
    @staticmethod
    def is_rtl_language(language: str) -> bool:
        """Check if language is right-to-left"""
        return language in LocalizationUtils.get_rtl_languages()


# Translation strings for common UI elements
UI_TRANSLATIONS = {
    'navigation': {
        'dashboard': _lazy('Dashboard'),
        'courses': _lazy('Courses'),
        'files': _lazy('Files'),
        'ai_generator': _lazy('AI Generator'),
        'exports': _lazy('Exports'),
        'analytics': _lazy('Analytics'),
        'settings': _lazy('Settings'),
        'help': _lazy('Help'),
        'logout': _lazy('Logout'),
    },
    'actions': {
        'create': _lazy('Create'),
        'edit': _lazy('Edit'),
        'delete': _lazy('Delete'),
        'save': _lazy('Save'),
        'cancel': _lazy('Cancel'),
        'upload': _lazy('Upload'),
        'download': _lazy('Download'),
        'share': _lazy('Share'),
        'export': _lazy('Export'),
        'import': _lazy('Import'),
    },
    'forms': {
        'title': _lazy('Title'),
        'description': _lazy('Description'),
        'name': _lazy('Name'),
        'email': _lazy('Email'),
        'password': _lazy('Password'),
        'confirm_password': _lazy('Confirm Password'),
        'file': _lazy('File'),
        'category': _lazy('Category'),
        'language': _lazy('Language'),
    },
    'messages': {
        'success': _lazy('Operation completed successfully'),
        'error': _lazy('An error occurred'),
        'warning': _lazy('Please check your input'),
        'info': _lazy('Information'),
        'loading': _lazy('Loading...'),
        'no_data': _lazy('No data available'),
        'confirm_delete': _lazy('Are you sure you want to delete this item?'),
    },
    'time': {
        'today': _lazy('Today'),
        'yesterday': _lazy('Yesterday'),
        'last_week': _lazy('Last week'),
        'last_month': _lazy('Last month'),
        'never': _lazy('Never'),
    }
}


class ContentTranslationMixin(models.Model):
    """Mixin to add translation capabilities to models"""
    
    class Meta:
        abstract = True
    
    def get_translated_field(self, field_name: str, language: str = None) -> str:
        """Get translated version of a field"""
        translation_manager = TranslationManager()
        return translation_manager.get_translated_content(self, field_name, language)
    
    def set_translated_field(self, field_name: str, content: str, language: str) -> bool:
        """Set translated version of a field"""
        translation_manager = TranslationManager()
        return translation_manager.set_translated_content(self, field_name, content, language)
    
    def get_available_translations(self) -> List[str]:
        """Get available translations for this object"""
        translation_manager = TranslationManager()
        return translation_manager.get_available_translations(self)


# Django management command for translation management
class TranslationCommand:
    """Management command utilities for translations"""
    
    @staticmethod
    def extract_translatable_strings(app_name: str = None) -> Dict[str, List[str]]:
        """Extract translatable strings from code"""
        # This would scan Python and template files for translatable strings
        # For now, return a placeholder
        return {
            'python_strings': [],
            'template_strings': [],
            'javascript_strings': []
        }
    
    @staticmethod
    def generate_po_files(languages: List[str] = None) -> bool:
        """Generate .po files for specified languages"""
        if not languages:
            languages = list(LanguageManager.SUPPORTED_LANGUAGES.keys())
        
        # This would use Django's makemessages command
        # For now, return success placeholder
        return True
    
    @staticmethod
    def compile_translations() -> bool:
        """Compile translation files"""
        # This would use Django's compilemessages command
        return True


# Context processor for template translations
def translation_context(request):
    """Add translation context to templates"""
    language_manager = LanguageManager()
    current_language = translation.get_language()
    
    return {
        'current_language': current_language,
        'supported_languages': language_manager.get_supported_languages(),
        'is_rtl': LocalizationUtils.is_rtl_language(current_language),
        'ui_translations': UI_TRANSLATIONS,
    }


# Middleware for language detection and setting
class LanguageMiddleware:
    """Middleware to detect and set user language preferences"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.language_manager = LanguageManager()
    
    def __call__(self, request):
        # Detect language preference
        detected_language = self.language_manager.detect_language_from_request(request)
        
        # Set language for this request
        if detected_language:
            translation.activate(detected_language)
            request.LANGUAGE_CODE = detected_language
            
            # Update session if needed
            if hasattr(request, 'session') and request.session.get('django_language') != detected_language:
                request.session['django_language'] = detected_language
        
        response = self.get_response(request)
        
        # Add language information to response headers
        response['Content-Language'] = translation.get_language()
        
        # Deactivate language
        translation.deactivate()
        
        return response


# Template tags for translations
def register_translation_tags():
    """Register custom template tags for translations"""
    from django import template
    
    register = template.Library()
    
    @register.simple_tag
    def translate_field(obj, field_name, language=None):
        """Translate a specific field of an object"""
        if hasattr(obj, 'get_translated_field'):
            return obj.get_translated_field(field_name, language)
        return getattr(obj, field_name, '')
    
    @register.filter
    def format_localized_date(date_obj, language=None):
        """Format date according to locale"""
        return LocalizationUtils.format_date(date_obj, language)
    
    @register.filter
    def format_localized_number(number, language=None):
        """Format number according to locale"""
        return LocalizationUtils.format_number(number, language)
    
    @register.simple_tag
    def language_flag(language_code):
        """Get flag emoji or icon for language"""
        flags = {
            'en': 'ðŸ‡ºðŸ‡¸', 'fr': 'ðŸ‡«ðŸ‡·', 'es': 'ðŸ‡ªðŸ‡¸', 'de': 'ðŸ‡©ðŸ‡ª',
            'pt': 'ðŸ‡µðŸ‡¹', 'it': 'ðŸ‡®ðŸ‡¹', 'ru': 'ðŸ‡·ðŸ‡º', 'zh': 'ðŸ‡¨ðŸ‡³',
            'ja': 'ðŸ‡¯ðŸ‡µ', 'ar': 'ðŸ‡¸ðŸ‡¦', 'he': 'ðŸ‡®ðŸ‡±'
        }
        return flags.get(language_code, 'ðŸŒ')
    
    return register


# AI Translation Integration
class AITranslationService:
    """Service for AI-powered translation of educational content"""
    
    def __init__(self):
        self.supported_services = ['google_translate', 'deepl', 'azure_translator']
    
    def translate_content(self, content: str, source_lang: str, target_lang: str, service: str = 'google_translate') -> Dict[str, Any]:
        """Translate content using AI service"""
        # This would integrate with actual translation APIs
        result = {
            'translated_text': f"[{target_lang.upper()}] {content}",
            'source_language': source_lang,
            'target_language': target_lang,
            'confidence_score': 0.95,
            'service_used': service,
            'translation_time': datetime.now().isoformat()
        }
        
        return result
    
    def translate_quiz_questions(self, questions: List[Dict], target_language: str) -> List[Dict]:
        """Translate quiz questions while preserving structure"""
        translated_questions = []
        
        for question in questions:
            translated_question = question.copy()
            
            # Translate question text
            if 'question' in question:
                translation_result = self.translate_content(
                    question['question'], 
                    'en',  # Assume source is English
                    target_language
                )
                translated_question['question'] = translation_result['translated_text']
            
            # Translate options if present
            if 'options' in question and isinstance(question['options'], list):
                translated_options = []
                for option in question['options']:
                    if isinstance(option, str):
                        translation_result = self.translate_content(option, 'en', target_language)
                        translated_options.append(translation_result['translated_text'])
                    else:
                        translated_options.append(option)
                translated_question['options'] = translated_options
            
            # Translate explanation if present
            if 'explanation' in question:
                translation_result = self.translate_content(
                    question['explanation'], 
                    'en', 
                    target_language
                )
                translated_question['explanation'] = translation_result['translated_text']
            
            translated_questions.append(translated_question)
        
        return translated_questions
