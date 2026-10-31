"""Builds the static site: index.html and one case-study page per project.
Edit the content here, then run:  python3 build.py
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
GH = "https://github.com/thatboypage"
LINKEDIN = "https://www.linkedin.com/in/richardolanite"
EMAIL = "richardolaniteolamide@gmail.com"
CV = "assets/Richard_Olanite_CV.pdf"
HAS_CV = (ROOT / CV).exists()

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,600..800&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}css/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M4 6v20M4 16 C12 16 20 14 28 8' stroke='%2318232c' stroke-width='3' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
</head>
<body>
<header class="site-head"><div class="wrap">
  {wordmark}
  <nav class="site-nav" aria-label="Main">
    <a href="{base}index.html#work">Work</a>
    <a href="{base}index.html#about">About</a>
    <a href="{base}index.html#experience">Experience</a>
    <a href="{base}index.html#writing">Writing</a>
    <a href="{base}index.html#contact">Contact</a>
{cvnav}  </nav>
</div></header>
"""

FOOT = """<footer class="site-foot"><div class="wrap">
  Richard Olamide Olanite, Lagos, Nigeria. Code for every project is public on <a href="{gh}">GitHub</a>.
</div></footer>
{script}
</body>
</html>
"""

# ---------------------------------------------------------------- projects
PROJECTS = [
  dict(
    slug="beamtwin",
    title="BeamTwin: a digital twin that finds damage in beams from their vibration",
    short="BeamTwin",
    row_title="BeamTwin: finding damage in a beam from how it vibrates",
    summary="Finite element model written from scratch, a physics-hybrid neural surrogate, and a Bayesian detector that locates damage from vibration readings. Deployed with a live demo.",
    stack="Python, NumPy, PyTorch, FastAPI, Docker, GitHub Actions",
    stat="55×", stat_label="lower frequency error than a plain neural network",
    thumb="beam-modes.jpg",
    lede="When a beam cracks it gets less stiff, and its natural frequencies drop. BeamTwin works backwards from those frequencies to say where the damage is and how bad it is.",
    facts=[("0.001%","FEM vs textbook frequency error, first four modes"),("55×","lower surrogate error with physics built in"),("0.3%","median location error, low-noise sensors"),("0.03 s","per damage estimate")],
    problem=[
      "Vibration-based structural health monitoring rests on a simple idea: damage lowers stiffness, and lower stiffness lowers natural frequencies. Turning a few measured frequencies back into a damage location is an inverse problem, and solving it needs thousands of simulations per estimate.",
      "A finite element model is accurate but too slow to run thousands of times on demand. The question was whether a neural network could stand in for it without losing the small frequency shifts that damage causes (about 1.5% on average).",
    ],
    approach=[
      "Wrote an Euler-Bernoulli beam finite element solver from scratch and validated it against textbook formulas: tip deflection matches PL³/3EI exactly, and the first four natural frequencies agree to within 0.001%.",
      "Trained two identical networks on the solver's results. The plain one learns everything from 7 inputs. The hybrid one gets the healthy frequencies from the exact cantilever formula and learns only the damage-induced ratio, which dimensional analysis shows depends on just 2 inputs.",
      "Built a Bayesian detector that scores 18,281 candidate damage states in one batch with the surrogate, and reports the most likely location and severity with 90% ranges and the probability that the beam is damaged at all.",
      "Served it with FastAPI and Docker, tested with pytest in GitHub Actions, and deployed a web demo where you hide damage in a beam and watch the twin find it.",
    ],
    figures=[
      ("beam-surrogate.jpg","Predicted vs true damage-induced frequency drop on 600 unseen beams. The hybrid surrogate (physics built in) sits on the diagonal."),
      ("beam-detection.jpg","Probability maps of damage location and severity from noisy vibration data: an easy case near the clamp, and a harder one near the free tip, where the estimate is close but slightly off."),
    ],
    table=dict(
      head=["", "Plain network", "Hybrid (physics + network)"],
      rows=[["Mean frequency error","0.38–0.42%","0.006–0.008%"],["Worst frequency error","2.1–2.8%","0.04–0.06%"],["Signal-to-error ratio","3–4","190–240"]],
      best=None, caption="Test set: 600 unseen beams. Damage lowers frequencies by about 1.5% on average, so the plain network's error is too large to see it reliably."),
    table2=dict(
      head=["Sensor noise","Low","Medium","High"],
      rows=[["Location error, median","0.3% of length","0.5%","1.3%"],["Damaged beams detected","100%","98%","100%"],["False alarms on healthy beams","0%","4%","32%"]],
      best=None, caption="Detector accuracy on 200 damaged and 50 healthy simulated beams per noise level."),
    limits=[
      "All results so far use simulated data. Validation on a physical clamped steel strip is the next step.",
      "Uniform beams and a single damage zone only. The detector assumes geometry and material are known exactly.",
      "With noisy sensors (±0.5% frequencies), about a third of healthy beams raise a false alarm.",
      "The surrogate is only valid inside its training ranges (0.5–2 m long, metals, up to 50% stiffness loss).",
    ],
    links=[("Code on GitHub", f"{GH}/beamtwin"), ("Live demo", "https://beamtwin.onrender.com")],
  ),
  dict(
    slug="filter-rul",
    title="Predicting when industrial filters will clog, when most never failed",
    short="Filter remaining life",
    row_title="Remaining-life prediction when 45 of 50 filters never failed",
    summary="A physics-informed clogging model predicts remaining useful life from right-censored data, then turns its uncertainty into replace-or-wait maintenance decisions.",
    stack="Python, SciPy, scikit-learn, XGBoost, survival analysis",
    stat="58%", stat_label="lower error than gradient boosting",
    thumb="rul-comparison.jpg",
    lede="Filters fail when their pressure drop reaches 600 Pa. In the training data only 5 of 50 were allowed to fail; the rest were replaced on schedule. I modelled how the pressure rises instead of guessing failure times.",
    facts=[("15.5 s","RMSE on the official test set (vs 36.4 s)"),("58%","lower error than gradient boosting"),("43%","lower simulated maintenance cost"),("2 vs 5","in-service failures vs historical schedule")],
    problem=[
      "Predictive maintenance needs remaining useful life. But when parts are replaced before they fail, their failure times are hidden (right-censored). Treating each replacement as a failure, the usual shortcut, teaches a model that filters die far earlier than they do.",
      "My first version of this project fell into exactly that trap, and later into target leakage. I retired it and rebuilt the approach from the physics. Both versions are kept in the repository.",
    ],
    approach=[
      "Censoring hides when filters fail, but not how their pressure rises. So every training trajectory is fully usable if you model the degradation signal instead of the labels.",
      "Modelled pressure against cumulative dust mass as a smooth transition from depth filtration to cake filtration, so that at high load it becomes linear in deposited mass, as cake-filtration theory predicts. Population parameters are fitted on all 50 censored trajectories; each filter gets its own onset and rate.",
      "For a new filter, inferred its parameters from its own history (MAP estimate), solved for the mass at which pressure reaches 600 Pa, and converted that to time.",
      "Chose the one tuned setting with a label-free check on the training set. The test set was used once.",
      "Turned predictions into a replace-or-wait rule using calibrated uncertainty, and priced it against the plant's historical schedule.",
    ],
    figures=[
      ("rul-comparison.jpg","Test-set error for each model, with 95% bootstrap intervals."),
      ("rul-costs.jpg","Long-run maintenance cost per 100 s of operation for each decision policy (failure costs 10× a planned change)."),
    ],
    table=dict(
      head=["Model","RMSE (s)","95% CI","Median % error"],
      rows=[["Physics-informed degradation model","15.5","9.9–20.6","21%"],["Hybrid: physics-imputed lives + gradient boosting","19.2","13.2–24.3","21%"],["Gradient boosting, replacement treated as failure","36.4","26.5–45.2","88%"],["Weibull survival model, no sensor data","62.9","52.3–73.0","136%"]],
      best=0, caption="Official test set, 50 filters. A leave-one-filter-out check on the training set agrees: 13.3 s vs 40.8 s."),
    table2=None,
    limits=[
      "Coarse dust is the weak point: RMSE 26.7 s vs 4.6 s for fine dust, because training never saw coarse-dust filters near failure.",
      "Uncertainty is under-calibrated: nominal 90% intervals cover 62% of test cases even after conformal calibration.",
      "A simple pressure alarm set from the 5 recorded failures does almost as well on cost (1.43 vs 1.37). The model's advantage is the remaining-life estimate, which the alarm cannot give.",
      "This is a laboratory benchmark with assumed cost ratios, so the savings are simulated, not plant savings.",
    ],
    links=[("Code on GitHub", f"{GH}/industrial-filter-predictive-maintenance")],
  ),
  dict(
    slug="anomaly-twin",
    title="A digital twin that catches anomalies and names the sensor that caused them",
    short="Anomaly detection twin",
    row_title="Anomaly detection that names the root-cause sensor",
    summary="A residual-based digital twin on a 5-million-point sensor benchmark, evaluated the way an operator experiences alarms: events caught, false alarms per day, delay.",
    stack="Python, NumPy, scikit-learn, system identification",
    stat="0.09", stat_label="false alarms per day, catching 80% of anomalies",
    thumb="cats-comparison.jpg",
    lede="Many anomalies look normal on their own and are only wrong relative to what the system was told to do. A model of the system's input-output behaviour can see them; generic detectors cannot.",
    facts=[("80%","of 146 unseen anomalies caught"),("0.09","false alarms per day"),("0.88","event F1 (PCA: 0.69)"),("98%","correct root-cause sensor")],
    problem=[
      "Industrial telemetry is full of normal variation driven by operator commands and the environment. A detector that ignores those inputs either misses anomalies or floods operators with false alarms.",
      "Most published scores on such benchmarks are also inflated by point-adjusted metrics. I wanted results an operator would recognise.",
    ],
    approach=[
      "Split the data the way it would run in operation: an anomaly-free period to fit models and measure normal error, one month only for choosing settings and thresholds, and three months as a test set scored once.",
      "For each telemetry channel, fitted a linear ARX model that predicts the channel from the commands and environmental inputs over the previous ~6 minutes. Fitted on normal data only.",
      "Scaled prediction errors by their normal size (robust MAD), smoothed over 60 s, and took the largest channel as both the anomaly score and the root-cause estimate.",
      "Compared against PCA reconstruction error and Isolation Forest using event recall, false alarms per day, event F1 and detection delay, without point adjustment.",
    ],
    figures=[
      ("cats-comparison.jpg","Event recall, false alarms per day and event F1 for each detector on the test months."),
      ("cats-example.jpg","An anomaly that PCA misses. The twin's prediction error is small to the eye but hundreds of times its normal size, so it crosses the alarm threshold set on validation data."),
    ],
    table=dict(
      head=["Detector","Event recall","False alarms / day","Event F1","Median delay"],
      rows=[["Digital-twin residuals","80%","0.09","0.88","6 s"],["PCA reconstruction error","55%","0.37","0.69","161 s"],["Isolation Forest, point-wise","32%","35.3","0.17","273 s"],["Isolation Forest, 60 s windows","58%","73.0","0.15","118 s"]],
      best=0, caption="Test set: 146 anomalies over about 35 days. All thresholds fixed on the validation month."),
    table2=None,
    limits=[
      "The benchmark is simulated and noise-free. With sensor noise added, the twin's event F1 falls to 0.69–0.77; it never drops below PCA, but at 1% noise the two are level.",
      "A real plant would need nonlinear or physics-based models, refitted whenever the plant changes.",
      "Weakest anomaly categories reach 67–69% recall, and PCA does better on two of the 13 categories.",
    ],
    links=[("Code on GitHub", f"{GH}/cats-digital-twin-anomaly-detection")],
  ),
  dict(
    slug="kw51-bridge",
    title="Separating temperature from structural change on a real railway bridge",
    short="KW51 railway bridge",
    row_title="Separating temperature from structural change on a real bridge",
    summary="15 months of measured data from the KW51 steel railway bridge in Leuven. A temperature model learned before a retrofit reveals what the retrofit actually changed.",
    stack="Python, NumPy, pandas, SciPy, blocked cross-validation, bootstrap",
    stat="98%", stat_label="of post-retrofit days flagged for mode 13, up from 0%",
    thumb="kw51-chart.jpg",
    lede="Temperature moves a bridge's natural frequencies as much as damage or repair does. Before anyone can say what a repair did, temperature has to be taken out.",
    facts=[("15 months","of hourly measured data"),("+2.1%","retrofit effect on mode 6, at fixed temperature"),("½","alarm band width for three of five modes"),("98%","post-retrofit days flagged (was 0%)")],
    problem=[
      "KW51 is a steel bowstring arch railway bridge between Leuven and Brussels, monitored by KU Leuven from 2018 to 2020. Damage was found at its connections, and the bridge was strengthened in 2019.",
      "Steel softens as it warms and stiffens sharply when it freezes, so the raw frequencies swing with the seasons. On a simple alarm chart, that swing hides the retrofit entirely for some modes.",
    ],
    approach=[
      "Used the five vibration modes tracked at least 80% of the time in every period, and the steel deck temperature.",
      "For each mode, modelled frequency as a linear function of temperature plus an extra stiffening term below a freezing knot. The model and knot were chosen by blocked cross-validation on the pre-retrofit months only, so nothing after the retrofit influenced the choice.",
      "Applied the pre-retrofit model unchanged during and after the works. The mean post-retrofit residual is the retrofit's effect at a fixed temperature, with bootstrap intervals.",
      "Compared alarm charts on raw and temperature-compensated frequencies.",
    ],
    figures=[
      ("kw51-temperature.jpg","Frequency against steel deck temperature for modes 6 and 13. Frequencies fall as the steel warms and jump below about 1 °C; the retrofit shifts the whole curve."),
      ("kw51-chart.jpg","Alarm chart for mode 13. Raw frequencies never flag the retrofit; compensated ones flag 98% of post-retrofit days."),
    ],
    table=None, table2=None,
    limits=[
      "A single freezing knot cannot follow a multi-day cold spell in January 2019; that spike causes most of the remaining false-alarm days.",
      "The confidence intervals cover measurement noise, not model error. For the noisier modes the estimate moves by up to 0.18 percentage points between comparison windows.",
      "KW51 is an established benchmark and its authors have studied these effects. This project reproduces that kind of analysis independently and adds per-mode, temperature-adjusted effect sizes with uncertainty.",
    ],
    links=[("Code on GitHub", f"{GH}/kw51-bridge-monitoring")],
  ),
  dict(
    slug="crack-segmentation",
    title="Measuring concrete crack width from photographs",
    short="Crack segmentation",
    row_title="Measuring crack width from photos, and a leak in a public benchmark",
    summary="A U-Net finds cracks in concrete photos and turns them into length and width. The engineering question: under what photo conditions is the width reliable enough for inspection?",
    stack="Python, PyTorch, segmentation-models-pytorch, OpenCV, scikit-image",
    stat="79%", stat_label="of a benchmark's test photos leaked into training",
    thumb="crack-resolution.jpg",
    lede="Design codes judge cracks by width (Eurocode 2 recommends about 0.3 mm). So instead of asking only whether a model finds cracks, I asked whether it can measure them well enough for an inspector.",
    facts=[("0.74","Dice on held-out photos (95% CI 0.71–0.77)"),("0.77","Dice on an unseen concrete dataset"),("79%","test photos leaking into training in the official split"),("12 px","minimum crack width for ±25% accuracy")],
    problem=[
      "Crack segmentation papers usually report overlap scores. Inspectors need widths in millimetres, and a model that draws every crack a few pixels too wide can score well while being useless for that.",
    ],
    approach=[
      "Traced the 9,159 images of CrackSeg9k back to about 1,635 original photographs, and found that 79% of the official test photos have crops in the training set. Re-split by original photograph.",
      "Trained a U-Net with a ResNet-34 encoder, and tested on held-out photos and on three datasets never used in training (concrete, asphalt, tiles).",
      "Converted predicted outlines into crack length and width, compared against the labels, and simulated camera distance by resizing to find where width becomes reliable.",
    ],
    figures=[
      ("crack-resolution.jpg","Left: predicted against true crack width at six image scales; thin cracks come out too wide. Right: the width error stays within ±25% only above about 12 px."),
      ("crack-width.jpg","Predicted vs labelled crack width."),
    ],
    table=None, table2=None,
    limits=[
      "Thin cracks are always drawn 2–4 px too wide, so width is reliable only above about 12 px: about 7 cm from the wall with a 12 MP phone camera, for a 0.3 mm crack.",
      "The model does not transfer to new materials: Dice 0.60 on asphalt and 0.29 on ceramic tiles.",
      "Width 'truth' is the dataset labels, whose style varies by source. Field validation with hand-measured cracks is in progress.",
    ],
    links=[("Code on GitHub", f"{GH}/concrete-crack-segmentation")],
  ),
]

