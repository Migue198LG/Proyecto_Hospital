# Proyecto Hospital: Sistema de Gestión de Citas

Proyecto final de Bases de Datos ESCOM periodo 27-1.

## Descripción
Sistema web para gestionar las citas de un hospital, junto con farmacia,
servicios, recetas y consultorios. La información vive en una base de datos
Microsoft SQL Server y se accede mediante un login con distintos perfiles.

## Perfiles y qué puede hacer cada uno
**Paciente**
- Darse de alta a sí mismo y consultar sus datos personales.
- Agendar una cita eligiendo especialidad, doctor, fecha y horario
  (solo se muestran opciones disponibles) y obtener su comprobante y línea de pago.
- Ver su historial de citas (con filtro por fecha o estatus) y cancelarlas.

**Doctor**
- Consultar sus datos, sus citas y el historial médico de sus pacientes.
- Generar recetas.
- No puede editar sus datos sensibles (número de empleado, cédula, CURP,
  nombre y especialidad) ni darse de alta a sí mismo.

**Recepcionista**
- Dar de alta y consultar recepcionistas, doctores y pacientes.
- Administrar especialidades, consultorios, citas y servicios extra.
- Cancelar citas (por solicitud del paciente o del doctor).
- Controlar el inventario de farmacia y el cobro de medicamentos y servicios.
- No puede ver recetas ni historiales médicos.

## Reglas de negocio principales
- **Agendar:** con mínimo 48 hrs y máximo 3 meses de anticipación (no hay citas de "hoy para hoy").
- **Pago:** el paciente tiene 8 hrs para pagar; si no, la cita se cancela y se libera la fecha.
- **Una cita no se puede agendar si:** el doctor está ocupado, el horario está fuera de su jornada laboral, la fecha ya pasó, o el paciente ya tiene una cita pendiente con ese doctor.
- **No se reagenda:** solo se cancela y se solicita una nueva.
- **Política de cancelación:** 48 hrs o más = 100% de reembolso, 24 hrs = 50%, menos de 24 hrs = 0%. Si cancela el doctor, se reembolsa el 100%.
- **Estatus de la cita:** agendada pendiente de pago, pagada pendiente por atender, cancelada por falta de pago, cancelada por paciente, cancelada por doctor, atendida y no acudió.
- **Bitácoras:** solo permiten consulta e inserción; nadie puede actualizar ni borrar sus registros.
