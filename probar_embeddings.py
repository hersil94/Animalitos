from sentence_transformers import SentenceTransformer
from PIL import Image

print("Cargando el modelo CLIP (puede tardar la primera vez)...")
modelo = SentenceTransformer('clip-ViT-B-32')


ruta_foto = "C:/mascotas-perdidas/Fotos/test1.png"


imagen = Image.open(ruta_foto)
embedding = modelo.encode(imagen)

print("¡Listo! El embedding de esta imagen tiene", len(embedding), "números.")
print("Los primeros 5 números son:", embedding[:5])
