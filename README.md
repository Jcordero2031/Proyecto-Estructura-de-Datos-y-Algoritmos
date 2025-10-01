# Proyecto-Estructura-de-Datos-y-Algoritmos
En este proyecto diseñamos un sistema para la gestión segura y eficiente de llaves criptográficas dentro de una infraestructura distribuida. Las llaves son el núcleo de la seguridad en transacciones digitales y comunicaciones, por lo que nuestro objetivo fue garantizar que su uso fuera confiable, balanceado y auditable.

Partimos de la idea de que cada servidor almacena un conjunto limitado de llaves, cada una con un número máximo de usos. Cuando una transacción solicita una llave, nuestro sistema decide qué servidor la asigna, evitando sobrecargar un único nodo y asegurando la rotación constante de llaves.

Además, incorporamos mecanismos para: controlar la expiración automática de llaves, permitir su reemplazo o rotación, y mantener un registro de auditoría que documenta cada uso. Para la implementación, utilizamos estructuras de datos como colas, tablas hash y conjuntos, que nos permitieron organizar los accesos de manera eficiente.

En conclusión, lo que buscamos con este trabajo es mostrar que la seguridad no solo depende del cifrado, sino también de cómo se administran las llaves que lo hacen posible. Nuestro sistema propone una solución escalable y práctica que puede aplicarse a contextos reales como plataformas financieras, servicios en la nube o aplicaciones móviles de pago.
