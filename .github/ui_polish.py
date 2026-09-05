from pathlib import Path
import re
import subprocess
import tempfile

path = Path('index.html')
text = path.read_text(encoding='utf-8')


def replace_between(source, start, end, replacement):
    a = source.find(start)
    if a < 0:
        raise RuntimeError(f'missing start anchor: {start[:50]}')
    b = source.find(end, a)
    if b < 0:
        raise RuntimeError(f'missing end anchor: {end[:50]}')
    return source[:a] + replacement + source[b:]


marquee_css = '''.marquee{
  position:relative;overflow:hidden;contain:layout paint;
  border-top:1px solid var(--line-soft);border-bottom:1px solid var(--line-soft);
  background:var(--bg-panel);padding:18px 0;
}
.marquee::before,.marquee::after{
  content:"";position:absolute;top:0;bottom:0;width:min(8vw,88px);z-index:2;pointer-events:none;
}
.marquee::before{left:0;background:linear-gradient(90deg,var(--bg-panel),transparent);}
.marquee::after{right:0;background:linear-gradient(-90deg,var(--bg-panel),transparent);}
.marquee-track{
  display:flex;align-items:center;width:max-content;white-space:nowrap;
  transform:translate3d(0,0,0);will-change:transform;
}
.marquee-track span{
  font-family:var(--font-display);font-weight:700;
  font-size:clamp(20px,3.4vw,34px);letter-spacing:-0.01em;
  color:transparent;-webkit-text-stroke:1px var(--line);
  padding:0 18px;
}
.marquee-track span.dot{
  -webkit-text-stroke:0;color:var(--accent);font-size:14px;padding:0 4px;vertical-align:middle;
}
@media (prefers-reduced-motion: reduce){
  .marquee-track{transform:none !important;will-change:auto;}
}
'''
text = replace_between(text, '.marquee{\n', '\n \n.manifesto{', marquee_css)

boot_css = '''#boot-screen{
  position:fixed;inset:0;z-index:9998;background:var(--bg);
  display:flex;align-items:center;justify-content:center;padding:18px;
  opacity:1;visibility:visible;
  transition:opacity .55s var(--ease),visibility 0s linear .55s;
}
#boot-screen::before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:
    radial-gradient(circle at 50% 46%,var(--accent-glow),transparent 34%),
    linear-gradient(var(--line-soft) 1px,transparent 1px),
    linear-gradient(90deg,var(--line-soft) 1px,transparent 1px);
  background-size:auto,42px 42px,42px 42px;opacity:.32;
  mask-image:radial-gradient(circle at center,#000 18%,transparent 72%);
  -webkit-mask-image:radial-gradient(circle at center,#000 18%,transparent 72%);
}
#boot-screen.boot-done{opacity:0;visibility:hidden;pointer-events:none;}
.boot-inner{
  position:relative;width:min(680px,calc(100vw - 36px));overflow:hidden;
  border:1px solid var(--line);border-radius:14px;background:var(--bg-card);
  box-shadow:0 32px 90px -34px rgba(0,0,0,.72),0 0 0 1px var(--accent-glow);
  font-family:var(--font-mono);font-size:13px;color:var(--text-dim);
}
.boot-head{
  display:flex;align-items:center;justify-content:space-between;gap:18px;
  padding:12px 16px;border-bottom:1px solid var(--line);background:var(--bg-panel);
}
.boot-brand{color:var(--text);font-weight:600;letter-spacing:.01em;}
.boot-prompt{color:var(--accent);margin-right:8px;}
.boot-state{display:inline-flex;align-items:center;gap:7px;color:var(--text-dimmer);font-size:11px;text-transform:uppercase;letter-spacing:.09em;}
.boot-state::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 3px var(--accent-glow);animation:bootPulse 1.4s ease-in-out infinite;}
.boot-console{padding:22px 22px 18px;}
#bootInner{min-height:116px;display:flex;flex-direction:column;justify-content:flex-end;}
.boot-line{opacity:0;white-space:pre-wrap;line-height:1.8;transform:translateY(4px);transition:opacity .22s ease,transform .32s var(--ease);}
.boot-line.visible{opacity:1;transform:translateY(0);}
.boot-line.ok{color:var(--accent);}
body.boot-lock{overflow:hidden;}
.boot-bar-row{display:flex;align-items:center;gap:12px;margin-top:14px;opacity:0;transition:opacity .3s ease;}
.boot-bar-row.show{opacity:1;}
.boot-bar{position:relative;flex:1;height:4px;background:var(--line);border-radius:999px;overflow:hidden;}
.boot-bar-fill{position:absolute;left:0;top:0;height:100%;width:0%;background:linear-gradient(90deg,var(--accent-dim),var(--accent));box-shadow:0 0 10px var(--accent-glow);will-change:width;}
.boot-pct{font-size:12px;color:var(--accent);min-width:40px;text-align:right;font-variant-numeric:tabular-nums;}
.boot-meta{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-top:10px;font-size:10.5px;color:var(--text-dimmer);}
.boot-stage{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.boot-skip{white-space:nowrap;opacity:.72;}
@keyframes bootPulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:.42;transform:scale(.72);}}
@media (max-width:540px){
  .boot-console{padding:18px 16px 15px;}
  #bootInner{min-height:104px;}
  .boot-state{display:none;}
  .boot-meta{font-size:10px;}
}
@media (prefers-reduced-motion: reduce){#boot-screen{display:none;}.boot-state::before{animation:none;}}
'''
text = replace_between(text, '#boot-screen{\n', '\n\n \n.hero-mark{', boot_css)

