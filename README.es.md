# Maestro MCZ - Recetas

<img src="https://raw.githubusercontent.com/olerida/maestro_recipes/main/custom_components/maestro_recipes/brand/icon.png" alt="Maestro MCZ Recipes" width="128">

[English](README.md)

> [!WARNING]
> El modo normal es de solo lectura. El modo avanzado, que se activa marcando **Opciones avanzadas** durante la instalación, permite modificar los parámetros de combustión de la estufa y está destinado únicamente a técnicos o personas con conocimientos avanzados.

Maestro MCZ Recipes es una integración personalizada para [Home Assistant](https://www.home-assistant.io/) que muestra las opciones de recetas de estufas MCZ Maestro. Puede habilitar controles para Activo, Pellet y el modo de adaptación. Utiliza la integración existente [Maestro MCZ](https://github.com/Robbe-B/maestro_mcz) y no requiere introducir de nuevo las credenciales.

La integración es experimental. Las órdenes se han probado mediante simulaciones, pero **todavía no se ha verificado su aplicación en una estufa real**. Consulta la [investigación](docs/investigacion.md) y la [autoevaluación de calidad](docs/bronze-review.md); esta última no es una clasificación oficial.

La integración incluye el icono y el logotipo de MCZ como marca local para Home Assistant 2026.3 o posterior.

## Dispositivos compatibles

El código admite la estructura de coordinadores de **Maestro MCZ 0.6.7-beta**. La investigación de las pantallas se ha realizado con Maestro+ 5.6.9 y una MCZ Ego Comfort Air con firmware M2S.AIR.24.20. No se han verificado escrituras reales ni la compatibilidad completa con otras estufas o versiones de la integración original.

## Requisitos previos

1. Configura la estufa en la app Maestro+ MCZ y comprueba que esté conectada.
2. Instala y configura [Maestro MCZ](https://github.com/Robbe-B/maestro_mcz) en Home Assistant y comprueba que detecte la estufa.
3. Asegúrate de que la integración original pueda acceder a la nube de MCZ.

## Instalación

### Instalación manual

1. Copia la carpeta `custom_components/maestro_recipes` de este repositorio dentro de `custom_components` de la configuración de Home Assistant. Si no existe, créala.
2. Reinicia Home Assistant.

### HACS

[![Abrir esta integración en Home Assistant Marketplace](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=olerida&repository=maestro_recipes&category=integration)

El botón abre el diálogo para añadir el repositorio personalizado en HACS. También puedes añadirlo manualmente:

1. En HACS, abre **Integraciones** y selecciona **Repositorios personalizados** en el menú.
2. Añade `https://github.com/olerida/maestro_recipes` con la categoría **Integración**.
3. Busca **Maestro MCZ Recipes**, descárgala y reinicia Home Assistant.

Es un repositorio personalizado y no está incluido en el catálogo predeterminado de HACS. La integración está en fase beta; activa **Mostrar versiones beta** en HACS si la versión no aparece.

## Actualización

Actualiza los archivos mediante HACS cuando haya una versión disponible y reinicia Home Assistant. Si instalaste manualmente, sustituye la carpeta de la integración por la versión deseada y reinicia. Consulta el [historial de cambios](CHANGELOG.md) antes de actualizar.

## Configuración

1. Abre **Ajustes** → **Dispositivos y servicios** en Home Assistant.
2. Selecciona **Añadir integración** y busca **Maestro MCZ Recipes**.
3. Selecciona la cuenta configurada en Maestro MCZ.
4. Deja **Opciones avanzadas** desactivada para ver los valores sin controles. Actívala si deseas habilitar los controles compatibles y confirma.

No se solicitan credenciales adicionales. Cada cuenta Maestro MCZ se puede añadir una vez. Para cambiarla más tarde, abre **Ajustes** → **Dispositivos y servicios** → **Maestro MCZ Recipes**, pulsa **Configurar** y modifica **Opciones avanzadas**. La integración se recarga y conserva la cuenta. Las entidades del modo anterior permanecen en el registro como no disponibles.

## Funciones compatibles

| Opción de la app | Lectura | Con opciones avanzadas |
|---|---|---|
| Activo | Ajuste y estado de activación | Ajuste y activación/desactivación |
| Pellet | Ajuste | Ajuste |
| Modo de adaptación | Estado | Activación/desactivación |

Los campos de lectura solo aparecen si la integración original proporciona un valor. Los controles solo aparecen cuando los metadatos de la estufa contienen identificadores, tipos y límites reconocidos. Los ajustes numéricos se limitan al intervalo observado en Maestro+ (−3 a +3) y a cualquier límite más restrictivo del modelo. Algunos valores pueden duplicar entidades de Maestro MCZ Extra Sensors.

## Actualización de datos y órdenes

La integración utiliza el coordinador existente de Maestro MCZ para leer los valores; el intervalo de actualización depende de la integración original. Con los controles avanzados, las órdenes se envían a través de esa misma integración y se solicita una actualización posterior.

Para cambiar Activo, se actualiza el origen y se envían juntos el ajuste y su estado de activación. Esto reduce las posibles colisiones, pero no elimina una carrera si Maestro+ u otro cliente cambia el ajuste simultáneamente. Evita cambios simultáneos y comprueba el valor actualizado: una respuesta aceptada no demuestra por sí sola que la estufa haya aplicado la orden.

## Limitaciones conocidas

- Es un proyecto comunitario independiente, no una integración oficial de MCZ.
- Las órdenes no se han validado en una estufa real; los controles son experimentales.
- Solo se muestran valores disponibles en la integración original y controles reconocidos para el modelo.
- Se utilizan interfaces internas de Maestro MCZ, que pueden cambiar. Solo se admite la estructura de la versión 0.6.7-beta.
- Recarga Recipes después de recargar o actualizar Maestro MCZ.
- El formulario y los nombres de las entidades están disponibles en español e inglés.

## Solución de problemas

- **No aparece ninguna cuenta:** configura primero Maestro MCZ y comprueba que esté cargada. Cada cuenta solo se puede añadir una vez.
- **Falta un valor:** espera una actualización del coordinador y revisa las entidades deshabilitadas. La estufa y la integración original deben proporcionar ese dato.
- **Falta un control:** comprueba que activaste **Opciones avanzadas**. El control también requiere metadatos del modelo reconocidos y, para números, límites válidos.
- **Los valores no están disponibles o no se actualizan:** revisa la conexión de la estufa y Maestro MCZ. Tras recargar la integración original, recarga también Recipes.
- **HACS no muestra una versión:** comprueba las opciones de versión del repositorio. Activa **Mostrar versiones beta** si no aparece la versión.

## Eliminar la integración

Abre **Ajustes** → **Dispositivos y servicios**, selecciona **Maestro MCZ Recipes**, abre su menú y pulsa **Eliminar**. Para borrar también los archivos, elimina `custom_components/maestro_recipes` y reinicia Home Assistant. La integración Maestro MCZ original y su cuenta son independientes.

## Licencia

El código se distribuye bajo la [licencia MIT](LICENSE). El icono Maestro+ y las marcas MCZ pertenecen a su titular y no están incluidos en la licencia MIT.
