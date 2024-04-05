# estamos en AppLegal/views.py
# Aquí se definen las vistas de la API RESTful que se utilizarán para manejar los documentos y plantillas en la aplicación LegalIA.
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Documento, Template
from .serializers import DocumentoSerializer, UserSerializer, TemplateSerializer
from django.contrib.auth.models import User
from django.conf import settings
from .models import Documento, Template
from rest_framework.permissions import IsAuthenticated
import os
from django.core.files.storage import default_storage
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from functools import wraps
from rest_framework import status
from functools import lru_cache
from .nlp_services import extract_entities, generate_text, summarize_text, classify_text, answer_question, translate_text # Importa las funciones de servicios NLP
from .document_utils import extract_text_from_pdf, extract_text_from_docx  # Importa las funciones de utilidad

@lru_cache(maxsize=None)
def get_generator():
    return pipeline('text-generation', model='sshleifer/distilbart-cnn-12-6', revision='a4f8f3e')

@lru_cache(maxsize=None)
def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

@lru_cache(maxsize=None)
def get_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# Tokenizador y modelo para clasificación secuencial
tokenizer = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-cased")
model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

# Decorador para manejar excepciones en las vistas de la API y evitar el uso de try-except en cada vista
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Aquí puedes manejar diferentes tipos de excepciones si es necesario
            # y devolver mensajes de error personalizados
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper

# Carga global de modelos y tokenizadores
class GenerateTextView(APIView):
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt', '')
        if not prompt:
            return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)
        #generator = get_generator()
        generated_text = generate_text(prompt)
        return Response({"generated_text": generated_text})
    
class DocumentSummaryView(APIView):
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        document_text = request.data.get('document', '')
        max_length = request.data.get('max_length', 130)
        min_length = request.data.get('min_length', 30)

        if not document_text:
            return Response({"error": "Document text is required."}, status=status.HTTP_400_BAD_REQUEST)

        summary = summarize_text(document_text, max_length=max_length, min_length=min_length)
        return Response({"summary": summary})
# Devuelve el resumen del documento