boot_markup = '''<div id="boot-screen" aria-hidden="true">
  <div class="boot-inner">
    <div class="boot-head">
      <span class="boot-brand"><span class="boot-prompt">&gt;_</span>hans@sysadmin</span>
      <span class="boot-state" id="bootState">initializing</span>
    </div>
    <div class="boot-console">
      <div id="bootInner"></div>
      <div class="boot-bar-row" id="bootBarRow">
        <div class="boot-bar"><div class="boot-bar-fill" id="bootBarFill"></div></div>
        <span class="boot-pct" id="bootPct">0%</span>
      </div>
      <div class="boot-meta">
        <span class="boot-stage" id="bootStage">starting local session</span>
        <span class="boot-skip" id="bootSkip">Esc / tap to skip</span>
      </div>
    </div>
  </div>
</div>
'''
text = replace_between(text, '<div id="boot-screen" aria-hidden="true">\n', '<div id="scroll-progress"></div>', boot_markup)

icon_card = '''        <div class="mini-card stagger-item">
          <h4>Icon system</h4>
          <p>Even the favicon is on-brand: a hand-drawn terminal prompt glyph, vector, generated at every size from one SVG source.</p>
          <button class="also-more" type="button" aria-expanded="false">View more <span aria-hidden="true">+</span></button>
          <div class="also-detail">
            <p>One SVG source exports to every favicon size plus the apple-touch icon, so the terminal-prompt mark stays crisp from a browser tab to a phone home screen, in light or dark theme, with no separate art pass per size.</p>
          </div>
          <a href="favicon.ico" target="_blank" rel="noopener">View favicon.ico</a>
        </div>
'''
if text.count(icon_card) != 1:
    raise RuntimeError('Icon system card anchor changed')
text = text.replace(icon_card, '')
text = text.replace(
    '.also-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px;}',
    '.also-grid{display:grid;grid-template-columns:minmax(0,720px);gap:18px;}'
)

