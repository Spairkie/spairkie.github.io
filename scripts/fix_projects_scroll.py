from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

old = 'height:610vh;padding:0;background:var(--folio-bg);color:var(--folio-ink);position:relative;isolation:isolate;overflow:visible;'
new = 'height:455vh;padding:0;background:var(--folio-bg);color:var(--folio-ink);position:relative;isolation:isolate;overflow:visible;'
assert old in text, 'desktop Projects scroll span not found'
text = text.replace(old, new, 1)

old = '''    smoothWheel: true,\n    wheelMultiplier: 1\n  });'''
new = '''    smoothWheel: true,\n    wheelMultiplier: 1,\n    virtualScroll: function(e){\n      var target = e.event && e.event.target;\n      if(window.innerWidth > 820 && target && target.closest && target.closest('.folio-section')){\n        e.deltaY *= 1.35;\n      }\n    }\n  });'''
assert old in text, 'Lenis options block not found'
text = text.replace(old, new, 1)

old = "  var currentPosition=0,targetPosition=0,activeIndex=0,renderRAF=null,inSection=false;"
new = "  var currentPosition=0,targetPosition=0,activeIndex=0,inSection=false;"
assert old in text, 'Projects render state declaration not found'
text = text.replace(old, new, 1)

old = "  function animateRender(){renderRAF=null;if(staticLayout())return;currentPosition+=(targetPosition-currentPosition)*.16;if(Math.abs(targetPosition-currentPosition)<.001)currentPosition=targetPosition;render(currentPosition);if(currentPosition!==targetPosition)renderRAF=requestAnimationFrame(animateRender);}function wakeRender(){if(!renderRAF&&!staticLayout())renderRAF=requestAnimationFrame(animateRender);}"
new = "  function renderFromScroll(){if(staticLayout())return;currentPosition=targetPosition;render(currentPosition);}"
assert old in text, 'double-smoothing render loop not found'
text = text.replace(old, new, 1)

old = "  function syncFromScroll(){if(staticLayout())return;var rect=root.getBoundingClientRect(),span=Math.max(1,root.offsetHeight-window.innerHeight);targetPosition=clamp((-rect.top)/span,0,1)*(N-1);inSection=rect.top<=window.innerHeight*.22&&rect.bottom>=window.innerHeight*.78;wakeRender();}"
new = "  function syncFromScroll(){if(staticLayout())return;var rect=root.getBoundingClientRect(),span=Math.max(1,root.offsetHeight-window.innerHeight);targetPosition=clamp((-rect.top)/span,0,1)*(N-1);inSection=rect.top<=window.innerHeight*.22&&rect.bottom>=window.innerHeight*.78;renderFromScroll();}"
assert old in text, 'scroll sync function not found'
text = text.replace(old, new, 1)

old = "  function scrollToIndex(index,instant){index=clamp(index,0,N-1);if(staticLayout()){var c=cards[index];if(c)c.scrollIntoView({behavior:instant||reduce?'auto':'smooth',block:'center'});return;}var span=Math.max(1,root.offsetHeight-window.innerHeight),y=sectionTop()+(N>1?span*(index/(N-1)):0);targetPosition=index;wakeRender();if(window.hsLenis){try{window.hsLenis.scrollTo(y,instant?{immediate:true}:{duration:.9});return;}catch(e){}}window.scrollTo({top:y,behavior:instant||reduce?'auto':'smooth'});}"
new = "  function scrollToIndex(index,instant){index=clamp(index,0,N-1);if(staticLayout()){var c=cards[index];if(c)c.scrollIntoView({behavior:instant||reduce?'auto':'smooth',block:'center'});return;}var span=Math.max(1,root.offsetHeight-window.innerHeight),y=sectionTop()+(N>1?span*(index/(N-1)):0);targetPosition=index;if(instant){currentPosition=index;render(index);}if(window.hsLenis){try{window.hsLenis.scrollTo(y,instant?{immediate:true}:{duration:.72});return;}catch(e){}}window.scrollTo({top:y,behavior:instant||reduce?'auto':'smooth'});}"
assert old in text, 'project index scroll function not found'
text = text.replace(old, new, 1)

old = "  if(!staticLayout()){if(window.hsLenis&&typeof window.hsLenis.on==='function')window.hsLenis.on('scroll',syncFromScroll);else window.addEventListener('scroll',syncFromScroll,{passive:true});window.addEventListener('resize',syncFromScroll);syncFromScroll();currentPosition=targetPosition;render(currentPosition);}else{"
new = "  if(!staticLayout()){if(window.hsLenis&&typeof window.hsLenis.on==='function')window.hsLenis.on('scroll',syncFromScroll);window.addEventListener('scroll',syncFromScroll,{passive:true});window.addEventListener('resize',syncFromScroll);syncFromScroll();}else{"
assert old in text, 'Projects scroll listener setup not found'
text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
