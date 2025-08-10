import csv
from pathlib import Path
from docfinder.models import Provider, Taxonomy, ProviderTaxonomy

BASE_DIR = Path(__file__).resolve().parent.parent

def load_providers():
    with open(BASE_DIR / 'data' / 'providers.csv', newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            npi = row['npi'].zfill(10)
            try:
                Provider.objects.get_or_create(
                    npi=npi,
                    defaults={
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'middle_name': row['middle_name'],
                        'credential': row['credential'],
                        'address_1': row['address_1'],
                        'address_2': row['address_2'],
                        'city': row['city'],
                        'state': row['state'],
                        'zip': row['zip'],
                        "phone_number": row['phone_number']
                    }
                )
            except Exception as e:
                print(f"Row {i} failed: {e}")

def load_taxonomy():
    with open(BASE_DIR / 'data' / 'taxonomy.csv', newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            try:
                Taxonomy.objects.get_or_create(
                    code=row['code'],
                    defaults={
                        'grouping': row['grouping'],
                        'classification': row['classification'],
                        'specialization': row['specialization'],
                        'definition': row['definition'],
                        'display_name': row['display_name'],
                    }
                )
            except Exception as e:
                print(f"Taxonomy Row {i} failed: {e}")

def load_provider_taxonomies():
    with open(BASE_DIR / 'data' / 'provider_taxonomies.csv', newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            npi = row['provider_npi'].zfill(10)
            taxonomy_code = row['taxonomy_code']
            try:
                provider = Provider.objects.get(npi=npi)
                taxonomy = Taxonomy.objects.get(code=taxonomy_code)
                ProviderTaxonomy.objects.get_or_create(
                    provider=provider,
                    taxonomy=taxonomy,
                    defaults={'primary': row['primary'].lower() == 'true'}
                )
            except Provider.DoesNotExist:
                print(f"Skipped: Provider NPI not found → {npi}")
            except Taxonomy.DoesNotExist:
                print(f"Skipped: Taxonomy code not found → {taxonomy_code}")
            except Exception as e:
                print(f"Row {i} failed: {e}")

def run():
    load_providers()
    load_taxonomy()
    load_provider_taxonomies()
