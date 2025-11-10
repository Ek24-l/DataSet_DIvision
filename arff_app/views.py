# arff_app/views.py
from django.shortcuts import render
from .forms import ARFFUploadForm
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import arff
import pandas as pd
import json
import traceback

def upload_arff(request):
    context = {}
    form = ARFFUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        try:
            # Guardar archivo sin usar form.save() si tu Form no tiene modelo
            uploaded_file = request.FILES['file']

            # Leer archivo ARFF
            data = arff.load(uploaded_file)
            df = pd.DataFrame(data['data'], columns=[attr[0] for attr in data['attributes']])

            total_datos = len(df)

            # Separar features y target
            X = df.iloc[:, :-1]
            y = df.iloc[:, -1]

            # Filtrar clases con menos de 2 muestras
            counts = y.value_counts()
            valid_classes = counts[counts >= 2].index
            removed_classes = counts[counts < 2].index
            if len(removed_classes) > 0:
                df = df[df.iloc[:, -1].isin(valid_classes)]
                X = df.iloc[:, :-1]
                y = df.iloc[:, -1]
                context['warning'] = f"Se eliminaron clases con menos de 2 muestras: {list(removed_classes)}"

            # Decidir si se puede estratificar
            min_class_count = y.value_counts().min()
            if min_class_count < 3:
                stratify_train = None
                warning_stratify = "Dataset pequeño o clases desbalanceadas: división realizada sin estratificación."
            else:
                stratify_train = y
                warning_stratify = None

            # Separar train+val / test
            X_train_val, X_test, y_train_val, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42, stratify=stratify_train
            )

            # Separar train / val
            stratify_val = y_train_val if stratify_train is not None else None

            X_train, X_val, y_train, y_val = train_test_split(
                X_train_val, y_train_val, test_size=0.3, random_state=42, stratify=stratify_val
            )

            if warning_stratify:
                context['warning'] = (context.get('warning', '') + ' ' + warning_stratify).strip()

            # Contar ejemplos
            count_train = len(X_train)
            count_val = len(X_val)
            count_test = len(X_test)

            # Entrenar modelo
            clf = DecisionTreeClassifier()
            clf.fit(X_train, y_train)

            # Validación y test
            acc_val = accuracy_score(y_val, clf.predict(X_val))
            acc_test = accuracy_score(y_test, clf.predict(X_test))

            # Tabla HTML
            table_html = df.to_html(classes="table table-striped", index=False)

            # Conteo de clases
            class_counts = df.iloc[:, -1].value_counts().to_dict()

            context.update({
                'form': form,
                'total_datos': total_datos,
                'count_train': count_train,
                'count_val': count_val,
                'count_test': count_test,
                'acc_val': acc_val,
                'acc_test': acc_test,
                'table_html': table_html,
                'class_labels_json': json.dumps(list(class_counts.keys())),
                'class_values_json': json.dumps(list(class_counts.values())),
            })

        except Exception as e:
            context['form'] = form
            context['error'] = f"Error procesando el archivo ARFF: {str(e)}"
            context['traceback'] = traceback.format_exc()

    else:
        context['form'] = form

    return render(request, 'arff_app/upload.html', context)
