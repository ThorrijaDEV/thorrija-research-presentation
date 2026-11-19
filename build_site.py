#!/usr/bin/env python3
"""
Generador automático de la presentación web + PDF.
Fuente única de verdad: esta lista de slides → docs/index.html → PDF por Chromium.

Cada slide lleva:
  - eyebrow, título, cuerpo (HTML con clases del sistema visual)
  - "plain": texto en lenguaje natural, sin tecnicismo, para explicar oralmente.
"""

from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"

C = {
    "indigo": "#8ea0e8", "amber": "#c8944e", "teal": "#5fb3ac", "plum": "#a97fa2",
    "red": "#c06a5f", "green": "#6abf8b", "cyan": "#4ec9b0", "orange": "#d49b4a",
}

def esc(s): return html.escape(s)

def card(color, title, body):
    return (f'<div class="card"><div class="bar" style="background:var(--{color})"></div>'
            f'<h3 style="color:var(--{color})">{title}</h3><p>{body}</p></div>')

def bullets(items):
    return '<div class="stack">' + "".join(
        f'<div class="bullet"><span class="k">{k}</span><span>{t}</span></div>' for k, t in items
    ) + '</div>'

# ── Diagramas HTML nativos (sin posiciones manuales → sin solapes) ──────────────

def diagram_box_kernel():
    return '''
<div class="diag cols">
  <div class="diag-col">
    <div class="formula">G = (V, E, ι, λ, σ)</div>
    <div class="diag-rows">
      <div><b>V</b> — flechas. Cada flecha es una identidad.</div>
      <div><b>E</b> — una flecha apunta a otra flecha.</div>
      <div><b>ι</b> — etiqueta que se copia o se pierde.</div>
      <div><b>λ</b> — etiqueta de dónde viene.</div>
      <div><b>σ</b> — semilla: misma semilla, mismo resultado.</div>
    </div>
  </div>
  <div class="diag-col">
    <div class="mini-title">LO QUE APARECE DESPUÉS (NO ESTÁ PROGRAMADO)</div>
    <div class="stack">
      <div class="mini" style="--c:var(--indigo)"><b>identidad</b><span>quien comparte etiqueta es "el mismo"</span></div>
      <div class="mini" style="--c:var(--teal)"><b>linaje</b><span>de dónde viene cada flecha</span></div>
      <div class="mini" style="--c:var(--amber)"><b>comunidad</b><span>quienes llevan la misma etiqueta</span></div>
    </div>
  </div>
</div>'''

def diagram_box_rules():
    rules = [("R1", "transformar", "crea una flecha nueva"),
             ("R2", "etiquetar", "toda flecha lleva una etiqueta"),
             ("R3", "copiar", "la etiqueta se copia o se pierde"),
             ("R4", "emparejar", "se juntan por etiqueta igual"),
             ("R5", "enlazar", "el emparejamiento crea otra flecha"),
             ("R6", "cerrar", "nada más está programado")]
    left = "".join(f'<div class="rule-row"><span class="rk">{k}</span><b>{n}</b><span>{d}</span></div>' for k, n, d in rules)
    return f'''
<div class="diag cols">
  <div class="diag-col"><div class="mini-title">LAS SEIS REGLAS</div>{left}</div>
  <div class="diag-col"><div class="mini-title">LO QUE SALE SIN PROGRAMARLO</div>
    <div class="stack">
      <div class="mini" style="--c:var(--indigo)"><b>identidad</b><span>quien comparte etiqueta</span></div>
      <div class="mini" style="--c:var(--teal)"><b>linaje</b><span>de dónde nació cada una</span></div>
      <div class="mini" style="--c:var(--amber)"><b>comunidad</b><span>quién se agrupa con quién</span></div>
    </div>
    <p class="diag-note">Las reglas no dicen "crea una identidad". La identidad aparece sola al aplicarlas.</p>
  </div>
</div>'''

def diagram_box_exp():
    return '''
<div class="diag">
  <div class="diag-band">
    <div class="mini-title">CÓMO NACE UNA IDENTIDAD</div>
    <p>Flecha A (etiqueta α) → aparece B copiando α → aparece C copiando α → A y C se emparejan y nace D.</p>
    <p class="diag-note">Medible: contar flechas con la misma etiqueta. Repetible: misma semilla, mismo resultado.</p>
  </div>
  <div class="grid-3" style="margin-top:12px">
    <div class="card"><div class="bar" style="background:var(--indigo)"></div><h3 class="accent-indigo">PRUEBA 1 — el freno</h3><p>Al interrumpir el sistema de vez en cuando, sigue vivo. p=0.001 con 10.000 semillas.</p></div>
    <div class="card"><div class="bar" style="background:var(--teal)"></div><h3 class="accent-teal">PRUEBA 5 — la pausa</h3><p>Sin interrupciones se queda quieto. Con interrupciones sigue cambiando.</p></div>
    <div class="card"><div class="bar" style="background:var(--amber)"></div><h3 style="color:var(--amber)">PRUEBA 6 — la semilla</h3><p>Misma semilla, misma historia siempre. Se puede volver a obtener.</p></div>
  </div>
  <div class="grid-2" style="margin-top:12px">
    <div class="card"><div class="bar" style="background:var(--teal)"></div><h3 class="accent-teal">PASO A TYPESCRIPT — NIVEL 3</h3><p>La estructura es igual, pero dos piezas faltan (since_inflow y Rule.to_dict). No digo que sea idéntico byte a byte.</p></div>
    <div class="card"><div class="bar" style="background:var(--red)"></div><h3 style="color:var(--red)">LÍMITES — Veredicto: mecanismo explicado, sin descubrimiento</h3><p>1 No sirve aún fuera de laboratorio · 2 No hay hardware · 3 No aprende · 4 Solo una métrica admitida · 5 Sin comparación con otros sistemas · 6 El puerto TS está incompleto</p></div>
  </div>
</div>'''

