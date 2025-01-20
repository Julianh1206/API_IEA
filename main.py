from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from pathlib import Path
from uuid import uuid4  # Para generar IDs únicos

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar carpetas de plantillas y estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta del archivo JSON donde guardarás los datos
DATA_PATH = Path("data/clients.json")
DATA_PATH.parent.mkdir(exist_ok=True)  # Crear carpeta si no existe
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]")  # Crear archivo vacío inicial

# Ruta para mostrar el formulario
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Ruta para manejar el envío del formulario
@app.post("/submit/")
async def submit_form(
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    direccion: str = Form(...),
    edad: int = Form(...),
    genero: str = Form(...),
    ubicacion: str = Form(...),
    fecha_compra: str = Form(...),  # Asegúrate de enviar la fecha en formato adecuado
    metodo_pago: str = Form(...),
    mercancia: str = Form(...),
    valor_mercancia: float = Form(...),
    valor_venta: float = Form(...)
):
    # Leer datos existentes del archivo JSON
    with open(DATA_PATH, "r") as file:
        clients = json.load(file)

    # Calcular la ganancia
    ganancia = valor_venta - valor_mercancia

    # Crear un nuevo cliente con un ID único
    new_client = {
        "id_cliente": str(uuid4()),  # Generar un ID único
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "direccion": direccion,
        "edad": edad,
        "genero": genero,
        "ubicacion": ubicacion,
        "fecha_compra": fecha_compra,
        "metodo_pago": metodo_pago,
        "mercancia": mercancia,
        "valor_mercancia": valor_mercancia,
        "valor_venta": valor_venta,
        "ganancia": ganancia
    }

    # Agregar el nuevo cliente a la lista
    clients.append(new_client)

    # Guardar datos actualizados en el archivo JSON
    with open(DATA_PATH, "w") as file:
        json.dump(clients, file, indent=4)

    return {"message": "Datos enviados con éxito", "data": new_client}
