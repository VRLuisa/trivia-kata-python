# Trivia Refactoring Kata en Python

## Estado inicial del proyecto

Este proyecto es una versión en Python del Trivia Refactoring Kata original en Java.

El objetivo es refactorizar `game.py` sin cambiar el comportamiento observable del juego. Para lograrlo, se usa un Golden Master en `tests/test_game.py`, que compara la salida de `Game` contra `GameOld` usando las mismas semillas aleatorias.

Archivos principales:

- `trivia/game.py`: código que será refactorizado.
- `trivia/game_old.py`: código legado usado como oráculo del Golden Master.
- `trivia/play_game.py`: script para jugar manualmente.
- `tests/test_game.py`: prueba Golden Master.

## Paso 0.3 — Partida manual

### ¿Qué tipos de mensajes aparecen en consola?

Aparecen mensajes sobre:

- Jugadores agregados al juego.
- Número asignado a cada jugador.
- Jugador actual.
- Número obtenido en el dado.
- Movimiento en el tablero.
- Nueva posición del jugador.
- Categoría de la pregunta.
- Pregunta realizada.
- Respuesta correcta o incorrecta.
- Monedas acumuladas.
- Envío del jugador a la caja de penalización.
- Salida o no salida de la caja de penalización.
- Fin de la partida.

### ¿Qué secuencia tiene un turno de juego?

El turno inicia mostrando quién es el jugador actual y el número obtenido en el dado.
Si el jugador no está en la caja de penalización, avanza en el tablero, se muestra su nueva ubicación, se determina la categoría y se realiza una pregunta.
Después, si la respuesta es correcta, el jugador gana una moneda. Si la respuesta es incorrecta, el jugador es enviado a la caja de penalización.
Si el jugador está en la caja de penalización, solo puede salir cuando obtiene un número impar en el dado. Si obtiene un número par, no sale y pierde el turno.
Finalmente, el turno pasa al siguiente jugador.

### ¿Cuándo termina la partida?

La partida termina cuando un jugador responde correctamente y alcanza la condición de victoria. En el código actual, la condición está es llegar a 6 monedas.

## Bloque 1 — Ficha de análisis de `game.py`

### 1. Olores de código detectados

1. Método `roll()` demasiado largo.
   - Contiene lógica de turno, movimiento, penalización, impresión en consola y selección de pregunta.
   - Tiene varios niveles de condicionales anidados.

2. Método `handleCorrectAnswer()` demasiado largo.
   - Mezcla lógica de respuesta correcta, monedas, penalización, cambio de jugador y condición de victoria.
   - Contiene duplicación entre el caso de jugador en penalización y jugador normal.

3. Uso de listas paralelas.
   - `players`, `places`, `purses` e `inPenaltyBox` dependen del mismo índice.
   - Esto indica que falta una abstracción para representar a un jugador.

4. Nombres poco expresivos.
   - `places` no comunica claramente que representa la posición de cada jugador.
   - `purses` no comunica claramente que representa monedas.
   - `isPlayable()` podría expresar mejor que valida si hay suficientes jugadores.
   - `currentPlayer` representa un índice, no directamente un jugador.

5. Números mágicos.
   - `6`: cantidad de monedas necesarias para ganar.
   - `12`: tamaño del tablero.
   - `50`: cantidad de preguntas generadas por categoría.
   - `2`: mínimo de jugadores para que el juego sea jugable.

6. Duplicación en el movimiento del jugador.
   - La lógica de avanzar en el tablero aparece tanto cuando el jugador sale de la caja de penalización como cuando juega normalmente.

7. Duplicación en el cambio de jugador.
   - La lógica para avanzar al siguiente jugador aparece varias veces.

8. Método `currentCategory()` con muchas condiciones repetidas.
   - La asignación de categoría depende de varios `if`.
   - Podría simplificarse con una estructura basada en categorías o módulo.

9. Método `askQuestion()` llama varias veces a `currentCategory()`.
   - Calcula la misma categoría más de una vez.
   - Podría calcularse una vez y reutilizarse.

10. Mezcla de responsabilidades en una sola clase.
    - `Game` administra jugadores, tablero, preguntas, turnos, penalizaciones, monedas, condición de victoria y salida por consola.

11. Typo detectado.
    - El mensaje `"Answer was corrent!!!!"` contiene un error ortográfico.
    - Debería decir `"Answer was correct!!!!"`

12. Posible bug a revisar.
    - La lógica de posiciones, categorías y condición de victoria debe revisarse con cuidado.


### 2. Responsabilidades que deberían estar separadas

1. Estado del jugador.
   - Nombre.
   - Posición.
   - Monedas.
   - Estado de penalización.

2. Gestión del mazo de preguntas.
   - Crear preguntas.
   - Guardar preguntas por categoría.
   - Entregar la siguiente pregunta de una categoría.