def diagram_singularity():
    agents = [("NAVIGATOR", "explora", "indigo"), ("MAPPER", "dibuja el mapa", "teal"),
              ("PLANNER", "decide", "amber"), ("EXECUTOR", "ejecuta", "plum"),
              ("VERIFIER", "comprueba", "green")]
    al = "".join(f'<div class="mini" style="--c:var(--{c})"><b>{n}</b><span>{d}</span></div>' for n, d, c in agents)
    return f'''
<div class="diag">
  <div class="orch">ORQUESTADOR <span>reparte tareas y decide quién hace qué</span></div>
  <div class="agent-row">{al}</div>
  <div class="diag-band green">
    <b>EL VERIFICADOR NO SE CREE NADA</b><p>Ejecuta las pruebas, compara resultados y rechaza lo que no se puede repetir. Nunca confía en lo que el agente dice de sí mismo.</p>
  </div>
  <div class="grid-2" style="margin-top:12px">
    <div class="card"><div class="bar" style="background:var(--red)"></div><h3 style="color:var(--red)">RESULTADO E1 — colaborar salió PEOR</h3><p>Solo: 0,78 · Juntos: 0,62 · Diferencia −0,16, p&lt;0,001. Hablar costó más de lo que aportó.</p></div>
    <div class="card"><div class="bar" style="background:var(--amber)"></div><h3 style="color:var(--amber)">DOS FORMAS DE PROBARLO</h3><p>A cada agente trabaja por su lado. B los agentes se comunican. La hipótesis era que B ganaría: fue falsa.</p></div>
  </div>
  <p class="diag-note">Límite: probado solo en un entorno pequeño y con una sola forma de colaborar.</p>
</div>'''

def diagram_hermes():
    agents = [("OBSERVER", "mira", "indigo"), ("ANALYZER", "detecta", "teal"), ("PLANNER", "planea", "amber"),
              ("EXECUTOR", "hace", "plum"), ("VALIDATOR", "valida", "green"), ("CORRECTOR", "corrige", "red"),
              ("SYNCHRONIZER", "sincroniza", "indigo"), ("ARCHIVIST", "guarda todo", "teal"), ("GOVERNOR", "manda", "amber")]
    grid = "".join(f'<div class="mini" style="--c:var(--{c})"><b>{n}</b><span>{d}</span></div>' for n, d, c in agents)
    return f'''
<div class="diag">
  <div class="agent-grid">{grid}</div>
  <div class="diag-band green" style="margin-top:12px">
    <b>UN DIRECTOR QUE REPARTE</b><p>Da órdenes, lleva el ritmo y decide cuándo intervenir. Mide: cuánto tarda, cuántas veces interviene y si el resultado se puede repetir.</p>
  </div>
  <p class="diag-note">Reglas de autonomía: quien solo mira, no toca nada. Quien planea, solo propone. Quien ejecuta, solo con autorización. Governor es la única autoridad para cambiar los límites.</p>
  <p class="diag-note" style="color:var(--orange)">Estado: SPECULATIVO — es un diseño pensado con cuidado, pero todavía no hay código ejecutando. "Deriva semántica" está definida, no medida.</p>
</div>'''

def diagram_showcase():
    ms = [("1 · Wi-Fi Time Machine", "Mira el historial de redes que hubo: qué redes, en qué canal y con qué seguridad.", "indigo"),
          ("2 · BLE Radar", "Muestra dispositivos Bluetooth sin tener hardware Bluetooth: aparecen, cambian y desaparecen.", "teal"),
          ("3 · Process Monitor", "Lee los procesos de Linux como si fueran un ecosistema: quienes nacen, mueren y quedan huérfanos.", "amber"),
          ("4 · Terminal Generative Engine", "Genera arte a partir de una semilla. Con la misma semilla sale siempre lo mismo, y se puede ir a cualquier fotograma sin recorrer los anteriores.", "plum")]
    cs = "".join(card(c, n, b) for n, b, c in ms)
    return f'''
<div class="diag">
  <div class="grid-2">{cs}</div>
  <div class="diag-band" style="margin-top:12px">
    <b>CÓMO ESTÁ HECHO</b><p>Web hecha con Vite y TypeScript. 182 pruebas. Se publica en GitHub Pages y se comprueba cada semana. Sin dependencias en tiempo de ejecución.</p>
  </div>
</div>'''

