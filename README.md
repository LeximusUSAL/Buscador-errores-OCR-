# 📄 Buscador en documentos históricos con errores de OCR

Herramienta para buscar palabras clave en documentos que tienen errores de OCR. Desarrollada especialmente para los textos de prensa histórica disponibles completos en txt en la hemeroteca de la Biblioteca Nacional de España. 

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-Academic-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Script-Ready-orange.svg" alt="scriptLexiMus">
</p>

# 📘 INSTRUCCIONES: Buscador Genérico de Palabras

## 🎯 ¿Qué hace este script?

Este script busca palabras específicas en corpus de textos históricos con errores de OCR. Está pensado para iniciarse en la investigación en Humanidades Digitales.

**Características principales:**
- ✅ Tolerante a errores de OCR (hasta 30% de error)
- ✅ Búsqueda por variantes ortográficas
- ✅ Sistema de validación manual integrado
- ✅ Genera reportes HTML interactivos
- ✅ Exporta resultados en JSON

---

## 📋 PASO 1: Configurar qué palabra buscar

Abre el archivo `buscador_generico_palabras.py` con cualquier editor de texto (TextEdit, Notepad++, etc.)

Busca la sección que dice:
```
# ============================================================================
# ★★★ SECCIÓN 1: CONFIGURACIÓN MODIFICABLE - CAMBIAR AQUÍ ★★★
# ============================================================================
```

### 🔸 1.1 Palabra principal
```python
PALABRA_CLAVE = 'prokofieff'
```
**CAMBIA AQUÍ** la palabra que quieres buscar. Escríbela en minúsculas, entre comillas.

**Ejemplos:**
- Para buscar "Beethoven": `PALABRA_CLAVE = 'beethoven'`
- Para buscar "Wagner": `PALABRA_CLAVE = 'wagner'`
- Para buscar "Jazz": `PALABRA_CLAVE = 'jazz'`

---

### 🔸 1.2 Nombre para mostrar
```python
NOMBRE_MOSTRAR = 'Prokofieff/Prokofiev'
```
**CAMBIA AQUÍ** cómo quieres que aparezca la palabra en los informes. Puede incluir mayúsculas, acentos, etc.

**Ejemplos:**
- `NOMBRE_MOSTRAR = 'Beethoven'`
- `NOMBRE_MOSTRAR = 'Wagner / Vagner'`
- `NOMBRE_MOSTRAR = 'Jazz'`

---

### 🔸 1.3 Descripción
```python
DESCRIPCION = 'Serguéi Prokófiev (1891-1953) - Compositor ruso'
```
**CAMBIA AQUÍ** la descripción que aparecerá en los resultados.

**Ejemplos:**
- `DESCRIPCION = 'Ludwig van Beethoven (1770-1827) - Compositor alemán'`
- `DESCRIPCION = 'Richard Wagner (1813-1883) - Compositor alemán'`
- `DESCRIPCION = 'Género musical afroamericano (s. XX)'`

---

### 🔸 1.4 Variantes ortográficas
```python
VARIANTES_ORTOGRAFICAS = {
    'prokofieff', 'prokofief', 'prokofiew',
    'Prokofieff', 'Prokofief', 'Prokofiew',
}
```
**CAMBIA AQUÍ** las variantes ortográficas que quieres buscar. Cada palabra va entre comillas, separadas por comas.

**Ejemplos para Beethoven:**
```python
VARIANTES_ORTOGRAFICAS = {
    'beethoven', 'bethowen', 'betoven', 'bethoven',
    'Beethoven', 'Bethowen', 'Betoven', 'Bethoven',
    'BEETHOVEN', 'BETHOWEN', 'BETOVEN',
}
```

**Ejemplos para Wagner:**
```python
VARIANTES_ORTOGRAFICAS = {
    'wagner', 'vagner', 'wágner',
    'Wagner', 'Vagner', 'Wágner',
    'WAGNER', 'VAGNER',
}
```

⚠️ **IMPORTANTE:** No olvides la coma después de cada palabra.

---

### 🔸 1.5 Lista de exclusión
```python
LISTA_EXCLUSION = {
    'profecía',
    'profético',
    'profeta',
}
```
**CAMBIA AQUÍ** las palabras que NO quieres detectar (falsos positivos). Escríbelas en minúsculas.

