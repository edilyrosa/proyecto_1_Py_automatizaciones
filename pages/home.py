import streamlit as st

#* 🔏 Verificar autenticación
if not st.session_state.get("authenticated", False):
    st.warning("Debes iniciar sesión para acceder a esta página") #* de pestaneo por la sig redireccion
    st.switch_page("pages/login.py")

st.title("🏠 Bienvenido")

#* Mostrar información del usuario, de las var session
nombre = st.session_state.get("user_nombre", "Usuario")
st.markdown(f"### Hola, **{nombre}** 👋")

st.markdown("""
Esta es tu página principal. Desde aquí puedes:
- ✏️ **Actualizar tu perfil**
- 🗑️ **Eliminar tu cuenta**
- 🚪 **Cerrar sesión**

Usa el menú de la izquierda o los botones de abajo.
""")

#* 2 columnas una para cada btn: btn CRUD y Btn Cerrar sesion
col1, col2 = st.columns(2)
with col1: #* btn CRUD
    if st.button("✏️ Ver/Editar perfil"):
        st.switch_page("pages/perfil.py") #TODO: Hay de crearla
with col2: #* Btn Cerrar sesion
    if st.button("🚪 Cerrar sesión"): 
        #* Resetteamos las var session del login.
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user_email = None
        st.session_state.user_nombre = None
        st.session_state.user_edad = None
        st.rerun() #* al recaragar →  st.switch_page("pages/login.py")