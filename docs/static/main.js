document.addEventListener('DOMContentLoaded',()=>{
  let lastScroll=0;
  const header=document.querySelector('header');
  window.addEventListener('scroll',()=>{
    const st=window.pageYOffset||0;
    if(st>lastScroll) header.classList.add('hidden');
    else header.classList.remove('hidden');
    lastScroll=st<=0?0:st;
  });
});
