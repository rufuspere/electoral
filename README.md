# hondt
Código python para elecciones y ficheros de resultados de las elecciones
Está escrito en PYTHON 3.8.2  y consta de diferentes partes o módulos.
PARTE 0: IMPORTACIÓN DE PAQUETES Y ESTABLECER DIRECTORIO DE TRABAJO
Se comienza importando algunos paquetes necesarios como pandas, xlrd, collections y estableciendo el directorio de trabajo.
PARTE i: importación de datos
Se continúa con la importación de los datos del Ministerio del Interior, modificados según seexplica en el documento word (EL MÉTODO D.docx) al DataFrame df0.
Asimismo, se importa a df2 una tabla de partidos creada por el autor en la que se asignan a cada candidatura un número (1-67) y un grupo político ('DERECHA', 'CENTRO', 'IZQUIERDA', 'NACIONALISTAS' y 'OTROS'):
PARTE II: INTRODUCIR GRUPOS
En este módulo introducimos los grupos como columnas en df1, de modo que podemos calcular los votos por grupo para las columnas 'DERECHA', 'CENTRO', 'IZQUIERDA', 'NACIONALISTAS' y 'OTROS' que suman los votos a cada grupo sean mayores o menores que el 3%.
PARTE III: ELIMINAR CANDIDATURAS DE <3%
Solo las candidaturas cuyos votos que superen el 3% de los votos válidos se mantendrán para asignar diputados a través de la tabla d’Hondt, aun cuando no todas ellas conseguirán diputados. El data frame df5 empleado tiene df5[x][df5[x]/df5['VOTOS_VÁLIDOS'] < 0.03] = 0 ∀x∈[^' 1^','2',…^' NPARTIDOS'], es decir, son nulos los votos a candidaturas que han obtenido menos del 3% de los votos válidos de la circunscripción. La columna 'VOTOS_REPARTIR' suma los que proceden de candidaturas con más del 3%.
PARTE IV: TABLAS d'HONDT
Usamos df3 para calcular las tablas d’Hondt para asignar los escaños a las candidaturas. Se da la oportunidad de descargar las tablas d’Hondt calculadas por si se desea hacer comprobaciones.
PARTE V: COMPROBAR SI HAY EMPATES
Normalmente no habrá ningún empate entre candidaturas, pero, por si acaso comprobaremos este extremo y, si hay candidaturas empatadas, procederemos a la elección por sorteo de las correspondientes candidaturas.
PARTE VI: SI HAY EMPATES
Se procede a elegir candidatura(s) repetida(s) por sorteo que se añade(n) a las no repetidas mediante el método random.sample().
PARTE VII: ASIGNACIÓN DE ESCAÑOS DEFINITIVA
Tal como está estructurada la aplicación, haya o no empates ha de ejecutarse esta parte ya que en ella se asignan los escaños con o sin repetición de índices d’Hondt.
PARTE VIII: LISTADOS DE COMPROBACIÓN Y ARCHIVO DE SALIDA EXCEL
Realizamos una serie de listados y, si se desea, se extrae un fichero Excel que puede utilizarse para realizar investigaciones sobre los datos.
PARTE IX: DESAPARECER PARTIDOS Y REASIGNAR VOTO
Su finalidad es simular los resultados en caso de candidaturas concéntricas unitarias, teniendo o no en cuenta los posibles cambios en la abstención diferencial.

