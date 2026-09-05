from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old_lenis = '''  hsLenis = new Lenis({
    duration: 1.05,
    easing: function(t){ return Math.min(1, 1 - Math.pow(2, -10 * t)); },
    smoothWheel: true,
    wheelMultiplier: 1,
    virtualScroll: function(e){
      var target = e.event && e.event.target;
      if(window.innerWidth > 820 && target && target.closest && target.closest('.folio-section')){
        e.deltaY *= 1.35;
      }
    }
  });'''
new_lenis = '''  hsLenis = new Lenis({
    duration: 0.78,
    easing: function(t){ return Math.min(1, 1 - Math.pow(2, -10 * t)); },
    smoothWheel: false
  });'''
if old_lenis not in text:
    raise SystemExit('Lenis block not found')
text = text.replace(old_lenis, new_lenis, 1)

text = text.replace('height:455vh;padding:0;background:var(--folio-bg);', 'height:430vh;padding:0;background:var(--folio-bg);', 1)
text = text.replace('transform-origin:center;}\n.folio-project-inner', 'transform-origin:center;backface-visibility:hidden;-webkit-backface-visibility:hidden;}\n.folio-project-inner', 1)
text = text.replace('<span class="folio-instruction">Scroll / drag / arrows</span>', '<span class="folio-instruction" id="folioInstruction">Scroll · ← → select · ↓ open</span>', 1)
text = text.replace('<div class="folio-ribbon" id="folioRibbon" aria-label="Project gallery">', '<div class="folio-ribbon" id="folioRibbon" aria-label="Project gallery" aria-keyshortcuts="ArrowLeft ArrowRight ArrowDown Enter">', 1)
text = text.replace('<div class="folio-detail-scroll" id="folioDetailScroll">', '<div class="folio-detail-scroll" id="folioDetailScroll" data-lenis-prevent tabindex="-1">', 1)

start = text.index("(function(){\n  var root=document.querySelector('.folio-section')")
end_marker = "\n\n\n(function(){\n  var canvas = document.getElementById('aboutCanvas');"
end = text.index(end_marker, start)

