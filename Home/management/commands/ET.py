# management/commands/import_event_types.py
"""
Advanced management command to import event types from CSV or JSON
Usage: 
    python manage.py import_event_types --csv events.csv
    python manage.py import_event_types --json events.json
"""

import csv
import json
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Import event types from CSV or JSON file'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            help='Path to CSV file with event types',
        )
        parser.add_argument(
            '--json',
            type=str,
            help='Path to JSON file with event types',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing event types before import',
        )
    
    def handle(self, *args, **options):
        EventType = apps.get_model('Home', 'EventType')
        
        # Clear if requested
        if options['clear']:
            count = EventType.objects.count()
            EventType.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Cleared {count} existing event types"))
        
        # Import from CSV
        if options['csv']:
            self.import_from_csv(options['csv'], EventType)
        
        # Import from JSON
        elif options['json']:
            self.import_from_json(options['json'], EventType)
        
        else:
            self.stdout.write(self.style.ERROR("Please provide --csv or --json file"))
    
    def import_from_csv(self, filepath, EventType):
        """Import event types from CSV file"""
        try:
            with open(filepath, 'r') as file:
                reader = csv.DictReader(file)
                created = 0
                
                for row in reader:
                    event_type, created_flag = EventType.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'description': row.get('description', ''),
                            'icon': row.get('icon', 'fas fa-calendar'),
                            'display_order': int(row.get('display_order', 0)),
                            'is_active': row.get('is_active', 'True').lower() == 'true'
                        }
                    )
                    if created_flag:
                        created += 1
                        self.stdout.write(f"✓ Created: {row['name']}")
                
                self.stdout.write(self.style.SUCCESS(f"\nImported {created} new event types"))
                
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {filepath}"))
    
    def import_from_json(self, filepath, EventType):
        """Import event types from JSON file"""
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                created = 0
                
                for item in data:
                    event_type, created_flag = EventType.objects.get_or_create(
                        name=item['name'],
                        defaults={
                            'description': item.get('description', ''),
                            'icon': item.get('icon', 'fas fa-calendar'),
                            'display_order': item.get('display_order', 0),
                            'is_active': item.get('is_active', True)
                        }
                    )
                    if created_flag:
                        created += 1
                        self.stdout.write(f"✓ Created: {item['name']}")
                
                self.stdout.write(self.style.SUCCESS(f"\nImported {created} new event types"))
                
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {filepath}"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Invalid JSON in file: {filepath}"))