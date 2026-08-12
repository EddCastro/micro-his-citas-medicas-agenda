# Micro-HIS Citas médicas y agenda

## Datos generales

- **Estudiante:** Eddy Adolfo Castro Véliz
- **GitHub:** EddCastro
- **Módulo:** Citas médicas y agenda
- **Actividad:** Tarea 3 - Micro Servicios y Monolito
- **Repositorio:** https://github.com/EddCastro/micro-his-citas-medicas-agenda
- **Rama:** `main`

## Objetivo

Implementar un micro-monolito educativo en PHP 8.2+ vanilla para ejecutar el flujo de solicitud, validación de disponibilidad y confirmación o cancelación de una cita médica.

## Flujo principal

1. Registrar una solicitud de cita.
2. Validar los datos requeridos.
3. Verificar la disponibilidad del médico.
4. Registrar la cita cuando el horario se encuentre disponible.
5. Permitir la confirmación de la cita.
6. Permitir la cancelación de la cita.

## Arquitectura requerida

El proyecto se organiza en cuatro capas principales:

- **Presentation:** entrada y salida de información.
- **Application:** coordinación de los casos de uso.
- **Domain:** reglas y objetos del negocio.
- **Persistence:** acceso a datos mediante PDO.

## Requisitos técnicos

- PHP 8.2 o superior.
- PHP vanilla, sin framework.
- PDO con sentencias preparadas.
- Configuración separada del código.
- Datos exclusivamente ficticios.
- Pruebas automatizadas.

## Pruebas mínimas

- Camino feliz.
- Regla de dominio.
- Error de persistencia.

## Estado actual

Proyecto inicializado. La implementación se realizará de forma incremental y cada cambio relevante quedará registrado mediante commits con propósito.
