from django.shortcuts import render
from .forms import ARFFUploadForm
import arff

def upload_arff(request):
    if request.method == 'POST':
        form = ARFFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Guardar temporalmente
            temp_path = '/tmp/upload.arff'

            with open(temp_path, 'wb') as temp:
                for chunk in uploaded_file.chunks():
                    temp.write(chunk)

            try:
                with open(temp_path, 'rb') as f:  # <-- 'rb' !!!
                    data = arff.load(f)

                return render(request, 'arff_app/result.html', {
                    'relation': data['relation'],
                    'attributes': data['attributes'],
                    'data': data['data'],
                })

            except Exception as e:
                return render(request, 'arff_app/upload.html', {
                    'form': form,
                    'error': f"Error procesando el archivo ARFF: {str(e)}"
                })

    else:
        form = ARFFUploadForm()

    return render(request, 'arff_app/upload.html', {'form': form})
