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
            uploaded_file = request.FILES['file']  # archivo en memoria

            # Abrir en modo binario
            f = uploaded_file.open('rb')
            data = arff.load(f)

            df = pd.DataFrame(data['data'], columns=[attr[0] for attr in data['attributes']])

            total_datos = len(df)

            X = df.iloc[:, :-1]
            y = df.iloc[:, -1]

            counts = y.value_counts()
            valid_classes = counts[counts >= 2].index
            removed_classes = counts[counts < 2].index

            if len(removed_classes) > 0:
                df = df[df.iloc[:, -1].isin(valid_classes)]
                X = df.iloc[:, :-1]
                y = df.iloc[:, -1]
                context['warning'] = f"Se eliminaron clases con menos de 2 muestras: {list(removed_classes)}"

            min_class_count = y.value_counts().min()
            if min_class_count < 3:
                stratify_train = None
                warning_stratify = "Dataset pequeño o desbalanceado. División sin estratificación."
            else:
                stratify_train = y
                warning_stratify = None

            X_train_val, X_test, y_train_val, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42, stratify=stratify_train
            )

            stratify_val = y_train_val if stratify_train is not None else None

            X_train, X_val, y_train, y_val = train_test_split(
                X_train_val, y_train_val, test_size=0.3, random_state=42, stratify=stratify_val
            )

            if warning_stratify:
                context['warning'] = (context.get('warning', '') + ' ' + warning_stratify).strip()

            clf = DecisionTreeClassifier()
            clf.fit(X_train, y_train)

            acc_val = accuracy_score(y_val, clf.predict(X_val))
            acc_test = accuracy_score(y_test, clf.predict(X_test))

            table_html = df.to_html(classes="table table-striped", index=False)

            class_counts = df.iloc[:, -1].value_counts().to_dict()

            context.update({
                'form': form,
                'total_datos': total_datos,
                'count_train': len(X_train),
                'count_val': len(X_val),
                'count_test': len(X_test),
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