def diagram_appendix():
    return '''
<div class="diag">
  <div class="code-grid">
    <div class="pre"><div class="mini-title">THE BOX — KERNEL (Rust)</div><code><span class="kw">pub struct</span> ArcIncidenceGraph {
    arcs: Vec&lt;Arc&gt;,
    incidence: Vec&lt;Vec&lt;usize&gt;&gt;,
}
<span class="kw">pub struct</span> Arc {
    label: Label,      <span class="c">// etiqueta de identidad</span>
    lineage: Label,    <span class="c">// de dónde viene</span>
    seed: Seed,        <span class="c">// semilla</span>
    since_inflow: Option&lt;usize&gt;, <span class="c">// defecto</span>
}
<span class="kw">pub trait</span> Rule { fn to_dict(&amp;self); } <span class="c">// falta</span></code></div>
    <div class="pre"><div class="mini-title">ORACLE E1 — ESTADÍSTICA (Python)</div><code>stat, p = mannwhitneyu(a, b, <span class="s">'two-sided'</span>)
delta  = cliffs_delta(a, b)
ci     = bootstrap(a, b, n_resamples=<span class="s">10000</span>)
<span class="c"># a=0.78 · b=0.62 · Δ=−0.16 · p&lt;0.001 · δ=−0.47</span>
<span class="c"># potencia 0.99 con 500 semillas por grupo</span></code></div>
    <div class="pre full"><div class="mini-title">SINGULARITY — CONTRATO DE AGENTE (TypeScript)</div><code><span class="kw">interface</span> AgentContract {
  invariants: Invariant[];       <span class="c">// pruebas de propiedad</span>
  autonomy_level: AutonomyLevel; <span class="c">// READ_ONLY | PROPOSE | EXECUTE</span>
  drift_threshold?: number;
}
<span class="kw">class</span> Verifier {
  <span class="c">// ejecuta con semilla fija, valida invariantes,</span>
  <span class="c">// compara la huella de la traza y</span>
  <span class="c">// NUNCA se cree el auto-informe del agente</span>
}</code></div>
  </div>
</div>'''

# ── Slides ────────────────────────────────────────────────────────────────────

S = []

S.append(dict(n=1, tag="PORTADA", eyebrow="", title="", cls="cover", plain=
    "Hola, soy Rubén. Hoy vengo a contarte qué he construido y, sobre todo, por qué lo he hecho de esta manera.",
    body='''
  <h1>THORRIJA</h1>
  <div class="sub">Presentación para equipo de investigación IA</div>
  <div class="date">Noviembre 2026 &nbsp;·&nbsp; Rubén Núñez Sierra</div>
  <div class="rule rule-amber" style="width:60%"></div>
  <div class="links">github.com/ThorrijaDEV &nbsp;·&nbsp; thorrijadev.github.io/showcase</div>'''))

S.append(dict(n=2, tag="TESIS", eyebrow="01 — TESIS + FIDELIDAD", title="Tres pilares, una disciplina", plain=
    "Antes de decir que algo funciona, primero compruebo que funciona. Y si descubro que no, también lo digo. No es humildad: es la única forma de avanzar de verdad.",
    body='''
<div class="grid-3">
  <div class="card"><div class="bar" style="background:var(--indigo)"></div><h3 class="accent-indigo">AFIRMACIÓN → EVIDENCIA → VEREDICTO</h3><p>Nada se afirma sin una prueba. Nada se mide sin poder rastrearlo. Nada se da por bueno sin haber intentado tumbarlo.</p></div>
  <div class="card"><div class="bar" style="background:var(--teal)"></div><h3 class="accent-teal">FIDELIDAD DECLARADA (1–4)</h3><p>Cada reconstrucción lleva escrito su nivel: 1 es copia directa, 4 es solo una idea parecida. Y se dice cuál es.</p></div>
  <div class="card"><div class="bar" style="background:var(--amber)"></div><h3 style="color:var(--amber)">RESULTADOS NEGATIVOS PUBLICADOS</h3><p>Cuando algo no funciona, lo cuento. Aquí tienes dos ejemplos y dos defectos míos, sin esconderlos.</p></div>
</div>'''))

S.append(dict(n=3, tag="PREGUNTAS", eyebrow="02 — PREGUNTAS + SUSTRATOS", title="Cinco preguntas, tres sustratos", plain=
    "Todo lo que he construido gira alrededor de cinco preguntas. No son preguntas decorativas para la charla: son las que me quitan el sueño de verdad.",
    body='''
<div class="col2">
  <div class="stack">
    <div class="bullet"><span class="k">1.</span><span>¿Cómo comprobar algo sin fiarme de mí mismo?</span></div>
    <div class="bullet"><span class="k">2.</span><span>¿Con cuántas reglas aparece algo interesante?</span></div>
    <div class="bullet"><span class="k">3.</span><span>¿Cuándo trabajar en equipo sale peor?</span></div>
    <div class="bullet"><span class="k">4.</span><span>¿Cómo medir que un agente se está desviando?</span></div>
    <div class="bullet"><span class="k">5.</span><span>¿Qué fallos de diseño frenan todo lo demás?</span></div>
  </div>
  <div class="stack">
    <div class="card"><div class="bar" style="background:var(--indigo)"></div><h3 class="accent-indigo">THE BOX</h3><p>Seis reglas y aparecen identidad, historia y grupos. Hecho en Rust y TypeScript.</p></div>
    <div class="card"><div class="bar" style="background:var(--teal)"></div><h3 class="accent-teal">SINGULARITY / ORACLE</h3><p>Varios agentes trabajando y uno que solo comprueba. Un experimento demostró que colaborar puede salir mal.</p></div>
    <div class="card"><div class="bar" style="background:var(--amber)"></div><h3 style="color:var(--amber)">HERMES</h3><p>Un diseño de director de orquesta para agentes. Aún en papel, y lo digo.</p></div>
  </div>
</div>'''))

S.append(dict(n=4, tag="KERNEL", eyebrow="03 — THE BOX: NÚCLEO", title="Multigrafo de incidencia arco-arco", plain=
    "Imagina un montón de flechas que se apuntan entre sí. Pues eso es The Box. No hay objetos separados: las flechas SON las identidades, y al apuntarse unas a otras aparecen la historia y los grupos sin que yo los programara.",
    body=diagram_box_kernel()))

