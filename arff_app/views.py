from django.shortcuts import render
from .forms import ARFFUploadForm
import pandas as pd
import arff

def upload_arff(request):
    context = {}
    form = ARFFUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        try:
            # Guardar archivo subido
            arff_file = form.save()

            # Abrir el archivo en modo binario
            with open(arff_file.file.path, 'rb') as f:
                data = arff.load(f)

            # Crear DataFrame
            df = pd.DataFrame(
                data['data'],
                columns=[attr[0] for attr in data['attributes']]
            )

            # Guardar datos en contexto
            context['table'] = df.to_html(classes='table table-striped', index=False)
            context['success'] = "Archivo ARFF procesado correctamente."

        except Exception as e:
            context['error'] = f"Error al procesar el archivo ARFF: {str(e)}"

    context['form'] = form
    return render(request, 'upload.html', context)
