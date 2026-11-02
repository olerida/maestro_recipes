# Investigación de recetas

## Fuentes y alcance

El APK principal de Maestro+ 5.8.0 (`it.mcz.maestro`, SHA-256 `0aa7b6b623fe193e1dbb0844f85847fb9b70a5c4be41c0310a55526763fcba2b`) se ha inventariado con REA (evidencia `ev_3fbf623ea1da6b6a8170d791c9677e4fc8300d91ca4e4915e32db561e6d07083`). Las conclusiones siguientes proceden del análisis estático anterior de la biblioteca ARM64 de Maestro+ 5.6.9 mediante Blutter; no prueban el comportamiento de 5.8.0 ni la aceptación de órdenes por la estufa.

## Pantallas y valores

La pantalla Recetas conduce a las pantallas Activo, Pellet y Modo de adaptación. Los valores mostrados corresponden respectivamente a `pos_ric_flu`, `pos_ric_pel` y `mod_ada_on` del estado. La integración Maestro MCZ ya conserva esos valores y maestro_rtinfo puede mostrarlos.

Las pantallas presentan acciones de guardar y cancelar. En 5.6.9 el código de guardado construye una petición de cambio de programa: Pellet envía un parámetro (`SENSOR_PALLET`), modo de adaptación envía uno (`SENSOR_PELLET_MOD_ADA_ON`) y Activo envía dos (`SENSOR_PELLET_ACT_VALUE` y `SENSOR_PELLET_ACT`). El segundo se inicializa desde `StateResponse.act` y corresponde al interruptor de activación mostrado en esa pantalla. El código emplea la configuración `CONFIGURATION_PELLET`. Los identificadores concretos de sensores y configuración varían entre familias AIR e HYDRO; no deben suponerse universales. Los límites y condiciones de disponibilidad requieren verificación adicional y pueden depender del modelo.

El objeto `Model` de la integración original conserva configuraciones, identificadores y límites; `MaestroStove.ActivateProgramMultipleCommands` permite enviar órdenes usando la conexión existente. Es necesario verificar el mapeo al modelo y el tratamiento de errores y refresco antes de implementar controles.

## Verificación pendiente

El emulador conserva instalada la app 5.6.9 y permitió consultar las pantallas tras iniciar sesión. Falta verificar la selección para cada familia de estufas y contrastar dinámicamente las peticiones generadas y su aplicación. No se han enviado órdenes ni modificado ajustes de la estufa durante esta investigación.

## Observación en el emulador y ruta de envío

En Maestro+ 5.6.9 con la estufa seleccionada, la pantalla Activo mostró valores enteros de −3 a +3 y un selector Activar/Desactivar; Pellet mostró −3 a +3; Adaptación mostró Activar/Desactivar. Se consultaron las pantallas y se canceló la navegación sin guardar ni enviar cambios.

La app construye una petición de cambio de programa que contiene la configuración y una lista de comandos de sensor. En Activo incluye tanto el valor como el estado `act`. En la integración comunitaria 0.6.7-beta, `ActivateProgramMultipleCommands` construye un POST a `/mcz/v1.0/Program/ActivateProgram/{id}` con `ModelId`, `ConfigurationId`, `SensorSetTypeId` y `Commands` (`SensorId`, `Value`). Usa el controlador y la autenticación existentes. El controlador acepta una respuesta HTTP 200 con JSON; esto no demuestra que la estufa haya aplicado el cambio. Después solicita actualizaciones de estado.

La implementación selecciona identificadores reconocidos solo si aparecen habilitados en los metadatos del modelo. Los límites se intersectan con −3 a +3; faltando límites, no se expone el número. Las pruebas usan objetos simulados; el envío y la aplicación de las órdenes siguen sin verificarse con una estufa real.
