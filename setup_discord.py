import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# === Servidor HTTP mínimo para Render ===
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot activo ✅")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"Servidor escuchando en puerto {port}")
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# === Intents correctos ===
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# === Eventos de tu bot ===
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    guild = bot.guilds[0]
    print(f"Configurando servidor: {guild.name}")

    roles = [
        ("CEO 👑", discord.Permissions.all()),
        ("Partner 🤝", discord.Permissions(administrator=True)),
        ("Supervisores 📊", discord.Permissions()),
        ("Closer 🎯", discord.Permissions()),
        ("Agents 🎧", discord.Permissions()),
        ("RRHH 🧑‍💼", discord.Permissions()),
        ("Programmers 💻", discord.Permissions()),
        ("Bookkeeper 💵", discord.Permissions()),
    ]

    created_roles = {}
    for name, perms in roles:
        role = discord.utils.get(guild.roles, name=name)
        if not role:
            role = await guild.create_role(
                name=name,
                permissions=perms,
                mentionable=True,
                hoist=True
            )
        created_roles[name] = role
        print(f"Rol creado o existente: {name}")

    categories = {
        "01_Estrategia": ["📢_anuncios", "📊_board-reports", "🎯_okrs"],
        "02_Operaciones": ["🗓_turnos", "✅_calidad-qa", "📈_kpis", "📖_playbooks", "👥_supervisores", "🎯_closer"],
        "03_Personal": ["📄_contratos", "👋_onboarding", "🌱_cultura", "📌_plan-carrera"],
        "04_Mercado_y_Leads": ["📣_marketplace", "🗑_descartados", "⭐_limpios", "🔥_leads-hot"],
        "05_Tecnologia": ["🤖_ai-models", "📐_crm-flujos", "🔒_seguridad"],
        "06_Finanzas": ["💵_pagos", "📊_proyecciones", "📑_reportes"],
        "07_Legal_Compliance": ["🛡_privacidad", "📃_políticas"],
        "Generales": ["👋_bienvenida", "💬_chat-general", "🙋‍♂️_soporte"]
    }

    for cat_name, chans in categories.items():
        category = discord.utils.get(guild.categories, name=cat_name)
        if not category:
            category = await guild.create_category(cat_name)
        for chan in chans:
            existing = discord.utils.get(guild.text_channels, name=chan.lower())
            if not existing:
                await guild.create_text_channel(chan, category=category)
        print(f"Categoría creada o existente: {cat_name}")

    role_agents = discord.utils.get(guild.roles, name="Agents 🎧")
    if role_agents:
        for member in guild.members:
            if role_agents not in member.roles and not member.bot:
                await member.add_roles(role_agents)
                print(f"✅ Rol 'Agents 🎧' asignado a {member.name}")

@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name="👋_bienvenida")
    
    if channel:
        await channel.send(
            f"👋 Bienvenido {member.mention} al servidor **Ninja Agents AI** 🎉\n"
            "Revisa los canales y asigna tu rol correspondiente para empezar."
        )

    role = discord.utils.get(guild.roles, name="Agents 🎧")
    if role:
        await member.add_roles(role)
        print(f"✅ Rol 'Agents 🎧' asignado a {member.name}")

bot.run(TOKEN)
