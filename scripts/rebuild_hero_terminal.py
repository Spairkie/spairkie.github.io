from pathlib import Path

path = Path('index.html')
s = path.read_text(encoding='utf-8')

old_grid = """  .hero-inner{\n    max-width:1300px;\n    display:grid;\n    grid-template-columns:minmax(0,1fr) minmax(360px,420px);\n    align-items:start;\n    column-gap:56px;\n  }\n  .hero-inner .terminal{max-width:none;width:100%;margin-top:6px;}\n"""
new_grid = """  .hero-inner{\n    max-width:1360px;\n    display:grid;\n    grid-template-columns:minmax(0,1fr) minmax(420px,500px);\n    align-items:start;\n    column-gap:48px;\n  }\n  .hero-inner .terminal{max-width:none;width:100%;margin-top:6px;}\n"""
assert old_grid in s, 'desktop hero grid block not found'
s = s.replace(old_grid, new_grid, 1)

old_css = """ \n.terminal{\n  max-width:560px;\n  background:var(--bg-card);\n  border:1px solid var(--line);\n  border-radius:10px;\n  overflow:hidden;\n  box-shadow:0 20px 60px -20px rgba(0,0,0,0.6);\n}\n.terminal-bar{\n  display:flex;align-items:center;gap:8px;padding:10px 14px;\n  border-bottom:1px solid var(--line);background:var(--bg-panel);\n}\n.terminal-dot{width:10px;height:10px;border-radius:50%;}\n.terminal-dot.red{background:#ff5f56;}\n.terminal-dot.yellow{background:#ffbd2e;}\n.terminal-dot.green{background:#27c93f;}\n.terminal-title{font-family:var(--font-mono);font-size:12px;color:var(--text-dimmer);margin-left:6px;}\n.terminal-body{\n  padding:16px 18px 20px;font-family:var(--font-mono);font-size:13.5px;line-height:1.85;\n  min-height:150px;\n}\n.terminal-body .prompt{color:var(--accent);}\n.terminal-line{color:var(--text-dim);white-space:pre-wrap;}\n.terminal-out{color:var(--text);}\n"""
new_css = """ \n.terminal{\n  --term-bg:#07100f;--term-panel:#0b1514;--term-panel-2:#0d1917;--term-line:rgba(94,234,212,.16);\n  --term-line-strong:rgba(94,234,212,.34);--term-text:#dff8f2;--term-dim:#82a39c;--term-dimmer:#5f7d77;\n  max-width:580px;position:relative;isolation:isolate;overflow:hidden;\n  background:linear-gradient(180deg,#0a1312 0%,var(--term-bg) 100%);\n  border:1px solid var(--term-line-strong);border-radius:14px;\n  box-shadow:0 28px 80px -34px rgba(0,0,0,.9),0 0 0 1px rgba(94,234,212,.035),0 0 70px -45px rgba(94,234,212,.55);\n  color:var(--term-text);transform:translateZ(0);\n  transition:border-color .25s ease,box-shadow .35s ease,transform .35s var(--ease);\n}\n.terminal::before{\n  content:\"\";position:absolute;inset:-1px;z-index:0;pointer-events:none;opacity:.55;\n  background:radial-gradient(380px circle at 88% -5%,rgba(94,234,212,.13),transparent 64%),radial-gradient(260px circle at 8% 112%,rgba(240,180,41,.06),transparent 68%);\n}\n.terminal::after{\n  content:\"\";position:absolute;inset:0;z-index:4;pointer-events:none;opacity:.12;mix-blend-mode:screen;\n  background:repeating-linear-gradient(180deg,rgba(255,255,255,.018) 0,rgba(255,255,255,.018) 1px,transparent 1px,transparent 4px);\n}\n.terminal > *{position:relative;z-index:2;}\n:root[data-theme=\"light\"] .terminal{box-shadow:0 24px 64px -32px rgba(31,42,38,.42),0 0 0 1px rgba(20,140,124,.08);}\n.terminal:hover{border-color:rgba(94,234,212,.46);}\n.terminal-bar{\n  min-height:44px;display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:12px;padding:0 14px;\n  border-bottom:1px solid var(--term-line);background:rgba(9,18,17,.92);backdrop-filter:blur(10px);\n}\n.terminal-window-controls{display:flex;align-items:center;gap:6px;}\n.terminal-dot{width:9px;height:9px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(0,0,0,.18);}\n.terminal-dot.red{background:#ff5f56;}.terminal-dot.yellow{background:#ffbd2e;}.terminal-dot.green{background:#27c93f;}\n.terminal-bar-title{min-width:0;display:flex;align-items:center;gap:7px;font-family:var(--font-mono);font-size:11.5px;overflow:hidden;}\n.terminal-title{color:var(--term-text);font-weight:600;white-space:nowrap;}\n.terminal-path{color:var(--term-dimmer);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}\n.terminal-bar-actions{display:flex;align-items:center;gap:10px;}\n.terminal-live{display:inline-flex;align-items:center;gap:6px;font-family:var(--font-mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--term-dim);white-space:nowrap;}\n.terminal-live::before{content:\"\";width:6px;height:6px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 3px rgba(94,234,212,.09),0 0 10px rgba(94,234,212,.45);}\n.terminal-copy{border:0;background:transparent;color:var(--term-dimmer);font-family:var(--font-mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.08em;padding:5px 0;cursor:pointer;transition:color .2s ease;}\n.terminal-copy:hover,.terminal-copy:focus-visible{color:var(--accent);}\n.terminal-snapshot{padding:15px 16px 13px;border-bottom:1px solid var(--term-line);background:linear-gradient(135deg,rgba(94,234,212,.055),transparent 48%);}\n.terminal-snapshot-main{display:flex;align-items:center;gap:11px;margin-bottom:12px;}\n.terminal-avatar{width:34px;height:34px;display:grid;place-items:center;flex:0 0 auto;border:1px solid var(--term-line-strong);background:rgba(94,234,212,.055);color:var(--accent);font-family:var(--font-mono);font-size:13px;font-weight:600;}\n.terminal-identity{min-width:0;line-height:1.2;}\n.terminal-identity strong{display:block;font-family:var(--font-display);font-size:14px;letter-spacing:-.01em;color:var(--term-text);}\n.terminal-identity small{display:block;margin-top:4px;font-family:var(--font-mono);font-size:9.8px;line-height:1.45;color:var(--term-dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}\n.terminal-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid var(--term-line);background:rgba(3,9,8,.26);}\n.terminal-fact{min-width:0;padding:7px 9px;border-right:1px solid var(--term-line);font-family:var(--font-mono);line-height:1.25;}\n.terminal-fact:last-child{border-right:0;}\n.terminal-fact b{display:block;margin-bottom:3px;font-size:8px;font-weight:500;letter-spacing:.11em;color:var(--term-dimmer);}\n.terminal-fact span{display:block;font-size:10.5px;color:var(--term-text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}\n.terminal-screen{position:relative;background:rgba(3,8,8,.62);}\n.terminal-body{\n  min-height:190px;max-height:248px;overflow-y:auto;overscroll-behavior:contain;padding:14px 16px 12px;\n  font-family:var(--font-mono);font-size:11.5px;line-height:1.62;scrollbar-width:thin;scrollbar-color:rgba(94,234,212,.22) transparent;\n}\n.terminal-body::-webkit-scrollbar{width:5px}.terminal-body::-webkit-scrollbar-track{background:transparent}.terminal-body::-webkit-scrollbar-thumb{background:rgba(94,234,212,.22);border-radius:4px;}\n.term-entry{margin:0 0 9px;white-space:pre-wrap;word-break:break-word;}\n.term-entry:last-child{margin-bottom:0;}\n.term-entry.term-boot{opacity:0;transform:translateY(4px);animation:termLineIn .38s var(--ease) forwards;animation-delay:var(--term-delay,0ms);}\n@keyframes termLineIn{to{opacity:1;transform:translateY(0)}}\n.term-command-line{display:flex;align-items:flex-start;gap:7px;color:var(--term-text);}\n.term-shell-prompt{color:var(--accent);white-space:nowrap;user-select:none;}\n.term-command-text{color:#b7d6cf;}\n.term-output{padding-left:0;color:var(--term-dim);}\n.term-output.ok{color:#8ee8cf}.term-output.bright{color:var(--term-text)}.term-output.warn{color:#f4ca70}.term-output.err{color:#ff9b9b;}\n.term-output .term-label{color:var(--term-dimmer);}\n.terminal-quickbar{display:flex;gap:6px;padding:8px 10px;border-top:1px solid var(--term-line);border-bottom:1px solid var(--term-line);background:rgba(11,21,20,.76);overflow-x:auto;scrollbar-width:none;}\n.terminal-quickbar::-webkit-scrollbar{display:none;}\n.term-quick{flex:0 0 auto;border:1px solid var(--term-line);background:rgba(94,234,212,.025);color:var(--term-dim);font-family:var(--font-mono);font-size:9.5px;padding:5px 8px;border-radius:4px;cursor:pointer;transition:color .2s ease,border-color .2s ease,background .2s ease,transform .15s ease;}\n.term-quick:hover,.term-quick:focus-visible{color:var(--accent);border-color:var(--term-line-strong);background:rgba(94,234,212,.06);text-decoration:none;}\n.term-quick:active{transform:scale(.96);}\n.terminal-input-shell{min-height:42px;display:flex;align-items:center;padding:0 12px;background:#081110;font-family:var(--font-mono);font-size:11.5px;}\n.term-input-prompt{display:flex;align-items:center;flex:0 0 auto;white-space:nowrap;color:var(--term-dim);}\n.term-input-user{color:var(--accent)}.term-input-colon{color:var(--term-dimmer)}.term-input-path{color:#f0c36b}.term-input-dollar{color:var(--term-dim);margin-right:7px;}\n#termInput{min-width:0;flex:1;background:transparent;border:0;outline:0;color:var(--term-text);font-family:var(--font-mono);font-size:11.5px;caret-color:var(--accent);padding:9px 0;}\n#termInput::placeholder{color:#47615c;opacity:1;}\n.term-tab-hint{flex:0 0 auto;margin-left:8px;border:1px solid var(--term-line);padding:2px 5px;border-radius:3px;color:var(--term-dimmer);font-family:var(--font-mono);font-size:8.5px;text-transform:uppercase;letter-spacing:.04em;}\n.terminal-statusbar{display:flex;align-items:center;gap:12px;padding:6px 12px;background:#060d0c;border-top:1px solid rgba(94,234,212,.08);font-family:var(--font-mono);font-size:8.5px;letter-spacing:.02em;color:var(--term-dimmer);}\n.terminal-statusbar span:last-child{margin-left:auto;color:#52726b;}\n.terminal-ready-dot{display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--accent);margin-right:5px;vertical-align:1px;}\n.terminal.is-copied .terminal-copy{color:var(--accent);}\n@media (max-width:1099px){.terminal{margin-top:4px;}}\n@media (max-width:600px){\n  .terminal{max-width:none;width:100%;border-radius:10px;}\n  .terminal-bar{grid-template-columns:auto minmax(0,1fr) auto;padding:0 11px;gap:9px;}\n  .terminal-live{font-size:0;gap:0}.terminal-live::before{margin:0;}\n  .terminal-copy{font-size:9px;}\n  .terminal-snapshot{padding:13px 12px 11px;}\n  .terminal-snapshot-main{margin-bottom:10px;}\n  .terminal-fact{padding:6px 7px}.terminal-fact b{font-size:7.5px}.terminal-fact span{font-size:9.5px;}\n  .terminal-body{min-height:174px;max-height:224px;padding:12px;font-size:10.8px;}\n  .terminal-input-shell{padding:0 10px;font-size:10.5px;}\n  #termInput{font-size:10.8px;}\n  .term-input-user{display:none}.term-input-colon{display:none;}\n  .terminal-statusbar{gap:9px;padding:6px 10px;font-size:8px;}\n  .terminal-statusbar span:nth-child(2){display:none;}\n}\n@media (prefers-reduced-motion: reduce){.term-entry.term-boot{opacity:1;transform:none;animation:none;}}\n"""
assert old_css in s, 'old terminal css block not found'
s = s.replace(old_css, new_css, 1)

