from django.shortcuts import render
from django.http import HttpResponse
from .forms import ARFFUploadForm
import arff
import io

def upload_arff(request):
    if request.method == "POST":
        form = ARFFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            try:
                # Leer el contenido binario
                raw_data = uploaded_file.read()

                # Convertir a texto
                text_data = raw_data.decode("utf-8")

                # Crear un buffer de texto
                fp = io.StringIO(text_data)

                # Cargar el ARFF desde un archivo en texto
                data = arff.load(fp)

                return HttpResponse("Archivo ARFF procesado correctamente!")

            except Exception as e:
                return HttpResponse(f"Error procesando el archivo ARFF: {e}")

    else:
        form = ARFFUploadForm()

    return render(request, "upload.html", {"form": form})
