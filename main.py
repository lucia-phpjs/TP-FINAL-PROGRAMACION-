#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from servicios.sistema import SistemaEntrevistas

def ejecutar_demo(sistema: SistemaEntrevistas):
    """Ejecuta una demostración completa."""
    print("\n" + "="*60)
    print("EJECUTANDO DEMO COMPLETA")
    print("="*60)
    
    print("\n📝 REGISTRANDO CANDIDATOS...")
    cand1 = sistema.registrar_candidato("Alice Johnson", "alice@email.com", "1111111111", 6, "Senior Developer")
    if cand1: cand1.agregar_multiples_habilidades(["Python", "JavaScript", "SQL", "AWS"])
    
    cand2 = sistema.registrar_candidato("Bob Smith", "bob@email.com", "2222222222", 3, "Full Stack Developer")
    if cand2: cand2.agregar_multiples_habilidades(["Python", "React", "PostgreSQL"])
    
    cand3 = sistema.registrar_candidato("Carol White", "carol@email.com", "3333333333", 8, "Technical Lead")
    if cand3: cand3.agregar_multiples_habilidades(["Python", "JavaScript", "AWS", "Docker", "Kubernetes"])
    
    print("\n🔍 CREANDO BÚSQUEDAS...")
    busq1 = sistema.crear_busqueda("Senior Python Developer", "Buscamos dev senior", 80000, 120000, ["Python", "AWS", "SQL"], 5)
    busq2 = sistema.crear_busqueda("Full Stack Developer", "Dev full stack", 40000, 70000, ["Python", "React", "PostgreSQL"], 2)
    
    print("\n📊 EVALUANDO CANDIDATOS...")
    sistema.evaluar_candidato(cand1.id if cand1 else 1, busq1.id, "Juan Manager", "aprobado", 95, "Excelente perfil")
    sistema.evaluar_candidato(cand2.id if cand2 else 2, busq2.id, "Juan Manager", "aprobado", 88, "Buen candidato")
    sistema.evaluar_candidato(cand3.id if cand3 else 3, busq1.id, "Juan Manager", "aprobado", 98, "Perfecto match")
    
    print("\n📅 AGENDANDO TURNOS...")
    fecha_manana = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
    sistema.agendar_turno(1, fecha_manana, "09:30", "Luis Recruiter", "Sala A")
    sistema.agendar_turno(2, fecha_manana, "10:00", "Luis Recruiter", "Sala B")
    sistema.agendar_turno(3, fecha_manana, "14:00", "Maria HR", "Sala C")
    
    print("\n✅ DEMO COMPLETADA\n")
    sistema.generar_reportes()

def menu_principal():
    """Menú principal de la aplicación."""
    sistema = SistemaEntrevistas()
    
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE TURNOS DE ENTREVISTAS LABORALES")
        print("="*60)
        print("1. Registrar candidato")
        print("2. Crear búsqueda de empleo")
        print("3. Evaluar candidato")
        print("4. Agendar turno")
        print("5. Generar reportes")
        print("6. Ejecutar demo completa")
        print("0. Salir")
        print("="*60)
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            nombre = input("Nombre: ")
            email = input("Email: ")
            telefono = input("Teléfono: ")
            anos = int(input("Años de experiencia: "))
            cv = input("CV/Descripción: ")
            habilidades = input("Habilidades (separadas por coma): ").split(",")
            cand = sistema.registrar_candidato(nombre, email, telefono, anos, cv)
            if cand:
                cand.agregar_multiples_habilidades([h.strip() for h in habilidades])
        
        elif opcion == "2":
            titulo = input("Título del puesto: ")
            desc = input("Descripción: ")
            sal_min = float(input("Salario mínimo: "))
            sal_max = float(input("Salario máximo: "))
            skills = input("Skills requeridos (separados por coma): ").split(",")
            exp_min = int(input("Experiencia mínima (años): "))
            sistema.crear_busqueda(titulo, desc, sal_min, sal_max, [s.strip() for s in skills], exp_min)
        
        elif opcion == "3":
            cand_id = int(input("ID del candidato: "))
            busq_id = int(input("ID de la búsqueda: "))
            evaluador = input("Nombre del evaluador: ")
            resultado = input("Resultado (aprobado/rechazado): ")
            puntuacion = float(input("Puntuación (0-100): "))
            comentarios = input("Comentarios: ")
            sistema.evaluar_candidato(cand_id, busq_id, evaluador, resultado, puntuacion, comentarios)
        
        elif opcion == "4":
            eval_id = int(input("ID de evaluación: "))
            fecha = input("Fecha (YYYY-MM-DD): ")
            hora = input("Hora (HH:MM): ")
            entrevistador = input("Nombre del entrevistador: ")
            sala = input("Sala: ")
            sistema.agendar_turno(eval_id, fecha, hora, entrevistador, sala)
        
        elif opcion == "5":
            sistema.generar_reportes()
        
        elif opcion == "6":
            ejecutar_demo(sistema)
        
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    menu_principal()