**Ejemplos para Wagner:**
```python
LISTA_EXCLUSION = {
    'vagar',      # verbo común español
    'vagón',      # palabra común similar
}
```

**Ejemplos para Bach:**
```python
LISTA_EXCLUSION = {
    'bache',      # palabra común española
    'bacha',
}
```

---

### 🔸 1.6 Parámetros de búsqueda

#### UMBRAL_LEVENSHTEIN
```python
UMBRAL_LEVENSHTEIN = 2
```
Cuántos errores tolerar:
- **1** = Muy estricto (solo 1 letra diferente)
- **2** = Normal - **RECOMENDADO PARA OCR**
- **3** = Flexible (3 letras diferentes)
- **4** = Muy flexible (puede dar falsos positivos)

#### MIN_LONGITUD_PALABRA
```python
MIN_LONGITUD_PALABRA = 8
```
Palabras más cortas serán ignoradas.

**Recomendación:** Longitud de tu palabra menos 1 o 2 letras
- Para "Beethoven" (9 letras): usa **7** u **8**
- Para "Bach" (4 letras): usa **3** o **4**
- Para "Piano" (5 letras): usa **4** o **5**

#### VENTANA_CONTEXTO
```python
VENTANA_CONTEXTO = 150
```
Cuántos caracteres mostrar alrededor de la coincidencia:
- **100** = Contexto corto (una frase)
- **150** = Contexto medio - **RECOMENDADO**
- **200** = Contexto amplio (párrafo pequeño)

---

### 🔸 1.8 Emoji (Opcional)
```python
EMOJI = '🎵'
```
**CAMBIA AQUÍ** el emoji que aparecerá en los informes.

**Ejemplos:**
- Música: `🎵` `🎶` `🎼`
- Piano: `🎹`
- Violín: `🎻`
- Guitarra: `🎸`
- Trompeta: `🎺`
- Periódico: `📰`

---

## 📋 PASO 2: Ejecutar el script

### En Mac/Linux:
1. Abre la Terminal
2. Escribe:
```bash
cd ~/Desktop
python3 buscador_generico_palabras.py "/ruta/al/corpus1" "/ruta/al/corpus2"
```

### Ejemplo real:
```bash
python3 buscador_generico_palabras.py "/Users/maria/ElDebate" "/Users/maria/ElSol"
```

### En Windows:
1. Abre CMD o PowerShell
2. Escribe:
```cmd
cd Desktop
python buscador_generico_palabras.py "C:\Users\maria\ElDebate" "C:\Users\maria\ElSol"
```

---

## 📊 PASO 3: Ver los resultados

El script generará varios archivos **por cada corpus**:

### Archivos JSON (datos)
- `resultados_{palabra}_{corpus}.json` → Estadísticas generales
- `todos_contextos_{palabra}_{corpus}.json` → Todos los contextos encontrados

### Archivos HTML (visualización)
- `resultados_{palabra}_{corpus}.html` → **Resumen estadístico** con gráficos
- `resultados_{palabra}_{corpus}_detalle.html` → **Sistema de validación interactivo** ✅

### Archivo TXT (validación manual)
- `validacion_{palabra}_{corpus}_contextos.txt` → Lista de todos los contextos para imprimir

### Archivo comparativo (si buscaste en varios corpus)
- `resultados_{palabra}_TODOS_CORPUS.html` → **Comparativa entre todos los corpus**

---

## ✅ PASO 4: Validar los resultados

1. Abre el archivo `resultados_{palabra}_{corpus}_detalle.html` en tu navegador
2. Verás todos los contextos encontrados
3. Para cada contexto, marca:
   - **✓ Sí** - Es válido
   - **✗ No** - Falso positivo
   - **? Duda** - No estás seguro
4. Puedes añadir notas en cada contexto
5. El progreso se guarda automáticamente cada 30 segundos
6. Cuando termines, haz clic en "💾 Exportar JSON" para descargar los resultados

---

## 💡 EJEMPLOS DE CONFIGURACIÓN COMPLETA

