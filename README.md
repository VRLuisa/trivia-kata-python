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