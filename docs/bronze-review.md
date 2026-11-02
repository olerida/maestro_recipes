# Autoevaluación de calidad Bronze

Revisión local basada en los criterios inventariados en `maestro_rtinfo` y en Home Assistant 2026.10.4 instalado para pruebas. No es una clasificación oficial ni una evaluación de aceptación en Home Assistant Core. La integración fuente es un componente personalizado y utiliza interfaces internas; su elegibilidad para Core no está establecida.

| Área | Estado y límites |
|---|---|
| Configuración y entrada única | Flujo de interfaz con selección de cuenta, identificación única y casilla avanzada desactivada por defecto. Las pruebas del gestor real del flujo cubren duplicados, errores y selección avanzada. |
| Comprobación antes de configurar e iniciar | Se comprueba que el coordinador existente tenga una actualización correcta, sin peticiones adicionales. Es una comprobación histórica, no una prueba de conectividad actual; se propone esta limitación como excepción, pendiente de revisión formal. |
| Actualización | Reutiliza el coordinador de Maestro MCZ, sin sondeo propio. Los nuevos valores de lectura se descubren en actualizaciones posteriores. Las órdenes explícitas usan el refresco posterior de la integración fuente. |
| Entidades y ciclo de vida | Identificadores estables por estufa y función; nombres traducidos, dispositivo compartido y datos de ejecución en `runtime_data`. Los listeners de descubrimiento se liberan al descargar la entrada. |
| Escritura | Los controles requieren selección avanzada, metadatos reconocidos y límites válidos. Activo envía ambos valores juntos; las operaciones se serializan por estufa. Las pruebas usan datos y comandos simulados; no prueban aceptación ni aplicación física. |
| Documentación | Los README describen requisitos, instalación, configuración, funcionalidad, limitaciones, diagnóstico y eliminación. No se registran acciones, condiciones ni disparadores propios. |
| Dependencias y marca | No hay dependencias Python adicionales; se declara la integración personalizada `maestro_mcz` como dependencia. La instalación de esta dependencia es responsabilidad del usuario. Los recursos locales de marca se incluyen; su elegibilidad para el repositorio oficial de marcas no está evaluada. |
| Pruebas | Pruebas de Home Assistant aisladas, sin red ni acceso a la estufa. La cobertura del flujo y el total se pueden reproducir con el comando siguiente. |

```sh
python -m pip install -r requirements-test.txt
pytest tests_ha -q --cov=custom_components/maestro_recipes --cov-report=term-missing
```

No se afirma alcanzar Bronze: quedan pendientes la revisión formal de las excepciones, la elegibilidad de la dependencia y de la marca, las diferencias entre versiones de Maestro MCZ y la validación física de las escrituras. La integración no fuerza ni realiza pruebas sobre una estufa durante la instalación.
