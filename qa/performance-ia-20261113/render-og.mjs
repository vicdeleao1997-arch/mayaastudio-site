import {createRequire} from 'node:module';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const require=createRequire(import.meta.url);
const {chromium}=require('../_tools/node_modules/playwright-core');
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
try{const page=await browser.newPage({viewport:{width:1200,height:630}});await page.goto(pathToFileURL(resolve('qa/performance-ia-20261113/og.html')).href);await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:'site/assets/victor/og-mayaa-victor.png'});}finally{await browser.close();}
