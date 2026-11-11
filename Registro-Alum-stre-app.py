from datetime import datetime
import json
import os
import streamlit as st

ARCHIVO_DATOS = "academia_ritmo_sabor.json"

class AcademiaBaile:
    def __init__(self):
        self.datos = self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists(ARCHIVO_DATOS):
            try:
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                    contenido = json.load(f)
                    if isinstance(contenido, dict) and "alumnos" in contenido:
                        return contenido
            except json.JSONDecodeError:
                pass
        return {"alumnos": [], "asistencias": []}

    def guardar_datos(self):
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, indent=4, ensure_ascii=False)

def main():
    st.set_page_config(page_title="Academia Ritmo y Sabor", page_icon="💃", layout="wide")
    
    academia = AcademiaBaile()
    
    # Menú lateral para navegar entre las opciones
    st.sidebar.title("🎶 Ritmo y Sabor Ecuador")
    menu = st.sidebar.radio(
        "Menú Principal", 
        [
            "Registrar nuevo alumno", 
            "Ver lista de alumnos", 
            "Registrar asistencia diaria", 
            "Calcular costos / mensualidad", 
            "Ver reporte por mes"
        ]
    )
    
    if menu == "Registrar nuevo alumno":
        st.header("💃 Registro de Nuevo Alumno")
        
        with st.form("form_registro"):
            cedula = st.text_input("Cédula / ID (solo números, mín. 7 dígitos):").strip()
            nombre = st.text_input("Nombre completo:").strip()
            fecha_nac = st.text_input("Fecha de nacimiento [Formato: YYYY-MM-DD]:", value="2000-05-12").strip()
            telefono = st.text_input("Teléfono principal (solo números, mín. 7 dígitos):").strip()
            correo = st.text_input("Correo electrónico:").strip()
            
            st.subheader("🚨 Ficha Médica y Emergencia")
            tel_emergencia = st.text_input("Teléfono de contacto de emergencia:").strip()
            ficha_medica = st.text_input("Alergias o condiciones físicas (Si no tiene, escriba 'Ninguna'):", value="Ninguna").strip()
            
            st.subheader("📚 Selección Académica")
            estilo = st.selectbox("Estilo de baile:", ["Salsa On1", "Salsa On2", "Salsa Caleña", "Bachata Sensual", "Bachata Tradicional", "Merengue", "Urbano"])
            nivel = st.selectbox("Nivel:", ["Principiante", "Intermedio", "Avanzado"])
            horario = st.selectbox("Horario:", ["Mañanas (10:00 AM - 12:00 PM)", "Tardes (04:00 PM - 05:00 PM)", "Tardes (06:00 PM - 07:00 PM)", "Noches (08:00 PM - 09:00 PM)"])
            dias = st.selectbox("Días de clase:", ["Lunes y Miércoles", "Martes y Jueves", "Viernes"])
            
            submitted = st.form_submit_button("Guardar Alumno")
            
            if submitted:
                # Validaciones conservando tu lógica original
                errores = []
                if not cedula.isdigit() or len(cedula) < 7:
                    errores.append("La cédula debe contener únicamente números y tener al menos 7 dígitos.")
                elif any(a["cedula"] == cedula for a in academia.datos["alumnos"]):
                    errores.append("Ya existe un alumno registrado con esa cédula.")
                
                if not nombre or not all(c.isalpha() or c.isspace() for c in nombre):
                    errores.append("El nombre solo debe contener letras y espacios.")
                
                try:
                    datetime.strptime(fecha_nac, "%Y-%m-%d")
                except ValueError:
                    errores.append("Formato de fecha incorrecto. Use YYYY-MM-DD.")
                
                if not telefono.isdigit() or len(telefono) < 7:
                    errores.append("El teléfono debe contener solo números válidos (mín. 7 dígitos).")
                
                if "@" not in correo or "." not in correo or len(correo) <= 5:
                    errores.append("Correo electrónico inválido.")
                
                if not tel_emergencia.isdigit() or len(tel_emergencia) < 7:
                    errores.append("El teléfono de emergencia debe contener solo números.")
                
                if not ficha_medica:
                    errores.append("La ficha médica no puede estar vacía.")
                
                if errores:
                    for err in errores:
                        st.error(f"❌ {err}")
                else:
                    nuevo_alumno = {
                        "cedula": cedula, "nombre": nombre, "fecha_nacimiento": fecha_nac,
                        "telefono": telefono, "correo": correo, "emergencia": tel_emergencia,
                        "ficha_medica": ficha_medica, "estilo": estilo, "nivel": nivel,
                        "horario": horario, "dias": dias,
                        "fecha_ingreso": datetime.now().strftime("%Y-%m-%d"),
                        "estado": "Activo"
                    }
                    academia.datos["alumnos"].append(nuevo_alumno)
                    academia.guardar_datos()
                    st.success(f"🎉 ¡Registro exitoso de {nombre} en Ritmo y Sabor Ecuador!")

    elif menu == "Ver lista de alumnos":
        st.header("📂 Lista de Alumnos Inscritos")
        alumnos = academia.datos.get("alumnos", [])
        if not alumnos:
            st.info("No hay alumnos registrados todavía.")
        else:
            st.dataframe(alumnos)

    elif menu == "Registrar asistencia diaria":
        st.header("📝 Registro de Asistencia Diaria")
        alumnos_activos = [a for a in academia.datos.get("alumnos", []) if a.get("estado") == "Activo"]
        if not alumnos_activos:
            st.warning("No hay alumnos activos para registrar asistencia.")
        else:
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            st.write(f"Fecha de hoy: **{fecha_hoy}**")
            
            with st.form("form_asistencia"):
                asistencias_dia = []
                for a in alumnos_activos:
                    asistio = st.checkbox(f"¿Asistió {a.get('nombre')} ({a.get('estilo')})?", value=True)
                    asistencias_dia.append((a, "Presente" if asistio else "Ausente"))
                
                guardar_asist = st.form_submit_button("Guardar Asistencias")
                if guardar_asist:
                    for a, estado_asistencia in asistencias_dia:
                        registro = {
                            "cedula": a.get("cedula"),
                            "nombre": a.get("nombre"),
                            "fecha": fecha_hoy,
                            "estado": estado_asistencia
                        }
                        academia.datos["asistencias"].append(registro)
                    academia.guardar_datos()
                    st.success("✅ Asistencias registradas y guardadas correctamente.")

    elif menu == "Calcular costos / mensualidad":
        st.header("💰 Cálculo de Costos / Mensualidades")
        num_personas = st.number_input("Número de personas a inscribir juntas:", min_value=1, max_value=10, value=1, step=1)
        
        if num_personas == 1:
            total = 45
        elif num_personas == 2:
            total = 80
        else:
            total = 100
            
        st.info(f"💵 El valor total a pagar por **{num_personas}** persona(s) es: **${total} USD**.")

    elif menu == "Ver reporte por mes":
        st.header("📊 Reporte de Inscripciones por Mes")
        alumnos = academia.datos.get("alumnos", [])
        if not alumnos:
            st.info("No hay alumnos registrados para generar el reporte.")
        else:
            conteo_meses = {}
            for a in alumnos:
                fecha_ingreso = a.get("fecha_ingreso", "")
                if len(fecha_ingreso) >= 7:
                    mes_anio = fecha_ingreso[:7]
                    conteo_meses[mes_anio] = conteo_meses.get(mes_anio, 0) + 1
            
            for mes, cantidad in sorted(conteo_meses.items()):
                st.metric(label=f"Mes: {mes}", value=f"{cantidad} alumno(s) nuevo(s)")

if __name__ == "__main__":
    main()