marquee_js = '''(function(){
  var track = document.querySelector('.marquee-track');
  var section = document.querySelector('.marquee');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!track || !section) return;
  if(reduce){ track.style.transform = 'translate3d(0,0,0)'; return; }

  var BASE_SPEED = 34;
  var MAX_BOOST = 92;
  var offset = 0;
  var loopWidth = 0;
  var scrollImpulse = 0;
  var scrollBoost = 0;
  var hoverTarget = 1;
  var hoverFactor = 1;
  var inView = true;
  var raf = null;
  var lastFrame = 0;
  var lastScrollY = window.scrollY;
  var lastScrollAt = performance.now();

  function measure(){
    loopWidth = track.scrollWidth / 2;
    if(loopWidth > 0){
      offset = -(Math.abs(offset) % loopWidth);
      track.style.transform = 'translate3d(' + offset.toFixed(2) + 'px,0,0)';
    }
  }

  function onScroll(){
    var now = performance.now();
    var y = window.scrollY;
    var dt = Math.max(16, now - lastScrollAt);
    var velocity = Math.abs(y - lastScrollY) / dt * 1000;
    scrollImpulse = Math.min(MAX_BOOST, velocity * 0.036);
    lastScrollY = y;
    lastScrollAt = now;
  }

  function frame(now){
    if(!inView || document.hidden){ raf = null; lastFrame = 0; return; }
    var dt = lastFrame ? Math.min(0.05, (now - lastFrame) / 1000) : 0;
    lastFrame = now;
    scrollBoost += (scrollImpulse - scrollBoost) * Math.min(1, dt * 8);
    scrollImpulse *= Math.exp(-dt * 6);
    hoverFactor += (hoverTarget - hoverFactor) * Math.min(1, dt * 7);
    if(loopWidth > 0 && dt > 0){
      offset -= (BASE_SPEED + scrollBoost) * hoverFactor * dt;
      if(offset <= -loopWidth) offset += loopWidth;
      track.style.transform = 'translate3d(' + offset.toFixed(2) + 'px,0,0)';
    }
    raf = requestAnimationFrame(frame);
  }

  function start(){
    if(!raf && inView && !document.hidden){ lastFrame = 0; raf = requestAnimationFrame(frame); }
  }
  function stop(){
    if(raf){ cancelAnimationFrame(raf); raf = null; }
    lastFrame = 0;
  }

  section.addEventListener('pointerenter', function(){ hoverTarget = 0.24; });
  section.addEventListener('pointerleave', function(){ hoverTarget = 1; });
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', function(){ measure(); start(); });
  document.addEventListener('visibilitychange', function(){ if(document.hidden) stop(); else start(); });
  if('ResizeObserver' in window) new ResizeObserver(measure).observe(track);
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(measure).catch(function(){});
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(entries){
      inView = entries[0].isIntersecting;
      if(inView) start(); else stop();
    }, {rootMargin:'100px 0px',threshold:0}).observe(section);
  }
  measure();
  start();
})();
'''
marquee_start = "(function(){\n  var track = document.querySelector('.marquee-track');\n"
marquee_end = "\n})();\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n(function(){\n  var screen = document.getElementById('boot-screen');"
a = text.find(marquee_start)
b = text.find(marquee_end, a)
if a < 0 or b < 0:
    raise RuntimeError('marquee JS anchors changed')
text = text[:a] + marquee_js + "\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + text[b + len("\n})();\n\n\n\n\n\n\n\n\n\n\n\n\n\n"):]

