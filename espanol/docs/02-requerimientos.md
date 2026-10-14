# Requerimientos iniciales

Estado: borrador v0.1. Las referencias S1, D-* y P-* están en `00-contexto.md`; RN-* y PRN-* en `03-reglas-negocio.md`. Los criterios son propuestas de verificación y deben concretarse al especificar cada flujo.

## Requerimientos funcionales

| ID | Requerimiento | Criterio de aceptación inicial | Fuente / reglas |
| --- | --- | --- | --- |
| RF-01 | Autenticar usuarios y mostrar navegación por rol | Cada uno de los cinco perfiles accede a su navegación; una operación fuera de sus permisos es rechazada por el servidor | S1 p. 1; D-01; permisos detallados P-02 |
| RF-02 | Registrar pacientes y consultar sus datos | Una persona crea su cuenta de paciente y consulta sus datos; recepción puede darla de alta | RN-10/RN-15; campos en P-09 |
| RF-03 | Gestionar altas y consulta de empleados, cuentas y roles | Recepción registra doctores; recepción o administrador registra recepcionistas; alta de cajeros y demás permisos según P-02 | RN-11/RN-15; extensión propuesta D-01 |
| RF-04 | Gestionar especialidades, costos, consultorios y jornadas | Se consultan catálogos y horarios utilizados para agendar; existe una única especialidad activa por doctor | RN-04/RN-13/RN-18/RN-19; responsables P-02 |
| RF-05 | Agendar citas con disponibilidad válida | Se eligen especialidad, doctor, fecha y horario; se rechazan fechas, horarios y duplicados que incumplan RN-01/02/03/04 | S1 pp. 1/2; límites P-03/P-04/P-05 |
| RF-06 | Generar comprobante y línea de pago | Al crear la cita se muestran folio, paciente, fecha, horario, consultorio, especialidad, doctor, línea, plazo de pago y política de cancelación | S1 p. 3; RN-06/RN-07 |
| RF-07 | Registrar pagos y resolver vencimientos | Caja registra la confirmación y la cita pasa a pagada; una cita que no cumple el plazo se cancela y libera disponibilidad | RN-06/RN-22; mecanismo P-01/P-05 |
| RF-08 | Consultar citas e historial con filtros | Paciente ve sus citas por fecha/estado; doctor consulta su agenda; recepción consulta agenda general | S1 pp. 2/3/4; RN-09/RN-10 |
| RF-09 | Gestionar cancelaciones | Paciente o recepción cancela según la política; doctor solicita y recepción aprueba antes de cancelar; no existe reagendar | RN-05/RN-07/RN-08; P-06 |
| RF-10 | Gestionar devoluciones asociadas a cancelaciones | Se distingue el importe que corresponde devolver del reembolso ejecutado; caja registra su ejecución | RN-07/RN-08; responsabilidad y mecanismo propuestos P-07 |
| RF-11 | Registrar atención y consultar historial médico | El doctor accede a los datos clínicos permitidos y registra el resultado de consulta; recepción no recibe el contenido clínico | S1 p. 3; RN-14; P-04/P-06/P-12 |
| RF-12 | Emitir y consultar recetas | Receta incluye folio, fecha, doctor, cédula, paciente, edad, diagnóstico, medicamentos, tratamientos y observaciones | S1 p. 3; RN-14; correcciones P-12 |
| RF-13 | Gestionar medicamentos e inventario | Se consultan medicamentos, precios y existencias; la propuesta de venta actualiza cantidades | S1 p. 4; PRN-03; responsables y detalle P-02/P-08 |
| RF-14 | Gestionar servicios y ventas | Caja puede vender servicios y medicamentos a un cliente sin cuenta de paciente; se calcula el total y genera ticket | S1 pp. 4/5; RN-16/RN-18/RN-22 |
| RF-15 | Registrar y consultar bitácoras | Se registra actor y movimiento de citas/consultas; ninguna interfaz ni permiso permite modificar o borrar entradas | S1 pp. 4/5; RN-17; consulta P-12 |

## Requerimientos no funcionales

| ID | Requerimiento | Verificación propuesta | Estatus |
| --- | --- | --- | --- |
| RNF-01 | Usar Microsoft SQL Server | Demostrar conexión y scripts ejecutables en el motor elegido | Fuente S1/S3 |
| RNF-02 | Ofrecer las cinco interfaces mediante navegador | Abrir cada experiencia web; paciente usable en móvil y operaciones internas en computadora | Web confirmado D-02; adaptación propuesta |
| RNF-03 | Restringir por VPN a recepción, administrador y cajero | Con credenciales válidas, fuera de VPN no se accede a sus operaciones; dentro de VPN se aplican además permisos del rol | Confirmado D-03; diseño técnico P-10 |
| RNF-04 | Aplicar autenticación y autorización en servidor | Rechazar acceso directo no autorizado, aunque se conozca URL o identificador del recurso | Propuesto; materializa permisos S1 |
| RNF-05 | Mantener integridad ante operaciones concurrentes | Dos reservas simultáneas para un mismo espacio no producen doble ocupación; operaciones de venta/pago no dejan cambios parciales | Propuesto PRN-02/PRN-03/PRN-04 |
| RNF-06 | Proteger credenciales y datos de usuarios | Transporte protegido, contraseñas sin almacenamiento en texto y respuestas acordes con permisos | Propuesto; decisiones técnicas pendientes |
| RNF-07 | Facilitar uso y comprensión | Formularios con etiquetas, navegación por teclado, estados expresados con texto además de color y mensajes específicos | Propuesto; objetivo de accesibilidad por definir |
| RNF-08 | Conservar trazabilidad | Cada cambio relevante incluye actor, referencia y momento; bitácoras protegidas contra actualización/borrado | Fuente RN-17; implementación propuesta |
| RNF-09 | Definir recuperación y respaldo | Documentar y demostrar restauración con datos de prueba | Propuesto; frecuencia, RPO y RTO por definir |
| RNF-10 | Establecer objetivos medibles de rendimiento | Medir agenda y confirmación de cita con volumen y concurrencia acordados | Pendiente; no se inventan tiempos ni capacidad |

## Datos mínimos de los documentos

- **Comprobante:** los campos enumerados en RF-06.
- **Historial médico:** identificador de historial/paciente, nombre, alergias, tipo de sangre, padecimientos previos, peso y estatura (S1 p. 3).
- **Receta:** los campos enumerados en RF-12.
- **Bitácora de cita:** folio, fecha de movimiento, estado, fecha de cita, especialidad, costo, política de cancelación y monto devuelto (S1 p. 4).
- **Bitácora operativa de consulta:** historial, usuario, cita, fecha/hora, paciente, folio de receta, doctor, resultado de consulta, especialidad y consultorio; máquina/IP opcional (S1 p. 4). La referencia a una receta no concede acceso a su contenido.

Los formularios personales, obligatoriedad, tipos, longitudes y validaciones se definirán en el diccionario de datos. No inferirlos de un boceto.

## Comprobaciones prioritarias para futuras specs

1. Agendamiento válido y rechazo por cada RN aplicable, incluyendo límites temporales una vez resueltos.
2. Solicitudes simultáneas del mismo horario y del mismo paciente/doctor.
3. Pago confirmado, plazo vencido y pago registrado en el límite acordado.
4. Cancelación a 48 horas, a 24 horas y por debajo de 24; cancelación por doctor aprobada.
5. Recepción sin permisos de cobro ni contenido clínico; roles internos con/sin VPN.
6. Venta a cliente no registrado; existencias y total correctos.
7. Registro de movimiento y rechazo de modificación/borrado de bitácora.