S.append(dict(n=5, tag="REGLAS", eyebrow="04 — THE BOX: 6 REGLAS", title="Seis reglas. Nada más.", plain=
    "Le di al sistema solo seis instrucciones muy simples. Sin embargo, de esas seis salen cosas que nadie escribió: quién es quién, de dónde viene y con quién se agrupa. Eso es lo que me parece interesante.",
    body=diagram_box_rules()))

S.append(dict(n=6, tag="EXP + TS", eyebrow="05 — THE BOX: EXPERIMENTOS + TS + LÍMITES", title="Un hallazgo admitido, dos defectos, puerto a medias", plain=
    "Hice tres pruebas. Salieron dos cosas: el sistema sigue vivo si lo interrumpes de vez en cuando, y con la misma semilla sale siempre lo mismo. Pero también encontré dos fallos míos y el puerto a TypeScript está incompleto. Veredicto: entiendo cómo funciona, no he descubierto nada nuevo.",
    body=diagram_box_exp()))

S.append(dict(n=7, tag="NOX", eyebrow="06 — NOX: COGNITIVE RUNTIME", title="Persistent Autonomous Cognitive Runtime", plain=
    "NOX es un asistente que recuerda. No empieza de cero cada vez: guarda lo que aprende y lo recupera después. Todo corre en mi propio ordenador, sin servicios externos y sin enviar datos a nadie.",
    body='''
<div class="col2">
  <div class="card"><div class="bar" style="background:var(--indigo)"></div><h3 class="accent-indigo">CÓMO FUNCIONA</h3><p>Mira, piensa, actúa y guarda lo aprendido. Esa memoria sobrevive aunque apagues el programa. Usa herramientas como código, terminal y archivos, y sus modelos viven en local.</p></div>
  <div class="card"><div class="bar" style="background:var(--cyan)"></div><h3 style="color:var(--cyan)">QUÉ LO DIFERENCIA</h3><p>La memoria de verdad persiste. Cada paso se comprueba. No llama a ningún servicio externo. Cada herramienta tiene un contrato claro. Y no vendo humo: lo que no hace, lo digo.</p></div>
</div>'''))

S.append(dict(n=8, tag="ECHO", eyebrow="07 — ECHO: VIDA ARTIFICIAL COMPUTACIONAL", title="Un organismo que vive en un mundo simulado", plain=
    "ECHO no era un chatbot. Era un experimento de vida artificial: un organismo que percibe, aprende, recuerda, razona y se mueve en un mundo propio, sin que yo le diga a cada momento qué hacer. Dos referencias: ECHO en project_life (el proyecto principal) y ASTER como infraestructura independiente.",
    body='''
<div class="diag">
  <div class="agent-grid">
    <div class="mini" style="--c:var(--indigo)"><b>cognición</b><span>procesa, razona, decide</span></div>
    <div class="mini" style="--c:var(--teal)"><b>memoria</b><span>guarda y recupera experiencias</span></div>
    <div class="mini" style="--c:var(--amber)"><b>aprendizaje</b><span>se adapta con la experiencia</span></div>
    <div class="mini" style="--c:var(--plum)"><b>ecosistema</b><span>interactúa con otros organismos</span></div>
    <div class="mini" style="--c:var(--cyan)"><b>simulación</b><span>su propio mundo para vivir</span></div>
    <div class="mini" style="--c:var(--green)"><b>autonomía</b><span>actúa sin instrucciones constantes</span></div>
  </div>
  <div class="diag-band" style="margin-top:12px">
    <b>MODELOS + REFERENCIAS</b><p>Integración de modelos de IA para las capacidades cognitivas. Referencias: <b>~/Projects/project_life</b> (ECHO canónico) y <b>ASTER</b> (infraestructura y ecosistema independiente).</p>
  </div>
  <div class="diag-band green" style="margin-top:10px">
    <b>PHASE 2.5 — VALIDACIÓN ADVERSARIA CORTA + ASIMILACIÓN ECHO/ASTER</b><p>Un prompt para que NØX: 1) descubra las capacidades legítimamente expuestas por ECHO y ASTER, 2) aprenda sus protocolos, esquemas, mensajes y respuestas, 3) las integre mediante un <b>CapabilityRegistry</b>, y 4) distinga descubrir capacidades de escalar privilegios.</p>
  </div>
  <p class="diag-note">En resumen: construir un organismo capaz de percibir, aprender, recordar, razonar e interactuar con un entorno propio.</p>
</div>'''))

S.append(dict(n=9, tag="ORACLE", eyebrow="08 — SINGULARITY / ORACLE", title="Multi-agente + verificación independiente", plain=
    "Puse cinco agentes a trabajar juntos y uno aparte que solo comprueba. El verificador no se cree lo que los otros dicen de sí mismos: lo ejecuta todo otra vez. Y aquí viene la sorpresa: cuando los dejé hablarse entre ellos, fue peor que cuando trabajaron solos. Lo publiqué igual.",
    body=diagram_singularity()))

S.append(dict(n=10, tag="HERMES", eyebrow="09 — HERMES", title="9 tipos de agente · autonomía por diseño", plain=
    "HERMES es el director de orquesta. Reparte tareas, lleva el ritmo y decide cuándo hay que intervenir. Cada agente tiene su nivel de autonomía escrito de antemano. Es el diseño más completo, y también el que menos código tiene: está en papel.",
    body=diagram_hermes()))

