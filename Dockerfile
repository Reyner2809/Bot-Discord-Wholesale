# Usa Python 3.11.9 (que sí tiene audioop)
FROM python:3.11.9-slim

# Carpeta donde vivirá tu código dentro del contenedor
WORKDIR /app

# Copiamos las dependencias e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el resto del código (setup_discord.py y demás)
COPY . .

# Comando para arrancar tu bot
CMD ["python", "setup_discord.py"]
