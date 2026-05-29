import streamlit as st
from werkzeug.security import check_password_hash
from supabase import Client

#* Redirigir al home/ si ya está logueado
if st.session_state.get("authenticated", False): #? authenticated == True → login exitoso.
    st.switch_page("pages/home.py")              #TODO: Hay q crear la page.

st.title("🔑 Inicio de sesión")

with st.form("login_form"):
    #* inputs de login + btn
    correo = st.text_input("Correo electrónico")
    contrasena = st.text_input("Contraseña", type="password")
    submitted = st.form_submit_button("Iniciar sesión")

    #* Clic sobre btn de envio
    if submitted:
        if not correo or not contrasena:                 #! campos vacios
            st.error("Completa todos los campos")
        else:                                            #* Campos llenos
            supabase: Client = st.session_state.supabase    #* llamemos a supa para comprobacion
                                                            #* Buscar usuario por correo
            response = supabase.table("usuarios").select("*").eq("correo", correo).execute()
            
            if response.data:                               #* Si devueve algo, existe el registro con ese correo
                # TODO-TAREA: contorla responde.error → con try-except, que excepts pueden ocurrir??
                usuario = response.data[0]                  #* Desestructuramos el registro
                #* 🔏🔏🔏Verificar contraseña usando werkzeug
                if check_password_hash(usuario["contrasena_hash"], contrasena):
                    #* Guardar sesión del suusario sesionante que navega por las pages (PERSISTENCIA)
                    st.session_state.authenticated = True #&💡✅Aquii es donde setteamos
                    st.session_state.user_id = usuario["id"]
                    st.session_state.user_email = usuario["correo"]
                    st.session_state.user_nombre = usuario["nombre"]
                    st.session_state.user_edad = usuario["edad"]
                    st.success("✅ ¡Sesión iniciada correctamente!")
                    st.rerun()  #* Recargar para aplicar la redirección a home/ de arriba
                    #? st.rerun() 
                    # Vuelve a ejecutar el script desde cero, manteniendo los valores de st.session_state.
                    # Flujo:
                    # El usuario inicia sesión correctamente.
                    # Se establece st.session_state.authenticated = True.
                    # Se ejecuta st.rerun() → el script se ejecuta de nuevo.
                    # Al iniciar la nueva ejecución, la primera línea del script es:
                    # st.session_state.authenticated == True → st.switch_page("pages/home.py")
                else: #! no hay match de credenciales, lo informamos
                    st.error("❌ Contraseña incorrecta")
            else: #! No se tuvo → response.data, no existe ese correo, se sugiere registro
                st.error("❌ Usuario no encontrado. ¿Necesitas registrarte?")

#* Enlace para ir al registro
st.markdown("---")
if st.button("¿No tienes cuenta? Regístrate aquí"):
    st.switch_page("pages/registro.py") #* navegacion a registro