S.append(dict(n=11, tag="SHOWCASE", eyebrow="10 — SHOWCASE: 4 MODELOS NIVEL 1", title="Cuatro reconstrucciones ejecutables", plain=
    "Estos cuatro son los que mejor funcionan: copias directas de comportamientos reales. Uno reconstruye el historial de redes wifi, otro muestra Bluetooth sin hardware, otro lee los procesos de Linux y el último genera arte con semillas. Son los más fáciles de explicar y los que cualquiera puede ejecutar.",
    body=diagram_showcase()))

S.append(dict(n=12, tag="SÍNTESIS", eyebrow="11 — SÍNTESIS: 5 SUSTRATOS", title="Una disciplina de verificación", plain=
    "Si tuviera que resumir esto en una frase: no me interesa tener razón, me interesa poder comprobar. En los cinco proyectos repito lo mismo — especificar, probar, verificar, guardar la semilla, declarar el nivel y publicar lo que falla. Esa es mi forma de trabajar.",
    body='''
<div class="stack" style="margin-top:14px">
  <div class="card"><div class="bar" style="background:var(--amber)"></div><h3 style="color:var(--amber)">LAS SIETE CAPAS DE LA VERIFICACIÓN</h3><p>Contrato claro · Pruebas que generan casos · Otro proceso que comprueba · Semillas y huellas guardadas · Nivel declarado · Negativos publicados · Defectos documentados.</p></div>
  <div class="card"><div class="bar" style="background:var(--indigo)"></div><h3 class="accent-indigo">EL HILO COMÚN</h3><p>Lo mismo en The Box, NOX, ECHO, SINGULARITY y HERMES: no creerme a mí, crear la herramienta que me corrige.</p></div>
  <div class="card"><div class="bar" style="background:var(--teal)"></div><h3 class="accent-teal">UN NEGATIVO NO ES UN FRACASO</h3><p>Es un límite que ya conocemos. ORACLE demostró que colaborar puede salir mal; The Box explica su mecanismo pero no descubre nada. Publicarlo evita que otros pierdan el tiempo.</p></div>
</div>'''))

S.append(dict(n=13, tag="HEATMAP", eyebrow="12 — MAPA DE LIMITACIONES + PROBLEMAS ABIERTOS", title="Intensidad por sustrato, con criterio de falsificación", plain=
    "Esta tabla es mi mapa de debilidades. Rojo means que algo bloquea de verdad, ámbar que reduce el alcance, gris que está documentado. Debajo están las seis preguntas que me quedan. Cada una dice cómo sabría que la he resuelto: no son deseos, son retos con un criterio claro.",
    body='''
<table>
  <tr><th>Dimensión</th><th>The Box</th><th>NOX</th><th>ECHO</th><th>ORACLE</th><th>HERMES</th></tr>
  <tr><td>Defectos de diseño</td><td style="color:var(--red)">bloquea</td><td>doc</td><td>doc</td><td>doc</td><td>—</td></tr>
  <tr><td>Sin hardware</td><td style="color:var(--red)">bloquea</td><td style="color:var(--amber)">alcance</td><td style="color:var(--red)">bloquea</td><td style="color:var(--amber)">alcance</td><td style="color:var(--amber)">alcance</td></tr>
  <tr><td>No aprende</td><td style="color:var(--red)">bloquea</td><td>doc</td><td style="color:var(--amber)">alcance</td><td>doc</td><td>doc</td></tr>
  <tr><td>Sin comparación externa</td><td style="color:var(--red)">bloquea</td><td>doc</td><td style="color:var(--amber)">alcance</td><td style="color:var(--amber)">alcance</td><td style="color:var(--amber)">alcance</td></tr>
  <tr><td>Serialización a medias</td><td style="color:var(--red)">bloquea</td><td>—</td><td>doc</td><td>doc</td><td>—</td></tr>
  <tr><td>Verificación no exhaustiva</td><td>doc</td><td style="color:var(--amber)">alcance</td><td style="color:var(--amber)">alcance</td><td style="color:var(--amber)">alcance</td><td style="color:var(--amber)">alcance</td></tr>
  <tr><td>Diseño sin código</td><td>—</td><td>—</td><td style="color:var(--red)">bloquea</td><td>—</td><td style="color:var(--red)">bloquea</td></tr>
  <tr><td>Deriva sin medir</td><td>—</td><td>doc</td><td style="color:var(--amber)">alcance</td><td style="color:var(--amber)">alcance</td><td style="color:var(--amber)">alcance</td></tr>
</table>
<div class="grid-2" style="margin-top:12px">
  <div class="card"><h3 class="accent-indigo">P1 · Arreglar The Box</h3><p>Resolver los dos defectos y ver si entonces sirve para cosas más grandes.</p></div>
  <div class="card"><h3 class="accent-teal">P2 · Que colaborar funcione</h3><p>Buscar formas de trabajar en equipo donde hablar compense lo que cuesta.</p></div>
  <div class="card"><h3 style="color:var(--amber)">P3 · Verificar lo emergente</h3><p>Pasar de comprobar la estructura a comprobar el significado.</p></div>
  <div class="card"><h3 style="color:var(--plum)">P4 · Salir a la realidad</h3><p>Qué interfaz mínima haría falta para conectar The Box con sensores sin perder determinismo.</p></div>
  <div class="card"><h3 style="color:var(--red)">P5 · Medir la deriva</h3><p>Cómo medir que un agente se desvía si no tenemos una verdad contra la que comparar.</p></div>
  <div class="card"><h3 class="faint">P6 · Rust y TypeScript</h3><p>Consiguen la misma estructura pero no los mismos bytes. ¿Se puede arreglar?</p></div>
</div>'''))

