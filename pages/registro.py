import streamlit as st
from werkzeug.security import generate_password_hash
from supabase import Client

if st.session_state.get("authenticated", False):
    st.switch_page("pages/home.py") #TODO: Hay q crearlo. Usuario logeado tendria q deslogearse para entrar en pages/registro

st.title("📝 Registro de usuario")

with st.form("registro_form"):
    #? with 
    # Delimitar un bloque de código que agrupa varios widgets.
    # No se ejecutarán inmediatamente al interactuar con ellos, como ocurre fuera de un formulario.
    # Solo cuando el usuario pulse el botón especial st.form_submit_button() se enviarán todos 
    # los valores de los widgets del formulario a la vez.
    #! Sin with
    # tendrías que asignar cada widget al formulario manualmente, por ejemplo:
        # form = st.form("mi_formulario")
        # nombre = form.text_input("Nombre")
        # edad = form.number_input("Edad")
        # submit = form.form_submit_button("Enviar")

    #* inputs
    #TODO: colocar placeholders, 1er parm es el label sobre la cajota input
    nombre = st.text_input("Nombre completo", placeholder="Ej: Ana Pérez")  
    correo = st.text_input("Correo electrónico", placeholder="ana@ejemplo.com")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    contrasena = st.text_input("Contraseña", type="password", help="Mínimo 6 caracteres")
    confirmar = st.text_input("Confirmar contraseña", type="password") #TODO
    
    #* Creamos el btn de envio de form, y lo guadamos en variable.
    submitted = st.form_submit_button("Registrarse")
    
    #* si clic sobre el btn submit → Verificacion y saneamiento de los datos antes de enviarlos a la BBDD
    if submitted: #* Fue clickeado el btn de envio
        if not nombre or not correo or not contrasena: #! si algun campo esta vacio
            st.error("Todos los campos son obligatorios") #! 👀👀APARECERA SI INTENYO ENVIAR CON ALGUN CAMPO VACIO
        elif len(contrasena) < 6:                      #! contrasena menor a 6 digitos.
            st.error("La contraseña debe tener al menos 6 caracteres")
        elif contrasena != confirmar:                   #! disparidad
            st.error("Las contraseñas no coinciden")
        else:                                           #* ✅Todos los campo tiene data valida
            # 💡obtenemos el cliente que representa tu tabla de la sesion (Potencia de la sesion).
            #  recuerda en app.py (line21): st.session_state.supabase = create_client(supabase_url, supabase_key)
            supabase: Client = st.session_state.supabase 
            existe = supabase.table("usuarios").select("id").eq("correo", correo).execute()
            if existe.data: #! Si traes id de un registro con el mismo correo que intenta registrarse
                st.error("El correo ya está registrado. ¿Quieres iniciar sesión?")
            else: #* ✅ no trae nada, no existe correo en la BBDD, puedo registrarlo (POST, INSERT INTO)
                contrasena_hash = generate_password_hash(contrasena) #🔏 Hash de la contrasena. 
                datos = { #*Creamos dict de los datos.
                    "nombre": nombre,
                    "correo": correo,
                    "edad": edad,
                    "contrasena_hash": contrasena_hash #Guardas en BD este hash 🚩(NUNCA guardar la clave en texto plano)
                }
                supabase.table("usuarios").insert(datos).execute() #* insertamos (POST) el dict data en la BBDD
                st.success("✅ ¡Registro exitoso! Ya puedes iniciar sesión.") #* Bandera de exito.
                # TODO-TAREA: Limpia el formulario
                st.balloons() # Apareceran 🎈
                # Guardamos una variable en session_state para mostrar el botón luego
                st.session_state.registro_exitoso = True

#* ⬇️ Botón fuera del formulario, para login, si lo desea, es necesario para authenticated == True?
if st.session_state.get("registro_exitoso", False): 
# registro_exitoso ahora es True, la condición se cumple y se muestra el botón "Ir a Iniciar Sesión".
    if st.button("Ir a Iniciar Sesión"):
        st.switch_page("pages/login.py")

#? Al iniciar sesión → como se compara el hash guardado en la BBDD y con clave ingresada??
#* if check_password_hash(hash_guardado_en_bd, clave_ingresada):
#*     print("¡Contraseña correcta!")

#? ¿Por qué es seguro? 
# Porque incluso la misma contraseña genera hashes diferentes cada vez  que llamas a 
# generate_password_hash desde cero, (gracias al "salt" incluido), y los algoritmos 
# usados (scrypt por defecto) están diseñados para ser lentos, 
# dificultando ataques por fuerza bruta

#? un "salt" (valor aleatorio) 
# nuevo para cada llamada, y ese salt se guarda dentro del propio hash. 