old_extra_css = """ \n.terminal-body{max-height:260px;overflow-y:auto;scrollbar-width:thin;}\n.terminal-body::-webkit-scrollbar{width:6px;}\n.terminal-body::-webkit-scrollbar-thumb{background:var(--line);border-radius:3px;}\n.term-input-row{display:flex;align-items:center;gap:0;}\n.term-input-row .prompt{flex-shrink:0;}\n#termInput{\n  flex:1;background:transparent;border:none;outline:none;color:var(--text);\n  font-family:var(--font-mono);font-size:13.5px;caret-color:var(--accent);padding:0 0 0 6px;\n}\n.terminal-line a{color:var(--accent);text-decoration:underline;}\n.terminal-hint{color:var(--text-dimmer);font-size:12px;}\n.terminal-echo{color:var(--text-dim);}\n.terminal-err{color:#ff8f8f;}\n"""
assert old_extra_css in s, 'old terminal supplemental css not found'
s = s.replace(old_extra_css, '', 1)

old_markup = """    <div class=\"terminal\">\n      <div class=\"terminal-bar\">\n        <span class=\"terminal-dot red\"></span><span class=\"terminal-dot yellow\"></span><span class=\"terminal-dot green\"></span>\n        <span class=\"terminal-title\">whoami.sh</span>\n      </div>\n      <div class=\"terminal-body\" id=\"termBody\"></div>\n    </div>\n"""
new_markup = """    <div class=\"terminal\" id=\"heroTerminal\" aria-label=\"Interactive portfolio operations console\">\n      <div class=\"terminal-bar\">\n        <div class=\"terminal-window-controls\" aria-hidden=\"true\"><span class=\"terminal-dot red\"></span><span class=\"terminal-dot yellow\"></span><span class=\"terminal-dot green\"></span></div>\n        <div class=\"terminal-bar-title\"><span class=\"terminal-title\">hans@portfolio</span><span class=\"terminal-path\">~/ops-console</span></div>\n        <div class=\"terminal-bar-actions\"><span class=\"terminal-live\">shell ready</span><button class=\"terminal-copy\" id=\"termCopy\" type=\"button\" aria-label=\"Copy terminal transcript\">copy</button></div>\n      </div>\n      <div class=\"terminal-snapshot\">\n        <div class=\"terminal-snapshot-main\"><span class=\"terminal-avatar\" aria-hidden=\"true\">&gt;_</span><div class=\"terminal-identity\"><strong>Hans Sai</strong><small>systems administration → security engineering</small></div></div>\n        <div class=\"terminal-facts\" aria-label=\"Profile snapshot\">\n          <div class=\"terminal-fact\"><b>ROLE</b><span>SysAdmin</span></div><div class=\"terminal-fact\"><b>CLEARANCE</b><span>Secret</span></div><div class=\"terminal-fact\"><b>FOCUS</b><span>Security</span></div>\n        </div>\n      </div>\n      <div class=\"terminal-screen\"><div class=\"terminal-body\" id=\"termBody\" role=\"log\" aria-live=\"off\" aria-relevant=\"additions text\"></div></div>\n      <div class=\"terminal-quickbar\" aria-label=\"Quick terminal commands\">\n        <button class=\"term-quick\" type=\"button\" data-term-command=\"help\">help</button><button class=\"term-quick\" type=\"button\" data-term-command=\"projects\">projects</button><button class=\"term-quick\" type=\"button\" data-term-command=\"skills\">skills</button><button class=\"term-quick\" type=\"button\" data-term-command=\"resume\">resume</button><button class=\"term-quick\" type=\"button\" data-term-command=\"contact\">contact</button>\n      </div>\n      <div class=\"terminal-input-shell\">\n        <span class=\"term-input-prompt\" aria-hidden=\"true\"><span class=\"term-input-user\">hans@portfolio</span><span class=\"term-input-colon\">:</span><span class=\"term-input-path\">~</span><span class=\"term-input-dollar\">$</span></span>\n        <input id=\"termInput\" type=\"text\" autocomplete=\"off\" autocapitalize=\"off\" spellcheck=\"false\" aria-label=\"Portfolio terminal command\" placeholder=\"type help or choose a command\">\n        <span class=\"term-tab-hint\" aria-hidden=\"true\">tab</span>\n      </div>\n      <div class=\"terminal-statusbar\" aria-hidden=\"true\"><span>↑↓ history</span><span>Tab autocomplete</span><span>Ctrl+L clear</span><span><i class=\"terminal-ready-dot\"></i>interactive</span></div>\n    </div>\n"""
assert old_markup in s, 'old terminal markup not found'
s = s.replace(old_markup, new_markup, 1)

