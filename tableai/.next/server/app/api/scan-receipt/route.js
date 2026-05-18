"use strict";(()=>{var e={};e.id=864,e.ids=[864],e.modules={399:e=>{e.exports=require("next/dist/compiled/next-server/app-page.runtime.prod.js")},517:e=>{e.exports=require("next/dist/compiled/next-server/app-route.runtime.prod.js")},5040:(e,t,r)=>{r.r(t),r.d(t,{originalPathname:()=>g,patchFetch:()=>m,requestAsyncStorage:()=>u,routeModule:()=>c,serverHooks:()=>l,staticGenerationAsyncStorage:()=>d});var a={};r.r(a),r.d(a,{POST:()=>p});var o=r(3278),s=r(5002),n=r(4877),i=r(1309);async function p(e){try{let t=(await e.formData()).get("image");if(!t)return i.NextResponse.json({error:"No image provided"},{status:400});let r=await t.arrayBuffer(),a=Buffer.from(r).toString("base64"),o=t.type||"image/jpeg",s=process.env.ANTHROPIC_API_KEY;if(!s)return i.NextResponse.json({error:"Anthropic API key not configured"},{status:500});let n=new Date().toISOString().split("T")[0],p=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",headers:{"Content-Type":"application/json","x-api-key":s,"anthropic-version":"2023-06-01"},body:JSON.stringify({model:"claude-haiku-4-5-20241022",max_tokens:1024,messages:[{role:"user",content:[{type:"image",source:{type:"base64",media_type:o,data:a}},{type:"text",text:`You are a receipt scanner for a restaurant expense tracking system. Extract information from this receipt image and return ONLY a JSON object with these exact fields:
{
  "amount": <number, the total amount paid>,
  "vendor": <string, the business/vendor name>,
  "date": <string, YYYY-MM-DD format, use ${n} if not visible>,
  "category": <string, one of: food_cost, alcohol, labor, rent, utilities, marketing, supplies, other>,
  "description": <string, brief description of what was purchased, max 60 characters>
}

Category guidelines:
- food_cost: groceries, produce, meat, dairy, dry goods for cooking
- alcohol: beer, wine, spirits, mixers
- labor: payroll, staffing services
- rent: rent, lease payments
- utilities: gas, electric, water, internet, phone
- marketing: ads, printing, social media, design
- supplies: cleaning, paper goods, smallwares, packaging
- other: anything that does not fit above

Return ONLY the JSON object, no other text.`}]}]})});if(!p.ok){let e=await p.text();return console.error("Anthropic API error:",e),i.NextResponse.json({error:"Failed to analyze receipt"},{status:500})}let c=await p.json(),u=(c.content?.[0]?.text||"").match(/\{[\s\S]*\}/);if(!u)return i.NextResponse.json({error:"Could not parse receipt data"},{status:500});let d=JSON.parse(u[0]);return i.NextResponse.json(d)}catch(e){return console.error("Scan receipt error:",e),i.NextResponse.json({error:"Internal server error"},{status:500})}}let c=new o.AppRouteRouteModule({definition:{kind:s.x.APP_ROUTE,page:"/api/scan-receipt/route",pathname:"/api/scan-receipt",filename:"route",bundlePath:"app/api/scan-receipt/route"},resolvedPagePath:"/root/.openclaw/workspace/tableai/app/api/scan-receipt/route.ts",nextConfigOutput:"",userland:a}),{requestAsyncStorage:u,staticGenerationAsyncStorage:d,serverHooks:l}=c,g="/api/scan-receipt/route";function m(){return(0,n.patchFetch)({serverHooks:l,staticGenerationAsyncStorage:d})}}};var t=require("../../../webpack-runtime.js");t.C(e);var r=e=>t(t.s=e),a=t.X(0,[787,833],()=>r(5040));module.exports=a})();