import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# === Intents correctos ===
intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # Necesario para detectar miembros nuevos y asignar roles

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    guild = bot.guilds[0]  # Primer servidor donde está el bot
    print(f"Configurando servidor: {guild.name}")

    # === CREACIÓN DE ROLES ===
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
                mentionable=True,  # Se puede mencionar con @
                hoist=True         # Aparece separado en la lista de miembros
            )
        created_roles[name] = role
        print(f"Rol creado o existente: {name}")

    # === CREACIÓN DE CATEGORÍAS Y CANALES ===
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

    print("✅ Configuración del servidor terminada")

    # === ASIGNAR ROL "Agents 🎧" A TODOS LOS MIEMBROS EXISTENTES ===
    role_agents = discord.utils.get(guild.roles, name="Agents 🎧")
    if role_agents:
        for member in guild.members:
            if role_agents not in member.roles and not member.bot:  # evitar bots
                await member.add_roles(role_agents)
                print(f"✅ Rol 'Agents 🎧' asignado a {member.name}")

# === BIENVENIDA AUTOMÁTICA Y ROL POR DEFECTO ===
@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name="👋_bienvenida")
    
    if channel:
        await channel.send(
            f"👋 Bienvenido {member.mention} al servidor **Ninja Agents AI** 🎉\n"
            "Revisa los canales y asigna tu rol correspondiente para empezar."
        )

    # Asignar rol por defecto "Agents 🎧"
    role = discord.utils.get(guild.roles, name="Agents 🎧")
    if role:
        await member.add_roles(role)
        print(f"✅ Rol 'Agents 🎧' asignado a {member.name}")

bot.run(TOKEN)
