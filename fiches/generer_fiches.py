import math, html
# ---------- Pont de Léonard (vue de côté), géométrie : bouts des planches SUR les traverses, milieu SOUS une traverse ----------
h=t=7.8; L=117.0; N=6; s=55.0
y=[-h/2]+[-h/2+(h+t)*k*(N-k) for k in range(1,N)]+[-h/2]   # centre des traverses, 0 et N = sol
def P(j): return y[j]+h/2+t/2   # hauteur du centre d'une planche posée sur la traverse j
S=1.55; X0=40; GY=300  # échelle px/mm, marge gauche, ligne du sol (px)
def X(x): return X0+x*S
def Y(v): return GY-v*S
def plank(k,col,lab):
    x1,y1=(k-1)*s,P(k-1); x2,y2=(k+1)*s,P(k+1)
    ang=math.atan2(y2-y1,x2-x1); cx,cy=(x1+x2)/2,(y1+y2)/2
    dx,dy=math.cos(ang)*L/2,math.sin(ang)*L/2
    ax,ay,bx,by=cx-dx,cy-dy,cx+dx,cy+dy
    nx,ny=-math.sin(ang)*t/2,math.cos(ang)*t/2
    pts=[(ax+nx,ay+ny),(bx+nx,by+ny),(bx-nx,by-ny),(ax-nx,ay-ny)]
    d=" ".join(f"{X(px):.1f},{Y(py):.1f}" for px,py in pts)
    lx,ly=X(cx-dx*0.55),Y(cy-dy*0.55)
    return f'<polygon points="{d}" fill="{col}" stroke="#5a3d1a" stroke-width="1.4"/>'+(f'<circle cx="{lx:.1f}" cy="{ly-16:.1f}" r="11" fill="#fff" stroke="#1d3a8a" stroke-width="1.5"/><text x="{lx:.1f}" y="{ly-11.5:.1f}" class="num">{lab}</text>' if lab else "")
def bar(k,lab,col="#e9c27a"):
    w=23.4
    return f'<rect x="{X(k*s-w/2):.1f}" y="{Y(y[k]+h/2):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="2" fill="{col}" stroke="#5a3d1a" stroke-width="1.4"/>'+(f'<circle cx="{X(k*s):.1f}" cy="{Y(y[k]+h/2)-17:.1f}" r="11" fill="#d1283a"/><text x="{X(k*s):.1f}" y="{Y(y[k]+h/2)-12.5:.1f}" class="num w">{lab}</text>' if lab else "")
order={}  # numéro de pose
n=1
order[("p",1)]=n;n+=1
for k in range(1,N):
    order[("b",k)]=n;n+=1
    if k+1<=N-1: order[("p",k+1)]=n;n+=1
# ordre réel : P1, T1, P2, T2, P3 ...  -> refaire proprement
seq=[("p",1),("b",1)]
for k in range(2,N): seq+= [("p",k),("b",k)]
order={e:i+1 for i,e in enumerate(seq)}
def bridge_svg(adult_until=0,highlight=None,labels=True,width=560):
    W=X(N*s)+40; H=GY+30
    out=[f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="{width}" xmlns="http://www.w3.org/2000/svg">',
         '<style>.num{font:700 13px "DejaVu Sans",sans-serif;text-anchor:middle;fill:#1d3a8a}.num.w{fill:#fff}</style>']
    # rivière + sol + butées
    out.append(f'<rect x="{X(1.2*s):.0f}" y="{GY:.0f}" width="{(3.6*s)*S:.0f}" height="14" fill="#9cc7ef"/>')
    out.append(f'<line x1="0" y1="{GY}" x2="{W:.0f}" y2="{GY}" stroke="#3a3a46" stroke-width="2"/>')
    for bx in (X(-L/2*0.95)-14, X(N*s+L/2*0.95)+2):
        out.append(f'<rect x="{bx:.0f}" y="{GY-34}" width="12" height="34" fill="#7d8597"/>')
    # traverses derrière, planches serrées (paires paires) derrière, écartées devant
    els=[]
    for k in range(1,N):
        els.append(("b",k))
    for k in range(2,N,2): els.insert(0,("p",k))
    for k in range(1,N,2): els.append(("p",k))
    for e in els:
        lab=order[e] if labels else None
        if e[0]=="p":
            col="#c98f4a" if e[1]%2 else "#f0d3a0"
            if highlight and e in highlight: col="#e05561"
            out.append(plank(e[1],col,lab))
        else:
            col="#e05561" if highlight and e in highlight else "#e9c27a"
            out.append(bar(e[1],lab,col))
    out.append('</svg>')
    return "".join(out)