class TextClassificationView(APIView):
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        labels = request.data.get('labels', ['Carta Documento', 'Demanda', 'Nota Simple', 'Solicitud de Informe'])

        if not text:
            return Response({"error": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)
        #classifier = get_classifier()
        classification = classify_text(text, labels)
        return Response({"classification": classification})

# Modelo de QA (Answer Question) para responder preguntas sobre un contexto dado    
class DocumentInteractionView(APIView): # Vista para interactuar con un documento
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        question = request.data.get('question', '')
        
        if not file or not question:
            return Response({"error": "File and question are required."}, status=status.HTTP_400_BAD_REQUEST)

        if file.name.endswith('.pdf'):
            context_text = extract_text_from_pdf(file)
        elif file.name.endswith('.docx'):
            context_text = extract_text_from_docx(file)
        else:
            return Response({"error": "Unsupported file type."}, status=status.HTTP_400_BAD_REQUEST)

        answer = answer_question(question, context_text)
        return Response({"answer": answer})
    
class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        # Verifica la extensión del archivo
        valid_extensions = ['.doc', '.docx', '.pdf']
        if not any(file.name.endswith(ext) for ext in valid_extensions):
            return Response({"error": "File type not supported. Only .doc, .docx, and .pdf files are allowed."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:    # Guarda el archivo en el sistema de archivos
            file_name = default_storage.save(file.name, file)
            file_url = default_storage.url(file_name)
            # Aquí podrías crear y guardar un nuevo objeto Document con el URL del archivo, etc.
        except Exception as e:
            return Response({"error": f"Failed to upload file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"url": file_url}, status=status.HTTP_201_CREATED)
class DocumentoViewSet(viewsets.ModelViewSet):  # Actualización de la clase DocumentoViewSet para integrar la lógica de NLP
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated]  # Usar IsAuthenticated para restringir el acceso a usuarios autenticados
    
    def perform_create(self, serializer):   # Actualización del método perform_create para asociar el documento con el usuario autenticado
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['get'])   # Actualización del método resumen para generar un resumen del documento

    def resumen(self, request, pk=None):    # Método resumen para generar un resumen del documento
        documento = self.get_object()
        # Aquí integrarías la lógica para generar el resumen usando tus modelos de NLP
        return Response({'resumen': 'Este es un resumen ficticio del documento.'})
    
class UserViewSet(viewsets.ModelViewSet):   # Actualización de la clase UserViewSet para integrar la lógica de NLP
    queryset = User.objects.all()   # Actualización del queryset para listar todos los usuarios
    serializer_class = UserSerializer   # Actualización del serializador para el modelo User
    permission_classes = [IsAuthenticated]  # Usar IsAuthenticated para restringir el acceso a usuarios autenticados

class NERView(APIView):  # Vista para extraer entidades nombradas de un texto
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        if not text:
            return Response({"error": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        entities = extract_entities(text)
        return Response({"entities": entities})
    
class TranslationView(APIView):
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        if not text:
            return Response({"error": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        translation = translate_text(text)
        return Response({"translation": translation})


class TemplateListViewSet(viewsets.ModelViewSet):   # Actualización de la clase TemplateListViewSet para listar y crear plantillas
    queryset = Template.objects.all()   # Actualización del queryset para listar todas las plantillas
    serializer_class = TemplateSerializer
    # La clase de permisos y demás configuraciones van aquí
    def get(self, request): # Actualización del método get para listar todas las plantillas
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request):    # Actualización del método post para crear una nueva plantilla
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Actualización de la clase DocumentoList para listar y crear documentos
#class DocumentoList(generics.ListCreateAPIView):
    
class DocumentoListViewSet(viewsets.ModelViewSet):  # Actualización de la clase DocumentoListViewSet para listar y crear documentos
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    #permission_classes = [IsAuthenticated]  # Opcional: Restringir acceso a usuarios autenticados

# Actualización de la clase UserList para listar y crear usuarios
#class UserList(generics.ListCreateAPIView):
class UserListViewSet(viewsets.ModelViewSet):   # Actualización de la clase UserListViewSet para listar y crear usuarios
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAuthenticated]  # Opcional: Restringir acceso a usuarios autenticados

# Vista para manejar la carga de archivos
#class FileUploadView(APIView):


def home_view(request):
    funciones = [
        {
            'nombre': ' Descargar Documentos | ',
            'descripcion': 'Permite la descarga de documentos almacenados.'
        },
        {
            'nombre': ' Subir Documento | ',
            'descripcion': 'Permite subir un documento al sistema.'
        },
        {
            'nombre': ' Listar Documentos | ',
            'descripcion': 'Permite listar todos los documentos almacenados.'
        },
        {
            'nombre': ' Generador de textos | ',
            'descripcion': 'Genera textos automáticamente basado en un prompt.',
            #'ruta': f'{base_url}/api/generar-texto/',
        },
        {
            'nombre': ' Resumen de documentos |',
            'descripcion': 'Proporciona un resumen del contenido de un documento.',
            #'ruta': f'{base_url}/api/documentos/<id>/resumen/',
        },
        {
            'nombre': ' Interactuar con un documento |',
            'descripcion': 'Permite realizar acciones específicas con un documento.',
            #'ruta': f'{base_url}/api/documentos/<id>/interactuar/',
        },
        # Agrega las demás funcionalidades aquí...
    ]

    # Crear una representación de texto de las funcionalidades
    funciones_texto = [" Funciones Disponibles: "]
    for funcion in funciones:
        funciones_texto.append(f"{funcion['nombre']}: {funcion['descripcion']}")

    # Unir todas las líneas en una sola cadena de texto
    respuesta = "\n".join(funciones_texto)

    # Devolver la respuesta como texto plano
    return HttpResponse(respuesta, content_type="text/plain")
#    return JsonResponse(funciones)

# Servicio de descarga de documentos almacenados en MEDIA_ROOT
def download_documento(request, file_path):
    full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(full_file_path):
        with open(full_file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(full_file_path)}"'
            return response
    else:
        raise Http404


"""
# Carga global de modelos y tokenizadores(Opcion 2)

#generator = pipeline('text-generation', model='sshleifer/distilbart-cnn-12-6', revision='a4f8f3e')
#summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
#model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
#tokenizer = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-cased")

# Clase de servicio NLP (Opcion 3)
class NLPService:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        try:
            # Inicializar los pipelines de Transformers
            self.summarizer = pipeline("summarization")
            self.text_generator = pipeline("text-generation", model=model_name)
            self.text_classifier = pipeline("zero-shot-classification")
        except Exception as e:
            print(f"Error al inicializar los pipelines: {e}")

    def generate_text(self, prompt_text):
        try:
            generated_text = self.text_generator(prompt_text, max_length=50, do_sample=True)[0]["generated_text"]
            return generated_text
        except Exception as e:
            print(f"Error al generar texto: {e}")
            return "Ocurrió un error al generar el texto."

    def summarize_text(self, document_text):
        try:
            summary_text = self.summarizer(document_text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
            return summary_text
        except Exception as e:
            print(f"Error al resumir el texto: {e}")
            return "Ocurrió un error al resumir el texto."

    def classify_text(self, text, labels):
        try:
            classification_result = self.text_classifier(text, labels=labels)["labels"][0]
            return classification_result
        except Exception as e:
            print(f"Error al clasificar el texto: {e}")
            return "Ocurrió un error al clasificar el texto."

# Ejemplo de uso
if __name__ == "__main__":
    nlp_service = NLPService()
    
    # Ejemplo de clasificación de texto en un estudio jurídico
    text_to_classify = "Se solicita un informe detallado sobre el historial del inmueble situado en..."
    legal_labels = ["Nota Simple", "Demanda", "Solicitud de Informe", "Carta Documento"]
    classification_result = nlp_service.classify_text(text_to_classify, legal_labels)
    print(f"La clasificación del texto es: {classification_result}")
    
"""

"""Carga el tokenizer y el modelo
#tokenizer = AutoTokenizer.from_pretrained("nombre-del-modelo")
#model = AutoModel.from_pretrained("nombre-del-modelo")

#def obtener_vector_de_texto(texto):
#    Convierte un texto a un vector utilizando el modelo de Transformers.
#    inputs = tokenizer(texto, return_tensors="pt", padding=True, truncation=True, max_length=512)
#    outputs = model(**inputs)
    return torch.mean(outputs.last_hidden_state, dim=1)

def buscar_documentos_legales(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse({"resultados": []})
    
    query_vector = obtener_vector_de_texto(query)
    
    # Buscar una forma de comparar este vector de consulta con los vectores de tus documentos.
    # Esto puede implicar tener una base de datos de vectores o un índice de búsqueda como Elasticsearch.
    # Ejemplo simplificado.
    
    documentos_similares = []
    for documento in DocumentoLegal.objects.all():
        doc_vector = obtener_vector_de_texto(documento.contenido)
        similitud = torch.cosine_similarity(query_vector, doc_vector).item()
        
        # Añadir el documento a los resultados si la similitud supera un umbral
        if similitud > 0.5:  # Umbral de similitud, ajustable según tus necesidades
            documentos_similares.append({
                "titulo": documento.titulo,
                "contenido": documento.contenido,
                "similitud": similitud
            })
    
    # Ordenar los documentos por similitud
    documentos_similares = sorted(documentos_similares, key=lambda x: x["similitud"], reverse=True)
    
    return JsonResponse({"resultados": documentos_similares})"""

## Busqueda semántica con Hugging Face Transformers para buscar documentos legales en la base de datos o en una API externa.
#search_pipeline = pipeline("text-search", model="YourModelForSemanticSearch")
#def buscar_documentos_legales(request):
#   query = request.GET.get("q", "")
    # Simulación de búsqueda: falta adaptarlo para buscar en la base de datos o llamar a una API externa
    # de documentos legales. Aquí usamos una búsqueda simple por coincidencia de texto.
    #documentos = DocumentoLegal.objects.filter(contenido__icontains=query)
    
    # Preparar los resultados para la respuesta
    #resultados = [{"titulo": doc.titulo, "contenido": doc.contenido} for doc in documentos]
    
    #return JsonResponse({"resultados": resultados})