from django.shortcuts import render
from .forms import ARFFUploadForm
import arff

def upload_arff(request):
    if request.method == 'POST':
        form = ARFFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            try:
                # Leer el archivo como texto
                text = uploaded_file.read().decode('utf-8', errors='ignore')

                # Cargar el ARFF desde string
                data = arff.loads(text)

                return render(request, 'arff_app/result.html', {
                    'relation': data['relation'],
                    'attributes': data['attributes'],
                    'data': data['data'],
                })

            except Exception as e:
                return render(request, 'arff_app/upload.html', {
                    'form': form,
                    'error': f"Error procesando el archivo ARFF: {e}"
                })

    else:
        form = ARFFUploadForm()

    return render(request, 'arff_app/upload.html', {'form': form})