def junction_svg():
    return '''<svg viewBox="0 0 320 150" width="250" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans" font-size="12">
<rect x="20" y="104" width="280" height="16" fill="#f0d3a0" stroke="#5a3d1a" stroke-width="1.5" transform="rotate(-6 160 112)"/>
<rect x="138" y="80" width="44" height="16" rx="2" fill="#e9c27a" stroke="#5a3d1a" stroke-width="1.5"/>
<rect x="40" y="52" width="122" height="16" fill="#c98f4a" stroke="#5a3d1a" stroke-width="1.5" transform="rotate(14 160 64)"/>
<rect x="160" y="52" width="122" height="16" fill="#c98f4a" stroke="#5a3d1a" stroke-width="1.5" transform="rotate(-14 160 64)"/>
<text x="10" y="22" fill="#1d3a8a">③ les BOUTS des planches : SUR la traverse</text>
<text x="192" y="95" fill="#d1283a">② traverse</text>
<text x="10" y="145" fill="#1d3a8a">① le MILIEU d'autres planches : SOUS la traverse</text></svg>'''
def top_svg():
    return '''<svg viewBox="0 0 300 130" width="230" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans" font-size="12">
<rect x="20" y="22" width="250" height="20" fill="#c98f4a" stroke="#5a3d1a"/><rect x="20" y="94" width="250" height="20" fill="#c98f4a" stroke="#5a3d1a"/>
<rect x="20" y="48" width="250" height="18" fill="#f0d3a0" stroke="#5a3d1a"/><rect x="20" y="70" width="250" height="18" fill="#f0d3a0" stroke="#5a3d1a"/>
<rect x="140" y="10" width="28" height="116" rx="2" fill="#e9c27a" stroke="#5a3d1a" opacity=".9"/>
<text x="176" y="20" fill="#5a3d1a">traverse</text></svg>'''

ROWS=[  # page, énigme, réponse, contenu, cachette par défaut
 (1,"Le mot secret","LUNE","Пакетик №1 внедорожника","Sous un coussin du canapé"),
 (2,"La devinette du jardin","L'escargot","Пакетик №2 внедорожника","Dans le panier à chaussures"),
 (3,"La suite mystère (J F M A M J ?)","J","Инструкция внедорожника, часть 1","Derrière les livres de l'étagère"),
 (4,"Le garage d'Anatole","La bleue","Инструкция внедорожника, часть 2","Sous le tapis de l'entrée"),
 (5,"СТРОЙКА 1 · Le tout-terrain (LEGO 11036)","—","—","—"),
 (6,"Les chiffres à l'envers","5","Пакетик астронавта","Sous la nappe"),
 (7,"L'invention","L'engrenage","Инструкция астронавта, часть 1","Salle de bain, serviettes"),
 (8,"La planète au chapeau","Saturne","Инструкция астронавта, часть 2","Dans le panier à linge"),
 (9,"СТРОЙКА 2 · Le pilote (LEGO 11037)","—","—","—"),
 (10,"Encore des lettres (L M M J V S ?)","D","Карточка моста, часть 1","Boîte à jouets"),
 (11,"Qui vit dans la rivière ?","Le poisson","Карточка моста, часть 2","Derrière un rideau"),
 (12,"Les piliers du pont","4","Картонная дорога","Sous le lit d'un enfant"),
 (13,"СТРОЙКА 3 · Le pont de Léonard (Kapla)","—","—","—"),
 (14,"Le calcul de roues","12","Пакетик №1 ракеты","Placard de la cuisine"),
 (15,"Le compte à rebours","2","Пакетик №2 ракеты","Tiroir de la cuisine"),
 (16,"Le mot mélangé","FUSÉE","Инструкция ракеты","Derrière la porte du salon"),
 (17,"СТРОЙКА 4 · La fusée (LEGO 11037)","—","—","—"),
 (18,"La dernière page","L'âge","Подарки (наборы LEGO)","La grande boîte, salon"),
]
rows="".join(f'<tr class="{"m" if r[2]=="—" else ""}"><td>{r[0]}</td><td>{html.escape(r[1])}</td><td>{html.escape(r[2])}</td><td>{html.escape(r[3])}</td><td>{html.escape(r[4])}</td><td class="box"></td></tr>' for r in ROWS)
LABELS=["Sac n°1 · Le tout-terrain","Sac n°2 · Le tout-terrain","Notice du tout-terrain · morceau 1","Notice du tout-terrain · morceau 2",
 "Sac · L'astronaute","Notice de l'astronaute · morceau 1","Notice de l'astronaute · morceau 2","La route en carton",
 "Sac n°1 · La fusée","Sac n°2 · La fusée","Notice de la fusée","La boîte d'Anatole"]
