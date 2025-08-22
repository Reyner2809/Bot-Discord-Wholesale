# 🚀 Configuración Automática Discord – Ninja Agents AI

Este bot configura un servidor de Discord con todos los roles, categorías, canales y permisos según el checklist oficial de Ninja Agents AI.

## 🔹 Instalación Rápida

1. **Crea un bot en Discord Developer Portal**  
   - https://discord.com/developers/applications  
   - Crea una aplicación → "Ninja Agents AI Setup Bot"  
   - En la pestaña *Bot*, genera el **TOKEN** y cópialo.  
   - Activa permisos de **Administrator**.  

2. **Descarga este ZIP y descomprímelo**  
   ```bash
   unzip discord_setup_ninja_agents.zip
   cd discord_setup_ninja_agents
   ```

3. **Instala dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura el TOKEN**  
   - Copia `.env.example` a `.env`  
   - Pega tu TOKEN dentro.  

5. **Ejecuta el bot**  
   ```bash
   python setup_discord.py
   ```

6. **Invita el bot a tu servidor**  
   - Usa el link de invitación con permisos de admin.  
   - Una vez dentro, configurará todo automáticamente.  
