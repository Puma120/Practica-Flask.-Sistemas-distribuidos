Pablo Urbina Macip
27/01/2026

Link al repositorio https://github.com/Puma120/Practica-Flask.-Sistemas-distribuidos 

¿Qué quedó más acoplado en el monolito? La base de datos y el backend, se podrían haber hecho incluso en el mismo archivo aunque fuera una mala practica, pero de todas formas prefiero la logica separada, me ayuda a no confundirme tanto.

¿Qué separarías primero si lo migraras a API/microservicio? en lo personal, primero cambiaria el frontend a un nuevo repositorio al igual que usar la BD desde algun servicio en la nube y de esa forma tenerlo separado ej. MoongoDB atlas.

¿Qué problemas surgen si dos equipos trabajan en paralelo en el mismo monolito? Más que nada, problemas de merge, los diminuí haciendo que siempre estuvieramos trabajando en un archivo diferente y cada que estuviera listo ese archivo se hace un push al repositorio para que no se trabaje en el mismo archivo.