labels="".join(f'<div class="lab"><small>Le carnet d\'Anatole</small>{html.escape(l)}</div>' for l in LABELS)
def road():
    dash="".join(f'<rect x="{10+i*30}" y="27" width="18" height="4" fill="#fff"/>' for i in range(9))
    return f'<svg viewBox="0 0 280 58" width="100%" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="280" height="58" fill="#55595f"/><rect x="0" y="3" width="280" height="2" fill="#fff"/><rect x="0" y="53" width="280" height="2" fill="#fff"/>{dash}</svg>'
doc=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Fiches à imprimer</title><style>
@page{{size:A4;margin:12mm}}
body{{font-family:"Fira Sans","DejaVu Sans",sans-serif;color:#2b2b36;font-size:9.6pt;margin:0}}
h1,h2,h3{{font-family:"Comic Relief","Fira Sans",sans-serif;color:#1d3a8a;margin:0 0 4mm}}
h1{{font-size:20pt}} h2{{font-size:16pt}} h3{{font-size:12.5pt;margin-top:4mm}}
.page{{page-break-after:always}} .page:last-child{{page-break-after:auto}}
table{{border-collapse:collapse;width:100%;font-size:8.6pt}} td,th{{border:1px solid #b9cbe8;padding:.9mm 1.6mm;text-align:left;vertical-align:top}}
th{{background:#eef3fb}} tr.m td{{background:#e6f4ea;font-weight:600}} td.box{{width:7mm}}
ul,ol{{margin:1mm 0 2mm;padding-left:5mm}} li{{margin:.6mm 0}}
.card{{height:128mm;box-sizing:border-box;padding:6mm 8mm;border:2px solid #1d3a8a;border-radius:4mm;position:relative;overflow:hidden}}
.cut{{border:0;border-top:2px dashed #888;margin:5mm 0;position:relative}} .cut::after{{content:"✂ découper";position:absolute;right:0;top:-3.5mm;background:#fff;font-size:8pt;color:#888;padding-left:2mm}}
.tag{{position:absolute;top:5mm;right:8mm;font-family:"Comic Relief",sans-serif;color:#d1283a;font-size:12pt}}
.big{{font-size:11.5pt;line-height:1.35}} .big p{{margin:0 0 2mm}} .row{{display:flex;gap:6mm;align-items:center}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:0}} .lab{{border:1.5px dashed #888;height:34mm;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;font-family:"Comic Relief",sans-serif;font-size:17pt;color:#1d3a8a;padding:3mm}}
.lab small{{font-size:9pt;color:#d1283a;font-family:"Fira Sans",sans-serif;margin-bottom:2mm}}
.strip{{border:1px dashed #888;padding:3mm;margin:6mm 0}} .note{{font-size:9pt;color:#555}}
.legend span{{display:inline-block;width:10mm;height:3mm;border:1px solid #5a3d1a;margin-right:1.5mm;vertical-align:middle}}
</style></head><body>

<section class="page">
<h1>Квест «Le carnet d'Anatole» — подготовка</h1>
<p>Сайт: <b>nsviattsau.github.io/quete-r8</b>. При первом запуске придумайте 4-значный код и впишите имена детей. Тайники можно поменять в «Mode parent».</p>
<table><tr><th>Стр.</th><th>Загадка / стройка</th><th>Ответ</th><th>Что положить в тайник</th><th>Тайник по умолчанию</th><th>✓</th></tr>{rows}</table>
<h3>Что подготовить</h3>
<ul>
<li><b>LEGO 11036</b> (внедорожник / off-roader) и <b>11037</b> (астронавт и ракета): инструкции бесплатно на lego.com → Service → Building instructions → номер набора. Распечатайте страницы нужной модели. Инструкции внедорожника и астронавта разрежьте пополам (2 части), ракету оставьте целой.</li>
<li>По инструкции разложите детали каждой модели по пакетикам (внедорожник и ракета — на 2 пакетика, астронавт — 1). Наклейте этикетки со страницы 3.</li>
<li><b>Мост:</b> «река» на полу около 30 см (синяя лента или полотенце), два упора (книги, плинтус), 10 + 5 дощечек Капла. Карточку моста (стр. 2) разрежьте по пунктиру. До игры поставьте элементы <b>1–4</b> сами (это «fondations» Анатоля), рядом — стопку Капла. Обязательно соберите мост целиком один раз заранее.</li>
<li><b>Картонная дорога</b> (стр. 4): наклейте две полоски на картон и соедините скотчем.</li>
<li>Коробка «La boîte d'Anatole» для находок, подарочные наборы LEGO в «grande boîte».</li>
</ul>
</section>

<section class="page">
<div class="card"><div class="tag">Fiche du pont · morceau 1/2</div>
<h2>Le pont de Léonard de Vinci</h2>
<p class="big">Pas de clou, pas de colle : les planches se tiennent toutes seules ! Posez-les dans l'ordre des numéros. Anatole a déjà posé <b>1, 2, 3 et 4</b>.</p>
{bridge_svg()}
<p class="legend note"><span style="background:#c98f4a"></span>planches écartées &nbsp; <span style="background:#f0d3a0"></span>planches serrées &nbsp; <span style="background:#e9c27a"></span>traverses (numéros rouges)</p>
</div>
<hr class="cut">
<div class="card"><div class="tag">Fiche du pont · morceau 2/2</div>
<h2>Les 2 gestes à répéter</h2>
<div class="row" style="align-items:flex-start"><div class="big" style="flex:1">
<p><b>Geste 1.</b> Prenez 2 planches de l'autre sorte (écartées ↔ serrées). Posez leur bout arrière <b>SUR</b> la traverse qui est sur le milieu des dernières planches. Le bout avant touche le sol.</p>
<p><b>Geste 2.</b> Soulevez un peu l'avant des dernières planches et glissez une nouvelle traverse <b>DESSOUS</b>, posée sur le milieu des nouvelles planches.</p>
<p>Recommencez jusqu'à l'autre rive !</p></div>
<div>{top_svg()}<p class="note" style="text-align:center;margin:0">vu d'en haut</p>{junction_svg()}</div></div>
</div>
</section>

<section class="page">
<h2>Étiquettes</h2><p class="note">Découper et coller sur les sacs, les morceaux de notice et la boîte.</p>
<div class="grid">{labels}</div>
</section>

<section class="page">
<h2>La route en carton</h2>
<p class="note">Découper les deux bandes, les coller sur du carton fin (boîte de céréales), puis les assembler bout à bout avec du scotch. La route se pose sur le pont à la fin de la construction 3.</p>
<div class="strip">{road()}</div><div class="strip">{road()}</div>
</section>
</body></html>'''
open('fiches.html','w').write(doc)
print("ok", [round(v,1) for v in y])