new_projects = r'''(function(){
  var root = document.querySelector('.folio-section');
  var ribbon = document.getElementById('folioRibbon');
  var detail = document.getElementById('folioDetail');
  var sourceWrap = document.getElementById('folioSource');
  if(!root || !ribbon || !detail || !sourceWrap) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobileMQ = window.matchMedia ? window.matchMedia('(max-width:820px)') : {matches:false};
  var cards = Array.prototype.slice.call(ribbon.querySelectorAll('.folio-project'));
  var N = cards.length;
  if(!N) return;

  function pad(n){ return String(n).padStart(2,'0'); }
  function clamp(v,a,b){ return Math.max(a,Math.min(b,v)); }
  function staticLayout(){ return reduce || mobileMQ.matches; }

  var PROJECTS = cards.map(function(card,i){
    var source = sourceWrap.querySelector('.proj-source[data-project="' + card.id + '"]');
    return {
      id: card.id,
      index: i,
      card: card,
      source: source,
      media: source ? source.querySelector('.scene-media') : null,
      copy: source ? source.querySelector('.scene-detail-copy') : null,
      title: card.dataset.title || card.id,
      type: card.dataset.type || '',
      stack: card.dataset.stack || '',
      status: card.dataset.status || '',
      bg: card.dataset.bg || '#0a0b0b',
      ink: card.dataset.ink || '#e7edf5',
      accent: card.dataset.accent || '#5eead4',
      hint: card.dataset.hint || ''
    };
  });

  function indexForId(id){
    for(var i=0;i<N;i++) if(PROJECTS[i].id === id) return i;
    return -1;
  }

  var progressFill = document.getElementById('folioProgressFill');
  var captionIndex = document.getElementById('folioCaptionIndex');
  var captionTitle = document.getElementById('folioCaptionTitle');
  var metaType = document.getElementById('folioMetaType');
  var metaStack = document.getElementById('folioMetaStack');
  var metaStatus = document.getElementById('folioMetaStatus');
  var openBtn = document.getElementById('folioOpen');
  var prevBtn = document.getElementById('folioPrev');
  var nextBtn = document.getElementById('folioNext');
  var instruction = document.getElementById('folioInstruction');

  var activeIndex = -1;
  var keyboardIndex = 0;
  var position = 0;
  var lastRendered = NaN;
  var sectionStart = 0;
  var sectionHeight = 1;
  var sectionSpan = 1;
  var inSection = false;
  var scrollRAF = null;

  function setActive(index){
    index = clamp(index,0,N-1);
    if(index === activeIndex) return;
    activeIndex = index;
    var p = PROJECTS[index];
    root.style.setProperty('--folio-accent',p.accent);
    cards.forEach(function(card,i){
      var active = i === index;
      card.classList.toggle('is-active',active);
      if(active) card.setAttribute('aria-current','true');
      else card.removeAttribute('aria-current');
    });
    if(captionIndex) captionIndex.textContent = pad(index+1) + ' / ' + pad(N);
    if(captionTitle) captionTitle.textContent = p.title;
    if(metaType) metaType.textContent = p.type;
    if(metaStack) metaStack.textContent = p.stack;
    if(metaStatus) metaStatus.textContent = p.status;
  }

  function render(nextPosition){
    if(staticLayout()) return;
    if(Number.isFinite(lastRendered) && Math.abs(nextPosition-lastRendered) < 0.00025) return;
    lastRendered = nextPosition;
    position = nextPosition;
    var spacing = clamp(window.innerWidth * 0.086,88,126);
    cards.forEach(function(card,i){
      var d = i-nextPosition;
      var ad = Math.abs(d);
      var x = d*spacing;
      var y = Math.min(118,ad*ad*6.5);
      var z = -Math.min(430,ad*96);
      var ry = clamp(d*-12.5,-64,64);
      var scale = 1-Math.min(.29,ad*.052);
      var opacity = clamp(1-ad*.085,.22,1);
      card.style.transform = 'translate(-50%,-50%) translate3d(' + x.toFixed(2) + 'px,' + y.toFixed(2) + 'px,' + z.toFixed(2) + 'px) rotateY(' + ry.toFixed(2) + 'deg) scale(' + scale.toFixed(3) + ')';
      card.style.opacity = opacity.toFixed(3);
      card.style.zIndex = String(100-Math.round(ad*10));
    });
    if(progressFill){
      var pp = N > 1 ? clamp(nextPosition/(N-1),0,1) : 1;
      progressFill.style.transform = 'scaleX(' + pp.toFixed(4) + ')';
    }
    setActive(clamp(Math.round(nextPosition),0,N-1));
  }

  function setSectionState(next){
    if(next === inSection) return;
    inSection = next;
    document.body.classList.toggle('folio-active',next);
    try{ window.dispatchEvent(new CustomEvent('hs:folio-active',{detail:next})); }catch(e){}
  }

  function measure(){
    if(staticLayout()) return;
    var rect = root.getBoundingClientRect();
    sectionStart = window.scrollY + rect.top;
    sectionHeight = root.offsetHeight || 1;
    sectionSpan = Math.max(1,sectionHeight-window.innerHeight);
    lastRendered = NaN;
    scheduleFromScroll();
  }

  function updateFromScroll(){
    scrollRAF = null;
    if(staticLayout()) return;
    var y = window.scrollY;
    var progress = clamp((y-sectionStart)/sectionSpan,0,1);
    var nextPosition = progress*(N-1);
    var nextInSection = y >= sectionStart-window.innerHeight*.22 && y <= sectionStart+sectionHeight-window.innerHeight*.78;
    setSectionState(nextInSection);
    render(nextPosition);
    if(!nextInSection || !root.matches(':hover')) keyboardIndex = clamp(Math.round(nextPosition),0,N-1);
  }

  function scheduleFromScroll(){
    if(scrollRAF || staticLayout()) return;
    scrollRAF = requestAnimationFrame(updateFromScroll);
  }

  function sectionTop(){ return sectionStart; }

  function scrollToIndex(index,instant,source){
    index = clamp(index,0,N-1);
    keyboardIndex = index;
    if(staticLayout()){
      var c = cards[index];
      if(c) c.scrollIntoView({behavior:instant||reduce?'auto':'smooth',block:'center'});
      return;
    }
    var y = sectionTop() + (N>1 ? sectionSpan*(index/(N-1)) : 0);
    if(instant){
      if(window.hsLenis){
        try{ window.hsLenis.scrollTo(y,{immediate:true}); return; }catch(e){}
      }
      window.scrollTo({top:y,behavior:'auto'});
      return;
    }
    if(window.hsLenis){
      try{
        window.hsLenis.scrollTo(y,{
          duration: source === 'keyboard' ? .36 : .52,
          onComplete: function(){ keyboardIndex = activeIndex < 0 ? index : activeIndex; }
        });
        return;
      }catch(e){}
    }
    window.scrollTo({top:y,behavior:reduce?'auto':'smooth'});
  }

  function resetKeyboardToScroll(){
    requestAnimationFrame(function(){
      keyboardIndex = activeIndex < 0 ? clamp(Math.round(position),0,N-1) : activeIndex;
    });
  }

  if(!staticLayout()){
    window.addEventListener('scroll',scheduleFromScroll,{passive:true});
    window.addEventListener('resize',measure);
    root.addEventListener('wheel',resetKeyboardToScroll,{passive:true});
    root.addEventListener('pointerdown',resetKeyboardToScroll,{passive:true});
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(measure).catch(function(){});
    window.addEventListener('load',measure,{once:true});
    measure();
  }else{
    if(instruction) instruction.textContent = 'Tap a project';
    cards.forEach(function(c){ c.style.transform=''; c.style.opacity=''; c.style.zIndex=''; });
    setActive(0);
    keyboardIndex = 0;
    if('IntersectionObserver' in window){
      var mobileIO = new IntersectionObserver(function(entries){
        entries.forEach(function(en){ en.target.classList.toggle('is-mobile-active',en.isIntersecting); });
      },{threshold:.48});
      cards.forEach(function(c){ mobileIO.observe(c); });
    }
  }

  var dragStartX = 0;
  var dragging = false;
  var suppressClickUntil = 0;
  ribbon.addEventListener('pointerdown',function(e){
    if(staticLayout() || (e.pointerType==='mouse' && e.button!==0)) return;
    dragStartX = e.clientX;
    dragging = true;
    ribbon.classList.add('is-dragging');
    try{ ribbon.setPointerCapture(e.pointerId); }catch(err){}
  });
  ribbon.addEventListener('pointerup',function(e){
    if(!dragging) return;
    dragging = false;
    ribbon.classList.remove('is-dragging');
    var dx = e.clientX-dragStartX;
    if(Math.abs(dx)>42){
      suppressClickUntil = Date.now()+350;
      scrollToIndex(activeIndex+(dx<0?1:-1),false,'drag');
    }
  });
  ribbon.addEventListener('pointercancel',function(){ dragging=false; ribbon.classList.remove('is-dragging'); });

  var detailScroll = document.getElementById('folioDetailScroll');
  var detailClose = document.getElementById('folioDetailClose');
  var detailTopPos = document.getElementById('folioDetailTopPos');
  var detailNumber = document.getElementById('folioDetailNumber');
  var detailKicker = document.getElementById('folioDetailKicker');
  var detailTitle = document.getElementById('folioDetailTitle');
  var detailSummary = document.getElementById('folioDetailSummary');
  var detailType = document.getElementById('folioDetailType');
  var detailStack = document.getElementById('folioDetailStack');
  var detailStatus = document.getElementById('folioDetailStatus');
  var detailIndex = document.getElementById('folioDetailIndex');
  var detailMedia = document.getElementById('folioDetailMedia');
  var detailCopy = document.getElementById('folioDetailCopy');
  var detailPos = document.getElementById('folioDetailPos');
  var detailPrev = document.getElementById('folioDetailPrev');
  var detailNext = document.getElementById('folioDetailNext');
  var detailIndexActive = -1;
  var detailGen = 0;

  function setHash(id,mode){
    if(mode===false) return;
    try{
      if(mode==='replace') history.replaceState(null,'','#'+id);
      else history.pushState(null,'','#'+id);
    }catch(e){}
  }

  function returnDetailContent(){
    if(detailIndexActive===-1) return;
    var p = PROJECTS[detailIndexActive];
    if(!p.source) return;
    if(p.media && p.media.parentNode===detailMedia) p.source.insertBefore(p.media,p.source.firstChild);
    if(p.copy && p.copy.parentNode===detailCopy) p.source.appendChild(p.copy);
  }

  function populateDetail(index){
    returnDetailContent();
    var p = PROJECTS[index];
    detailIndexActive = index;
    detail.style.setProperty('--folio-detail-bg',p.bg);
    detail.style.setProperty('--folio-detail-ink',p.ink);
    detail.style.setProperty('--folio-detail-accent',p.accent);
    if(detailTopPos) detailTopPos.textContent = pad(index+1)+' / '+pad(N);
    if(detailNumber) detailNumber.textContent = pad(index+1);
    if(detailKicker) detailKicker.textContent = p.type+' · '+p.stack;
    if(detailTitle) detailTitle.textContent = p.title;
    if(detailSummary) detailSummary.textContent = p.hint;
    if(detailType) detailType.textContent = p.type;
    if(detailStack) detailStack.textContent = p.stack;
    if(detailStatus) detailStatus.textContent = p.status;
    if(detailIndex) detailIndex.textContent = pad(index+1)+' / '+pad(N);
    if(detailPos) detailPos.textContent = pad(index+1)+' / '+pad(N);
    if(p.media) detailMedia.appendChild(p.media);
    if(p.copy) detailCopy.appendChild(p.copy);
    if(detailScroll) detailScroll.scrollTop = 0;
  }

  function openDetail(index,opts){
    opts = opts || {};
    index = ((index%N)+N)%N;
    detailGen++;
    keyboardIndex = index;
    setActive(index);
    populateDetail(index);
    if(detail.hidden){
      detail.hidden = false;
      detail.setAttribute('aria-hidden','false');
      if(opts.instant||reduce) detail.style.transition='none';
      void detail.offsetWidth;
      detail.classList.add('is-open');
      if(opts.instant||reduce) requestAnimationFrame(function(){ requestAnimationFrame(function(){ detail.style.transition=''; }); });
    }
    document.body.classList.add('folio-detail-lock');
    if(window.hsLenis) window.hsLenis.stop();
    setHash(PROJECTS[index].id,opts.updateHash);
    if(!opts.noFocus && detailClose) detailClose.focus({preventScroll:true});
  }

  function closeDetail(opts){
    opts = opts || {};
    if(detail.hidden) return;
    detailGen++;
    var myGen = detailGen;
    var focusCard = detailIndexActive!==-1 ? PROJECTS[detailIndexActive].card : null;
    detail.classList.remove('is-open');
    detail.setAttribute('aria-hidden','true');
    document.body.classList.remove('folio-detail-lock');
    if(window.hsLenis) window.hsLenis.start();
    function finish(){
      if(myGen!==detailGen) return;
      detail.hidden = true;
      returnDetailContent();
      detailIndexActive = -1;
    }
    if(reduce) finish();
    else{
      var ended = false;
      detail.addEventListener('transitionend',function te(e){
        if(e.target!==detail) return;
        detail.removeEventListener('transitionend',te);
        ended = true;
        finish();
      });
      setTimeout(function(){ if(!ended) finish(); },820);
    }
    setHash('projects',opts.updateHash);
    if(focusCard && !opts.noFocus) focusCard.focus({preventScroll:true});
  }

  function nextDetail(){ openDetail((detailIndexActive===-1?activeIndex:detailIndexActive)+1,{updateHash:'replace',noFocus:true}); }
  function prevDetail(){ openDetail((detailIndexActive===-1?activeIndex:detailIndexActive)-1,{updateHash:'replace',noFocus:true}); }
  function scrollDetail(direction){
    if(!detailScroll) return;
    var amount = Math.max(220,window.innerHeight*.72)*direction;
    detailScroll.scrollBy({top:amount,behavior:reduce?'auto':'smooth'});
  }

  cards.forEach(function(card,i){
    card.addEventListener('click',function(){
      if(Date.now()<suppressClickUntil) return;
      keyboardIndex = i;
      openDetail(i);
    });
  });
  if(openBtn) openBtn.addEventListener('click',function(){ openDetail(activeIndex); });
  if(prevBtn) prevBtn.addEventListener('click',function(){ scrollToIndex(activeIndex-1,false,'button'); });
  if(nextBtn) nextBtn.addEventListener('click',function(){ scrollToIndex(activeIndex+1,false,'button'); });
  if(detailClose) detailClose.addEventListener('click',function(){ closeDetail(); });
  if(detailPrev) detailPrev.addEventListener('click',prevDetail);
  if(detailNext) detailNext.addEventListener('click',nextDetail);

  detail.addEventListener('keydown',function(e){
    if(e.key!=='Tab') return;
    var focusables = detail.querySelectorAll('a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])');
    if(!focusables.length) return;
    var first = focusables[0], last = focusables[focusables.length-1];
    if(e.shiftKey && document.activeElement===first){ e.preventDefault(); last.focus(); }
    else if(!e.shiftKey && document.activeElement===last){ e.preventDefault(); first.focus(); }
  });

  var swipeStartX = 0, swipeStartY = 0, swipeActive = false;
  detail.addEventListener('pointerdown',function(e){
    if(e.pointerType==='mouse') return;
    if(e.target.closest && (e.target.closest('iframe') || e.target.closest('.lf-overlay') || e.target.closest('a') || e.target.closest('button'))) return;
    swipeStartX=e.clientX; swipeStartY=e.clientY; swipeActive=true;
  });
  detail.addEventListener('pointerup',function(e){
    if(!swipeActive) return;
    swipeActive=false;
    var dx=e.clientX-swipeStartX, dy=e.clientY-swipeStartY;
    if(Math.abs(dx)>64 && Math.abs(dx)>Math.abs(dy)*1.35){ if(dx<0) nextDetail(); else prevDetail(); }
  });
  detail.addEventListener('pointercancel',function(){ swipeActive=false; });

  function typingTarget(el){
    if(!el) return false;
    var tag = el.tagName;
    return tag==='INPUT' || tag==='TEXTAREA' || tag==='SELECT' || tag==='IFRAME' || el.isContentEditable;
  }

  document.addEventListener('keydown',function(e){
    if(typingTarget(document.activeElement) || document.body.classList.contains('menu-open')) return;

    if(!detail.hidden){
      if(e.key==='Escape'){
        e.preventDefault();
        closeDetail();
      }else if(e.key==='ArrowRight'){
        e.preventDefault();
        nextDetail();
      }else if(e.key==='ArrowLeft'){
        e.preventDefault();
        prevDetail();
      }else if(e.key==='ArrowDown' || e.key==='PageDown'){
        e.preventDefault();
        scrollDetail(1);
      }else if(e.key==='ArrowUp' || e.key==='PageUp'){
        e.preventDefault();
        if(detailScroll && detailScroll.scrollTop<=8 && e.key==='ArrowUp') closeDetail();
        else scrollDetail(-1);
      }else if(e.key==='Home'){
        e.preventDefault();
        if(detailScroll) detailScroll.scrollTo({top:0,behavior:reduce?'auto':'smooth'});
      }else if(e.key==='End'){
        e.preventDefault();
        if(detailScroll) detailScroll.scrollTo({top:detailScroll.scrollHeight,behavior:reduce?'auto':'smooth'});
      }
      return;
    }

    if(!staticLayout() && inSection){
      if(e.key==='ArrowRight'){
        e.preventDefault();
        keyboardIndex = clamp(keyboardIndex+1,0,N-1);
        scrollToIndex(keyboardIndex,false,'keyboard');
      }else if(e.key==='ArrowLeft'){
        e.preventDefault();
        keyboardIndex = clamp(keyboardIndex-1,0,N-1);
        scrollToIndex(keyboardIndex,false,'keyboard');
      }else if(e.key==='ArrowDown' || e.key==='Enter'){
        e.preventDefault();
        openDetail(clamp(keyboardIndex,0,N-1));
      }
    }
  });

  window.addEventListener('hashchange',function(){
    var idx = indexForId(location.hash.slice(1));
    if(idx!==-1){
      if(!staticLayout()) scrollToIndex(idx,true);
      openDetail(idx,{updateHash:false});
    }else if(detailIndexActive!==-1){
      closeDetail({updateHash:false});
    }
  });

  window.hsScrollToProjSlide = function(el){
    if(!el) return false;
    var idx = el.id ? indexForId(el.id) : -1;
    if(idx===-1) return false;
    scrollToIndex(idx,false,'link');
    setTimeout(function(){ openDetail(idx); },reduce?0:360);
    return true;
  };

  window.hsProjects = {
    goToProject:function(i){ scrollToIndex(i,false,'api'); setTimeout(function(){ openDetail(i); },reduce?0:360); },
    next:function(){ if(detailIndexActive!==-1) nextDetail(); else scrollToIndex(activeIndex+1,false,'api'); },
    prev:function(){ if(detailIndexActive!==-1) prevDetail(); else scrollToIndex(activeIndex-1,false,'api'); },
    closeProjectDetail:closeDetail
  };

  var initialIdx = indexForId((window.hsInitialHash||'').slice(1));
  if(initialIdx!==-1){
    scrollToIndex(initialIdx,true);
    openDetail(initialIdx,{instant:true,updateHash:'replace'});
  }
})();'''

