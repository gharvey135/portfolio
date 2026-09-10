
(function(){
  var root=document.documentElement, seg=document.getElementById('seg'),
      btns=seg.querySelectorAll('button'), pill=seg.querySelector('.pill');
  function move(b){ pill.style.left=b.offsetLeft+'px'; pill.style.width=b.offsetWidth+'px'; }
  function set(m,save){
    root.setAttribute('data-mode',m);
    btns.forEach(function(b){
      var on=b.dataset.mode===m; b.setAttribute('aria-pressed',on?'true':'false'); if(on) move(b);
    });
    if(save){ try{ localStorage.setItem('pf-mode',m); }catch(e){} }
  }
  btns.forEach(function(b){ b.addEventListener('click',function(){ set(b.dataset.mode,true); }); });
  var saved=null; try{ saved=localStorage.getItem('pf-mode'); }catch(e){}
  set(saved==='tech'?'tech':'plain',false);
  window.addEventListener('resize',function(){ set(root.getAttribute('data-mode'),false); });
  window.addEventListener('load',function(){ set(root.getAttribute('data-mode'),false); });
})();
