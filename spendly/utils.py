import csv
from django.http import HttpResponse


def export_to_csv(filename, headers, queryset, row_builder):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{filename}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(headers)

    for obj in queryset:
        writer.writerow(row_builder(obj))

    return response