text = text[:start] + new_projects + text[end:]

old_ambient = '''  var t = 0;
  var visible = true;
  var raf = null;
  function draw(){
    t += 1;'''
new_ambient = '''  var t = 0;
  var visible = true;
  var folioPaused = false;
  var raf = null;
  function draw(){
    if(folioPaused || !visible){ raf = null; return; }
    t += 1;'''
if old_ambient not in text:
    raise SystemExit('ambient block not found')
text = text.replace(old_ambient,new_ambient,1)

old_vis = '''  document.addEventListener('visibilitychange', function(){
    visible = !document.hidden;
    if(visible && !raf) raf = requestAnimationFrame(draw);
    if(!visible && raf){ cancelAnimationFrame(raf); raf = null; }
  });'''
new_vis = '''  document.addEventListener('visibilitychange', function(){
    visible = !document.hidden;
    if(visible && !folioPaused && !raf) raf = requestAnimationFrame(draw);
    if(!visible && raf){ cancelAnimationFrame(raf); raf = null; }
  });
  window.addEventListener('hs:folio-active', function(e){
    folioPaused = !!e.detail;
    if(folioPaused && raf){ cancelAnimationFrame(raf); raf = null; }
    if(!folioPaused && visible && !raf) raf = requestAnimationFrame(draw);
  });'''
if old_vis not in text:
    raise SystemExit('ambient visibility block not found')
text = text.replace(old_vis,new_vis,1)

path.write_text(text,encoding='utf-8')
