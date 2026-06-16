#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from servicios.sistema import SistemaEntrevistas

# Inicializamos la aplicación Flask y el motor central de POO
app = Flask(__name__)
sistema = SistemaEntrevistas()

# ============================================================================
# 1. RUTAS DE NAVEGACIÓN (Renderizado de Vistas HTML)
# ============================================================================

@app.route('/')
def index():
    """Ruta raíz que renderiza el panel principal o Dashboard."""
    return render_template('index.html')

@app.route('/candidatos')
def vista_candidatos():
    """Muestra la lista de candidatos registrados."""
    return render_template('candidato.html')

@app.route('/candidatos/nuevo')
def vista_nuevo_candidato():
    """Muestra el formulario para crear un nuevo candidato."""
    return render_template('candidato_nuevo.html')

@app.route('/busquedas')
def vista_busquedas():
    """Muestra el listado de vacantes y búsquedas laborales."""
    return render_template('busquedas.html')

@app.route('/busquedas/nueva')
def vista_nueva_busqueda():
    """Muestra el formulario para abrir una nueva búsqueda."""
    return render_template('busqueda_nueva.html')

@app.route('/evaluaciones')
def vista_evaluaciones():
    """Muestra el panel de evaluaciones y calificaciones."""
    return render_template('evaluaciones.html')

@app.route('/turnos')
def vista_turnos():
    """Muestra la agenda y el calendario de entrevistas."""
    return render_template('turnos.html')



# 2. ENDPOINTS DE LA API REST (Control de Datos JSON)


# --- CONTROLADOR DE CANDIDATOS ---
@app.route('/api/candidatos', methods=['GET', 'POST'])
def api_candidatos():
    # CASO GET: El frontend solicita la lista de todos los candidatos
    if request.method == 'GET':
        lista_candidatos = []
        for candidato in sistema._candidatos.values():
            # Extraemos los atributos internos del objeto de POO
            lista_candidatos.append(candidato.__dict__)
        return jsonify(lista_candidatos), 200
    
    # CASO POST: El frontend envía datos para dar de alta un candidato
    elif request.method == 'POST':
        datos = request.get_json() or {}
        try:
            # Invoca las validaciones encapsuladas en tu capa de servicios/modelos
            nuevo_candidato = sistema.registrar_candidato(
                nombre=datos.get('nombre'),
                email=datos.get('email'),
                telefono=datos.get('telefono'),
                anos_experiencia=int(datos.get('anos_experiencia', 0)),
                cv=datos.get('cv', '')
            )
            
            # Si el JSON trae una lista de habilidades, las inyectamos en el objeto
            if nuevo_candidato and 'habilidades' in datos:
                nuevo_candidato.agregar_multiples_habilidades(datos['habilidades'])
                
            return jsonify({
                "status": "success", 
                "id": nuevo_candidato.id if nuevo_candidato else None
            }), 201
            
        except Exception as e:
            # Si una validación de negocio falla (ej. Email inválido), captura el error
            return jsonify({"status": "error", "message": str(e)}), 400


# --- CONTROLADOR DE BÚSQUEDA ---
@app.route('/api/busquedas', methods=['GET', 'POST'])
def api_busquedas():
    if request.method == 'GET':
        lista_busquedas = []
        for busqueda in sistema._busquedas.values():
            lista_busquedas.append(busqueda.__dict__)
        return jsonify(lista_busquedas), 200
    
    elif request.method == 'POST':
        datos = request.get_json() or {}
        try:
            nueva_busqueda = sistema.crear_busqueda(
                titulo_puesto=datos.get('titulo_puesto'),
                descripcion=datos.get('descripcion'),
                salario_minimo=float(datos.get('salario_minimo', 0)),
                salario_maximo=float(datos.get('salario_maximo', 0)),
                skills_requeridos=datos.get('skills_requeridos', []),
                experiencia_minima=int(datos.get('experiencia_minima', 0))
            )
            return jsonify({
                "status": "success", 
                "id": nueva_busqueda.id if nueva_busqueda else None
            }), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400


# CONTROLADOR DE EVALUACIONES 
@app.route('/api/evaluaciones', methods=['GET', 'POST'])
def api_evaluaciones():
    if request.method == 'GET':
        lista_evaluaciones = []
        for e in sistema._evaluaciones.values():

            # En vez de mandar el objeto Candidato entero, extraemos texto/ID primitivos.
            lista_evaluaciones.append({
                "id": e.id,
                "candidato_id": e.candidato.id,
                "candidato_nombre": e.candidato.nombre,
                "busqueda_id": e.busqueda.id,
                "busqueda_titulo": e.busqueda.titulo_puesto,
                "evaluador": e.evaluador,
                "resultado": e.resultado.value,  # .value extrae el str limpio del Enum
                "puntuacion": e.puntuacion,
                "comentarios": e.comentarios
            })
        return jsonify(lista_evaluaciones), 200
    
    elif request.method == 'POST':
        datos = request.get_json() or {}
        try:
            nueva_eval = sistema.evaluar_candidato(
                candidato_id=int(datos.get('candidato_id')),
                busqueda_id=int(datos.get('busqueda_id')),
                evaluador=datos.get('evaluador'),
                resultado=datos.get('resultado'),
                puntuacion=float(datos.get('puntuacion', 0)),
                comentarios=datos.get('comentarios', '')
            )
            return jsonify({
                "status": "success", 
                "id": nueva_eval.id if nueva_eval else None
            }), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400


# CONTROLADOR DE TURNOS 
@app.route('/api/turnos', methods=['GET', 'POST'])
def api_turnos():
    if request.method == 'GET':
        lista_turnos = []
        # Buscamos en el diccionario interno del objeto Calendario
        for t in sistema._calendario._turnos.values():
            lista_turnos.append({
                "id": t.id,
                "evaluacion_id": t.evaluacion.id,
                "candidato_nombre": t.evaluacion.candidato.nombre,
                "puesto": t.evaluacion.busqueda.titulo_puesto,
                "fecha": str(t.fecha),  
                "hora": t.hora,
                "entrevistador": t.entrevistador,
                "sala": t.sala,
                "estado": t.estado.value  
            })
        return jsonify(lista_turnos), 200
    
    elif request.method == 'POST':
        datos = request.get_json() or {}
        try:
            nuevo_turno = sistema.agendar_turno(
                evaluacion_id=int(datos.get('evaluacion_id')),
                fecha_str=datos.get('fecha'),
                hora=datos.get('hora'),
                entrevistador=datos.get('entrevistador'),
                sala=datos.get('sala')
            )
            return jsonify({
                "status": "success", 
                "id": nuevo_turno.id if nuevo_turno else None
            }), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400




if __name__ == '__main__':
    
    app.run(debug=True, port=5000)