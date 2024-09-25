#!/bin/bash

# Ejecuta la instrucción python
python nav.py

# Verifica si se proporcionó un parámetro
if [ $# -eq 1 ]; then
  respuesta="$1"
else
  # Si no se proporcionó ningún parámetro, pregunta si se desea publicar en la web o en local
  read -p "¿Deseas publicar en la web (w) o en local (l)? " respuesta
fi

# Verifica la respuesta dada
if [ "$respuesta" = "w" ]; then
  # Si la respuesta es "w", ejecuta mkdocs gh-deploy
  mkdocs gh-deploy
  # Abre Firefox con la dirección web correspondiente
  export MOZ_X11_EGL=1
  export MOZ_ENABLE_WAYLAND=1
  export MOZ_WEBRENDER=1
  firefox https://giganteavila.github.io/SRI
/ >/dev/null 2>&1
elif [ "$respuesta" = "l" ]; then
  # Si la respuesta es "l", verifica si el servidor local ya está en funcionamiento
  if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    # Si el servidor local ya está en funcionamiento, lo detiene
    echo "El servidor local ya está en funcionamiento. Lo detendrá y lo volverá a levantar."
    lsof -t -i :8000 | xargs kill -9 >/dev/null 2>&1
  fi
  # Levanta el servidor local
  mkdocs serve >/dev/null 2>&1 &
  # Espera 1 segundo para asegurarse de que el servidor esté en marcha
  sleep 1
  # Abre Firefox con la dirección local correspondiente
  export MOZ_X11_EGL=1
  export MOZ_ENABLE_WAYLAND=1
  export MOZ_WEBRENDER=1
  firefox http://localhost:8000 &
else
  # Si la respuesta no es "w" ni "l", muestra un mensaje de error
  echo "Respuesta no válida. Debe ser 'w' para publicar en la web o 'l' para ejecutar en local."
fi
