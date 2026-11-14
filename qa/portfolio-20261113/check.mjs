import {createRequire} from 'node:module';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);
const {chromium}=require('../_tools/node_modules/playwright-core');
const out='qa/portfolio-20261113',base='http://127.0.0.1:8843';
await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
const report={pages:[],interactions:[],errors:[]};
try{
 const context=await browser.newContext();
 await context.route('**/*',r=>r.request().url().startsWith(base)?r.continue():r.abort());
 const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
 for(const width of [1440,390]){
  await page.setViewportSize({width,height:width===1440?1000:844});
  for(const route of ['/','/portfolio/','/trafego-pago-com-ia/','/privacidade/','/cases/bvba-surrealismo/','/cases/alumee-vela-mel/','/cases/ana-lauren-modelo-ia/']){
   const response=await page.goto(base+route);await page.evaluate(()=>document.fonts.ready);
   for(let y=0;y<await page.evaluate(()=>document.body.scrollHeight);y+=700){await page.evaluate(y=>scrollTo(0,y),y);await page.waitForTimeout(75);}
   await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(700);
   const data=await page.evaluate(()=>({title:document.title,h1:document.querySelectorAll('h1').length,overflow:document.documentElement.scrollWidth>innerWidth,font:getComputedStyle(document.body).fontFamily,brand:document.querySelector('header .brand')?.innerText,brokenImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),badAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>a.hash.length>1&&!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.hash),schemas:[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>JSON.parse(s.textContent))}));
   const key=(route==='/'?'home':route.split('/').filter(Boolean).at(-1))+'-'+width;
   await page.screenshot({path:`${out}/${key}.png`,fullPage:true});
   if(route==='/'||route==='/portfolio/')await page.screenshot({path:`${out}/${key}-top.png`});
   report.pages.push({route,width,status:response.status(),...data});
   assert.equal(response.status(),200,key);assert.equal(data.h1,1,key);assert.equal(data.overflow,false,key);assert.deepEqual(data.brokenImages,[],key);assert.deepEqual(data.badAnchors,[],key);assert.match(data.brand,/MAYAA/);assert.match(data.brand,/Victor Mey/);assert.match(data.font,/Poppins/);
  }
 }
 await page.goto(base+'/');
 await page.getByRole('button',{name:'Abrir menu',exact:true}).click();assert.equal(await page.locator('#mobile-nav').isVisible(),true);await page.keyboard.press('Escape');assert.equal(await page.locator('#mobile-nav').isVisible(),false);assert.equal(await page.locator('.menu-button').evaluate(e=>e===document.activeElement),true);
 await page.getByRole('button',{name:'Read in English',exact:true}).click();assert.equal(await page.locator('html').getAttribute('lang'),'en');assert.match(await page.locator('h1').innerText(),/By Victor Mey/);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.getByRole('button',{name:'Ler em português',exact:true}).click();await page.locator('.hero-actions .button').click();assert.equal(new URL(page.url()).hash,'#recentes');
 assert.match(await page.locator('#contato>.button').getAttribute('href'),/instagram.com\/victormey.ai/);assert.match(await page.locator('.commerce-path a').getAttribute('href'),/instagram.com\/victormey.ai/);
 await page.getByText('Preciso entender de IA?',{exact:true}).click();assert.equal(await page.locator('.faq details').first().getAttribute('open'),'');
 report.interactions.push('Home: menu e Escape com foco; PT/EN; CTA projetos; contato geral e diagnóstico separados; FAQ');
 await page.goto(base+'/portfolio/');await page.getByRole('button',{name:'Abrir menu',exact:true}).click();assert.equal(await page.locator('#menu').isVisible(),true);await page.keyboard.press('Escape');assert.equal(await page.locator('#menu').isVisible(),false);
 await page.locator('.portfolio-project').first().click();assert.match(page.url(),/cases\/bvba-surrealismo/);assert.match(await page.locator('.case-author').innerText(),/Direção de Victor Mey/);
 report.interactions.push('Portfólio: menu; caso abre; autoria visível');
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const np=await nojs.newPage();await np.goto(base+'/');assert.equal(await np.locator('.desktop-nav').isVisible(),true);assert.equal(await np.locator('h1').isVisible(),true);report.interactions.push('Home acessível sem JavaScript');
 const reduced=await browser.newContext({reducedMotion:'reduce',viewport:{width:390,height:844}});const rp=await reduced.newPage();await rp.goto(base+'/');assert.equal(await rp.locator('.reveal.is-pending').count(),0);assert.equal(await rp.locator('.work-image>img').first().evaluate(e=>getComputedStyle(e).transitionDuration),'0s');report.interactions.push('Reduced motion respeitado');
 assert.deepEqual(report.errors,[]);
}finally{await fs.writeFile(`${out}/checks.json`,JSON.stringify(report,null,2));await browser.close();}
console.log(JSON.stringify({pages:report.pages.length,interactions:report.interactions,errors:report.errors}));