S.append(dict(n=14, tag="REPRO + CTA", eyebrow="13 — REPRODUCIBILIDAD + CONTRATO + CTA", title="Comandos, contrato y formas de trabajar", plain=
    "Todo lo que ves se puede ejecutar. Debajo están los comandos exactos. Lo que traigo son 24 proyectos y una disciplina; lo que pido es gente que me exija más de lo que me exijo yo. Y abajo tienes cuatro maneras concretas de empezar, ninguna es 'a ver qué sale'.",
    body='''
<div class="col2">
  <div class="pre"><code>cargo test --package the-box
npm test &amp;&amp; npm run build
pytest experiments/e1_negative.py --bootstrap 10000
cargo test --workspace
cat hermes/SPEC.md</code>
    <p style="margin-top:12px;color:var(--amber);font-size:13px">Pido gente que exija más rigor del que yo tengo hoy.</p>
    <p style="color:var(--faint);font-size:12px">No traigo credenciales inventadas ni cifras infladas.</p></div>
  <div class="stack">
    <div class="card"><div class="bar" style="background:var(--green)"></div><h3 style="color:var(--green)">1 · Arreglar The Box</h3><p>Los dos defectos y ver si funciona en problemas más grandes.</p></div>
    <div class="card"><div class="bar" style="background:var(--teal)"></div><h3 class="accent-teal">2 · Invertir el resultado E1</h3><p>Encontrar formas de colaborar que sí compensen.</p></div>
    <div class="card"><div class="bar" style="background:var(--amber)"></div><h3 style="color:var(--amber)">3 · Convertir HERMES en real</h3><p>Pasar del papel al código y poder medirlo.</p></div>
    <div class="card"><div class="bar" style="background:var(--indigo)"></div><h3 class="accent-indigo">4 · Esta versión web (roadmap ✅)</h3><p>La presentación como web interactiva, generada sola desde la misma fuente. Ya está hecha.</p></div>
  </div>
</div>'''))

S.append(dict(n=15, tag="APÉNDICE", eyebrow="14 — APÉNDICE: CÓDIGO + STATS", title="Artefactos técnicos", plain=
    "Por si quieres mirar el código de verdad, aquí va un trozo de cada una de las tres piezas centrales y los números del experimento. Lo dejo al final para que no estorbe mientras cuento la historia.",
    body=diagram_appendix()))

S.append(dict(n=16, tag="PERSONAL", eyebrow="15 — QUIÉN SOY", title="", cls="personal",
    plain="Para terminar: soy Rubén, tengo 15 años y no soy nadie especial. Solo alguien al que le gusta construir cosas y aprender de gente que sabe más. Si algo de lo que has visto te interesa, escanea el código o escríbeme. Gracias por escuchar.",
    body='''
<div class="cols">
  <div class="panel left"><div class="vbar"></div>
    <h3>Rubén Núñez Sierra</h3><div class="age">15 años</div>
    <div class="handwrite">
      <p>No destaco por mis notas.</p><p>No soy popular.</p><div class="para"></div>
      <p>Simplemente me considero un adolescente<br>bastante ambicioso que quiere aprender<br>de mucha gente.</p><div class="para"></div>
      <p>Lo que ves aquí — The Box, NOX, ECHO,<br>SINGULARITY, HERMES, el Showcase —<br>no es "deberes". Es lo que construyo<br>cuando nadie me obliga.</p><div class="para"></div>
      <p>Mi disciplina es simple:<br>si no se puede ejecutar, medir y repetir,<br>no existe.</p><div class="para"></div>
      <p>Los defectos los documento.<br>Los negativos los publico.<br>La fidelidad la declaro.</p><div class="para"></div>
      <p>Busco gente que exija más rigor<br>del que yo tengo hoy.</p><div class="para"></div>
      <p>Gracias por leer hasta aquí.</p>
    </div>
  </div>
  <div class="panel right"><div class="vbar"></div>
    <h3 class="accent-indigo">CONTACTO + ARTEFACTOS</h3>
    <div class="contact-block">
      <div class="qr"><img src="assets/qr.png" alt="QR a github.com/ThorrijaDEV"></div>
      <div class="cap">Escanea → github.com/ThorrijaDEV</div>
      <div class="links">
        <div>github.com/ThorrijaDEV</div>
        <div>thorrijadev.github.io/showcase</div>
        <div>thorrijadev.github.io/Portafolio/</div>
        <div>thorrija.contact@gmail.com</div>
      </div>
      <div class="stats">24 proyectos · 5 sustratos · 182 tests<br>0 deps runtime · 1 disciplina</div>
    </div>
  </div>
</div>
<div class="bottom-quote">"No me creas. Ejecuta el código." · Fidelidad declarada · Defectos documentados · Negativos versionados</div>'''))

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
:root{
  --bg:#0b0b0d;--panel:#131317;--edge:#2a2a31;--ink:#f2f0eb;--muted:#9a9aa6;--faint:#6a6a76;
  --indigo:#8ea0e8;--amber:#c8944e;--teal:#5fb3ac;--plum:#a97fa2;--red:#c06a5f;
  --green:#6abf8b;--cyan:#4ec9b0;--orange:#d49b4a;
  --mono:'DejaVu Sans Mono',ui-monospace,monospace;--sans:'DejaVu Sans',system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--bg);color:var(--ink);font-family:var(--sans)}