3. Lógica del turno.
   - Tirar dado.
   - Mover al jugador.
   - Revisar si sale de penalización.
   - Hacer pregunta.
   - Procesar respuesta correcta o incorrecta.

4. Control general del juego.
   - Agregar jugadores.
   - Saber quién es el jugador actual.
   - Cambiar al siguiente jugador.
   - Determinar si la partida terminó.

5. Reglas del tablero.
   - Tamaño del tablero.
   - Categoría según posición.
   - Reglas de movimiento.

### 3. Abstracciones ausentes

1. `Player`
   - Representaría a cada jugador con su nombre, posición, monedas y estado de penalización.

2. `QuestionDeck`
   - Administraría las preguntas por categoría.

3. Constantes del dominio
   - `BOARD_SIZE`
   - `WINNING_COINS`
   - `MAX_PLAYERS`
   - `QUESTIONS_PER_CATEGORY`
   - `MIN_PLAYERS`

4. Métodos pequeños con intención clara
   - `current_player()`
   - `move_current_player()`
   - `ask_question()`
   - `category_for_position()`
   - `advance_to_next_player()`
   - `player_has_won()`
   - `handle_penalty_box_turn()`
   - `handle_normal_turn()`

### 4. Itinerario tentativo de refactorización

1. Renombrar variables para revelar intención.
2. Extraer constantes para números mágicos.
3. Extraer métodos pequeños desde `roll()`.
4. Extraer métodos pequeños desde `handleCorrectAnswer()`.
5. Eliminar duplicación en el cambio de jugador.
6. Eliminar duplicación en el movimiento.
7. Crear clase `Player`.
8. Mover estado y comportamiento del jugador a `Player`.
9. Crear clase `QuestionDeck`.
10. Simplificar la lógica de categorías.
11. Releer el código y hacer limpieza final.
12. Corregir typo en `game.py` y `game_old.py`.
13. Corregir bug en `game.py` y `game_old.py`.
14. Implementar un cambio de requisito pequeño.


## Refactorizaciones realizadas
Durante el kata se realizaron refactorizaciones pequeñas, ejecutando `pytest` después de cada cambio importante para mantener el Golden Master en verde.

Principales cambios realizados:
1. Se extrajeron constantes para eliminar números mágicos:
   - `MAX_PLAYERS`
   - `MINIMUM_PLAYERS`
   - `QUESTIONS_PER_CATEGORY`
   - `BOARD_SIZE`
   - `WINNING_COINS`
   - `CATEGORIES`

2. Se renombraron variables para mejorar la intención del código:
   - `places` fue reemplazado por información de posición dentro de `Player`.
   - `purses` fue reemplazado por `coins` dentro de `Player`.
   - `inPenaltyBox` fue reemplazado por `in_penalty_box`.
   - `currentPlayer` fue reemplazado por `current_player_index`.

3. Se extrajeron métodos pequeños para reducir duplicación:
   - `advance_to_next_player()`
   - `current_player()`
   - `current_player_name()`
   - `current_player_position()`
   - `move_current_player()`
   - `show_location_and_ask_question()`
   - `handle_normal_turn()`
   - `handle_penalty_box_turn()`
   - `award_coin_to_current_player()`
   - `handle_correct_answer()`
   - `wrong_answer()`

4. Se creó la clase `Player`.

La clase `Player` ahora gestiona el estado de cada jugador:
- Nombre.
- Posición.
- Monedas.
- Estado de penalización.

También contiene comportamientos propios del jugador:
- Moverse en el tablero.
- Ganar una moneda.
- Entrar a la caja de penalización.
- Saber si ya ganó.

5. Se creó la clase `QuestionDeck`.
La clase `QuestionDeck` ahora gestiona las preguntas del juego:
- Crea las preguntas por categoría.
- Guarda las preguntas organizadas por categoría.
- Entrega la siguiente pregunta según la categoría solicitada.

Con esto, `Game` queda más enfocada en coordinar el flujo del juego.

## Uso del Golden Master

El Golden Master compara la salida de `Game` contra `GameOld` usando las mismas semillas aleatorias.
Esto permitió hacer refactorizaciones internas sin cambiar el comportamiento observable del juego.
Durante el proceso, después de cada micro-cambio se ejecutó: pytest


## Corrección del typo y del bug

### Typo detectado
Durante la revisión del código se encontró un error ortográfico en el mensaje que se imprime cuando un jugador responde correctamente fuera de la caja de penalización.
El mensaje original era: Answer was corrent!!!!

### Bug detectado
El bug encontrado estaba relacionado con la lógica de la caja de penalización.
Cuando un jugador estaba en la caja de penalización y tiraba un número par, el jugador no lograba salir de la caja. En ese caso, el programa imprimía que el jugador no salía de la penalización y no se realizaba ninguna pregunta.
La corrección se aplicó en ambos archivos:
- game.py
- game_old.py

