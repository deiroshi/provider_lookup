import csv
from pathlib import Path
from django.db import transaction
from docfinder.models import Provider, Taxonomy, ProviderTaxonomy

BASE_DIR = Path(__file__).resolve().parent.parent

def load_providers():
    file_path = BASE_DIR / 'data' / 'providers.csv'
    batch_size = 10000
    providers = []
    total = sum(1 for _ in open(file_path)) - 1  # minus header
    print(f"Total rows in providers.csv: {total}")
    created = 0

    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            npi = row['npi'].zfill(10)

            providers.append(Provider(
                npi=npi,
                first_name=row['first_name'],
                last_name=row['last_name'],
                middle_name=row['middle_name'],
                credential=row['credential'],
                address_1=row['address_1'],
                address_2=row['address_2'],
                city=row['city'],
                state=row['state'],
                zip=row['zip'],
                phone_number=row['phone_number'],
            ))

            if i % batch_size == 0:
                with transaction.atomic():
                    Provider.objects.bulk_create(providers, ignore_conflicts=True)
                created += len(providers)
                print(f"{created}/{total} rows inserted ({created/total*100:.2f}%)")
                providers.clear()

        if providers:
            with transaction.atomic():
                Provider.objects.bulk_create(providers, ignore_conflicts=True)
            created += len(providers)
            print(f"{created}/{total} rows inserted ({created/total*100:.2f}%)")

def load_taxonomy():
    file_path = BASE_DIR / 'data' / 'taxonomy.csv'
    total = sum(1 for _ in open(file_path)) - 1
    print(f"Total rows in taxonomy.csv: {total}")

    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        taxonomies = []
        for i, row in enumerate(reader, 1):
            taxonomies.append(Taxonomy(
                code=row['code'],
                grouping=row['grouping'],
                classification=row['classification'],
                specialization=row['specialization'],
                definition=row['definition'],
                display_name=row['display_name'],
            ))

        with transaction.atomic():
            Taxonomy.objects.bulk_create(taxonomies, ignore_conflicts=True)
        print(f"{len(taxonomies)} taxonomies inserted")

def load_provider_taxonomies():
    file_path = BASE_DIR / 'data' / 'provider_taxonomies.csv'
    total = sum(1 for _ in open(file_path)) - 1
    print(f"Total rows in provider_taxonomies.csv: {total}")
    batch_size = 10000
    created = 0
    mappings = []

    # Faster lookup using raw query maps (no .get, no .all)
    provider_qs = Provider.objects.values_list('npi', 'id')
    taxonomy_qs = Taxonomy.objects.values_list('code', 'id')
    provider_map = {npi: pid for npi, pid in provider_qs}
    taxonomy_map = {code: tid for code, tid in taxonomy_qs}
    print(f"✔ Cached {len(provider_map)} providers and {len(taxonomy_map)} taxonomies")

    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            npi = row['provider_npi'].zfill(10)
            taxonomy_code = row['taxonomy_code']

            provider_id = provider_map.get(npi)
            taxonomy_id = taxonomy_map.get(taxonomy_code)

            if provider_id and taxonomy_id:
                mappings.append(ProviderTaxonomy(
                    provider_id=provider_id,
                    taxonomy_id=taxonomy_id,
                    primary=row['primary'].lower() == 'true'
                ))

            if i % batch_size == 0:
                with transaction.atomic():
                    ProviderTaxonomy.objects.bulk_create(mappings, ignore_conflicts=True)
                created += len(mappings)
                print(f"{created}/{total} inserted ({created / total * 100:.2f}%)")
                mappings.clear()

        if mappings:
            with transaction.atomic():
                ProviderTaxonomy.objects.bulk_create(mappings, ignore_conflicts=True)
            created += len(mappings)
            print(f"{created}/{total} inserted ({created / total * 100:.2f}%)")

def run():
    print("\n🔄 Loading Providers...")
load_providers()
print("\n✅ Providers loaded.")

print("\n🔄 Loading Taxonomy...")
load_taxonomy()
print("\n✅ Taxonomy loaded.")

print("\n🔄 Linking Providers & Taxonomies...")
load_provider_taxonomies()
print("\n✅ Provider-Taxonomy links created.")