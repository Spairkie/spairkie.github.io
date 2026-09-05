from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace("  var activeIndex = -1;\n  var keyboardIndex = 0;\n  var position = 0;", "  var activeIndex = -1;\n  var keyboardIndex = 0;\n  var keyboardNavUntil = 0;\n  var position = 0;", 1)
s=s.replace("    if(!nextInSection || !root.matches(':hover')) keyboardIndex = clamp(Math.round(nextPosition),0,N-1);", "    if(performance.now() >= keyboardNavUntil) keyboardIndex = activeIndex < 0 ? clamp(Math.round(nextPosition),0,N-1) : activeIndex;", 1)
s=s.replace("    keyboardIndex = index;\n    if(staticLayout()){", "    keyboardIndex = index;\n    if(source === 'keyboard') keyboardNavUntil = performance.now()+520;\n    if(staticLayout()){", 1)
s=s.replace("          onComplete: function(){ keyboardIndex = activeIndex < 0 ? index : activeIndex; }", "          onComplete: function(){ keyboardNavUntil = 0; keyboardIndex = activeIndex < 0 ? index : activeIndex; }", 1)
s=s.replace("  function resetKeyboardToScroll(){\n    requestAnimationFrame(function(){", "  function resetKeyboardToScroll(){\n    keyboardNavUntil = 0;\n    requestAnimationFrame(function(){", 1)
p.write_text(s,encoding='utf-8')
