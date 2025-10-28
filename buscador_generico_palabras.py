#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscador Léxico Genérico - Versión Modificable
Proyecto LexiMus USAL - PID2022-139589NB-C33

Busca palabras específicas en múltiples corpus de textos históricos
Tolerante a errores OCR (hasta ~30% tasa de error)
CON SISTEMA DE VALIDACIÓN MANUAL INTEGRADO

USO:
    python3 buscador_generico_palabras.py /ruta/corpus1 /ruta/corpus2 ...

EJEMPLO:
    python3 buscador_generico_palabras.py "/Users/maria/ElDebate" "/Users/maria/ElSol"

SALIDAS POR CADA CORPUS:
    - resultados_{palabra}_{nombre_corpus}.json
    - todos_contextos_{palabra}_{nombre_corpus}.json
    - resultados_{palabra}_{nombre_corpus}.html
    - resultados_{palabra}_{nombre_corpus}_detalle.html
    - validacion_{palabra}_{nombre_corpus}_contextos.txt

SALIDA GLOBAL:
    - resultados_{palabra}_TODOS_CORPUS.html (comparativa)
"""

# ============================================================================
# ★★★ SECCIÓN 1: CONFIGURACIÓN MODIFICABLE - CAMBIAR AQUÍ ★★★
# ============================================================================
# Esta es la ÚNICA sección que necesitas modificar para buscar diferentes palabras

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 1.1 PALABRA PRINCIPAL A BUSCAR                                          │
# └─────────────────────────────────────────────────────────────────────────┘
# INSTRUCCIONES: Escribe aquí la palabra que quieres buscar EN MINÚSCULAS
# EJEMPLO: 'beethoven', 'wagner', 'jazz', 'piano', etc.

PALABRA_CLAVE = 'prokofieff'
# ← CAMBIA AQUÍ: Escribe tu palabra entre comillas simples, en minúsculas


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 1.2 NOMBRE PARA MOSTRAR EN RESULTADOS                                   │
# └─────────────────────────────────────────────────────────────────────────┘
# INSTRUCCIONES: Escribe cómo quieres que aparezca la palabra en los informes
# EJEMPLO: "Beethoven", "Wagner", "Jazz", "Piano", etc.

NOMBRE_MOSTRAR = 'Prokofieff/Prokofiev'
# ← CAMBIA AQUÍ: Puede incluir mayúsculas, acentos, variantes, etc.


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 1.3 DESCRIPCIÓN O CONTEXTO HISTÓRICO                                    │
# └─────────────────────────────────────────────────────────────────────────┘
# INSTRUCCIONES: Breve descripción que aparecerá en los resultados
# EJEMPLO: "Ludwig van Beethoven (1770-1827) - Compositor alemán"

DESCRIPCION = 'Serguéi Prokófiev (1891-1953) - Compositor ruso'
# ← CAMBIA AQUÍ: Escribe una breve descripción entre comillas


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 1.4 VARIANTES ORTOGRÁFICAS CONOCIDAS                                    │
# └─────────────────────────────────────────────────────────────────────────┘
# INSTRUCCIONES: Lista de variantes ortográficas que quieres buscar
# Cada variante debe ir entre comillas simples, separadas por comas
# EJEMPLO para Beethoven: 'beethoven', 'bethowen', 'betoven', 'Beethoven', etc.
# EJEMPLO para Wagner: 'wagner', 'vagner', 'Wagner', 'Vagner', etc.
# NOTA: Incluye versiones con mayúsculas y minúsculas

VARIANTES_ORTOGRAFICAS = {
    # Variantes en minúsculas
    'prokofieff', 'prokofief', 'prokofiew', 'prokofjew',
    'prokofiev', 'prokoffiev', 'prokoffief',
    'prokofyev', 'prokofyeff',
    'prokofiew', 'prokofjeff', 'prokofyew',
    # Variantes en MAYÚSCULAS
    'PROKOFIEFF', 'PROKOFIEF', 'PROKOFIEW', 'PROKOFJEW',
    'PROKOFIEV', 'PROKOFFIEV', 'PROKOFFIEF',
    # Variantes con capitalización (Primera letra mayúscula)
    'Prokofieff', 'Prokofief', 'Prokofiew', 'Prokofjew',
    'Prokofiev', 'Prokoffiev', 'Prokoffief',
}
# ← CAMBIA AQUÍ: Añade/elimina variantes según tu búsqueda
# FORMATO: Cada palabra entre comillas, separadas por comas
# NO olvides la coma final después de cada palabra


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 1.5 LISTA DE EXCLUSIÓN (Falsos Positivos)                               │
# └─────────────────────────────────────────────────────────────────────────┘
# INSTRUCCIONES: Palabras similares que NO quieres que se detecten
# EJEMPLO para Prokofiev: 'profecía', 'profético' (son palabras comunes españolas)
# EJEMPLO para Wagner: 'vagar', 'vagón' (palabras comunes que se parecen)
# Escribe las palabras EN MINÚSCULAS

LISTA_EXCLUSION = {
    'profecía',     # palabra común española similar a 'prokofiev'
    'profético',
    'profeta',
}
# ← CAMBIA AQUÍ: Añade palabras que quieres EXCLUIR de los resultados
# FORMATO: Cada palabra entre comillas, separadas por comas, en minúsculas


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 1.6 PARÁMETROS DE BÚSQUEDA                                              │
# └─────────────────────────────────────────────────────────────────────────┘
# INSTRUCCIONES: Estos números controlan qué tan "flexible" es la búsqueda

# UMBRAL DE LEVENSHTEIN: Cuántos errores tolerar
# VALORES RECOMENDADOS:
#   1 = Muy estricto (solo 1 letra diferente)
#   2 = Normal (hasta 2 letras diferentes) ← RECOMENDADO PARA OCR
#   3 = Flexible (hasta 3 letras diferentes)
#   4 = Muy flexible (puede dar falsos positivos)
UMBRAL_LEVENSHTEIN = 2
# ← CAMBIA AQUÍ: Cambia el número (1, 2, 3 o 4)

# LONGITUD MÍNIMA DE PALABRA: Palabras más cortas serán ignoradas
# EJEMPLO: Si buscas "Beethoven" (9 letras), pon 7 u 8
#          Si buscas "Bach" (4 letras), pon 3 o 4
# RECOMENDACIÓN: Longitud de tu palabra menos 1 o 2 letras
MIN_LONGITUD_PALABRA = 8
# ← CAMBIA AQUÍ: Cambia el número según tu palabra

# VENTANA DE CONTEXTO: Cuántos caracteres mostrar alrededor de la coincidencia
# VALORES RECOMENDADOS:
#   100 = Contexto corto (una frase)
#   150 = Contexto medio (1-2 frases) ← RECOMENDADO
#   200 = Contexto amplio (párrafo pequeño)
VENTANA_CONTEXTO = 150
# ← CAMBIA AQUÍ: Cambia el número de caracteres de contexto


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 1.7 MAPEO DE CARACTERES PARA ERRORES OCR                                │
# └─────────────────────────────────────────────────────────────────────────┘
# INSTRUCCIONES AVANZADAS: Define qué caracteres se pueden confundir en OCR
# FORMATO: 'letra': '[posibles_variantes]'
# SOLO MODIFICA SI CONOCES EXPRESIONES REGULARES
# Si no estás seguro, DEJA COMO ESTÁ

MAPEO_CARACTERES_OCR = {
    'a': '[aáà4@]',      # a puede ser: a, á, à, 4, @
    'e': '[eé3€]',       # e puede ser: e, é, 3, €
    'i': '[ií1lI|]',     # i puede ser: i, í, 1, l, I, |
    'o': '[oó0OQ]',      # o puede ser: o, ó, 0, O, Q
    'u': '[uú]',         # u puede ser: u, ú
    'n': '[nñ]',         # n puede ser: n, ñ
    'c': '[cC]',         # c puede ser: c, C
    # Añade más mapeos si es necesario
}
# ← CAMBIA AQUÍ SOLO SI ERES USUARIO AVANZADO
# Puedes añadir más letras siguiendo el formato


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 1.8 EMOJI PARA LA PALABRA (Opcional)                                    │
# └─────────────────────────────────────────────────────────────────────────┘
# INSTRUCCIONES: Emoji que aparecerá en los informes HTML
# EJEMPLOS: '🎵' para música, '🎹' para piano, '🎻' para violín, '📰' para prensa

EMOJI = '🎵'
# ← CAMBIA AQUÍ: Elige un emoji representativo


# ============================================================================
# ★★★ FIN DE LA SECCIÓN MODIFICABLE ★★★
# ============================================================================
# ⚠️ NO MODIFIQUES NADA DEBAJO DE ESTA LÍNEA A MENOS QUE SEAS PROGRAMADOR ⚠️
# ============================================================================

import os
import sys
import re
import json
from collections import defaultdict
from datetime import datetime
import unicodedata
from typing import List, Dict, Tuple, Set


# ============================================================================
# CÓDIGO DEL BUSCADOR (NO MODIFICAR)
# ============================================================================

class NormalizadorOCR:
    """Normaliza texto para compensar errores típicos de OCR."""

    @staticmethod
    def normalizar_basico(texto: str) -> str:
        texto = texto.lower()
        texto = ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
        return texto


class GeneradorPatronesFlexibles:
    """Genera expresiones regulares flexibles que capturan variaciones OCR."""

    @staticmethod
    def char_flexible(c: str, mapeo_custom: dict = None) -> str:
        c_lower = c.lower()

        # Usar mapeo personalizado si existe
        if mapeo_custom and c_lower in mapeo_custom:
            return mapeo_custom[c_lower]

        # Mapeo por defecto
        mapeo_default = {
            'a': '[aáà4@]',
            'e': '[eé3€]',
            'i': '[ií1lI|]',
            'o': '[oó0OQ]',
            'u': '[uú]',
            'n': '[nñ]',
        }

        # Combinar mapeos
        mapeo_final = {**mapeo_default, **MAPEO_CARACTERES_OCR}

        return mapeo_final.get(c_lower, f'[{c.lower()}{c.upper()}]')

    @staticmethod
    def generar_patron(palabra: str) -> str:
        patron = r'\b'
        for c in palabra:
            if c.isalpha():
                patron += GeneradorPatronesFlexibles.char_flexible(c)
            else:
                patron += re.escape(c)
        patron += r'\b'
        return patron


class BuscadorGenerico:
    """Buscador genérico de palabras con tolerancia a errores OCR."""

    def __init__(self, nombre_fuente: str, umbral_levenshtein: int = 2,
                 min_longitud_palabra: int = 8, ventana_contexto: int = 150):
        self.nombre_fuente = nombre_fuente
        self.palabra_objetivo = PALABRA_CLAVE
        self.nombre_mostrar = NOMBRE_MOSTRAR
        self.descripcion = DESCRIPCION
        self.umbral_levenshtein = umbral_levenshtein
        self.min_longitud_palabra = min_longitud_palabra
        self.ventana_contexto = ventana_contexto
        self.variantes = VARIANTES_ORTOGRAFICAS
        self.lista_exclusion = LISTA_EXCLUSION

        # Generar patrón flexible
        self.patron = GeneradorPatronesFlexibles.generar_patron(self.palabra_objetivo)

        def crear_metodo_dict():
            return {'exacta': 0, 'variantes': 0, 'fuzzy': 0}

        self.estadisticas = {
            'ocurrencias_totales': 0,
            'archivos_con_ocurrencias': 0,
            'ocurrencias_por_archivo': defaultdict(int),
            'ocurrencias_por_mes': defaultdict(int),
            'ocurrencias_por_mes_metodo': defaultdict(crear_metodo_dict),
            'archivos_procesados': [],
            'contextos': [],
            'todos_contextos_completos': [],
            'metodo_deteccion': defaultdict(int)
        }

        self.metadata = {
            'fecha_analisis': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_archivos_procesados': 0,
            'total_palabras_corpus': 0,
            'corpus_path': '',
            'fuente': nombre_fuente,
            'palabra_buscada': self.nombre_mostrar,
            'umbral_levenshtein': umbral_levenshtein,
            'contexto_historico': self.descripcion
        }

    def distancia_levenshtein(self, s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return self.distancia_levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def buscar_exacta(self, texto: str) -> List[Tuple[int, str]]:
        """Búsqueda con regex flexible"""
        coincidencias = []
        for match in re.finditer(self.patron, texto, re.IGNORECASE):
            palabra_encontrada = match.group()
            # Filtrar exclusiones
            if NormalizadorOCR.normalizar_basico(palabra_encontrada) not in self.lista_exclusion:
                coincidencias.append((match.start(), palabra_encontrada))
        return coincidencias

    def buscar_por_variantes(self, texto: str) -> List[Tuple[int, str]]:
        """Búsqueda por variantes ortográficas conocidas"""
        coincidencias = []
        texto_lower = texto.lower()
        for variante in self.variantes:
            variante_lower = variante.lower()
            # Saltar si está en lista de exclusión
            if variante_lower in self.lista_exclusion:
                continue
            pos = 0
            while pos < len(texto_lower):
                pos = texto_lower.find(variante_lower, pos)
                if pos == -1:
                    break
                # Verificar que sea palabra completa (boundary check)
                if pos > 0 and texto_lower[pos-1].isalnum():
                    pos += 1
                    continue
                fin = pos + len(variante_lower)
                if fin < len(texto_lower) and texto_lower[fin].isalnum():
                    pos += 1
                    continue
                coincidencias.append((pos, variante))
                pos += len(variante)
        return coincidencias

    def buscar_fuzzy(self, texto: str) -> List[Tuple[int, str, int]]:
        """Búsqueda fuzzy con Levenshtein"""
        palabra_norm = NormalizadorOCR.normalizar_basico(self.palabra_objetivo)
        primera_letra_objetivo = palabra_norm[0] if palabra_norm else ''
        coincidencias_fuzzy = []

        for match in re.finditer(r'\b\w+\b', texto):
            palabra_texto = match.group()

            if len(palabra_texto) < self.min_longitud_palabra:
                continue
            if sum(1 for c in palabra_texto if not c.isalnum()) > len(palabra_texto) * 0.3:
                continue

            palabra_texto_norm = NormalizadorOCR.normalizar_basico(palabra_texto)

            if palabra_texto_norm.lower() in self.lista_exclusion:
                continue

            # Verificar primera letra
            if palabra_texto_norm and primera_letra_objetivo:
                primera_letra_texto = palabra_texto_norm[0]
                if primera_letra_texto != primera_letra_objetivo:
                    continue

            # Ratio de longitud más tolerante para variantes ortográficas
            ratio_longitud = len(palabra_texto_norm) / len(palabra_norm)
            if not (0.75 <= ratio_longitud <= 1.25):
                continue

            distancia = self.distancia_levenshtein(palabra_norm, palabra_texto_norm)

            if distancia <= self.umbral_levenshtein:
                coincidencias_fuzzy.append((match.start(), palabra_texto, distancia))

        return coincidencias_fuzzy

    def extraer_contexto(self, texto: str, posicion: int) -> str:
        """Extrae contexto ampliado alrededor de la coincidencia"""
        inicio = max(0, posicion - self.ventana_contexto)
        fin = min(len(texto), posicion + self.ventana_contexto)
        return texto[inicio:fin].replace('\n', ' ').strip()

    def extraer_fecha_archivo(self, nombre_archivo: str) -> str:
        """Extrae fecha en formato YYYY-MM del nombre del archivo"""
        match = re.match(r'(\d{4})(\d{2})\d{2}', nombre_archivo)
        if match:
            año = match.group(1)
            mes = match.group(2)
            return f"{año}-{mes}"
        return None

    def analizar_archivo(self, ruta_archivo: str) -> Dict:
        try:
            with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
                texto = f.read()
        except Exception as e:
            print(f"  ⚠️  Error leyendo {os.path.basename(ruta_archivo)}: {e}")
            return None

        # Contar palabras válidas
        texto_norm = NormalizadorOCR.normalizar_basico(texto)
        tokens = re.findall(r'\b[a-záéíóúüñ]+\b', texto_norm)
        total_palabras_validas = len(tokens)
        self.metadata['total_palabras_corpus'] += total_palabras_validas

        nombre_archivo = os.path.basename(ruta_archivo)
        fecha_mes = self.extraer_fecha_archivo(nombre_archivo)

        # Realizar búsquedas
        coincidencias_exactas = self.buscar_exacta(texto)
        coincidencias_variantes = self.buscar_por_variantes(texto)
        posiciones_exactas = {pos for pos, _ in coincidencias_exactas}
        coincidencias_variantes_unicas = [
            (pos, match) for pos, match in coincidencias_variantes
            if pos not in posiciones_exactas
        ]

        coincidencias_fuzzy = self.buscar_fuzzy(texto)
        posiciones_previas = posiciones_exactas | {pos for pos, _ in coincidencias_variantes_unicas}
        coincidencias_fuzzy_unicas = [
            (pos, match, dist) for pos, match, dist in coincidencias_fuzzy
            if pos not in posiciones_previas
        ]

        total_ocurrencias = (
            len(coincidencias_exactas) +
            len(coincidencias_variantes_unicas) +
            len(coincidencias_fuzzy_unicas)
        )

        if total_ocurrencias > 0:
            self.estadisticas['ocurrencias_totales'] += total_ocurrencias
            self.estadisticas['archivos_con_ocurrencias'] += 1
            self.estadisticas['ocurrencias_por_archivo'][ruta_archivo] = total_ocurrencias
            self.estadisticas['metodo_deteccion']['exacta'] += len(coincidencias_exactas)
            self.estadisticas['metodo_deteccion']['variantes'] += len(coincidencias_variantes_unicas)
            self.estadisticas['metodo_deteccion']['fuzzy'] += len(coincidencias_fuzzy_unicas)

            if fecha_mes:
                self.estadisticas['ocurrencias_por_mes'][fecha_mes] += total_ocurrencias
                self.estadisticas['ocurrencias_por_mes_metodo'][fecha_mes]['exacta'] += len(coincidencias_exactas)
                self.estadisticas['ocurrencias_por_mes_metodo'][fecha_mes]['variantes'] += len(coincidencias_variantes_unicas)
                self.estadisticas['ocurrencias_por_mes_metodo'][fecha_mes]['fuzzy'] += len(coincidencias_fuzzy_unicas)

            # Guardar TODOS los contextos completos
            for pos, match in coincidencias_exactas:
                self.estadisticas['todos_contextos_completos'].append({
                    'metodo': 'exacta',
                    'coincidencia': match,
                    'contexto': self.extraer_contexto(texto, pos),
                    'archivo': nombre_archivo,
                    'fuente': self.nombre_fuente,
                    'distancia': 0,
                    'validado': None,
                    'notas': ''
                })

            for pos, match in coincidencias_variantes_unicas:
                self.estadisticas['todos_contextos_completos'].append({
                    'metodo': 'variantes',
                    'coincidencia': match,
                    'contexto': self.extraer_contexto(texto, pos),
                    'archivo': nombre_archivo,
                    'fuente': self.nombre_fuente,
                    'distancia': 0,
                    'validado': None,
                    'notas': ''
                })

            for pos, match, dist in coincidencias_fuzzy_unicas:
                self.estadisticas['todos_contextos_completos'].append({
                    'metodo': 'fuzzy',
                    'coincidencia': match,
                    'contexto': self.extraer_contexto(texto, pos),
                    'archivo': nombre_archivo,
                    'fuente': self.nombre_fuente,
                    'distancia': dist,
                    'validado': None,
                    'notas': ''
                })

            # Guardar ejemplos para estadísticas
            if len(self.estadisticas['contextos']) < 50:
                for pos, match in coincidencias_exactas[:2]:
                    self.estadisticas['contextos'].append({
                        'metodo': 'exacta',
                        'coincidencia': match,
                        'contexto': self.extraer_contexto(texto, pos),
                        'archivo': nombre_archivo,
                        'fuente': self.nombre_fuente
                    })

                if coincidencias_fuzzy_unicas and len(self.estadisticas['contextos']) < 50:
                    pos, match, dist = coincidencias_fuzzy_unicas[0]
                    self.estadisticas['contextos'].append({
                        'metodo': 'fuzzy',
                        'coincidencia': match,
                        'distancia': dist,
                        'contexto': self.extraer_contexto(texto, pos),
                        'archivo': nombre_archivo,
                        'fuente': self.nombre_fuente
                    })

            return {
                'archivo': nombre_archivo,
                'ruta': ruta_archivo,
                'ocurrencias': total_ocurrencias
            }

        return None

    def procesar_corpus(self, directorio_corpus: str):
        if not os.path.exists(directorio_corpus):
            print(f"\n❌ ERROR: El directorio no existe: {directorio_corpus}")
            return False
        if not os.path.isdir(directorio_corpus):
            print(f"\n❌ ERROR: La ruta no es un directorio: {directorio_corpus}")
            return False

        self.metadata['corpus_path'] = directorio_corpus

        print(f"\n📁 Fuente: {self.nombre_fuente}")
        print(f"   Ruta: {directorio_corpus}")
        print(f"   Buscando: {self.nombre_mostrar}")

        archivos_txt = []
        for root, dirs, files in os.walk(directorio_corpus):
            for file in files:
                if file.endswith('.txt'):
                    archivos_txt.append(os.path.join(root, file))

        total_archivos = len(archivos_txt)
        self.metadata['total_archivos_procesados'] = total_archivos

        if total_archivos == 0:
            print(f"   ⚠️  No se encontraron archivos .txt")
            return False

        print(f"   📄 Archivos .txt encontrados: {total_archivos}")

        archivos_con_resultados = []
        for i, archivo in enumerate(archivos_txt, 1):
            if i % 100 == 0 or i == 1 or i == total_archivos:
                print(f"      Procesando: {i}/{total_archivos} archivos...")

            resultado = self.analizar_archivo(archivo)
            if resultado:
                archivos_con_resultados.append(resultado)

        print(f"   ✓ Archivos con coincidencias: {len(archivos_con_resultados)}")
        return True

    def mostrar_resumen(self):
        stats = self.estadisticas
        total = stats['ocurrencias_totales']
        archivos = stats['archivos_con_ocurrencias']
        total_archivos = self.metadata.get('total_archivos_procesados', 1)
        porcentaje = (archivos / total_archivos * 100) if total_archivos > 0 else 0
        total_contextos_completos = len(stats['todos_contextos_completos'])

        print(f"\n   📊 FUENTE: {self.nombre_fuente}")
        print(f"      Ocurrencias totales: {total:,}")
        print(f"      Contextos completos: {total_contextos_completos:,}")
        print(f"      Archivos con coincidencias: {archivos:,} ({porcentaje:.2f}% del total)")

        total_palabras = self.metadata.get('total_palabras_corpus', 1)
        if total_palabras > 0:
            freq_rel = stats['ocurrencias_totales'] / total_palabras
            print(f"      Frecuencia relativa: {freq_rel:.6f} ({freq_rel*1000:.2f} por mil palabras)")

        if total > 0:
            total_metodos = sum(stats['metodo_deteccion'].values())
            print(f"      Métodos de detección:")
            for metodo, count in sorted(stats['metodo_deteccion'].items(),
                                       key=lambda x: x[1], reverse=True):
                pct = (count / total_metodos * 100) if total_metodos > 0 else 0
                print(f"         • {metodo:12}: {count:6,} ({pct:5.1f}%)")

    def guardar_json(self, nombre_archivo: str = None):
        """Guarda resultados estadísticos en JSON"""
        palabra_simple = self.palabra_objetivo.replace(' ', '_').lower()
        if nombre_archivo is None:
            nombre_archivo = f"resultados_{palabra_simple}_{self.nombre_fuente}.json"

        ocurrencias_temporales = sorted(
            [{'mes': k, 'ocurrencias': v} for k, v in self.estadisticas['ocurrencias_por_mes'].items()],
            key=lambda x: x['mes']
        )

        total_archivos = self.metadata.get('total_archivos_procesados', 1)
        porcentaje_archivos = (self.estadisticas['archivos_con_ocurrencias'] / total_archivos * 100) if total_archivos > 0 else 0

        resultados = {
            'ocurrencias_totales': self.estadisticas['ocurrencias_totales'],
            'archivos_con_ocurrencias': self.estadisticas['archivos_con_ocurrencias'],
            'porcentaje_archivos_con_palabra': round(porcentaje_archivos, 2),
            'metodo_deteccion': dict(self.estadisticas['metodo_deteccion']),
            'frecuencia_relativa': self.estadisticas['ocurrencias_totales'] / self.metadata.get('total_palabras_corpus', 1),
            'linea_temporal': ocurrencias_temporales,
            'contextos_ejemplos': self.estadisticas['contextos'][:20],
            'top_archivos': sorted(
                [{'archivo': os.path.basename(k), 'ocurrencias': v}
                 for k, v in self.estadisticas['ocurrencias_por_archivo'].items()],
                key=lambda x: x['ocurrencias'],
                reverse=True
            )[:20]
        }

        output = {
            'metadata': self.metadata,
            'palabra_objetivo': self.nombre_mostrar,
            'umbral_levenshtein': self.umbral_levenshtein,
            'estrategias': [
                'Búsqueda exacta con regex flexible',
                'Búsqueda por variantes ortográficas',
                'Búsqueda fuzzy con Levenshtein'
            ],
            'resultados': resultados
        }

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"   ✓ JSON guardado: {nombre_archivo}")

    def guardar_todos_contextos_json(self, nombre_archivo: str = None):
        """Guarda TODOS los contextos en JSON separado"""
        palabra_simple = self.palabra_objetivo.replace(' ', '_').lower()
        if nombre_archivo is None:
            nombre_archivo = f"todos_contextos_{palabra_simple}_{self.nombre_fuente}.json"

        output = {
            'metadata': self.metadata,
            'palabra_objetivo': self.nombre_mostrar,
            'total_contextos': len(self.estadisticas['todos_contextos_completos']),
            'contextos': self.estadisticas['todos_contextos_completos']
        }

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"   ✓ JSON con TODOS los contextos guardado: {nombre_archivo}")
        print(f"      Total de contextos: {len(self.estadisticas['todos_contextos_completos']):,}")

    def generar_txt_detalle(self, nombre_archivo: str = None):
        """Genera archivo TXT con todos los contextos para validación manual"""
        palabra_simple = self.palabra_objetivo.replace(' ', '_').lower()
        if nombre_archivo is None:
            nombre_archivo = f"validacion_{palabra_simple}_{self.nombre_fuente}_contextos.txt"

        todos_contextos = self.estadisticas['todos_contextos_completos']

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"VALIDACIÓN MANUAL: '{self.nombre_mostrar}'\n")
            f.write(f"Fuente: {self.nombre_fuente}\n")
            f.write(f"Fecha análisis: {self.metadata['fecha_analisis']}\n")
            f.write(f"Total contextos: {len(todos_contextos):,}\n")
            f.write(f"Descripción: {self.descripcion}\n")
            f.write("=" * 80 + "\n\n")

            # Estadísticas por método
            metodos = {'exacta': 0, 'variantes': 0, 'fuzzy': 0}
            for ctx in todos_contextos:
                metodos[ctx['metodo']] += 1

            f.write("ESTADÍSTICAS POR MÉTODO DE DETECCIÓN:\n")
            f.write("-" * 80 + "\n")
            for metodo, count in metodos.items():
                porcentaje = (count / len(todos_contextos) * 100) if todos_contextos else 0
                f.write(f"  {metodo.upper():12}: {count:6,} ({porcentaje:5.1f}%)\n")
            f.write("\n" + "=" * 80 + "\n\n")

            # Listar todos los contextos
            for idx, ctx in enumerate(todos_contextos, 1):
                f.write(f"CONTEXTO #{idx}\n")
                f.write("-" * 80 + "\n")
                f.write(f"Fuente:       {ctx['fuente']}\n")
                f.write(f"Archivo:      {ctx['archivo']}\n")
                f.write(f"Método:       {ctx['metodo'].upper()}\n")
                f.write(f"Coincidencia: '{ctx['coincidencia']}'\n")

                if ctx['distancia'] > 0:
                    f.write(f"Distancia:    {ctx['distancia']} (Levenshtein)\n")

                f.write("\nCONTEXTO:\n")
                f.write("-" * 80 + "\n")

                # Formatear el contexto
                contexto_formateado = ctx['contexto'].replace('\n', ' ').strip()
                palabras = contexto_formateado.split()
                lineas = []
                linea_actual = ""

                for palabra_ctx in palabras:
                    if len(linea_actual) + len(palabra_ctx) + 1 <= 76:
                        if linea_actual:
                            linea_actual += " " + palabra_ctx
                        else:
                            linea_actual = palabra_ctx
                    else:
                        if linea_actual:
                            lineas.append(linea_actual)
                        linea_actual = palabra_ctx

                if linea_actual:
                    lineas.append(linea_actual)

                for linea in lineas:
                    f.write("    " + linea + "\n")

                f.write("\n")
                f.write("VALIDACIÓN: [ ] SÍ  [ ] NO  [ ] DUDA\n")
                f.write("NOTAS: _________________________________________________________\n")
                f.write("\n" + "=" * 80 + "\n\n")

        return nombre_archivo

    def generar_html_detalle(self, nombre_archivo: str = None):
        """Genera página HTML de detalle CON VALIDACIÓN INTEGRADA"""
        palabra_simple = self.palabra_objetivo.replace(' ', '_').lower()
        if nombre_archivo is None:
            nombre_archivo = f"resultados_{palabra_simple}_{self.nombre_fuente}_detalle.html"

        todos_contextos = self.estadisticas['todos_contextos_completos']
        nombre_fuente = self.nombre_fuente

        ITEMS_POR_PAGINA = 100

        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{nombre_fuente} - Detalle: {self.nombre_mostrar} - LexiMus USAL</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .back-button {{
            display: inline-block;
            margin: 20px;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: background 0.3s;
        }}
        .back-button:hover {{ background: #5568d3; }}

        .stats-bar {{
            background: #f8f9fa;
            padding: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        .stat-box {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }}

        .section {{ padding: 40px; }}
        .filters {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        .filter-group {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        .filter-group label {{
            font-weight: 600;
            color: #2c3e50;
        }}
        select, input {{
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 0.95em;
        }}

        .context-item {{
            background: #fff;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }}
        .context-item:hover {{
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        .context-item.validated-si {{
            border-color: #4caf50;
            background: #f1f8f4;
        }}
        .context-item.validated-no {{
            border-color: #f44336;
            background: #fef5f5;
        }}
        .context-item.validated-duda {{
            border-color: #ff9800;
            background: #fff8e1;
        }}

        .context-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .context-meta {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .badge-metodo {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        .badge-distancia {{
            background: #ffebee;
            color: #c62828;
        }}
        .badge-archivo {{
            background: #f3e5f5;
            color: #7b1fa2;
        }}

        .coincidencia-box {{
            background: #fff59d;
            padding: 8px 12px;
            border-radius: 5px;
            margin-bottom: 10px;
            font-weight: bold;
            color: #f57f17;
            text-align: center;
        }}
        .context-text {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-family: Georgia, serif;
            line-height: 1.8;
            color: #2c3e50;
            white-space: pre-wrap;
        }}

        .validation-buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }}
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 0.9em;
        }}
        .btn-valid {{
            background: #4caf50;
            color: white;
        }}
        .btn-valid:hover {{
            background: #45a049;
            transform: scale(1.05);
        }}
        .btn-invalid {{
            background: #f44336;
            color: white;
        }}
        .btn-invalid:hover {{
            background: #da190b;
            transform: scale(1.05);
        }}
        .btn-doubt {{
            background: #ff9800;
            color: white;
        }}
        .btn-doubt:hover {{
            background: #f57c00;
            transform: scale(1.05);
        }}
        .btn-reset {{
            background: #9e9e9e;
            color: white;
        }}
        .btn-reset:hover {{
            background: #757575;
        }}

        .notes-input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-family: inherit;
            resize: vertical;
            min-height: 60px;
        }}

        .export-section {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 250px;
        }}
        .btn-export {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9em;
            width: 100%;
            margin-bottom: 10px;
        }}
        .btn-export:hover {{
            transform: scale(1.05);
        }}
        .btn-export.secondary {{
            background: #9e9e9e;
            font-size: 0.85em;
            padding: 8px 15px;
        }}
        .btn-export.secondary:hover {{
            background: #757575;
        }}
        .btn-export.danger {{
            background: #f44336;
            font-size: 0.85em;
            padding: 8px 15px;
        }}
        .btn-export.danger:hover {{
            background: #da190b;
        }}
        .progress-info {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        .save-indicator {{
            text-align: center;
            color: #4caf50;
            font-size: 0.8em;
            margin-top: 5px;
            opacity: 0;
            transition: opacity 0.3s;
            font-weight: 600;
        }}

        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 30px 0;
            flex-wrap: wrap;
        }}
        .pagination button {{
            padding: 10px 15px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .pagination button:hover {{
            background: #667eea;
            color: white;
        }}
        .pagination button:disabled {{
            background: #e0e0e0;
            border-color: #e0e0e0;
            color: #999;
            cursor: not-allowed;
        }}
        .pagination button.active {{
            background: #667eea;
            color: white;
        }}
        .pagination-info {{
            padding: 10px 20px;
            background: #f8f9fa;
            border-radius: 5px;
            font-weight: 600;
            color: #2c3e50;
        }}

        footer {{
            background: #2d3748;
            color: white;
            padding: 30px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📰 {nombre_fuente}</h1>
            <h2 style="font-size: 1.8em; margin-top: 15px;">📊 Resultados Detallados: "{self.nombre_mostrar}"</h2>
            <p style="margin-top: 10px;">Proyecto LexiMus USAL - PID2022-139589NB-C33</p>
            <p style="margin-top: 10px; font-size: 1.1em;">✅ Sistema de Validación Manual Integrado</p>
            <p style="margin-top: 10px; font-size: 0.95em;">{EMOJI} {self.descripcion}</p>
        </header>

        <div class="stats-bar">
            <div class="stat-box">
                <div class="stat-number" id="total-contextos">{len(todos_contextos)}</div>
                <div class="stat-label">Total Contextos</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="validados">0</div>
                <div class="stat-label">Sí ✓</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="invalidos">0</div>
                <div class="stat-label">No ✗</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="dudosos">0</div>
                <div class="stat-label">Duda ?</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="pendientes">{len(todos_contextos)}</div>
                <div class="stat-label">Pendientes</div>
            </div>
        </div>

        <a href="resultados_{palabra_simple}_{nombre_fuente}.html" class="back-button">← Volver al Resumen</a>

        <div class="section">
            <div class="filters">
                <div class="filter-group">
                    <label>Método:</label>
                    <select id="filter-metodo">
                        <option value="">Todos</option>
                        <option value="exacta">Exacta</option>
                        <option value="variantes">Variantes</option>
                        <option value="fuzzy">Fuzzy</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Estado:</label>
                    <select id="filter-estado">
                        <option value="">Todos</option>
                        <option value="pendiente">Pendientes</option>
                        <option value="si">Sí</option>
                        <option value="no">No</option>
                        <option value="duda">Duda</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Buscar:</label>
                    <input type="text" id="search-box" placeholder="Buscar en contextos...">
                </div>
            </div>

            <div id="contextos-container">
                <!-- Los contextos se insertarán aquí dinámicamente -->
            </div>

            <div class="pagination" id="pagination-controls">
                <!-- Los controles de paginación se insertarán aquí dinámicamente -->
            </div>
        </div>

        <footer>
            <p><strong>LexiMus USAL</strong> - PID2022-139589NB-C33</p>
            <p style="margin-top: 10px;">{EMOJI} {self.descripcion}</p>
        </footer>
    </div>

    <div class="export-section">
        <button class="btn-export" onclick="exportarValidacion()">💾 Exportar JSON</button>
        <button class="btn-export" onclick="guardarProgreso()">💿 Guardar Ahora</button>
        <button class="btn-export secondary" onclick="recuperarRespaldo()">🔄 Recuperar Respaldo</button>
        <button class="btn-export danger" onclick="limpiarAlmacenamiento()">🗑️ Limpiar Todo</button>
        <div class="progress-info">
            <strong id="progreso-porcentaje">0%</strong> completado
        </div>
        <div class="save-indicator" id="save-indicator">Guardado</div>
    </div>

    <script>
        const contextos = {json.dumps(todos_contextos, ensure_ascii=False, indent=2)};
        const palabraBuscada = "{self.nombre_mostrar}";
        const nombreFuente = "{nombre_fuente}";
        const ITEMS_POR_PAGINA = {ITEMS_POR_PAGINA};
        const STORAGE_KEY = 'validacion_{palabra_simple}_' + nombreFuente.replace(/[^a-zA-Z0-9]/g, '_');

        let validacionState = contextos.map(c => ({{
            ...c,
            validado: c.validado || null,
            notas: c.notas || ''
        }}));

        let paginaActual = 1;
        let datosFiltrados = validacionState;

        function cargarEstadoGuardado() {{
            try {{
                const estadoGuardado = localStorage.getItem(STORAGE_KEY);
                const timestamp = localStorage.getItem(STORAGE_KEY + '_timestamp');

                if (estadoGuardado) {{
                    const fecha = timestamp ? new Date(timestamp).toLocaleString('es-ES') : 'Desconocida';
                    const confirmRestore = confirm(`Se encontró una validación guardada del: ${{fecha}}\\n\\n¿Deseas continuar desde donde lo dejaste?`);
                    if (confirmRestore) {{
                        validacionState = JSON.parse(estadoGuardado);
                        console.log('Estado restaurado:', validacionState.length, 'contextos');
                        return true;
                    }}
                }}
                return false;
            }} catch (e) {{
                console.error('Error al cargar estado guardado:', e);
                return false;
            }}
        }}

        cargarEstadoGuardado();

        function actualizarEstadisticas() {{
            const validados = validacionState.filter(c => c.validado === 'si').length;
            const invalidos = validacionState.filter(c => c.validado === 'no').length;
            const dudosos = validacionState.filter(c => c.validado === 'duda').length;
            const pendientes = validacionState.filter(c => c.validado === null).length;

            document.getElementById('validados').textContent = validados;
            document.getElementById('invalidos').textContent = invalidos;
            document.getElementById('dudosos').textContent = dudosos;
            document.getElementById('pendientes').textContent = pendientes;

            const porcentaje = Math.round((validados + invalidos + dudosos) / validacionState.length * 100);
            document.getElementById('progreso-porcentaje').textContent = porcentaje + '%';
        }}

        function renderizarContextos(filtrados = null) {{
            const container = document.getElementById('contextos-container');
            const datos = filtrados || validacionState;
            datosFiltrados = datos;

            if (datos.length === 0) {{
                container.innerHTML = '<p style="text-align:center;color:#999;padding:40px;">No hay contextos que mostrar con los filtros aplicados</p>';
                document.getElementById('pagination-controls').innerHTML = '';
                return;
            }}

            const totalPaginas = Math.ceil(datos.length / ITEMS_POR_PAGINA);
            const inicio = (paginaActual - 1) * ITEMS_POR_PAGINA;
            const fin = Math.min(inicio + ITEMS_POR_PAGINA, datos.length);
            const datosPagina = datos.slice(inicio, fin);

            container.innerHTML = datosPagina.map((ctx, idx) => {{
                const realIdx = validacionState.indexOf(ctx);
                const estadoClass = ctx.validado === 'si' ? 'validated-si' :
                                   ctx.validado === 'no' ? 'validated-no' :
                                   ctx.validado === 'duda' ? 'validated-duda' : '';

                const distanciaBadge = ctx.distancia > 0 ?
                    `<span class="badge badge-distancia">Distancia: ${{ctx.distancia}}</span>` : '';

                return `
                    <div class="context-item ${{estadoClass}}" id="context-${{realIdx}}">
                        <div class="context-header">
                            <div class="context-meta">
                                <span class="badge badge-metodo">${{ctx.metodo.toUpperCase()}}</span>
                                ${{distanciaBadge}}
                                <span class="badge badge-archivo">${{ctx.archivo}}</span>
                            </div>
                        </div>

                        <div class="coincidencia-box">
                            Coincidencia encontrada: "${{ctx.coincidencia}}"
                        </div>

                        <div class="context-text">${{ctx.contexto}}</div>

                        <div class="validation-buttons">
                            <button class="btn btn-valid" onclick="validar(${{realIdx}}, 'si')">
                                ✓ Sí - Es válido
                            </button>
                            <button class="btn btn-invalid" onclick="validar(${{realIdx}}, 'no')">
                                ✗ No - Falso positivo
                            </button>
                            <button class="btn btn-doubt" onclick="validar(${{realIdx}}, 'duda')">
                                ? Duda
                            </button>
                            <button class="btn btn-reset" onclick="validar(${{realIdx}}, null)">
                                ↺ Reiniciar
                            </button>
                        </div>

                        <textarea class="notes-input"
                                  placeholder="Notas opcionales..."
                                  onchange="agregarNota(${{realIdx}}, this.value)">${{ctx.notas}}</textarea>
                    </div>
                `;
            }}).join('');

            renderizarPaginacion(totalPaginas, datos.length);
        }}

        function renderizarPaginacion(totalPaginas, totalItems) {{
            const paginationContainer = document.getElementById('pagination-controls');

            if (totalPaginas <= 1) {{
                paginationContainer.innerHTML = '';
                return;
            }}

            const inicio = (paginaActual - 1) * ITEMS_POR_PAGINA + 1;
            const fin = Math.min(paginaActual * ITEMS_POR_PAGINA, totalItems);

            let html = `
                <button onclick="cambiarPagina(1)" ${{paginaActual === 1 ? 'disabled' : ''}}>
                    ⏮️ Primera
                </button>
                <button onclick="cambiarPagina(${{paginaActual - 1}})" ${{paginaActual === 1 ? 'disabled' : ''}}>
                    ◀️ Anterior
                </button>
                <span class="pagination-info">
                    Página ${{paginaActual}} de ${{totalPaginas}} | Mostrando ${{inicio}}-${{fin}} de ${{totalItems}}
                </span>
                <button onclick="cambiarPagina(${{paginaActual + 1}})" ${{paginaActual === totalPaginas ? 'disabled' : ''}}>
                    Siguiente ▶️
                </button>
                <button onclick="cambiarPagina(${{totalPaginas}})" ${{paginaActual === totalPaginas ? 'disabled' : ''}}>
                    Última ⏭️
                </button>
            `;

            paginationContainer.innerHTML = html;
        }}

        function cambiarPagina(nuevaPagina) {{
            paginaActual = nuevaPagina;
            renderizarContextos(datosFiltrados);
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function validar(idx, estado) {{
            validacionState[idx].validado = estado;
            actualizarEstadisticas();
            aplicarFiltros();
            guardarEnLocalStorage();
        }}

        function agregarNota(idx, nota) {{
            validacionState[idx].notas = nota;
            guardarEnLocalStorage();
        }}

        function aplicarFiltros() {{
            const metodo = document.getElementById('filter-metodo').value;
            const estado = document.getElementById('filter-estado').value;
            const busqueda = document.getElementById('search-box').value.toLowerCase();

            let filtrados = validacionState;

            if (metodo) {{
                filtrados = filtrados.filter(c => c.metodo === metodo);
            }}

            if (estado === 'pendiente') {{
                filtrados = filtrados.filter(c => c.validado === null);
            }} else if (estado === 'si') {{
                filtrados = filtrados.filter(c => c.validado === 'si');
            }} else if (estado === 'no') {{
                filtrados = filtrados.filter(c => c.validado === 'no');
            }} else if (estado === 'duda') {{
                filtrados = filtrados.filter(c => c.validado === 'duda');
            }}

            if (busqueda) {{
                filtrados = filtrados.filter(c =>
                    c.contexto.toLowerCase().includes(busqueda) ||
                    c.coincidencia.toLowerCase().includes(busqueda) ||
                    c.archivo.toLowerCase().includes(busqueda)
                );
            }}

            paginaActual = 1;
            renderizarContextos(filtrados);
        }}

        function guardarEnLocalStorage() {{
            try {{
                const dataStr = JSON.stringify(validacionState);
                localStorage.setItem(STORAGE_KEY, dataStr);

                const timestamp = new Date().toISOString();
                localStorage.setItem(STORAGE_KEY + '_backup', dataStr);
                localStorage.setItem(STORAGE_KEY + '_timestamp', timestamp);

                mostrarMensajeGuardado('Guardado automático exitoso');
                return true;
            }} catch (e) {{
                console.error('Error al guardar:', e);
                return false;
            }}
        }}

        function mostrarMensajeGuardado(mensaje) {{
            const indicador = document.getElementById('save-indicator');
            if (indicador) {{
                indicador.textContent = mensaje;
                indicador.style.opacity = '1';
                setTimeout(() => {{
                    indicador.style.opacity = '0';
                }}, 2000);
            }}
        }}

        function guardarProgreso() {{
            if (guardarEnLocalStorage()) {{
                const timestamp = localStorage.getItem(STORAGE_KEY + '_timestamp');
                alert('✓ Progreso guardado correctamente\\n\\nFecha: ' + new Date(timestamp).toLocaleString('es-ES'));
            }}
        }}

        function exportarValidacion() {{
            try {{
                const exportData = {{
                    palabra: palabraBuscada,
                    fuente: nombreFuente,
                    fecha_exportacion: new Date().toISOString(),
                    total_contextos: validacionState.length,
                    validados: validacionState.filter(c => c.validado === 'si').length,
                    invalidos: validacionState.filter(c => c.validado === 'no').length,
                    dudosos: validacionState.filter(c => c.validado === 'duda').length,
                    pendientes: validacionState.filter(c => c.validado === null).length,
                    contextos: validacionState
                }};

                const dataStr = JSON.stringify(exportData, null, 2);
                const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);

                const exportFileDefaultName = `validacion_{palabra_simple}_${{nombreFuente}}_${{new Date().toISOString().split('T')[0]}}.json`;

                const linkElement = document.createElement('a');
                linkElement.setAttribute('href', dataUri);
                linkElement.setAttribute('download', exportFileDefaultName);
                linkElement.click();

                mostrarMensajeGuardado('Validación exportada correctamente');
            }} catch (e) {{
                console.error('Error al exportar:', e);
                alert('⚠️ Error al exportar: ' + e.message);
            }}
        }}

        function recuperarRespaldo() {{
            const backup = localStorage.getItem(STORAGE_KEY + '_backup');
            const timestamp = localStorage.getItem(STORAGE_KEY + '_timestamp');

            if (backup) {{
                const fecha = timestamp ? new Date(timestamp).toLocaleString('es-ES') : 'Desconocida';
                const confirmar = confirm(`Se encontró un respaldo del: ${{fecha}}\\n\\n¿Deseas recuperarlo?`);
                if (confirmar) {{
                    validacionState = JSON.parse(backup);
                    actualizarEstadisticas();
                    renderizarContextos();
                    alert('✓ Respaldo recuperado correctamente');
                }}
            }} else {{
                alert('⚠️ No se encontró ningún respaldo');
            }}
        }}

        function limpiarAlmacenamiento() {{
            const confirmar = confirm('⚠️ ADVERTENCIA: Esto eliminará toda la validación.\\n\\n¿Estás seguro?');
            if (confirmar) {{
                localStorage.removeItem(STORAGE_KEY);
                localStorage.removeItem(STORAGE_KEY + '_backup');
                localStorage.removeItem(STORAGE_KEY + '_timestamp');
                alert('✓ Almacenamiento limpiado. Recarga la página.');
            }}
        }}

        document.getElementById('filter-metodo').addEventListener('change', aplicarFiltros);
        document.getElementById('filter-estado').addEventListener('change', aplicarFiltros);
        document.getElementById('search-box').addEventListener('input', aplicarFiltros);

        actualizarEstadisticas();
        renderizarContextos();

        setInterval(() => {{
            guardarEnLocalStorage();
        }}, 30000);

        window.addEventListener('beforeunload', (e) => {{
            guardarEnLocalStorage();
        }});
    </script>
</body>
</html>
"""

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return nombre_archivo

    def generar_html(self, nombre_archivo: str = None):
        """HTML principal de resumen"""
        palabra_simple = self.palabra_objetivo.replace(' ', '_').lower()
        if nombre_archivo is None:
            nombre_archivo = f"resultados_{palabra_simple}_{self.nombre_fuente}.html"

        nombre_fuente = self.nombre_fuente
        stats = self.estadisticas

        total_metodos = sum(stats['metodo_deteccion'].values())
        pct_exacta = (stats['metodo_deteccion']['exacta'] / total_metodos * 100) if total_metodos > 0 else 0
        pct_variantes = (stats['metodo_deteccion']['variantes'] / total_metodos * 100) if total_metodos > 0 else 0
        pct_fuzzy = (stats['metodo_deteccion']['fuzzy'] / total_metodos * 100) if total_metodos > 0 else 0

        total_archivos = self.metadata.get('total_archivos_procesados', 1)
        porcentaje_archivos = (stats['archivos_con_ocurrencias'] / total_archivos * 100) if total_archivos > 0 else 0
        total_contextos_completos = len(stats['todos_contextos_completos'])

        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{nombre_fuente} - Búsqueda: {self.nombre_mostrar} - LexiMus USAL</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .metadata {{
            background: #f8f9fa;
            padding: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        .metadata-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .metadata-item h3 {{
            color: #667eea;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .metadata-item p {{ font-size: 1.5em; font-weight: bold; }}
        .section {{ padding: 40px; }}
        .word-section {{
            margin-bottom: 60px;
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
        }}
        .word-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 10px 10px 0 0;
            margin: -30px -30px 20px -30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-card .label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .detail-button {{
            display: inline-block;
            margin: 20px auto;
            padding: 15px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
            transition: background 0.3s;
            font-size: 1.1em;
        }}
        .detail-button:hover {{
            background: #5568d3;
        }}
        .button-container {{
            text-align: center;
            margin: 30px 0;
        }}
        .validation-badge {{
            background: #4caf50;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-left: 10px;
            font-weight: bold;
        }}
        footer {{
            background: #2d3748;
            color: white;
            padding: 30px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📰 {nombre_fuente}</h1>
            <h2 style="font-size: 1.5em; margin-top: 15px;">{EMOJI} Búsqueda: {self.nombre_mostrar}</h2>
            <p style="margin-top: 10px;">Proyecto LexiMus USAL - PID2022-139589NB-C33</p>
            <p style="margin-top: 10px; font-size: 0.95em;">{self.descripcion}</p>
            <p style="margin-top: 10px; font-size: 1.1em;">✅ Con Sistema de Validación Manual Integrado</p>
        </header>

        <div class="metadata">
            <div class="metadata-item">
                <h3>Fuente</h3>
                <p>{nombre_fuente}</p>
            </div>
            <div class="metadata-item">
                <h3>Fecha Análisis</h3>
                <p>{self.metadata['fecha_analisis']}</p>
            </div>
            <div class="metadata-item">
                <h3>Archivos</h3>
                <p>{self.metadata['total_archivos_procesados']:,}</p>
            </div>
            <div class="metadata-item">
                <h3>Palabra Buscada</h3>
                <p>{self.nombre_mostrar}</p>
            </div>
            <div class="metadata-item">
                <h3>Tolerancia OCR</h3>
                <p>±{self.umbral_levenshtein} caracteres</p>
            </div>
        </div>

        <div class="section">
            <div class="word-section">
                <div class="word-header">
                    <h3>"{self.nombre_mostrar}" <span class="validation-badge">✅ VALIDACIÓN DISPONIBLE</span></h3>
                </div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">{stats['ocurrencias_totales']:,}</div>
                        <div class="label">Ocurrencias</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{stats['archivos_con_ocurrencias']:,}</div>
                        <div class="label">Archivos</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{porcentaje_archivos:.2f}%</div>
                        <div class="label">% de archivos</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{(stats['ocurrencias_totales'] / self.metadata.get('total_palabras_corpus', 1))*1000:.2f}</div>
                        <div class="label">por mil palabras</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{pct_exacta:.1f}%</div>
                        <div class="label">Exacta</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{pct_variantes:.1f}%</div>
                        <div class="label">Variantes</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{pct_fuzzy:.1f}%</div>
                        <div class="label">Fuzzy</div>
                    </div>
                </div>

                <div class="chart-container">
                    <canvas id="chart_{palabra_simple}"></canvas>
                </div>

                <div class="button-container">
                    <a href="resultados_{palabra_simple}_{nombre_fuente}_detalle.html" class="detail-button">
                        📊 Ver y Validar TODOS los Contextos ({total_contextos_completos:,} totales) ✅
                    </a>
                </div>
            </div>
        </div>

        <footer>
            <p><strong>LexiMus USAL</strong> - PID2022-139589NB-C33</p>
            <p style="margin-top: 10px;">✅ Sistema de Validación Manual Integrado</p>
            <p style="margin-top: 10px;">{EMOJI} {self.descripcion}</p>
        </footer>
    </div>

    <script>
        const datos_temporales = {json.dumps(sorted([(k, v) for k, v in stats['ocurrencias_por_mes'].items()]))};
        const meses = datos_temporales.map(d => d[0]);
        const valores = datos_temporales.map(d => d[1]);

        const ctx = document.getElementById('chart_{palabra_simple}').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: meses,
                datasets: [{{
                    label: 'Ocurrencias de "{self.nombre_mostrar}"',
                    data: valores,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    title: {{
                        display: true,
                        text: 'Evolución Temporal de "{self.nombre_mostrar}" en {nombre_fuente}',
                        font: {{
                            size: 18
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Número de ocurrencias'
                        }}
                    }},
                    x: {{
                        title: {{
                            display: true,
                            text: 'Mes (AAAA-MM)'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"   ✓ HTML guardado: {nombre_archivo}")


def generar_html_comparativo(resultados_todas_fuentes):
    """Genera HTML comparativo de TODOS los corpus"""
    palabra_simple = PALABRA_CLAVE.replace(' ', '_').lower()
    nombre_archivo = f"resultados_{palabra_simple}_TODOS_CORPUS.html"

    # Preparar datos
    fuentes_data = []
    for fuente_nombre, buscador in resultados_todas_fuentes.items():
        stats = buscador.estadisticas
        fuentes_data.append({
            'nombre': fuente_nombre,
            'ocurrencias': stats['ocurrencias_totales'],
            'archivos': stats['archivos_con_ocurrencias'],
            'total_archivos': buscador.metadata['total_archivos_procesados']
        })

    # Ordenar por ocurrencias
    fuentes_data.sort(key=lambda x: x['ocurrencias'], reverse=True)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparativa {NOMBRE_MOSTRAR} - TODOS LOS CORPUS - LexiMus USAL</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        header h1 {{ font-size: 2.8em; margin-bottom: 10px; }}
        .section {{ padding: 40px; }}
        .fuente-card {{
            background: #f8f9fa;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .fuente-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 1.3em;
            font-weight: bold;
        }}
        .stats-inline {{
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }}
        .stat-inline {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .stat-inline .label {{
            color: #666;
            font-size: 0.95em;
        }}
        .stat-inline .value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #667eea;
        }}
        .link-button {{
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            transition: background 0.3s;
        }}
        .link-button:hover {{ background: #5568d3; }}
        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin: 30px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        footer {{
            background: #2d3748;
            color: white;
            padding: 30px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{EMOJI} COMPARATIVA: {NOMBRE_MOSTRAR}</h1>
            <h2 style="font-size: 1.5em; margin-top: 15px;">Análisis en TODOS los Corpus</h2>
            <p style="margin-top: 10px;">Proyecto LexiMus USAL - PID2022-139589NB-C33</p>
            <p style="margin-top: 10px; font-size: 0.95em;">{DESCRIPCION}</p>
        </header>

        <div class="section">
            <div class="chart-container">
                <canvas id="chart_comparativa"></canvas>
            </div>

            <h2 style="margin-bottom: 20px; color: #667eea;">📊 Resultados por Fuente:</h2>
"""

    for fuente in fuentes_data:
        porcentaje = (fuente['archivos'] / fuente['total_archivos'] * 100) if fuente['total_archivos'] > 0 else 0
        html_content += f"""
            <div class="fuente-card">
                <div class="fuente-header">📰 {fuente['nombre']}</div>
                <div class="stats-inline">
                    <div class="stat-inline">
                        <span class="label">Ocurrencias:</span>
                        <span class="value">{fuente['ocurrencias']:,}</span>
                    </div>
                    <div class="stat-inline">
                        <span class="label">Archivos con menciones:</span>
                        <span class="value">{fuente['archivos']:,}</span>
                    </div>
                    <div class="stat-inline">
                        <span class="label">Cobertura:</span>
                        <span class="value">{porcentaje:.1f}%</span>
                    </div>
                </div>
                <a href="resultados_{palabra_simple}_{fuente['nombre']}.html" class="link-button">
                    Ver análisis completo →
                </a>
                <a href="resultados_{palabra_simple}_{fuente['nombre']}_detalle.html" class="link-button">
                    Validar contextos ✅
                </a>
            </div>
"""

    html_content += f"""
        </div>

        <footer>
            <p><strong>LexiMus USAL</strong> - PID2022-139589NB-C33</p>
            <p style="margin-top: 10px;">{EMOJI} {DESCRIPCION}</p>
        </footer>
    </div>

    <script>
        const fuentes = {json.dumps([f['nombre'] for f in fuentes_data])};
        const ocurrencias = {json.dumps([f['ocurrencias'] for f in fuentes_data])};

        const ctx = document.getElementById('chart_comparativa').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: fuentes,
                datasets: [{{
                    label: 'Ocurrencias de "{NOMBRE_MOSTRAR}"',
                    data: ocurrencias,
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: '#667eea',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    title: {{
                        display: true,
                        text: 'Comparativa de Ocurrencias de "{NOMBRE_MOSTRAR}" por Fuente',
                        font: {{
                            size: 20
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Número de ocurrencias'
                        }}
                    }},
                    x: {{
                        title: {{
                            display: true,
                            text: 'Fuente'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✓ HTML comparativo guardado: {nombre_archivo}")
    print(f"   Incluye {len(fuentes_data)} fuentes analizadas")


def main():
    if len(sys.argv) < 2:
        print("\n" + "="*80)
        print(f"USO: python3 buscador_generico_palabras.py /ruta/corpus1 [/ruta/corpus2 ...]")
        print("="*80)
        print("\nEjemplo:")
        print('  python3 buscador_generico_palabras.py "/Users/maria/ElDebate" "/Users/maria/ElSol"')
        print(f"\nBusca: {NOMBRE_MOSTRAR}")
        print(f"Descripción: {DESCRIPCION}")
        print("✅ CON VALIDACIÓN MANUAL INTEGRADA")
        print("📊 GENERA COMPARATIVA DE TODAS LAS FUENTES")
        print("="*80 + "\n")
        sys.exit(1)

    directorios_corpus = sys.argv[1:]

    print("\n" + "="*80)
    print(f"BUSCADOR: {NOMBRE_MOSTRAR.upper()}")
    print("Proyecto LexiMus USAL - PID2022-139589NB-C33")
    print("="*80)
    print(f"\n📚 Total de fuentes a procesar: {len(directorios_corpus)}")
    print(f"🔍 Buscando: {NOMBRE_MOSTRAR}")
    print(f"📊 Tolerancia OCR: Levenshtein ≤{UMBRAL_LEVENSHTEIN}")
    print(f"{EMOJI} {DESCRIPCION}")
    print("\n" + "-"*80)

    resultados_todas_fuentes = {}

    for directorio in directorios_corpus:
        nombre_fuente = os.path.basename(directorio.rstrip('/'))

        buscador = BuscadorGenerico(
            nombre_fuente=nombre_fuente,
            umbral_levenshtein=UMBRAL_LEVENSHTEIN,
            min_longitud_palabra=MIN_LONGITUD_PALABRA,
            ventana_contexto=VENTANA_CONTEXTO
        )

        exito = buscador.procesar_corpus(directorio)

        if exito:
            resultados_todas_fuentes[nombre_fuente] = buscador
            buscador.mostrar_resumen()

            print(f"\n   Generando archivos de salida para {nombre_fuente}...")
            buscador.guardar_json()
            buscador.guardar_todos_contextos_json()
            buscador.generar_html()

            archivo_detalle = buscador.generar_html_detalle()
            total_contextos = len(buscador.estadisticas['todos_contextos_completos'])
            print(f"   🌐 {archivo_detalle} ({total_contextos:,} contextos)")

            archivo_txt = buscador.generar_txt_detalle()
            print(f"   📝 {archivo_txt} ({total_contextos:,} contextos)")

        print("-"*80)

    # Generar HTML comparativo
    if resultados_todas_fuentes:
        print("\n" + "="*80)
        print("GENERANDO ANÁLISIS COMPARATIVO")
        print("="*80)
        generar_html_comparativo(resultados_todas_fuentes)

    palabra_simple = PALABRA_CLAVE.replace(' ', '_').lower()
    print("\n" + "="*80)
    print("🎉 ANÁLISIS COMPLETADO")
    print("="*80)
    print(f"\n📊 Total fuentes procesadas: {len(resultados_todas_fuentes)}")
    print("\nArchivos generados POR CADA FUENTE:")
    print(f"  📄 resultados_{palabra_simple}_[FUENTE].json")
    print(f"  📄 todos_contextos_{palabra_simple}_[FUENTE].json")
    print(f"  🌐 resultados_{palabra_simple}_[FUENTE].html")
    print(f"  🌐 resultados_{palabra_simple}_[FUENTE]_detalle.html ✅ CON VALIDACIÓN")
    print(f"  📝 validacion_{palabra_simple}_[FUENTE]_contextos.txt ✅ VALIDACIÓN TXT")
    print("\nArchivo COMPARATIVO:")
    print(f"  🌐 resultados_{palabra_simple}_TODOS_CORPUS.html")
    print("\n✅ Cada fuente muestra su nombre en los resultados")
    print("✅ Validación manual integrada en HTML")
    print("✅ Progreso guardado automáticamente en el navegador")
    print("✅ Exportación en JSON disponible")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
