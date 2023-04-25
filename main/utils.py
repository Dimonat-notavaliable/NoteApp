from django.template.loader import get_template
import pdfkit


def html_2_pdf(template, context):
    html_content = get_template(template).render(context)
    config = pdfkit.configuration(wkhtmltopdf=r'D:\Python\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(html_content, False, configuration=config)
    return pdf
