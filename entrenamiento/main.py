from weka.classifiers import Classifier, Evaluation
from weka.core.classes import serialization_write, Random
from weka.core.converters import Loader
from weka.filters import Filter

def training(dataset, fichsalida,clasificador="weka.classifiers.trees.RandomForest",debug_level=0):
    resultados = [clasificador.split('.')[-1],dataset, fichsalida]
    # Carga de datos desde un archivo ARFF
    loader = Loader(classname="weka.core.converters.ArffLoader")
    data = loader.load_file(dataset)
    if debug_level>0:print(f'[Entrenamiento] Cargado dataset: {dataset}')

    # Establecer la última columna como clase objetivo
    data.class_is_last()

    # Aplicar un filtro de normalización
    normalize = Filter(classname="weka.filters.unsupervised.attribute.Normalize")
    normalize.inputformat(data)
    data_normalized = normalize.filter(data)

    # Dividir los datos en 70% entrenamiento y 30% prueba
    train, test = data_normalized.train_test_split(70.0, Random(1))

    # Crear y configurar el clasificador
    classifier = Classifier(classname=clasificador)

    # Entrenar el modelo con los datos de entrenamiento
    classifier.build_classifier(train)

    # Evaluar el modelo en el conjunto de prueba
    evaluation = Evaluation(train)
    evaluation.test_model(classifier, test)


    # Mostrar los resultados
    if debug_level==2:print(evaluation.summary())

    resultados.append(evaluation.percent_correct)

    # Guardar el modelo en un archivo
    serialization_write(fichsalida, classifier)
    if debug_level>0:print(f"[Entrenamiento] Guardado modelo en: {fichsalida}")
    return resultados


