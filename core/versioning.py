"""
Versioning Service for DidactAI

This module provides comprehensive versioning capabilities for files and AI-generated content,
enabling users to track changes, rollback to previous versions, and maintain content history.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models, transaction
from django.utils import timezone


class VersionManager:
    """Manager for handling version operations"""
    
    def __init__(self):
        self.version_model = None
    
    def create_version(self, content_object, user, change_notes: str = None, **kwargs) -> 'Version':
        """
        Create a new version of an object
        
        Args:
            content_object: The object to version
            user: User making the change
            change_notes: Optional notes about what changed
            **kwargs: Additional metadata
            
        Returns:
            Version instance
        """
        content_type = ContentType.objects.get_for_model(content_object)
        
        # Serialize object data
        serialized_data = self._serialize_object(content_object)
        data_hash = self._calculate_hash(serialized_data)
        
        # Check if this version already exists
        existing_version = Version.objects.filter(
            content_type=content_type,
            object_id=content_object.pk,
            data_hash=data_hash
        ).first()
        
        if existing_version:
            return existing_version
        
        # Get next version number
        latest_version = Version.objects.filter(
            content_type=content_type,
            object_id=content_object.pk
        ).order_by('-version_number').first()
        
        version_number = (latest_version.version_number + 1) if latest_version else 1
        
        # Create new version
        version = Version.objects.create(
            content_type=content_type,
            object_id=content_object.pk,
            version_number=version_number,
            data=serialized_data,
            data_hash=data_hash,
            created_by=user,
            change_notes=change_notes,
            metadata=kwargs
        )
        
        return version
    
    def get_versions(self, content_object) -> List['Version']:
        """Get all versions of an object"""
        content_type = ContentType.objects.get_for_model(content_object)
        return Version.objects.filter(
            content_type=content_type,
            object_id=content_object.pk
        ).order_by('-version_number')
    
    def get_version(self, content_object, version_number: int) -> Optional['Version']:
        """Get a specific version of an object"""
        content_type = ContentType.objects.get_for_model(content_object)
        return Version.objects.filter(
            content_type=content_type,
            object_id=content_object.pk,
            version_number=version_number
        ).first()
    
    def rollback_to_version(self, content_object, version_number: int, user) -> bool:
        """
        Rollback an object to a specific version
        
        Args:
            content_object: The object to rollback
            version_number: Version number to rollback to
            user: User performing the rollback
            
        Returns:
            Boolean indicating success
        """
        version = self.get_version(content_object, version_number)
        if not version:
            return False
        
        try:
            with transaction.atomic():
                # Restore object data
                self._restore_object(content_object, version.data)
                
                # Create new version marking the rollback
                self.create_version(
                    content_object,
                    user,
                    change_notes=f"Rolled back to version {version_number}",
                    rollback_from_version=version_number
                )
                
            return True
            
        except Exception:
            return False
    
    def compare_versions(self, content_object, version1: int, version2: int) -> Dict[str, Any]:
        """Compare two versions of an object"""
        v1 = self.get_version(content_object, version1)
        v2 = self.get_version(content_object, version2)
        
        if not v1 or not v2:
            return {'error': 'One or both versions not found'}
        
        return {
            'version1': {
                'number': v1.version_number,
                'created_at': v1.created_at,
                'created_by': v1.created_by.get_full_name(),
                'data': v1.data
            },
            'version2': {
                'number': v2.version_number,
                'created_at': v2.created_at,
                'created_by': v2.created_by.get_full_name(),
                'data': v2.data
            },
            'differences': self._calculate_differences(v1.data, v2.data)
        }
    
    def _serialize_object(self, obj) -> Dict[str, Any]:
        """Serialize object to dictionary"""
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        
        # Default serialization for Django models
        data = {}
        for field in obj._meta.fields:
            if field.name == 'id':
                continue
            
            value = getattr(obj, field.name)
            
            # Handle different field types
            if hasattr(value, 'isoformat'):  # DateTime
                data[field.name] = value.isoformat()
            elif hasattr(value, 'url'):  # File/Image fields
                data[field.name] = value.url if value else None
            else:
                data[field.name] = value
                
        return data
    
    def _restore_object(self, obj, data: Dict[str, Any]):
        """Restore object from serialized data"""
        for key, value in data.items():
            if hasattr(obj, key):
                # Handle datetime fields
                field = obj._meta.get_field(key)
                if field.__class__.__name__ in ['DateTimeField']:
                    if isinstance(value, str):
                        value = datetime.fromisoformat(value)
                
                setattr(obj, key, value)
        
        obj.save()
    
    def _calculate_hash(self, data: Dict[str, Any]) -> str:
        """Calculate hash of serialized data"""
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def _calculate_differences(self, data1: Dict, data2: Dict) -> Dict[str, Any]:
        """Calculate differences between two data dictionaries"""
        differences = {
            'added': {},
            'removed': {},
            'modified': {}
        }
        
        all_keys = set(data1.keys()) | set(data2.keys())
        
        for key in all_keys:
            if key in data1 and key in data2:
                if data1[key] != data2[key]:
                    differences['modified'][key] = {
                        'old': data1[key],
                        'new': data2[key]
                    }
            elif key in data2:
                differences['added'][key] = data2[key]
            else:
                differences['removed'][key] = data1[key]
        
        return differences


class Version(models.Model):
    """Model for storing object versions"""
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    version_number = models.PositiveIntegerField()
    data = models.JSONField()  # Serialized object data
    data_hash = models.CharField(max_length=64)  # SHA-256 hash
    
    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    change_notes = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        unique_together = ['content_type', 'object_id', 'version_number']
        ordering = ['-version_number']
        indexes = [
            models.Index(fields=['content_type', 'object_id', '-version_number']),
            models.Index(fields=['data_hash']),
        ]
    
    def __str__(self):
        return f"Version {self.version_number} of {self.content_object}"


class VersionedMixin(models.Model):
    """Mixin to add versioning capabilities to models"""
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        # Check if this is an update (object has pk)
        is_update = self.pk is not None
        
        super().save(*args, **kwargs)
        
        # Create version after successful save
        if is_update and hasattr(self, '_version_user'):
            version_manager = VersionManager()
            version_manager.create_version(
                self, 
                self._version_user,
                getattr(self, '_version_notes', None)
            )
    
    def set_version_info(self, user, notes: str = None):
        """Set version information for next save"""
        self._version_user = user
        self._version_notes = notes
    
    def get_versions(self):
        """Get all versions of this object"""
        version_manager = VersionManager()
        return version_manager.get_versions(self)
    
    def rollback_to_version(self, version_number: int, user):
        """Rollback to a specific version"""
        version_manager = VersionManager()
        return version_manager.rollback_to_version(self, version_number, user)


# File versioning helpers
class FileVersionManager:
    """Specialized version manager for files"""
    
    @staticmethod
    def create_file_version(uploaded_file, user, change_notes: str = None):
        """Create a version for an uploaded file"""
        from uploads.models import FileVersion
        
        # Get the latest version number
        latest_version = FileVersion.objects.filter(
            original_file=uploaded_file
        ).order_by('-version_number').first()
        
        version_number = (latest_version.version_number + 1) if latest_version else 1
        
        # Calculate file checksum
        checksum = FileVersionManager._calculate_file_checksum(uploaded_file.file)
        
        # Create file version
        file_version = FileVersion.objects.create(
            original_file=uploaded_file,
            version_number=version_number,
            file=uploaded_file.file,
            file_size=uploaded_file.file_size,
            checksum=checksum,
            change_notes=change_notes,
            created_by=user
        )
        
        return file_version
    
    @staticmethod
    def _calculate_file_checksum(file_obj):
        """Calculate SHA-256 checksum of file"""
        hash_sha256 = hashlib.sha256()
        
        # Reset file pointer
        file_obj.seek(0)
        
        # Read file in chunks
        for chunk in iter(lambda: file_obj.read(4096), b""):
            hash_sha256.update(chunk)
        
        # Reset file pointer
        file_obj.seek(0)
        
        return hash_sha256.hexdigest()


# Generation versioning helpers  
class GenerationVersionManager:
    """Specialized version manager for AI generations"""
    
    @staticmethod
    def create_generation_versions(generation, versions: List[str] = None, user=None):
        """Create multiple versions (A, B, C) for an AI generation"""
        from ai_generator.models import GenerationVersion
        
        if not versions:
            versions = ['A', 'B', 'C']
        
        created_versions = []
        
        for version_letter in versions:
            # Create version-specific data variations
            version_data = GenerationVersionManager._create_version_variations(
                generation.generated_content, 
                version_letter
            )
            
            gen_version = GenerationVersion.objects.create(
                original_generation=generation,
                version_letter=version_letter,
                generated_content=version_data['content'],
                variations=version_data['variations'],
                answer_key=version_data.get('answer_key', {}),
                is_primary=(version_letter == 'A')
            )
            
            created_versions.append(gen_version)
        
        return created_versions
    
    @staticmethod
    def _create_version_variations(content: Dict[str, Any], version_letter: str) -> Dict[str, Any]:
        """Create variations for a specific version"""
        import random
        
        # Use version letter as seed for reproducible variations
        random.seed(ord(version_letter))
        
        variations = {
            'question_order_shuffled': True,
            'options_shuffled': True,
            'numerical_variations': [],
            'version_identifier': version_letter
        }
        
        # Create a copy of the content
        version_content = content.copy()
        
        # Shuffle questions if present
        if 'questions' in version_content:
            questions = version_content['questions'].copy()
            random.shuffle(questions)
            
            # Shuffle options for multiple choice questions
            for question in questions:
                if question.get('type') == 'multiple_choice' and question.get('options'):
                    options = question['options'].copy()
                    correct_answer = question.get('correct_answer')
                    
                    # Shuffle options and update correct answer
                    random.shuffle(options)
                    question['options'] = options
                    
                    # Update correct answer if it was a letter (A, B, C, D)
                    if correct_answer and len(correct_answer) == 1 and correct_answer.isalpha():
                        # Find new position of correct answer
                        original_index = ord(correct_answer.upper()) - ord('A')
                        if original_index < len(options):
                            question['correct_answer'] = chr(65 + options.index(
                                content['questions'][questions.index(question)]['options'][original_index]
                            ))
            
            version_content['questions'] = questions
        
        # Generate numerical variations for math problems
        if 'questions' in version_content:
            for i, question in enumerate(version_content['questions']):
                if 'math' in question.get('tags', []) or 'calculation' in question.get('tags', []):
                    # Apply small numerical variations
                    variation_factor = random.uniform(0.9, 1.1)
                    variations['numerical_variations'].append({
                        'question_index': i,
                        'factor': variation_factor
                    })
        
        return {
            'content': version_content,
            'variations': variations,
            'answer_key': GenerationVersionManager._generate_answer_key(version_content)
        }
    
    @staticmethod
    def _generate_answer_key(content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate answer key for the version"""
        answer_key = {
            'answers': [],
            'total_points': 0,
            'generated_at': timezone.now().isoformat()
        }
        
        if 'questions' in content:
            for i, question in enumerate(content['questions']):
                answer_info = {
                    'question_number': i + 1,
                    'correct_answer': question.get('correct_answer'),
                    'explanation': question.get('explanation'),
                    'points': question.get('points', 1)
                }
                
                answer_key['answers'].append(answer_info)
                answer_key['total_points'] += answer_info['points']
        
        return answer_key


# Usage tracking for versions
class VersionUsageTracker:
    """Track version usage for analytics"""
    
    @staticmethod
    def track_version_access(version, user, action: str = 'view'):
        """Track when a version is accessed"""
        from analytics.models import UserActivityLog
        
        UserActivityLog.objects.create(
            user=user,
            action=f'version_{action}',
            description=f'{action.title()} version {version.version_number}',
            metadata={
                'version_id': version.id,
                'version_number': version.version_number,
                'content_type': str(version.content_type),
                'object_id': version.object_id
            }
        )
    
    @staticmethod
    def get_version_stats(content_object) -> Dict[str, Any]:
        """Get statistics about versions for an object"""
        versions = Version.objects.filter(
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.pk
        )
        
        return {
            'total_versions': versions.count(),
            'latest_version': versions.first(),
            'first_version': versions.last(),
            'contributors': versions.values_list('created_by__email', flat=True).distinct(),
            'creation_timeline': list(versions.values('version_number', 'created_at', 'created_by__get_full_name'))
        }