def cvnav(base):
    return f'    <a href="{base}{CV}">CV (PDF)</a>\n' if HAS_CV else ""

def table_html(t):
    if not t: return ""
    th = "".join(f"<th{' class=\"num\"' if i else ''} scope=\"col\">{escape(h)}</th>" for i, h in enumerate(t["head"]))
    rows = ""
    for r_i, r in enumerate(t["rows"]):
        cls = ' class="best"' if t.get("best") == r_i else ""
        tds = "".join(f"<td{' class=\"num\"' if i else ''}>{escape(c)}</td>" for i, c in enumerate(r))
        rows += f"<tr{cls}>{tds}</tr>"
    return f'<div class="table-scroll"><table><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div><p class="prose" style="color:var(--ink-2);font-size:.92rem;margin-top:10px">{escape(t["caption"])}</p>'

def case_page(p, nxt):
    base = "../"
    facts = "".join(f"<div><strong>{escape(v)}</strong><span>{escape(l)}</span></div>" for v, l in p["facts"])
    probs = "".join(f"<p>{escape(x)}</p>" for x in p["problem"])
    appr = "".join(f"<li>{escape(x)}</li>" for x in p["approach"])
    figs = "".join(f'<figure class="plot"><img src="{base}assets/fig/{f}" alt="{escape(c)}" loading="lazy"><figcaption>{escape(c)}</figcaption></figure>' for f, c in p["figures"])
    lim = "".join(f"<li>{escape(x)}</li>" for x in p["limits"])
    links = "".join(f'<a class="btn{" primary" if i == 0 else ""}" href="{u}">{escape(t)}</a>' for i, (t, u) in enumerate(p["links"]))
    html = HEAD.format(title=f"{p['short']} | Richard Olamide Olanite", desc=escape(p["summary"]), base=base, cvnav=cvnav(base), wordmark=f'<a class="wordmark" href="{base}index.html">Richard Olamide Olanite</a>')
    html += f"""<main class="case"><div class="wrap">
<div class="case-head">
  <a class="back" href="{base}index.html#work">Back to all work</a>
  <h1>{escape(p['title'])}</h1>
  <p class="lede">{escape(p['lede'])}</p>
  <div class="facts">{facts}</div>
  <div class="links">{links}</div>
</div>
<section class="prose"><h2>The problem</h2>{probs}</section>
<section><h2>What I did</h2><ol>{appr}</ol></section>
<section><h2>Results</h2>{figs}{table_html(p['table'])}{table_html(p.get('table2'))}</section>
<section><h2>Limitations</h2><ul>{lim}</ul></section>
<div class="next"><a href="{nxt['slug']}.html">Next project: {escape(nxt['short'])}</a></div>
</div></main>
"""
    html += FOOT.format(gh=GH, script="")
    (ROOT / "projects" / f"{p['slug']}.html").write_text(html)