Esto se hizo porque el Golden Master no detectaba el bug por sí solo: el error estaba presente tanto en el código refactorizado como en el código usado como oráculo. Por lo tanto, ambas versiones se comportaban igual, aunque la lógica fuera incorrecta según las reglas del juego.


## Bloque 4 — Retrospectiva

#### ¿En qué momento me sentí seguro de que el Golden Master cubría lo suficiente?
Me sentí seguro cuando el Golden Master comenzó a ejecutar miles de partidas con semillas aleatorias y comparó la salida de `Game` contra `GameOld`. Al usar las mismas entradas en ambos juegos, pude comprobar que mis cambios internos no alteraban el comportamiento observable del programa.
También me dio seguridad ejecutar `pytest` después de cada micro-refactorización. Si la prueba pasaba, sabía que el cambio no había modificado la salida del juego.

#### ¿Hubo algún cambio que el Golden Master no pudo detectar como peligroso? ¿Cuál?
Sí. El Golden Master no pudo detectar automáticamente el bug relacionado con la caja de penalización, porque ese error existía tanto en `game.py` como en `game_old.py`.
Cuando el jugador estaba en la caja de penalización y no lograba salir, no debía responder ninguna pregunta. Sin embargo, si después se llamaba a `wrongAnswer()`, el juego actuaba como si el jugador hubiera respondido mal, aunque realmente no hubo pregunta.

#### ¿Por qué creo que el README dice que no debemos escribir tests unitarios durante la refactorización? ¿Estoy de acuerdo?
El README recomienda no escribir tests unitarios durante la refactorización porque el objetivo principal del kata es practicar la técnica del Golden Master. En código legacy, primero se necesita una red de seguridad amplia que permita cambiar la estructura interna sin romper el comportamiento existente.
Estoy de acuerdo, porque al inicio el código estaba demasiado mezclado y escribir pruebas unitarias habría sido difícil. Después de refactorizar, el código quedó dividido en clases y métodos más claros, por lo que ahora sí sería más sencillo escribir pruebas unitarias específicas para `Player`, `QuestionDeck` y algunas reglas de `Game`.

### Sobre la refactorización
#### ¿Qué olor de código fue el más difícil de eliminar? ¿Por qué?
El olor más difícil de eliminar fue el uso de listas paralelas para representar a los jugadores.
Originalmente, el juego usaba varias estructuras separadas para guardar información relacionada con cada jugador: nombres, posiciones, monedas y estado de penalización. Todas dependían del mismo índice.
Esto era riesgoso porque cualquier error en el índice podía afectar el estado del jugador equivocado. Para corregirlo fue necesario crear la clase `Player` y mover poco a poco sus datos y comportamientos sin romper el Golden Master.

#### ¿Cuántas veces se puso en rojo el test? ¿Qué lo causó?
El test se puso en rojo durante los cambios que modificaban intencionalmente la salida del juego, especialmente al corregir el typo y el bug primero en `game.py` antes de hacer la misma corrección en `game_old.py`.
Esto ocurrió porque el Golden Master compara exactamente la salida de ambos archivos. Si uno cambia y el otro no, la prueba detecta una diferencia. Después de aplicar la misma corrección en ambos archivos el test volvió a estar en verde.

#### ¿Qué refactorización manual fue la más arriesgada?
La refactorización más arriesgada fue crear la clase `Player` y mover a ella el estado del jugador: posición, monedas y penalización.
Fue riesgosa porque el código original dependía de listas paralelas indexadas por `current_player_index`. Si se movía mal alguno de esos datos, el jugador actual podía quedar con una posición, monedas o estado de penalización incorrecto.
Para reducir el riesgo, se hizo en pasos pequeños: primero el nombre, luego la posición, después las monedas y finalmente el estado de penalización.

#### ¿Cómo podría mejorarse el diseño para que el próximo cambio de requisito sea más fácil?
El diseño podría mejorarse separando aún más las reglas del juego en métodos o clases específicas. Por ejemplo, se podría crear una clase para las reglas del tablero o para manejar la lógica de penalización.
También podría mejorarse haciendo que las categorías y preguntas sean configurables, en lugar de estar escritas directamente en el código. Esto permitiría agregar nuevas categorías, cambiar preguntas o modificar reglas sin tocar varias partes del programa.
Aun así, el diseño actual ya facilita más los cambios que el código original, porque ahora existen responsabilidades más claras:
- `Player` gestiona el estado del jugador.
- `QuestionDeck` gestiona las preguntas.
- `Game` coordina el flujo general del juego.

## Cambio de requisito implementado
Se implementó el requisito de máximo 6 jugadores.
Para hacerlo, se utilizó la constante: MAX_PLAYERS = 6