import streamlit as st
from werkzeug.security import generate_password_hash, check_password_hash
from supabase import Client

#* Verificar autenticación
if not st.session_state.get("authenticated", False):
    st.warning("Debes iniciar sesión para acceder a esta página") #* Relampago
    st.switch_page("pages/login.py")

#* de la session obtengo id y client supabase, para hacer select del usuario sesionante.
user_id = st.session_state.user_id
supabase: Client = st.session_state.supabase

#* Obtener datos del usuario
response = supabase.table("usuarios").select("*").eq("id", user_id).execute()
usuario = response.data[0] if response.data else None #* Ternario, None o usuario

#!None, debe exitir por la sesion lo reocnoce, pero: errores de red, servirdor (try/except)
if not usuario: 
    st.error("No se encontraron datos del usuario")
    st.stop()

#************************************ ok tenemos al usuario, pintamos la page! 
st.title("✏️ Mi perfil")

#* Pestañas para ver y editar: tabs() → <a/>
tab1, tab2, tab3 = st.tabs(["Ver perfil", "Editar datos", "Eliminar cuenta"])

with tab1: #* nos quedamos en el MISMO CONTEXTO with
    st.subheader("Información actual")
    st.write(f"**Nombre:** {usuario['nombre']}")
    st.write(f"**Correo:** {usuario['correo']}")
    st.write(f"**Edad:** {usuario['edad']} años")

with tab2:
    st.subheader("Editar perfil")
    
    with st.form("editar_form"):  #* OTRO CONTEXTO with para el form de editar
        nombre = st.text_input("Nombre", value=usuario["nombre"])
        correo = st.text_input("Correo", value=usuario["correo"])
        edad = st.number_input("Edad", min_value=0, max_value=120, value=usuario["edad"])
        nueva_contrasena = st.text_input("Nueva contraseña (opcional)", type="password")
        confirmar = st.text_input("Confirmar nueva contraseña", type="password")
        
        submitted = st.form_submit_button("Actualizar")
        
        if submitted:
            if not nombre or not correo:
                st.error("Nombre y correo son obligatorios")
            elif nueva_contrasena and nueva_contrasena != confirmar:
                st.error("Las contraseñas no coinciden")
            elif nueva_contrasena and len(nueva_contrasena) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres")
            else:
                datos_actualizados = {
                    "nombre": nombre,
                    "correo": correo,
                    "edad": edad
                }
                if nueva_contrasena:
                    datos_actualizados["contrasena_hash"] = generate_password_hash(nueva_contrasena)
                
                supabase.table("usuarios").update(datos_actualizados).eq("id", user_id).execute()
                
                #* Actualizar session_state
                st.session_state.user_nombre = nombre
                st.session_state.user_email = correo
                st.session_state.user_edad = edad
                
                st.success("✅ Perfil actualizado correctamente")
                st.rerun()

with tab3:
    st.subheader("⚠️ Zona peligrosa")
    st.warning("Esta acción es irreversible. Se eliminarán todos tus datos.")
    
    with st.form("eliminar_form"): #* OTRO CONTEXTO with para el fomr de DELETE del regustro
        confirmacion = st.text_input("Escribe tu correo para confirmar eliminación:")
        submitted_del = st.form_submit_button("Eliminar cuenta permanentemente")
        
        if submitted_del:
            if confirmacion == st.session_state.user_email:
                # Eliminar de la base de datos
                supabase.table("usuarios").delete().eq("id", user_id).execute()
                # Limpiar sesión
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_email = None
                st.session_state.user_nombre = None
                st.session_state.user_edad = None
                
                st.success("Cuenta eliminada. Serás redirigido al registro.")
                st.switch_page("pages/registro.py")
            else:
                st.error("El correo no coincide. No se eliminó la cuenta.")