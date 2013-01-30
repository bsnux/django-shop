# -*- coding: utf-8 -*-
import csv

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse


def encode_field(field):
    if field:
        return field.encode('utf-8')
    else:
        return ''


def generate_csv(filename, header, rows):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)

    writer = csv.writer(response)

    writer.writerow(header)

    for row in rows:
        writer.writerow(row)

    return response


def export_csv_orders(modeladmin, request, queryset):
    header = ['ID', 'Usuario', 'Estado', 'Total compra', 'Fecha', 'Dir. envio', 'Dir. facturacion', 'Forma de pago']
    filename = 'pedidos.csv'
    rows = []

    for order in queryset:
        username = ''
        payment_method = ''
        if order.user:
            username = order.user.username
        if len(order.orderpayment_set.all()) > 0:
            payment_method = encode_field(order.orderpayment_set.all()[0].payment_method)
        row = [order.id, username, order.get_status_display(),
               order.order_total, order.created.strftime('%d-%m-%Y %H:%M:%S'),
               encode_field(order.shipping_address_text), encode_field(order.billing_address_text),
               payment_method, ]
        rows.append(row)

    return generate_csv(filename, header, rows)
export_csv_orders.short_description = _(u'Exportar a fichero CSV (MS Excel)')
