Esta carpeta contiene las tareas que se deben realizar para el proyecto.

## Tareas

En proyectos modernos, tasks/ normalmente se usa para:

- Background jobs
- Procesos asíncronos
- Tareas que no dependen del request actual
- Celery / RQ / Dramatiq
- Jobs programados (cron)

tasks/
├── send_email.py
├── generate_report.py
├── clean_expired_tokens.py

Ideal para:
- IA
- Eventos
- Procesos en background
- Procesos en batch
- Procesos en streaming
- Procesos en batch
- Colas de mensajes (Celery, Redis, Kafka)

Son cosas que:

* No viven en el ciclo request-response
* Se ejecutan fuera del endpoint
* Pueden correr en otro worker