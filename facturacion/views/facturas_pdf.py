import io
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from facturacion.models import Factura, DetalleFactura

@login_required
def generar_factura_pdf(request, id):
    factura = get_object_or_404(Factura, id=id)
    detalles = DetalleFactura.objects.filter(factura=factura)

    context = {
        'factura': factura,
        'detalles': detalles,
        'empresa': {
            'nombre': 'New Level Developers',
            'rif': 'J-12345678-0',
            'web': 'https://newlevel-dev.freedev.app',
            'email': 'levelnew2026@gmail.com',
        }
    }

    template = get_template('facturas/factura_pdf.html')
    html = template.render(context)

    buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF de la factura', status=500)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Factura_{factura.numero_factura}.pdf"'
    return response