import io
from PIL import Image
from sentence_transformers import SentenceTransformer

# Esto se ejecuta UNA SOLA VEZ, cuando el servidor arranca
# (la primera vez que algo hace "import app.ai").
print("Cargando el modelo CLIP...")
modelo_clip = SentenceTransformer('clip-ViT-B-32')
print("Modelo CLIP listo.")


def calcular_embedding(bytes_imagen: bytes) -> list[float]:
    """Recibe los bytes de una imagen y devuelve su embedding como lista de números."""
    imagen = Image.open(io.BytesIO(bytes_imagen))
    vector = modelo_clip.encode(imagen)
    return vector.tolist()


def calcular_embedding_texto(texto: str) -> list[float]:
    """Recibe un texto y devuelve su embedding, en el mismo espacio que las imágenes."""
    vector = modelo_clip.encode(texto)
    return vector.tolist()