boot_js = '''(function(){
  var screen = document.getElementById('boot-screen');
  var inner = document.getElementById('bootInner');
  var stateEl = document.getElementById('bootState');
  var stageEl = document.getElementById('bootStage');
  var barRow = document.getElementById('bootBarRow');
  var barFill = document.getElementById('bootBarFill');
  var pctEl = document.getElementById('bootPct');
  if(!screen || !inner) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var seen = false;
  try{ seen = sessionStorage.getItem('hs_booted') === '1'; }catch(e){}
  if(reduce || seen){ screen.hidden = true; return; }

  document.body.classList.add('boot-lock');
  var flags = {dom:false,fonts:false,visual:false,min:false};
  var target = 0.08;
  var shown = 0;
  var finished = false;
  var finishRequested = false;
  var finishTimer = null;
  var raf = null;

  function setState(state, stage){
    if(stateEl) stateEl.textContent = state;
    if(stageEl) stageEl.textContent = stage;
  }
  function printLine(text, ok){
    var d = document.createElement('div');
    d.className = 'boot-line' + (ok ? ' ok' : '');
    d.textContent = text;
    inner.appendChild(d);
    requestAnimationFrame(function(){ d.classList.add('visible'); });
  }
  function milestone(name, progress, line, state, stage){
    if(flags[name]) return;
    flags[name] = true;
    target = Math.max(target, progress);
    printLine(line, true);
    setState(state, stage);
    maybeFinish();
  }
  function requestFinish(){
    if(finishRequested || finished) return;
    finishRequested = true;
    target = 1;
    printLine('> status: READY_', true);
    setState('ready', 'entering portfolio');
  }
  function maybeFinish(){
    if(flags.min && flags.dom && flags.fonts && flags.visual) requestFinish();
  }
  function finish(){
    if(finished) return;
    finished = true;
    if(raf) cancelAnimationFrame(raf);
    if(finishTimer) clearTimeout(finishTimer);
    try{ sessionStorage.setItem('hs_booted', '1'); }catch(e){}
    document.body.classList.remove('boot-lock');
    screen.classList.add('boot-done');
    window.removeEventListener('keydown', onKey);
    screen.removeEventListener('pointerdown', skip);
    setTimeout(function(){ screen.hidden = true; }, 600);
  }
  function skip(){
    if(finished) return;
    shown = Math.max(shown, 0.965);
    requestFinish();
  }
  function onKey(e){ if(e.key === 'Escape') skip(); }
  function frame(){
    shown += (target - shown) * 0.13;
    if(target >= 1 && target - shown < 0.004) shown = 1;
    var pct = Math.max(1, Math.min(100, Math.round(shown * 100)));
    if(barFill) barFill.style.width = pct + '%';
    if(pctEl) pctEl.textContent = pct + '%';
    if(shown >= 1){ setTimeout(finish, 180); return; }
    raf = requestAnimationFrame(frame);
  }

  printLine('> session: hans@sysadmin ... [ok]', true);
  setState('initializing', 'mounting interface');
  if(barRow) requestAnimationFrame(function(){ barRow.classList.add('show'); });
  raf = requestAnimationFrame(frame);

  requestAnimationFrame(function(){
    milestone('dom', 0.36, '> interface mounted ... [ok]', 'loading', 'preparing typography');
  });
  if(document.fonts && document.fonts.ready){
    document.fonts.ready.then(function(){
      milestone('fonts', 0.66, '> typography ready ... [ok]', 'loading', 'preparing visual assets');
    }).catch(function(){
      milestone('fonts', 0.66, '> typography fallback ready ... [ok]', 'loading', 'preparing visual assets');
    });
  }else{
    milestone('fonts', 0.66, '> typography ready ... [ok]', 'loading', 'preparing visual assets');
  }
  (function(){
    var img = document.querySelector('.about-photo img, img[src*="headshot"]');
    function ready(){ milestone('visual', 0.9, '> visual assets ready ... [ok]', 'finalizing', 'checking runtime'); }
    if(img && img.decode) img.decode().then(ready).catch(ready);
    else if(img && img.complete) ready();
    else if(img){ img.addEventListener('load', ready, {once:true}); img.addEventListener('error', ready, {once:true}); }
    else ready();
  })();

  setTimeout(function(){ flags.min = true; maybeFinish(); }, 820);
  finishTimer = setTimeout(requestFinish, 1900);
  window.addEventListener('keydown', onKey);
  screen.addEventListener('pointerdown', skip);
})();
'''
boot_start = "(function(){\n  var screen = document.getElementById('boot-screen');\n"
boot_end = "\n})();\n\n \n(function(){\n  var lines = ["
a = text.find(boot_start)
b = text.find(boot_end, a)
if a < 0 or b < 0:
    raise RuntimeError('boot JS anchors changed')
text = text[:a] + boot_js + "\n \n(function(){\n  var lines = [" + text[b + len(boot_end):]

checks = [
    ('Icon system' not in text, 'Icon system card remains'),
    ('View favicon.ico' not in text, 'favicon card link remains'),
    ('animation:marqueeScroll' not in text, 'legacy marquee CSS remains'),
    ('BASE_DUR' not in text, 'legacy marquee JS remains'),
    ('press any key to skip' not in text, 'legacy skip copy remains'),
    ('Esc / tap to skip' in text, 'new skip copy missing'),
    (text.count('id="boot-screen"') == 1, 'boot screen count'),
    (text.count('id="bootState"') == 1, 'boot state count'),
    (text.count('id="bootStage"') == 1, 'boot stage count'),
    (text.count('class="mini-card stagger-item"') == 1, 'mini card count'),
]
for ok, message in checks:
    if not ok:
        raise RuntimeError(message)

path.write_text(text, encoding='utf-8')

scripts = re.findall(r'(?is)<script\b(?![^>]*\bsrc=)([^>]*)>(.*?)</script\s*>', text)
with tempfile.TemporaryDirectory() as td:
    n = 0
    for attrs, body in scripts:
        if 'application/ld+json' in attrs.lower():
            continue
        n += 1
        js = Path(td) / f'script-{n}.js'
        js.write_text(body, encoding='utf-8')
        subprocess.run(['node', '--check', str(js)], check=True)

print('UI polish applied and inline JavaScript syntax validated.')