start_marker = "\n(function(){\n  var lines = [\n    {p:true, t:\"whoami\"},"
end_marker = "\n \n(function(){\n  var els = document.querySelectorAll('.reveal');"
start = s.find(start_marker)
end = s.find(end_marker, start)
assert start != -1 and end != -1, 'terminal JS boundaries not found'

new_js = r'''
(function(){
  var terminal = document.getElementById('heroTerminal');
  var log = document.getElementById('termBody');
  var input = document.getElementById('termInput');
  var copyBtn = document.getElementById('termCopy');
  if(!terminal || !log || !input) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var SECTIONS = ['about','experience','projects','skills','education','contact'];
  var COMMANDS = ['help','ls','pwd','whoami','about','status','projects','skills','experience','education','contact','resume','cat','cd','open','sysinfo','neofetch','uname','date','history','theme','github','linkedin','email','matrix','clear'];
  var OPEN_TARGETS = ['projects','skills','experience','education','about','contact','resume','github','linkedin','email'];
  var commandHistory = [];
  var historyIndex = 0;

  function matchSection(arg){
    if(!arg) return null;
    arg = arg.toLowerCase().replace(/^#/, '').replace(/\/$/, '');
    if(arg === 'home' || arg === '~' || arg === '/') return 'top';
    for(var i=0;i<SECTIONS.length;i++) if(SECTIONS[i] === arg || SECTIONS[i].indexOf(arg) === 0) return SECTIONS[i];
    return null;
  }

  function scrollToSection(id){
    if(id === 'top'){
      if(window.hsLenis){ try{ window.hsLenis.scrollTo(0,{duration:.52}); return; }catch(e){} }
      window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});
      return;
    }
    var target = document.getElementById(id);
    if(!target) return;
    if(window.hsScrollToProjSlide && window.hsScrollToProjSlide(target)) return;
    if(window.hsLenis){ try{ window.hsLenis.scrollTo(target,{offset:-10,duration:.52}); return; }catch(e){} }
    target.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
  }

  function runMatrixFX(){
    if(document.getElementById('matrixFX')) return;
    var canvas = document.createElement('canvas');
    canvas.id = 'matrixFX';
    canvas.setAttribute('aria-hidden','true');
    document.body.appendChild(canvas);
    var ctx = canvas.getContext('2d');
    function resize(){ canvas.width=window.innerWidth; canvas.height=window.innerHeight; }
    resize();
    var glyphs='アイウエオカキクケコサシスセソタチツテト01HANSSAI'.split('');
    var fontSize=15, columns=Math.max(1,Math.floor(canvas.width/fontSize)), drops=new Array(columns).fill(1);
    function draw(){
      ctx.fillStyle='rgba(10,14,20,0.15)';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#5eead4';ctx.font=fontSize+'px "JetBrains Mono", monospace';
      for(var i=0;i<drops.length;i++){var ch=glyphs[Math.floor(Math.random()*glyphs.length)];ctx.fillText(ch,i*fontSize,drops[i]*fontSize);if(drops[i]*fontSize>canvas.height&&Math.random()>.975)drops[i]=0;drops[i]++;}
    }
    var interval=setInterval(draw,45),done=false;
    function cleanup(){if(done)return;done=true;clearInterval(interval);canvas.classList.add('fade-out');window.removeEventListener('resize',resize);document.removeEventListener('keydown',onKey);setTimeout(function(){canvas.remove();},500);}
    function onKey(e){if(e.key==='Escape')cleanup();}
    window.addEventListener('resize',resize);document.addEventListener('keydown',onKey);canvas.addEventListener('click',cleanup);setTimeout(cleanup,4200);
  }

  function appendCommand(text, bootDelay){
    var entry=document.createElement('div');entry.className='term-entry'+(bootDelay!=null?' term-boot':'');
    if(bootDelay!=null) entry.style.setProperty('--term-delay',bootDelay+'ms');
    var line=document.createElement('div');line.className='term-command-line';
    var prompt=document.createElement('span');prompt.className='term-shell-prompt';prompt.textContent='hans@portfolio:~$';
    var cmd=document.createElement('span');cmd.className='term-command-text';cmd.textContent=text;
    line.appendChild(prompt);line.appendChild(cmd);entry.appendChild(line);log.appendChild(entry);return entry;
  }

  function appendOutput(text,tone,bootDelay){
    if(!text) return null;
    var entry=document.createElement('div');entry.className='term-entry'+(bootDelay!=null?' term-boot':'');
    if(bootDelay!=null) entry.style.setProperty('--term-delay',bootDelay+'ms');
    var out=document.createElement('div');out.className='term-output'+(tone?' '+tone:'');out.textContent=text;entry.appendChild(out);log.appendChild(entry);return entry;
  }

  function scrollLog(){ log.scrollTop=log.scrollHeight; }
  function clearLog(){ while(log.firstChild) log.removeChild(log.firstChild); }

  function openTarget(arg){
    arg=(arg||'').toLowerCase().trim();
    var sec=matchSection(arg);
    if(sec){scrollToSection(sec);return {text:'navigating → #'+(sec==='top'?'top':sec),tone:'ok'};}
    if(arg==='resume'){window.open('resume/Hans_Sai_Resume.pdf','_blank','noopener');return {text:'opening resume/Hans_Sai_Resume.pdf',tone:'ok'};}
    if(arg==='github'){window.open('https://github.com/Spairkie','_blank','noopener');return {text:'opening github.com/Spairkie',tone:'ok'};}
    if(arg==='linkedin'){window.open('https://www.linkedin.com/in/8pairkie/','_blank','noopener');return {text:'opening linkedin.com/in/8pairkie',tone:'ok'};}
    if(arg==='email'){window.location.href='mailto:saihanswissle@gmail.com';return {text:'opening mail client',tone:'ok'};}
    return {text:'open: unknown target "'+(arg||'')+'"\ntry: '+OPEN_TARGETS.join('  '),tone:'err'};
  }

  function runCommand(raw){
    var trimmed=raw.trim();
    if(!trimmed) return {text:''};
    var parts=trimmed.split(/\s+/),cmd=(parts.shift()||'').toLowerCase(),arg=parts.join(' ');
    switch(cmd){
      case 'help': return {text:'NAVIGATION   projects  skills  experience  education  about  contact\nPROFILE      whoami  status  sysinfo  pwd  ls\nACTIONS      resume  open <target>  github  linkedin  email\nSHELL        cd <section>  cat resume  history  date  theme  clear\nEXTRA        matrix\n\n↑/↓ history · Tab autocomplete · Ctrl+L clear · Esc blur',tone:'bright'};
      case 'ls': return {text:'about/  experience/  projects/  skills/  education/  contact/  resume.pdf',tone:'ok'};
      case 'pwd': return {text:'/home/hans/portfolio',tone:'bright'};
      case 'whoami':
      case 'about': return {text:'Hans Sai\nSystems Administrator · USAFR · IT Support Associate II @ Amazon\nCompTIA Security+ · Active DoD Secret clearance\nBuilding toward security engineering through applied tooling.',tone:'bright'};
      case 'status': return {text:'availability   OPEN_TO_OPPORTUNITIES\nclearance      ACTIVE_SECRET\ncertification  SECURITY+\nfocus          SECURITY_ENGINEERING\nsite           ONLINE',tone:'ok'};
      case 'projects': scrollToSection('projects'); return {text:'navigating → #projects',tone:'ok'};
      case 'skills': scrollToSection('skills'); return {text:'navigating → #skills',tone:'ok'};
      case 'experience': scrollToSection('experience'); return {text:'navigating → #experience',tone:'ok'};
      case 'education': scrollToSection('education'); return {text:'navigating → #education',tone:'ok'};
      case 'contact': scrollToSection('contact'); return {text:'navigating → #contact',tone:'ok'};
      case 'resume': window.open('resume/Hans_Sai_Resume.pdf','_blank','noopener'); return {text:'opening resume/Hans_Sai_Resume.pdf',tone:'ok'};
      case 'cd':
        var sec=matchSection(arg);if(!sec)return {text:arg?'cd: no such section: '+arg:'usage: cd <section>',tone:'err'};scrollToSection(sec);return {text:'cwd → #'+(sec==='top'?'top':sec),tone:'ok'};
      case 'open': return openTarget(arg);
      case 'cat':
        if(/resume/i.test(arg)){window.open('resume/Hans_Sai_Resume.pdf','_blank','noopener');return {text:'opening resume/Hans_Sai_Resume.pdf',tone:'ok'};}
        if(/about|profile|whoami/i.test(arg)) return {text:'Hans Sai — systems administrator focused on endpoint operations, automation, and applied security.',tone:'bright'};
        return {text:'cat: '+(arg||'(no file)')+': no such file',tone:'err'};
      case 'sysinfo':
      case 'neofetch':
      case 'uname': return {text:'HansOS 26.09 LTS\nHost       spairkie.github.io\nRole       Systems Administrator\nOps        5+ years\nEndpoints  150+ imaged / deployed\nTickets    1,000+ resolved yearly\nTooling    PowerShell · Python · AD · GPO · SCCM · Sysmon',tone:'bright'};
      case 'date': return {text:new Date().toLocaleString(),tone:'bright'};
      case 'history': return {text:commandHistory.length?commandHistory.map(function(v,i){return String(i+1).padStart(2,' ')+'  '+v;}).join('\n'):'history: empty',tone:'bright'};
      case 'theme':
        var desired=(arg||'').toLowerCase(),isLight=document.documentElement.getAttribute('data-theme')==='light',btn=document.getElementById('themeToggle');
        if(desired==='light'&&!isLight&&btn)btn.click();else if(desired==='dark'&&isLight&&btn)btn.click();else if(!desired&&btn)btn.click();else if(desired&&desired!=='light'&&desired!=='dark')return {text:'usage: theme [light|dark]',tone:'err'};
        return {text:'theme → '+(document.documentElement.getAttribute('data-theme')==='light'?'light':'dark'),tone:'ok'};
      case 'github': return openTarget('github');
      case 'linkedin': return openTarget('linkedin');
      case 'email': return openTarget('email');
      case 'matrix':
        if(reduce)return {text:'matrix visual skipped: reduced motion is enabled',tone:'warn'};runMatrixFX();return {text:'matrix overlay started · Esc or click to exit',tone:'ok'};
      case 'clear': return {clear:true};
      default:
        var suggestion='';for(var i=0;i<COMMANDS.length;i++){if(COMMANDS[i].indexOf(cmd)===0||cmd.indexOf(COMMANDS[i])===0){suggestion='\ndid you mean: '+COMMANDS[i]+' ?';break;}}
        return {text:cmd+': command not found'+suggestion+'\ntype help for commands',tone:'err'};
    }
  }

  function execute(raw,opts){
    opts=opts||{};var trimmed=raw.trim();if(!trimmed)return;
    if(!opts.noHistory){commandHistory.push(trimmed);if(commandHistory.length>30)commandHistory.shift();historyIndex=commandHistory.length;}
    appendCommand(trimmed);
    var result=runCommand(trimmed);
    if(result.clear){clearLog();}
    else if(result.text) appendOutput(result.text,result.tone||'');
    scrollLog();
  }

  function completionsFor(value){
    var trimmed=value.replace(/^\s+/,''),parts=trimmed.split(/\s+/),last=parts[parts.length-1].toLowerCase(),pool=COMMANDS;
    if(parts.length>1&&(parts[0]==='cd'||parts[0]==='open')) pool=parts[0]==='cd'?SECTIONS.concat(['top']):OPEN_TARGETS;
    return pool.filter(function(v){return v.indexOf(last)===0;});
  }

  function completeInput(){
    var value=input.value,parts=value.replace(/^\s+/,'').split(/\s+/),matches=completionsFor(value);
    if(matches.length===1){parts[parts.length-1]=matches[0];input.value=parts.join(' ')+(parts[0]==='cd'||parts[0]==='open'?' ':'');input.setSelectionRange(input.value.length,input.value.length);}
    else if(matches.length>1){appendOutput(matches.join('   '),'bright');scrollLog();}
  }

  var intro=[
    ['session --status','[ready] interactive portfolio shell mounted','ok'],
    ['whoami --brief','Hans Sai · Systems Administrator · Security+ · Active Secret','bright'],
    ['echo $NEXT_ROLE','security engineering, applied','ok']
  ];
  intro.forEach(function(row,i){appendCommand(row[0],i*115);appendOutput(row[1],row[2],i*115+55);});
  scrollLog();
  setTimeout(function(){log.setAttribute('aria-live','polite');},reduce?0:520);

  input.addEventListener('keydown',function(e){
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='l'){e.preventDefault();clearLog();return;}
    if(e.key==='Enter'){e.preventDefault();var raw=input.value;input.value='';execute(raw);return;}
    if(e.key==='ArrowUp'){e.preventDefault();if(!commandHistory.length)return;historyIndex=Math.max(0,historyIndex-1);input.value=commandHistory[historyIndex]||'';input.setSelectionRange(input.value.length,input.value.length);return;}
    if(e.key==='ArrowDown'){e.preventDefault();if(!commandHistory.length)return;historyIndex=Math.min(commandHistory.length,historyIndex+1);input.value=historyIndex===commandHistory.length?'':commandHistory[historyIndex]||'';input.setSelectionRange(input.value.length,input.value.length);return;}
    if(e.key==='Tab'){e.preventDefault();completeInput();return;}
    if(e.key==='Escape'){input.blur();}
  });

  terminal.querySelectorAll('[data-term-command]').forEach(function(btn){btn.addEventListener('click',function(e){e.stopPropagation();execute(btn.getAttribute('data-term-command')||'');input.focus({preventScroll:true});});});
  terminal.addEventListener('click',function(e){if(e.target.closest('button'))return;input.focus({preventScroll:true});});

  if(copyBtn){copyBtn.addEventListener('click',function(e){
    e.stopPropagation();var text=log.innerText||log.textContent||'';
    function mark(){terminal.classList.add('is-copied');copyBtn.textContent='copied';setTimeout(function(){terminal.classList.remove('is-copied');copyBtn.textContent='copy';},1200);}
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(text).then(mark).catch(function(){});
  });}

  window.hsTerminal={run:function(command){execute(String(command||''));},focus:function(){input.focus({preventScroll:true});},clear:clearLog};
})();
'''

s = s[:start] + '\n' + new_js.strip('\n') + s[end:]

path.write_text(s, encoding='utf-8')
