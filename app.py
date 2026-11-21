
import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Acompaña",
    page_icon="🏡",
    layout="wide"
)

# DISEÑO VISUAL

st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FB;
    }

    h1, h2, h3 {
        color: #243B53;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E1E8F0;
    }

    div.stButton > button {
        border-radius: 10px;
        border: none;
        padding: 10px 18px;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] {
        background-color: #EAF2FB;
    }

    .notificacion {
        background-color: white;
        border: 1px solid #E1E8F0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


# BASE DE DATOS SQLITE

def crear_base_datos():
    conexion = sqlite3.connect("acompanha.db")

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_hora TEXT NOT NULL
        )
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS adulto_mayor (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            edad INTEGER,
            telefono TEXT
        )
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS familiares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            parentesco TEXT,
            telefono TEXT NOT NULL
        )
    """)

    # AGREGAR ESTADO DE ATENCION A EVENTOS EXISTENTES

    columnas = conexion.execute(
        "PRAGMA table_info(eventos)"
    ).fetchall()

    nombres_columnas = [columna[1] for columna in columnas]

    if "atendida" not in nombres_columnas:
        conexion.execute("""
            ALTER TABLE eventos
            ADD COLUMN atendida INTEGER NOT NULL DEFAULT 0
        """)

    conexion.commit()
    conexion.close()


def registrar_evento(tipo, descripcion):
    conexion = sqlite3.connect("acompanha.db")

    conexion.execute(
        """
        INSERT INTO eventos (tipo, descripcion, fecha_hora)
        VALUES (?, ?, ?)
        """,
        (tipo, descripcion, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conexion.commit()
    conexion.close()


def obtener_eventos():
    conexion = sqlite3.connect("acompanha.db")

    eventos = conexion.execute(
        """
        SELECT id, tipo, descripcion, fecha_hora, atendida
        FROM eventos
        ORDER BY id DESC
        """
    ).fetchall()

    conexion.close()

    return eventos


# FUNCION PARA ACTUALIZAR NOTIFICACIONES

def actualizar_notificacion(evento_id, estado):
    conexion = sqlite3.connect("acompanha.db")

    conexion.execute(
        "UPDATE eventos SET atendida = ? WHERE id = ?",
        (estado, evento_id)
    )

    conexion.commit()
    conexion.close()


# FUNCIONES DEL PERFIL

def guardar_perfil(nombre, edad, telefono):
    conexion = sqlite3.connect("acompanha.db")

    conexion.execute("""
        INSERT OR REPLACE INTO adulto_mayor
        (id, nombre, edad, telefono)
        VALUES (1, ?, ?, ?)
    """, (nombre, edad, telefono))

    conexion.commit()
    conexion.close()


def obtener_perfil():
    conexion = sqlite3.connect("acompanha.db")

    perfil = conexion.execute(
        "SELECT nombre, edad, telefono FROM adulto_mayor WHERE id = 1"
    ).fetchone()

    conexion.close()

    return perfil


# FUNCIONES DE FAMILIARES

def guardar_familiar(nombre, parentesco, telefono):
    conexion = sqlite3.connect("acompanha.db")

    conexion.execute("""
        INSERT INTO familiares (nombre, parentesco, telefono)
        VALUES (?, ?, ?)
    """, (nombre, parentesco, telefono))

    conexion.commit()
    conexion.close()


def obtener_familiares():
    conexion = sqlite3.connect("acompanha.db")

    familiares = conexion.execute(
        "SELECT id, nombre, parentesco, telefono FROM familiares"
    ).fetchall()

    conexion.close()

    return familiares


crear_base_datos()


# ESTADOS INICIALES

if "movimiento" not in st.session_state:
    st.session_state.movimiento = True

if "puerta" not in st.session_state:
    st.session_state.puerta = False

if "alerta" not in st.session_state:
    st.session_state.alerta = False

if "ayuda" not in st.session_state:
    st.session_state.ayuda = False

if "confirmacion" not in st.session_state:
    st.session_state.confirmacion = False


# MENU LATERAL

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

with st.sidebar:

    st.title("🏡 Acompaña")
    st.caption("Asistencia inteligente")

    st.divider()

    st.subheader("Navegación")

    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.pagina = "Inicio"

    if st.button("📡 Monitoreo", use_container_width=True):
        st.session_state.pagina = "Monitoreo"

    if st.button("🚨 Alertas", use_container_width=True):
        st.session_state.pagina = "Alertas"

    if st.button("📋 Historial", use_container_width=True):
        st.session_state.pagina = "Historial"

    if st.button("👤 Perfil", use_container_width=True):
        st.session_state.pagina = "Perfil"

    if st.button("👨‍👩‍👧 Familiares", use_container_width=True):
        st.session_state.pagina = "Familiares"

    if st.button("🔔 Notificaciones", use_container_width=True):
        st.session_state.pagina = "Notificaciones"

    st.divider()

    st.success("Sistema activo")
    st.caption("Versión 1.1")


# NAVEGACIÓN DE PÁGINAS

if st.session_state.pagina == "Inicio":

    st.title("🏡 Bienvenido a Acompaña")
    st.write("Sistema inteligente de asistencia para adultos mayores")
    st.divider()

elif st.session_state.pagina == "Monitoreo":

    st.title("📡 Monitoreo")
    st.write("Supervisión de sensores y dispositivos")
    st.divider()

elif st.session_state.pagina == "Alertas":

    st.title("🚨 Centro de alertas")
    st.write("Supervisión de solicitudes y posibles emergencias")
    st.divider()

elif st.session_state.pagina == "Historial":

    st.title("📋 Historial de actividad")
    st.write("Registro de eventos del sistema")
    st.divider()

elif st.session_state.pagina == "Perfil":

    st.title("👤 Perfil del adulto mayor")
    st.write("Información de la persona que utiliza Acompaña.")
    st.divider()

elif st.session_state.pagina == "Familiares":

    st.title("👨‍👩‍👧 Familiares autorizados")
    st.write("Personas que podrán recibir avisos de Acompaña.")
    st.divider()

elif st.session_state.pagina == "Notificaciones":

    st.title("🔔 Centro de notificaciones")
    st.write("Administración de avisos y seguimiento de emergencias.")
    st.divider()


# PAGINA DE INICIO

if st.session_state.pagina == "Inicio":

    st.subheader("Resumen general")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Estado del sistema", "Activo")

    with col2:
        st.metric(
            "Movimiento",
            "Detectado" if st.session_state.movimiento else "Sin movimiento"
        )

    with col3:
        st.metric("Conexión", "En línea")

    st.divider()

    st.subheader("Bienvenido a Acompaña")
    st.write(
        "Desde aquí puedes supervisar el estado general "
        "del sistema de asistencia."
    )


# PAGINA DE MONITOREO

elif st.session_state.pagina == "Monitoreo":

    st.subheader("📡 Control de sensores")

    col1, col2 = st.columns(2)

    with col1:

        st.write("🚶 **Sensor de movimiento**")

        if st.button("Cambiar movimiento"):

            st.session_state.movimiento = not st.session_state.movimiento

            estado = (
                "Movimiento detectado"
                if st.session_state.movimiento
                else "Sin movimiento detectado"
            )

            registrar_evento("Movimiento", estado)
            st.rerun()

        st.write("🚪 **Sensor de puerta**")

        if st.button("Abrir / cerrar puerta"):

            st.session_state.puerta = not st.session_state.puerta

            estado = (
                "Puerta abierta"
                if st.session_state.puerta
                else "Puerta cerrada"
            )

            registrar_evento("Puerta", estado)
            st.rerun()

    with col2:

        st.write("⌚ **Pulsera inteligente**")
        st.success("Pulsera conectada")

        if st.button("⚠️ Simular posible caída"):

            st.session_state.alerta = True
            st.session_state.ayuda = False
            st.session_state.confirmacion = False

            registrar_evento("Alerta", "Posible caída detectada")
            st.rerun()

        st.write("🆘 **Botón de ayuda**")

        if st.button("Solicitar ayuda"):

            st.session_state.ayuda = True
            st.session_state.alerta = False

            registrar_evento("Ayuda", "Solicitud de ayuda activada")
            st.rerun()

    st.divider()

    st.subheader("Estado actual de los sensores")

    col1, col2 = st.columns(2)

    with col1:

        if st.session_state.movimiento:
            st.success("🚶 Movimiento detectado")
        else:
            st.warning("Sin movimiento detectado")

    with col2:

        if st.session_state.puerta:
            st.warning("🚪 Puerta abierta")
        else:
            st.success("🚪 Puerta cerrada")


# PAGINA DE ALERTAS

if st.session_state.pagina == "Alertas":

    st.subheader("🚨 Centro de alertas")

    if st.session_state.alerta:

        st.error("⚠️ Se detectó una posible caída.")

        st.subheader("¿Te encuentras bien?")
        st.write("Por favor, confirma tu estado.")

        col1, col2 = st.columns(2)

        with col1:

            if st.button("✅ Sí, estoy bien"):

                st.session_state.alerta = False
                st.session_state.confirmacion = True

                registrar_evento(
                    "Confirmación",
                    "Adulto mayor confirmó estar bien"
                )

                st.rerun()

        with col2:

            if st.button("🆘 Necesito ayuda"):

                st.session_state.alerta = False
                st.session_state.ayuda = True

                registrar_evento(
                    "Ayuda",
                    "Adulto mayor indicó que necesita ayuda"
                )

                st.rerun()

    if st.session_state.confirmacion:

        st.success("✅ El adulto mayor confirmó que se encuentra bien.")

    if st.session_state.ayuda:

        st.error("🆘 SOLICITUD DE AYUDA ACTIVADA")

        st.write("Se requiere asistencia de un familiar autorizado.")

        if st.button("Cerrar solicitud de ayuda"):

            st.session_state.ayuda = False

            registrar_evento(
                "Cierre",
                "Solicitud de ayuda cerrada"
            )

            st.rerun()

    if (
        not st.session_state.alerta
        and not st.session_state.ayuda
        and not st.session_state.confirmacion
    ):

        st.success("No hay alertas pendientes.")


# PAGINA DE HISTORIAL

if st.session_state.pagina == "Historial":

    st.subheader("📋 Historial de actividad")

    st.write("Registro de todos los eventos del sistema.")

    eventos = obtener_eventos()

    if eventos:

        st.dataframe(
            eventos,
            column_config={
                "0": "ID",
                "1": "Tipo de evento",
                "2": "Descripción",
                "3": "Fecha y hora",
                "4": "Atendida (0 = No, 1 = Sí)"
            },
            hide_index=True,
            use_container_width=True
        )

        st.caption(
            f"Total de eventos registrados: {len(eventos)}"
        )

    else:

        st.info("Todavía no hay eventos registrados.")


# PAGINA DE PERFIL

if st.session_state.pagina == "Perfil":

    st.subheader("👤 Datos del adulto mayor")

    perfil = obtener_perfil()

    nombre_actual = perfil[0] if perfil else ""
    edad_actual = perfil[1] if perfil else 60
    telefono_actual = perfil[2] if perfil else ""

    with st.form("formulario_perfil"):

        nombre = st.text_input(
            "Nombre completo",
            value=nombre_actual
        )

        edad = st.number_input(
            "Edad",
            min_value=1,
            max_value=120,
            value=edad_actual
        )

        telefono = st.text_input(
            "Número de teléfono",
            value=telefono_actual
        )

        guardar = st.form_submit_button("💾 Guardar perfil")

        if guardar:

            if nombre.strip():

                guardar_perfil(nombre, edad, telefono)

                st.success("¡Perfil guardado correctamente!")

            else:

                st.warning("Por favor, escribe el nombre.")

    st.divider()

    perfil = obtener_perfil()

    if perfil:

        st.subheader("📋 Perfil registrado")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("👤 Nombre", perfil[0])

        with col2:
            st.metric("🎂 Edad", f"{perfil[1]} años")

        with col3:
            st.metric("📞 Teléfono", perfil[2] or "No registrado")

        st.success("✅ Perfil registrado correctamente")


# PAGINA DE FAMILIARES

if st.session_state.pagina == "Familiares":

    st.subheader("👨‍👩‍👧 Registrar familiar autorizado")

    with st.form("formulario_familiar"):

        nombre_familiar = st.text_input("Nombre completo")

        parentesco = st.selectbox(
            "Parentesco",
            ["Hijo/a", "Esposo/a", "Hermano/a", "Nieto/a", "Otro"]
        )

        telefono_familiar = st.text_input("Número de teléfono")

        guardar_familiar_btn = st.form_submit_button(
            "💾 Registrar familiar"
        )

        if guardar_familiar_btn:

            if nombre_familiar.strip() and telefono_familiar.strip():

                guardar_familiar(
                    nombre_familiar,
                    parentesco,
                    telefono_familiar
                )

                st.success("¡Familiar registrado correctamente!")

            else:

                st.warning("Completa el nombre y el teléfono.")

    st.divider()

    st.subheader("📋 Familiares registrados")

    familiares = obtener_familiares()

    if familiares:

        for familiar in familiares:

            with st.container(border=True):

                st.write(f"👤 **{familiar[1]}**")
                st.write(f"Parentesco: {familiar[2]}")
                st.write(f"📞 Teléfono: {familiar[3]}")

    else:

        st.info("Todavía no hay familiares registrados.")


# PAGINA DE NOTIFICACIONES

if st.session_state.pagina == "Notificaciones":

    st.subheader("🔔 Centro de notificaciones")

    st.write(
        "Consulta las alertas generadas por el sistema "
        "y administra su estado de atención."
    )

    familiares = obtener_familiares()
    eventos = obtener_eventos()

    # FILTRAR EVENTOS QUE GENERAN NOTIFICACIONES

    notificaciones = [
        evento for evento in eventos
        if evento[1] in ["Alerta", "Ayuda"]
    ]

    pendientes = [
        evento for evento in notificaciones
        if evento[4] == 0
    ]

    atendidas = [
        evento for evento in notificaciones
        if evento[4] == 1
    ]

    # RESUMEN DE NOTIFICACIONES

    st.markdown("### 📊 Resumen de notificaciones")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total de avisos",
            len(notificaciones)
        )

    with col2:
        st.metric(
            "🔴 Pendientes",
            len(pendientes)
        )

    with col3:
        st.metric(
            "🟢 Atendidas",
            len(atendidas)
        )

    st.divider()

    # INFORMACION DE FAMILIARES

    st.markdown("### 👨‍👩‍👧 Familiares autorizados")

    if familiares:

        st.success(
            f"Hay {len(familiares)} familiar(es) registrado(s) "
            "para recibir avisos."
        )

    else:

        st.warning(
            "No hay familiares registrados. "
            "Agrega uno desde la sección Familiares."
        )

    st.divider()

    # FILTRO DE NOTIFICACIONES

    st.markdown("### 📩 Bandeja de notificaciones")

    filtro = st.radio(
        "Mostrar:",
        ["Todas", "Pendientes", "Atendidas"],
        horizontal=True
    )

    if filtro == "Pendientes":
        lista_mostrar = pendientes

    elif filtro == "Atendidas":
        lista_mostrar = atendidas

    else:
        lista_mostrar = notificaciones

    if not lista_mostrar:

        if filtro == "Pendientes":
            st.success("🎉 ¡Excelente! No hay avisos pendientes.")

        elif filtro == "Atendidas":
            st.info("Todavía no hay notificaciones atendidas.")

        else:
            st.info("Todavía no se han generado notificaciones.")

    else:

        for evento in lista_mostrar:

            evento_id = evento[0]
            tipo = evento[1]
            descripcion = evento[2]
            fecha = evento[3]
            estado = evento[4]

            # TIPO DE NOTIFICACION

            if tipo == "Alerta":
                titulo = "⚠️ Posible caída"
                color_estado = "error"

            else:
                titulo = "🆘 Solicitud de ayuda"
                color_estado = "warning"

            st.markdown(
                f"### {titulo}"
            )

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.write(f"**Evento:** {descripcion}")

                    st.write(f"📅 **Fecha y hora:** {fecha}")

                    st.write(f"🆔 **Número de aviso:** {evento_id}")

                with col2:

                    if estado == 0:
                        st.error("🔴 Pendiente")
                    else:
                        st.success("🟢 Atendida")

                st.divider()

                st.write("**👨‍👩‍👧 Destinatarios del aviso:**")

                if familiares:

                    for familiar in familiares:

                        st.write(
                            f"👤 {familiar[1]} "
                            f"({familiar[2]}) — 📞 {familiar[3]}"
                        )

                else:

                    st.caption(
                        "No hay familiares registrados como destinatarios."
                    )

                st.divider()

                # BOTONES PARA CAMBIAR EL ESTADO

                if estado == 0:

                    if st.button(
                        "✅ Marcar como atendida",
                        key=f"atender_{evento_id}",
                        use_container_width=True
                    ):

                        actualizar_notificacion(evento_id, 1)
                        st.rerun()

                else:

                    if st.button(
                        "↩️ Reabrir notificación",
                        key=f"reabrir_{evento_id}",
                        use_container_width=True
                    ):

                        actualizar_notificacion(evento_id, 0)
                        st.rerun()

                st.caption(
                    "Aviso generado localmente. "
                    "No se ha enviado ningún SMS ni mensaje de WhatsApp real."
                )

            st.write("")

    st.divider()

    st.caption(
        "Acompaña | Centro de notificaciones | Versión 1.1"
    )