.slide{width:100%;height:100%;background:var(--bg);padding:38px 56px;display:flex;flex-direction:column;position:relative}

/* BASE LAYOUT */
.eyebrow{font-family:var(--mono);font-size:12px;color:var(--indigo);letter-spacing:.08em;margin-bottom:10px;flex:none}
h1{font-size:88px;font-weight:700;letter-spacing:-.02em}
h2{font-size:32px;font-weight:700;line-height:1.12;flex:none}
h3{font-size:15px;font-weight:700}
p{font-size:13px;line-height:1.45}
.muted{color:var(--muted)}.faint{color:var(--faint)}.mono{font-family:var(--mono)}
.accent-indigo{color:var(--indigo)}.accent-teal{color:var(--teal)}
.rule{height:2px;background:var(--edge);width:100%;flex:none}
.rule-amber{height:3px;background:var(--amber)}
.footer{position:absolute;bottom:22px;left:56px;right:56px;display:flex;justify-content:space-between;
  font-family:var(--mono);font-size:11px;color:var(--faint)}

/* PLAIN LANGUAGE BLOCK — the speaker script */
.plain{background:#17140f;border-left:3px solid var(--amber);border-radius:4px;
  padding:10px 16px;margin-top:12px;flex:none}
.plain .lbl{font-family:var(--mono);font-size:10px;color:var(--amber);letter-spacing:.12em}
.plain p{font-size:14px;line-height:1.5;color:var(--ink);margin-top:3px;max-width:1450px}

/* CONTENT GRIDS */
.col2{display:grid;grid-template-columns:1fr 1fr;gap:22px;flex:1;align-content:center;margin-top:8px;min-height:0}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;flex:1;align-content:center;margin-top:8px;min-height:0}
.stack{display:flex;flex-direction:column;gap:10px}
.bullet{display:flex;gap:12px;align-items:flex-start;font-size:14px;line-height:1.4}
.bullet .k{color:var(--amber);font-family:var(--mono);flex:none}
.card{background:var(--panel);border:1px solid var(--edge);border-radius:8px;padding:16px;position:relative;overflow:hidden}
.card .bar{position:absolute;top:0;left:0;width:100%;height:4px}
.card h3{margin-bottom:8px;font-family:var(--mono)}

/* DIAGRAMS (HTML native — no overlap) */
.diag{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0;margin-top:6px}
.diag.cols{display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:center}
.diag-col{display:flex;flex-direction:column;gap:14px}
.formula{font-family:var(--mono);font-size:30px;color:var(--ink)}
.diag-rows{display:flex;flex-direction:column;gap:8px}
.diag-rows div{font-family:var(--mono);font-size:13px;color:var(--muted)}
.diag-rows b{color:var(--indigo)}
.mini-title{font-family:var(--mono);font-size:11px;color:var(--faint);letter-spacing:.08em}
.mini{background:var(--panel);border:1px solid var(--edge);border-left:3px solid var(--c);
  border-radius:6px;padding:10px 14px;display:flex;flex-direction:column;gap:4px}
.mini b{font-family:var(--mono);font-size:14px;color:var(--ink)}
.mini span{font-size:12px;color:var(--muted)}
.diag-band{background:var(--panel);border:1px solid var(--edge);border-radius:8px;padding:14px 18px}
.diag-band b{font-family:var(--mono);font-size:14px;color:var(--amber)}
.diag-band.green b{color:var(--green)}
.diag-band p{font-size:13px;color:var(--muted);margin-top:5px}
.diag-note{font-size:12px;color:var(--faint);font-style:italic;margin-top:8px;line-height:1.4}
.rule-row{display:flex;gap:12px;align-items:baseline;border-bottom:1px solid var(--edge);padding:7px 0}
.rule-row .rk{font-family:var(--mono);font-size:12px;color:var(--indigo);width:24px;flex:none}
.rule-row b{font-family:var(--mono);font-size:13px;color:var(--ink);width:100px;flex:none}
.rule-row span{font-size:13px;color:var(--muted)}
.orch{background:var(--panel);border:1.5px solid var(--indigo);border-radius:8px;padding:12px;
  text-align:center;font-family:var(--mono);font-size:17px;color:var(--indigo);margin-bottom:14px}
.orch span{display:block;font-family:var(--sans);font-size:12px;color:var(--muted);margin-top:4px}
.agent-row{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}
.agent-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.code-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.pre{background:var(--panel);border:1px solid var(--edge);border-radius:8px;padding:14px}
.pre.full{grid-column:1/-1}
code{font-family:var(--mono);font-size:11px;color:var(--muted);white-space:pre-wrap;line-height:1.45}
code .c{color:var(--faint)}code .kw{color:var(--indigo)}code .s{color:var(--teal)}
table{width:100%;border-collapse:collapse;margin-top:10px;font-size:11px}
th,td{border:1px solid var(--edge);padding:6px 8px;text-align:left}
th{font-family:var(--mono);color:var(--ink);background:var(--panel)}
td{color:var(--muted)}

/* COVER */
.cover{align-items:center;justify-content:center;text-align:center;gap:22px}
.cover .sub{font-size:24px;color:var(--muted)}
.cover .date{font-family:var(--mono);font-size:14px;color:var(--faint)}
.cover .links{font-family:var(--mono);font-size:13px;color:var(--amber)}

