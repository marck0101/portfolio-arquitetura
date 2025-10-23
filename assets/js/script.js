
const observer=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('show')})},{threshold:.12});
document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));
  const btn=document.querySelector('#menuBtn'),menu=document.querySelector('#mobileMenu');
  if(btn&&menu){btn.addEventListener('click',()=>menu.classList.toggle('hidden'))}

  // Filter (projects)
  const wrap=document.querySelector('[data-filter-wrap]');
  if(wrap){
    const buttons=wrap.querySelectorAll('button[data-filter]');
    const cards=document.querySelectorAll('[data-project-card]');
    let page=1; const PER_PAGE=9;
    function apply(){
      const active=wrap.querySelector('button[aria-pressed="true"]')?.dataset.filter || 'Todos';
      let shown=0;
      cards.forEach(card=>{
        const cats=(card.dataset.cats||'').split(',');
        const pass=active==='Todos'||cats.includes(active);
        if(pass && shown < PER_PAGE*page){ card.classList.remove('hidden'); shown++; }
        else { card.classList.add('hidden'); }
      });
      const moreBtn=document.getElementById('loadMore');
      if(moreBtn){
        const total=Array.from(cards).filter(c=>{const cats=(c.dataset.cats||'').split(',');return active==='Todos'||cats.includes(active)}).length;
        moreBtn.classList.toggle('hidden', shown>=total);
      }
    }
    buttons.forEach(b=>b.addEventListener('click',()=>{buttons.forEach(x=>x.setAttribute('aria-pressed','false'));b.setAttribute('aria-pressed','true');page=1;apply();}));
    document.getElementById('loadMore')?.addEventListener('click',()=>{page++;apply()});
    (buttons[0]||{}).click?.();
  }

  // Lightbox (project detail)
  const lb=document.querySelector('.lb-overlay');
  if(lb){
    const img=lb.querySelector('img');
    const thumbs=document.querySelectorAll('[data-lightbox-thumb]');
    let idx=0;
    function open(i){idx=i; img.src=thumbs[idx].getAttribute('data-full'); lb.classList.add('active');}
    thumbs.forEach((t,i)=>t.addEventListener('click',()=>open(i)));
    lb.addEventListener('click',e=>{if(e.target===lb)lb.classList.remove('active')});
    document.getElementById('lbPrev')?.addEventListener('click',()=>{idx=(idx-1+thumbs.length)%thumbs.length; img.src=thumbs[idx].getAttribute('data-full')});
    document.getElementById('lbNext')?.addEventListener('click',()=>{idx=(idx+1)%thumbs.length; img.src=thumbs[idx].getAttribute('data-full')});
    document.getElementById('lbClose')?.addEventListener('click',()=>lb.classList.remove('active'));
  }

  // More reviews
  const moreReviews=document.getElementById('moreReviews');
  if(moreReviews){ moreReviews.addEventListener('click',()=>{document.querySelectorAll('[data-review="extra"]').forEach(el=>el.classList.remove('hidden'));moreReviews.classList.add('hidden');}); }

  // WhatsApp CTA
  const waBtn=document.getElementById('waBtn');
  if(waBtn){ waBtn.addEventListener('click',()=>{const phone='+555596341317';const text=encodeURIComponent('Olá! Gostaria de um orçamento para um projeto de arquitetura.');window.open(`https://wa.me/${phone}?text=${text}`,'_blank');}); }
});
