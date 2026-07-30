import * as THREE from 'https://unpkg.com/three@0.165.0/build/three.module.js';
const canvas=document.getElementById('meat-scene');
if(canvas){
 const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
 const scene=new THREE.Scene();
 const camera=new THREE.PerspectiveCamera(35,1,.1,100); camera.position.set(0,0,8);
 const group=new THREE.Group(); scene.add(group);
 const steakMat=new THREE.MeshStandardMaterial({color:0x8d2018,roughness:.58,metalness:.02});
 const fatMat=new THREE.MeshStandardMaterial({color:0xf2caa2,roughness:.78});
 const hamMat=new THREE.MeshStandardMaterial({color:0xc5674c,roughness:.55});
 const boneMat=new THREE.MeshStandardMaterial({color:0xf6dfc1,roughness:.7});
 const steak=new THREE.Mesh(new THREE.TorusGeometry(1.05,.36,32,96),steakMat); steak.scale.set(1.25,.72,.18); steak.position.set(-.9,.5,0); group.add(steak);
 const fat=new THREE.Mesh(new THREE.TorusGeometry(1.1,.08,16,96),fatMat); fat.scale.set(1.28,.75,.2); fat.position.copy(steak.position); group.add(fat);
 const ham=new THREE.Mesh(new THREE.CapsuleGeometry(.65,1.55,12,28),hamMat); ham.rotation.z=.9; ham.position.set(1.05,-.55,.2); ham.scale.set(1.05,1.05,.55); group.add(ham);
 const bone=new THREE.Mesh(new THREE.CylinderGeometry(.18,.18,1.35,28),boneMat); bone.rotation.z=.9; bone.position.set(1.05,-.55,.22); group.add(bone);
 const shrimp=new THREE.Mesh(new THREE.TorusGeometry(.45,.12,16,48,Math.PI*1.35),new THREE.MeshStandardMaterial({color:0xe99662,roughness:.5})); shrimp.position.set(.55,1.35,-.2); shrimp.rotation.x=.7; group.add(shrimp);
 scene.add(new THREE.AmbientLight(0xffe0bc,1.7)); const key=new THREE.DirectionalLight(0xffd19a,2.8); key.position.set(3,4,5); scene.add(key); const rim=new THREE.DirectionalLight(0x9b2f19,1.2); rim.position.set(-4,-2,3); scene.add(rim);
 let mx=0,my=0; window.addEventListener('pointermove',e=>{mx=(e.clientX/window.innerWidth-.5)*2; my=(e.clientY/window.innerHeight-.5)*2;});
 function resize(){const w=canvas.clientWidth,h=canvas.clientHeight; renderer.setSize(w,h,false); camera.aspect=w/h; camera.updateProjectionMatrix();} window.addEventListener('resize',resize); resize();
 function tick(t){const s=window.scrollY/Math.max(1,document.body.scrollHeight-innerHeight); group.rotation.y+=((mx*.55+s*2.2)-group.rotation.y)*.05; group.rotation.x+=((-my*.35+s*.7)-group.rotation.x)*.05; group.position.y=Math.sin(t/900)*.09+(s-.5)*.8; group.scale.setScalar(1+s*.18); steak.rotation.z=t/2600; ham.rotation.y=t/1800; shrimp.rotation.z=-t/1500; renderer.render(scene,camera); requestAnimationFrame(tick)} requestAnimationFrame(tick);
}
const orderForm=document.querySelector('#order-form');
if(orderForm){
 const items=[...document.querySelectorAll('[data-item]')]; const summary=document.querySelector('#order-summary');
 function render(){let total=0,lines=[]; items.forEach(i=>{const qty=Number(i.value||0); if(qty>0){const price=Number(i.dataset.price); total+=qty*price; lines.push(`<div class="summary-line"><span>${qty} × ${i.dataset.item}</span><strong>$${(qty*price).toFixed(2)}</strong></div>`)}}); summary.innerHTML=lines.join('')+`<div class="summary-line"><span>Estimated subtotal</span><strong>$${total.toFixed(2)}</strong></div>`;}
 items.forEach(i=>i.addEventListener('input',render)); render();
 orderForm.addEventListener('submit',e=>{e.preventDefault(); const fd=new FormData(orderForm); const body=[...fd.entries()].map(([k,v])=>`${k}: ${v}`).join('\n'); localStorage.setItem('midwestLastOrder',body); document.querySelector('#order-result').innerHTML='<span class="status-pill">Order draft saved</span> We saved this order locally for now. Backend/email integration is the next wiring step.';});
}
const chat=document.querySelector('#chat-form');
if(chat){
 const log=document.querySelector('.chat-log'); const input=document.querySelector('#chat-input');
 const stock={ribeye:['available','12 boxes'],sirloin:['available','8 cases'],filet:['limited','3 cases'],ham:['available','10 hams'],bacon:['available','18 packs'],shrimp:['limited','6 bags'],salmon:['available','9 cases'],crab:['call ahead','seasonal'],chicken:['available','15 cases']};
 function add(text,who='bot'){const d=document.createElement('div');d.className='bubble '+who;d.textContent=text;log.appendChild(d);log.scrollTop=log.scrollHeight;}
 add('Hi — I’m the mocked MidWest inventory agent. Ask about ribeye, ham, shrimp, salmon, bundles, or delivery windows.');
 chat.addEventListener('submit',e=>{e.preventDefault(); const q=input.value.trim(); if(!q)return; add(q,'user'); input.value=''; const key=Object.keys(stock).find(k=>q.toLowerCase().includes(k)); if(key){const [status,count]=stock[key]; add(`${key.toUpperCase()}: ${status}. Current mock count: ${count}. Want me to add it to an order draft?`)} else if(q.toLowerCase().includes('delivery')) add('Free delivery is part of the current positioning. A real agent would check route capacity by zip code and preferred window.'); else add('I can answer from the mock inventory list right now. Once connected, I’ll query live stock, specials, delivery route capacity, and customer order history.');});
}
