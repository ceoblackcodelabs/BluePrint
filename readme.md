# Basic creation
python manage.py create_event_types

# List existing event types
python manage.py create_event_types --list

# Show count
python manage.py create_event_types --count

# Reset (delete and recreate)
python manage.py create_event_types --reset

# Append new types without deleting existing
python manage.py create_event_types --append

# Dry run (see what would happen)
python manage.py create_event_types --dry-run

# Reset with confirmation
python manage.py create_event_types --reset

# Import from CSV
python manage.py import_event_types --csv events.csv

# Import from JSON and clear existing
python manage.py import_event_types --json events.json --clear