def index_page():
    cv_btn = f'<a class="btn" href="{CV}">Download CV</a>' if HAS_CV else ""
    cv_link = f' &nbsp; <a href="{CV}">CV (PDF)</a>' if HAS_CV else ""
    rows = ""
    for p in PROJECTS:
        rows += f"""<li><a class="row" href="projects/{p['slug']}.html">
  <div class="thumb"><img src="assets/fig/{p['thumb']}" alt="" loading="lazy"></div>
  <div><h3>{escape(p['row_title'])}</h3><p>{escape(p['summary'])}</p><p class="stack">{escape(p['stack'])}</p></div>
  <div class="result"><strong>{escape(p['stat'])}</strong><span>{escape(p['stat_label'])}</span></div>
</a></li>"""
    sensors = "".join('<circle class="sensor" r="7" cx="{:.1f}" cy="130"></circle>'.format(60 + (i + 1) / 9 * 1000) for i in range(9))
    hatch = "".join(f'<line x1="40" y1="{y}" x2="60" y2="{y-14}" class="wall"/>' for y in range(52, 222, 16))
    html = HEAD.format(title="Richard Olamide Olanite | Machine learning engineer",
                       desc="Machine learning engineer and mechanical engineer. Physics-informed ML for predictive maintenance, anomaly detection and structural health monitoring.",
                       base="", cvnav=cvnav(""), wordmark="<span></span>")
    html += f"""<main>
<div class="wrap hero">
 <div class="hero-top">
 <div>
  <p class="hero-name">Richard Olamide Olanite</p>
  <h1>I build models that understand the machines they monitor.</h1>
  <p class="lede">Machine learning engineer and mechanical engineer in Lagos. I combine physics with ML for predictive maintenance, anomaly detection and structural health monitoring, and I report every result with its baseline and its limits.</p>
  <div class="actions">
    <a class="btn primary" href="#work">See my work</a>
    {cv_btn}
    <a class="btn" href="{GH}">GitHub</a>
  </div>
 </div>
  <img class="portrait" src="assets/richard.jpg" alt="Portrait of Richard Olamide Olanite" width="600" height="750">
 </div>
  <figure class="beam-figure">
    <svg id="beam" viewBox="0 0 1100 260" role="img" aria-label="A cantilever beam clamped on the left, vibrating in one of its bending modes, with nine sensors along it.">
      <line x1="60" y1="40" x2="60" y2="220" class="wall"/>{hatch}
      <line x1="60" y1="130" x2="1060" y2="130" class="rest"/>
      <path class="shape" d="M60 130 L1060 130"/>
      {sensors}
    </svg>
    <figcaption class="beam-caption">
      <span class="mode-picker" role="group" aria-label="Choose a vibration mode">
        <button type="button" aria-pressed="true">Mode 1</button><button type="button" aria-pressed="false">Mode 2</button><button type="button" aria-pressed="false">Mode 3</button>
      </span>
      <span>BeamTwin's 1 m steel cantilever and its nine virtual sensors. My finite element model puts this mode at <strong id="mode-label">8.15 Hz</strong>.</span>
    </figcaption>
  </figure>
</div>

<section id="work"><div class="wrap">
  <h2>Selected work</h2>
  <p class="section-intro">Each project has public code, a held-out test, a baseline to beat, and a written list of what it does not do yet.</p>
  <ul class="work">{rows}</ul>
</div></section>

<section id="about"><div class="wrap about-grid">
  <div class="prose">
    <h2>About</h2>
    <p>I studied mechanical engineering at the University of Ilorin, and I came to machine learning through the machines: how they wear, vibrate and fail. I founded Berm Engineering and Consulting in 2026 to apply ML to structural inspection and predictive maintenance, and I lead its in-house research.</p>
    <p>My work sits where physics meets data. I build models that encode what engineers already know, test them against honest baselines, and turn their predictions into decisions someone can act on. The same methods carry over to fraud detection, risk and forecasting in any industry.</p>
    <div class="skills">
      <div><h3>Modelling</h3><p>Physics-informed and surrogate models, finite element analysis, Bayesian inference, survival analysis, anomaly detection, time series, Kalman filtering.</p></div>
      <div><h3>ML and software</h3><p>Python, PyTorch, TensorFlow, scikit-learn, XGBoost, SciPy, pandas, SQL, MATLAB, pytest, Git.</p></div>
      <div><h3>Deployment</h3><p>FastAPI, Docker, GitHub Actions, Streamlit, Render.</p></div>
      <div><h3>Learning now</h3><p>MLflow, cloud deployment on AWS and GCP, and LLM systems with retrieval-augmented generation.</p></div>
    </div>
  </div>
</div></section>

<section id="experience"><div class="wrap">
  <h2>Experience</h2>
  <ol class="timeline">
    <li class="now"><span class="when">Jan 2026 to now</span><h3>Machine Learning Engineer and Founder, Berm Engineering and Consulting Ltd, Lagos</h3><p>Delivered machine-learning projects for business and individual clients, covering inspection, defect detection and predictive maintenance. Lead in-house R&amp;D in anomaly detection, remaining-life prediction and computer vision, including the projects above.</p></li>
    <li><span class="when">Feb 2025 to Apr 2026</span><h3>Machine Learning Engineer, Digital Fortress Institute, Lagos</h3><p>Built a Streamlit app covering the full ML workflow for machine-failure data, applied supervised, unsupervised and reinforcement learning to predictive maintenance and process control, and taught ML tutorials to junior team members.</p></li>
    <li><span class="when">Oct 2018 to Aug 2024</span><h3>B.Eng. Mechanical Engineering, University of Ilorin</h3><p>Second Class Honours (Upper Division). Final-year project: designed and built a 10-tonne hydraulic press.</p></li>
    <li><span class="when">Apr 2022 to Nov 2022</span><h3>Mechanical Engineering Intern, University of Ilorin Central Workshop</h3><p>Maintained and repaired lathes, milling and drilling machines, and machined precision parts to GD&amp;T specifications.</p></li>
  </ol>
</div></section>

<section id="writing"><div class="wrap">
  <h2>Papers and posts</h2>
  <ul class="posts">
    <li><a href="{LINKEDIN}/recent-activity/all/">A prediction is not a decision</a><p>How I found my own predictive-maintenance model was answering the wrong question, and what rebuilding it taught me. LinkedIn post.</p></li>
    <li><a href="{LINKEDIN}/recent-activity/all/">Strong metrics, wrong behaviour</a><p>Target leakage and censored data in predictive maintenance. LinkedIn post.</p></li>
    <li><a href="https://doi.org/10.1007/s12008-026-02555-z">Numerical simulation of the compositions, processing, materials, and properties of automotive brake pad production</a><p>Co-author. International Journal on Interactive Design and Manufacturing, Springer, 2026.</p></li>
    <li><span>Characterization of oil from trunk fish (Mormyrus rume)</span><p>Co-author. Journal of Engineering Research and Applied Science, 15(1), 2026.</p></li>
  </ul>
</div></section>

<section id="contact" class="contact"><div class="wrap">
  <h2>Contact</h2>
  <p class="section-intro">I'm open to machine learning engineer and data scientist roles, remote or on-site, in any industry.</p>
  <p class="big"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
  <p><a href="{LINKEDIN}">LinkedIn</a> &nbsp; <a href="{GH}">GitHub</a>{cv_link}</p>
</div></section>
</main>
"""
    html += FOOT.format(gh=GH, script='<script src="js/beam.js"></script>')
    (ROOT / "index.html").write_text(html)

if __name__ == "__main__":
    index_page()
    for i, p in enumerate(PROJECTS):
        case_page(p, PROJECTS[(i + 1) % len(PROJECTS)])
    print("built", 1 + len(PROJECTS), "pages")