### Ejemplo 1: Buscar "Beethoven"
```python
PALABRA_CLAVE = 'beethoven'
NOMBRE_MOSTRAR = 'Beethoven'
DESCRIPCION = 'Ludwig van Beethoven (1770-1827) - Compositor alemán'
VARIANTES_ORTOGRAFICAS = {
    'beethoven', 'bethowen', 'betoven', 'bethoven',
    'Beethoven', 'Bethowen', 'Betoven', 'Bethoven',
    'BEETHOVEN', 'BETHOWEN', 'BETOVEN',
}
LISTA_EXCLUSION = {
    'bet',
}
UMBRAL_LEVENSHTEIN = 2
MIN_LONGITUD_PALABRA = 7
VENTANA_CONTEXTO = 150
EMOJI = '🎼'
```

### Ejemplo 2: Buscar "Jazz"
```python
PALABRA_CLAVE = 'jazz'
NOMBRE_MOSTRAR = 'Jazz'
DESCRIPCION = 'Género musical afroamericano (siglo XX)'
VARIANTES_ORTOGRAFICAS = {
    'jazz', 'jas', 'jass', 'yaz',
    'Jazz', 'Jas', 'Jass', 'Yaz',
    'JAZZ', 'JAS', 'JASS',
}
LISTA_EXCLUSION = {
    'jas',  # excluir si es muy común
}
UMBRAL_LEVENSHTEIN = 2
MIN_LONGITUD_PALABRA = 3
VENTANA_CONTEXTO = 150
EMOJI = '🎺'
```

### Ejemplo 3: Buscar "Piano"
```python
PALABRA_CLAVE = 'piano'
NOMBRE_MOSTRAR = 'Piano'
DESCRIPCION = 'Instrumento musical de teclado'
VARIANTES_ORTOGRAFICAS = {
    'piano', 'plano',  # OCR confunde i/l
    'Piano', 'Plano',
    'PIANO', 'PLANO',
}
LISTA_EXCLUSION = {
    'plano',  # palabra común española
}
UMBRAL_LEVENSHTEIN = 1
MIN_LONGITUD_PALABRA = 4
VENTANA_CONTEXTO = 150
EMOJI = '🎹'
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "No se encontraron archivos .txt"
**Solución:** Verifica que la ruta al corpus sea correcta y contenga archivos .txt

### ❌ Error: "ModuleNotFoundError"
**Solución:** Instala las librerías necesarias:
```bash
pip3 install --upgrade pip
```
(Este script solo usa librerías estándar de Python, no necesita instalaciones adicionales)

### ❌ Demasiados falsos positivos
**Solución:**
1. Reduce `UMBRAL_LEVENSHTEIN` a **1**
2. Aumenta `MIN_LONGITUD_PALABRA`
3. Añade más palabras a `LISTA_EXCLUSION`

### ❌ No encuentra suficientes ocurrencias
**Solución:**
1. Aumenta `UMBRAL_LEVENSHTEIN` a **3**
2. Añade más variantes a `VARIANTES_ORTOGRAFICAS`
3. Reduce `MIN_LONGITUD_PALABRA`

---

## 🎓 Proyecto Académico

Este proyecto fue desarrollado como parte de:

**PID ID2025/280 LOS SOPORTES EFÍMEROS EN EL AULA UNIVERSITARIA**
coordinado por el Dr. Santiago Ruiz Torres- UNIVERSIDAD DE SALAMANCA

**Grupo de transferencia del conocimiento MUSLYME**
Música, Lenguaje y Medios de Comunicación- UNIVERSIDAD DE SALAMANCA

**LexiMus: Léxico y ontología de la música en español**
PID2022-139589NB-C33 UNIVERSIDAD DE SALAMANCA

Instituciones participantes:
- Universidad de Salamanca
- Instituto Complutense de Ciencias Musicales
- Universidad de La Rioja

## 📧 CONTACTO Y SOPORTE

**Proyecto:** LexiMus USAL - PID2022-139589NB-C33
**Institución:** Universidad de Salamanca

---

## 📜 LICENCIA

Este script es parte del proyecto LexiMus USAL y está disponible para uso académico e investigación.

---

**✨ ¡Buena suerte con tu investigación! ✨**
# Buscador-errores-OCR-
