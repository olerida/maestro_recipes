# Maestro MCZ Recipes

Integración experimental de Home Assistant para las recetas de estufas MCZ Maestro. Depende de [Maestro MCZ](https://github.com/Robbe-B/maestro_mcz), cuya cuenta y conexión reutiliza. No requiere credenciales adicionales.

## Funciones

Al instalarla, la casilla **Opciones avanzadas** está desactivada por defecto y solo se muestran valores. Actívala para habilitar los controles. Para cambiar esta elección, elimina y vuelve a añadir la integración.

Según la configuración proporcionada por el modelo de estufa, puede crear controles para el ajuste de Pellet, el ajuste y la activación de Activo, y el modo de adaptación. Los números se limitan al intervalo observado en Maestro+ (−3 a +3) y a los límites más restrictivos del modelo. Los controles solo se crean para identificadores, tipos y límites reconocidos. Los valores son los que recibe la integración original y pueden duplicar sensores de Maestro MCZ Extra Sensors.

Esta versión solo admite la estructura de coordinadores de Maestro MCZ **0.6.7-beta**; otras versiones no están verificadas. Las órdenes se han probado con simulaciones, no con una estufa real. Una respuesta HTTP aceptada por la integración original no demuestra que el dispositivo haya aplicado el ajuste: comprueba el valor actualizado después. El proyecto es independiente de MCZ.

## Instalación y configuración

Instala y configura primero Maestro MCZ. Copia `custom_components/maestro_recipes` en `custom_components` de Home Assistant, reinicia y añade **Maestro MCZ Recipes** desde Ajustes → Dispositivos y servicios, seleccionando la cuenta existente. También puedes añadir este repositorio como repositorio personalizado de integración en HACS. Recarga Recipes tras recargar la integración original.

No se incluye una clasificación oficial de calidad ni compatibilidad con otros modelos. Consulta [la investigación](docs/investigacion.md) y revisa los valores de tu dispositivo antes de usar los controles.

El código se distribuye bajo licencia MIT. Las marcas e imágenes de MCZ pertenecen a su titular.

## Solución de problemas y eliminación

- Si no aparece la cuenta, configura y carga primero Maestro MCZ. Cada cuenta solo puede añadirse una vez.
- Si faltan valores, espera una actualización del coordinador y revisa las entidades deshabilitadas. Solo aparecen campos recibidos de la estufa.
- En modo avanzado, un control puede no aparecer si el modelo no proporciona identificadores, tipos o límites reconocidos. El modo lectura no depende de esos metadatos.
- Si los datos no están disponibles, revisa la conexión y el estado de Maestro MCZ. Tras recargar esa integración, recarga también Recipes.
- Para eliminarla, abre **Ajustes → Dispositivos y servicios**, selecciona Maestro MCZ Recipes y elige **Eliminar**. Después puedes borrar su carpeta y reiniciar. Esto no elimina la cuenta de Maestro MCZ.

La [autoevaluación de calidad](docs/bronze-review.md) explica el alcance y los puntos pendientes; no es una certificación oficial.


Los cambios de Activo actualizan el origen antes de enviar ambos ajustes. Esto reduce, pero no elimina, las carreras con Maestro+ u otros clientes porque la API no ofrece escritura condicional atómica. Evita cambios simultáneos.
