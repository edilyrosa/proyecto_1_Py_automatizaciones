import streamlit as st
from supabase import create_client, Client

#* Configuración de la página: en la pestana titulo e icono
st.set_page_config(
    page_title="Mi App con Supabase", 
    page_icon="🔐",
    layout="centered"
)

#* --- INICIALIZACIÓN DEL CLIENTE DE SUPABASE ---
#? Verifica si 'supabase' ya existe en el session_state.
    # st.session_state es un diccionario que Streamlit mantiene durante toda la 
    # sesión del navegador (no se pierde al recargar la página).
if "supabase" not in st.session_state:
    try:
        #? Si no existe, intenta leer las claves de los secretos de Streamlit
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
        #? Crea el cliente y lo guarda en el session_state
        st.session_state.supabase = create_client(supabase_url, supabase_key)
        st.success("✅ Conectado a Supabase") # Mensaje de confirmación
        supabase: Client = st.session_state.supabase
        response = supabase.table("usuarios").select("*").execute()
        print(response.data)  # Imprime los datos para verificar la conexión
    except Exception as e:
        st.error(f"Error al conectar con Supabase: {e}")
        st.stop()

#* Contenido de la página principal
st.title("🔐 Bienvenido a la aplicación") #<h1>

st.markdown("""
Esta aplicación permite gestionar usuarios de manera segura:

- Registro de nuevos usuarios (con contraseña cifrada)
- Inicio de sesión
- Visualización y edición del perfil
- Eliminación de cuenta

**Para comenzar, utiliza el menú de la izquierda.**
""")

#* Mostrar estado de autenticación en la barra lateral
# .get("authenticated", False) intenta obtener el valor de la clave "authenticated". 
# Si no existe, devuelve False. Si el usuario está autenticado (True), entra al if.
if st.session_state.get("authenticated", False):
    st.sidebar.success(f"✅ Conectado como: {st.session_state.get('user_email', 'Usuario')}")
    if st.sidebar.button("🚪 Cerrar sesión"):
        for key in ['authenticated', 'user_id', 'user_email', 'user_nombre']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
else:
    st.sidebar.info("🔒 No autenticado") # "authenticated" == False
    
    
    
