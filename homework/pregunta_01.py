"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
  """
  Construya y retorne un dataframe de Pandas a partir del archivo
  'files/input/clusters_report.txt'. Los requerimientos son los siguientes:

  - El dataframe tiene la misma estructura que el archivo original.
  - Los nombres de las columnas deben ser en minusculas, reemplazando los
    espacios por guiones bajos.
  - Las palabras clave deben estar separadas por coma y con un solo
    espacio entre palabra y palabra.
  """
  import re
  import pandas as pd

  path = 'files/input/clusters_report.txt'
  header_re = re.compile(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$')

  def _finalize(curr, kws, rows):
    if curr is None:
      return
    text = ' '.join(kws).strip()
    text = re.sub(r'\s+', ' ', text)
    if text.endswith('.'):
      text = text[:-1]
    parts = [p.strip() for p in text.split(',') if p.strip()]
    rows.append({
      'cluster': int(curr[0]),
      'cantidad_de_palabras_clave': int(curr[1]),
      'porcentaje_de_palabras_clave': float(curr[2].replace(',', '.')),
      'principales_palabras_clave': ', '.join(parts)
    })

  rows = []
  current = None
  keywords = []

  with open(path, encoding='utf-8') as f:
    for raw in f:
      line = raw.rstrip('\n')
      if not line.strip():
        if current is not None:
          _finalize(current, keywords, rows)
          current = None
          keywords = []
        continue
      if line.strip().startswith('Cluster') or line.strip().startswith('---') or 'palabras clave' in line.lower():
        continue
      m = header_re.match(line)
      if m:
        if current is not None:
          _finalize(current, keywords, rows)
          keywords = []
        current = (m.group(1), m.group(2), m.group(3))
        first = m.group(4).strip()
        if first:
          keywords.append(first)
      else:
        if current is not None:
          keywords.append(line.strip())

  if current is not None:
    _finalize(current, keywords, rows)

  df = pd.DataFrame(rows, columns=[
    'cluster',
    'cantidad_de_palabras_clave',
    'porcentaje_de_palabras_clave',
    'principales_palabras_clave'
  ])

  return df
