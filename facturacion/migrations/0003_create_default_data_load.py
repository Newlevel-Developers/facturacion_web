from django.db import migrations

def cargar_tipos_documento(apps, schema_editor):
    TipoDocumento = apps.get_model('facturacion', 'TipoDocumento')
    
    # Insertar registros iniciales
    TipoDocumento.objects.bulk_create([
        TipoDocumento(tipo='Cédula de Identidad'),
        TipoDocumento(tipo='RIF'),
        TipoDocumento(tipo='Pasaporte'),
    ])

def reverter_carga(apps, schema_editor):
    TipoDocumento = apps.get_model('facturacion', 'TipoDocumento')
    TipoDocumento.objects.filter(tipo__in=['Cédula de Identidad', 'RIF', 'Pasaporte']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0002_create_default_superuser'),  # Depende de tu migración inicial
    ]

    operations = [
        migrations.RunPython(cargar_tipos_documento, reverter_carga),
    ]