/* PERSONAL */
.personal .cols{display:grid;grid-template-columns:1fr 1fr;gap:20px;flex:1;margin-top:10px;min-height:0}
.panel{border:1px solid var(--edge);border-radius:8px;background:var(--panel);padding:20px;
  position:relative;overflow:hidden;display:flex;flex-direction:column}
.panel.left{border-color:var(--amber)}.panel.right{border-color:var(--indigo)}
.panel .vbar{position:absolute;left:0;top:0;bottom:0;width:3px}
.panel.left .vbar{background:var(--amber)}.panel.right .vbar{background:var(--indigo)}
.panel h3{font-family:var(--sans);font-size:19px}
.panel .age{color:var(--amber);font-size:14px;font-weight:700;margin-bottom:10px}
.handwrite p{font-size:12px;line-height:1.45;margin-bottom:6px}
.handwrite .para{height:8px}
.contact-block{display:flex;flex-direction:column;gap:10px;align-items:center;justify-content:center;flex:1;text-align:center}
.contact-block .qr{width:150px;height:150px;background:#f2f0eb;border-radius:6px;padding:5px}
.contact-block .qr img{width:100%;height:100%}
.contact-block .cap{font-family:var(--mono);font-size:10px;color:var(--faint)}
.contact-block .links{font-family:var(--mono);font-size:11px;line-height:1.7}
.contact-block .stats{font-family:var(--mono);font-size:10px;color:var(--amber);line-height:1.5}
.bottom-quote{font-family:var(--mono);font-size:11px;color:var(--amber);text-align:center;
  padding:10px;border:1px solid var(--amber);border-radius:4px;background:var(--panel);flex:none;margin-top:10px}

/* SCREEN vs PRINT */
@media screen{
  body{display:flex;align-items:center;justify-content:center;min-height:100vh;overflow:hidden}
  .deck{width:1600px;height:900px;position:relative;transform-origin:center center}
  .slide{display:none;position:absolute;inset:0}
  .slide.active{display:flex}
  .nav{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);z-index:99;
    display:flex;gap:10px;align-items:center;background:#131317ee;border:1px solid var(--edge);
    border-radius:20px;padding:6px 14px;font-family:var(--mono);font-size:12px}
  .nav button{background:none;border:1px solid var(--edge);color:var(--ink);border-radius:12px;
    padding:4px 12px;cursor:pointer;font-family:var(--mono);font-size:12px}
  .nav button:hover{border-color:var(--amber);color:var(--amber)}
  .counter{color:var(--faint)}
}
@media print{
  @page{size:1200pt 675pt;margin:0}
  html,body{width:1600px;height:auto;overflow:visible}
  html body .deck{width:1600px;height:auto;transform:none!important}
  html body .slide{display:flex!important;position:relative;width:1600px;height:900px;
    page-break-after:always;break-after:page;overflow:hidden}
  html body .slide:last-child{page-break-after:auto;break-after:auto}
  html body .nav{display:none!important}
  *{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
}
"""

JS = """
(function(){
  const slides=[...document.querySelectorAll('.slide')];
  let i=0; const counter=document.getElementById('counter');
  function show(n){
    i=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach((s,k)=>s.classList.toggle('active',k===i));
    counter.textContent=(i+1)+' / '+slides.length;
    try{if(location.hash!=='#'+(i+1))history.replaceState(null,'',location.pathname+'#'+(i+1));}catch(e){}
    window.scrollTo(0,0);
  }
  document.getElementById('prev').onclick=()=>show(i-1);
  document.getElementById('next').onclick=()=>show(i+1);
  document.addEventListener('keydown',e=>{
    if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();show(i+1)}
    if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(i-1)}
    if(e.key==='Home')show(0); if(e.key==='End')show(slides.length-1);
  });
  const h=parseInt(location.hash.slice(1),10); show(isNaN(h)?0:h-1);
  function fit(){const d=document.getElementById('deck');
    d.style.transform='scale('+Math.min(window.innerWidth/1600,window.innerHeight/900)+')';}
  window.addEventListener('resize',fit); fit();
  let sx=0;
  document.addEventListener('touchstart',e=>sx=e.changedTouches[0].screenX,{passive:true});
  document.addEventListener('touchend',e=>{const d=e.changedTouches[0].screenX-sx;if(d>60)show(i-1);if(d<-60)show(i+1)},{passive:true});
})();
"""

def build():
    DOCS.mkdir(exist_ok=True)
    parts = [f'''<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>THORRIJA — Presentación para equipo de investigación IA</title>
<style>{CSS}</style></head><body><div class="deck" id="deck">''']
    for s in S:
        cls = "slide" + (" " + s["cls"] if s.get("cls") else "")
        parts.append(f'<section class="{cls}">')
        if s["eyebrow"]:
            parts.append(f'<div class="eyebrow">{s["eyebrow"]}</div>')
        if s["title"]:
            parts.append(f'<h2>{s["title"]}</h2>')
        parts.append(s["body"])
        if s["plain"]:
            parts.append(f'<div class="plain"><div class="lbl">CÓMO EXPLICARLO — EN PALABRAS SENCILLAS</div><p>{s["plain"]}</p></div>')
        parts.append(f'<div class="footer"><span>{s["n"]}/16</span><span>{s["tag"]}</span></div>')
        parts.append('</section>')
    parts.append(f'''</div><div class="nav" id="nav">
<button id="prev">◀</button><span class="counter" id="counter">1 / 16</span><button id="next">▶</button>
</div><script>{JS}</script></body></html>''')
    out = DOCS / "index.html"
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"Generado {out} con {len(S)} slides")

if __name__ == "__main__":
    build()