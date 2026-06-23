const TYPE_QUALITY = {github_repo:5,commit_release:6,demo_video:4,documentation:5,test_result:5,screenshot:2,transaction_hash:6,article_source:4,api_log:4,other:1};
const MATCHES = {
  builder_submission:new Set(["github_repo","documentation","demo_video","test_result"]),
  milestone_proof:new Set(["github_repo","commit_release","demo_video","test_result","transaction_hash"]),
  dispute_evidence:new Set(["documentation","screenshot","transaction_hash","article_source","api_log"]),
  agent_sla_claim:new Set(["test_result","transaction_hash","api_log"]),
  grant_proposal:new Set(["github_repo","documentation","demo_video","article_source"]),
  prediction_resolver:new Set(["transaction_hash","article_source","api_log"]),
  other:new Set(Object.keys(TYPE_QUALITY))
};
const TIMESTAMPED = new Set(["commit_release","test_result","transaction_hash","api_log"]);
const HARD_TO_FAKE = new Set(["commit_release","test_result","transaction_hash","api_log"]);

const form = document.querySelector("#evidenceForm");
const itemsHost = document.querySelector("#evidenceItems");
const template = document.querySelector("#evidenceTemplate");
let lastJson = "";

function addEvidence(item = {}) {
  const node = template.content.firstElementChild.cloneNode(true);
  node.querySelector(".evidence-type").value = item.type || "github_repo";
  node.querySelector(".evidence-url").value = item.url || "";
  node.querySelector(".evidence-description").value = item.description || "";
  node.querySelector(".remove-item").addEventListener("click", () => { node.remove(); renumber(); });
  itemsHost.append(node);
  renumber();
}

function renumber() {
  [...itemsHost.children].forEach((item, index) => item.querySelector(".item-index").textContent = index + 1);
}

function readItems() {
  return [...document.querySelectorAll(".evidence-item")].map(item => ({
    type:item.querySelector(".evidence-type").value,
    url:item.querySelector(".evidence-url").value.trim(),
    description:item.querySelector(".evidence-description").value.trim()
  })).filter(item => item.url || item.description);
}

function isPublic(url) {
  try { return ["http:", "https:"].includes(new URL(url).protocol); } catch { return false; }
}

function scorePack(pack) {
  const items = pack.evidence_items;
  const publicItems = items.filter(item => isPublic(item.url));
  const domains = new Set(publicItems.map(item => new URL(item.url).hostname.toLowerCase()));
  const independent = domains.size >= 2;
  const relevant = MATCHES[pack.target_use_case] || MATCHES.other;
  const matching = items.filter(item => relevant.has(item.type));
  const hasRelevant = matching.some(item => item.url);
  const completeness = (pack.claim_title?5:0) + (pack.claim_description.length>=20?5:pack.claim_description?2:0) + (items.length>=2?8:items.length?3:0) + (independent?6:publicItems.length?2:0) + (hasRelevant?6:0);
  const sourceQuality = Math.min(25, items.reduce((sum,item) => sum + (item.url?(TYPE_QUALITY[item.type]||1):0),0));
  const relevance = Math.min(20,(pack.claim_description.length>=20?5:pack.claim_description?2:0)+(pack.target_use_case?5:0)+Math.min(10,matching.length*2));
  const resistance = (publicItems.length?3:0)+(publicItems.some(item=>TIMESTAMPED.has(item.type))?4:0)+(independent?4:0)+(publicItems.some(item=>HARD_TO_FAKE.has(item.type))?4:0);
  const readiness = 3+(MATCHES[pack.target_use_case]?3:0)+(pack.claim_description?2:0)+(items.length>=2?2:0);
  const total = completeness+sourceQuality+relevance+resistance+readiness;
  const risk = resistance>=12?"low":resistance>=7?"medium":"high";
  const quality = sourceQuality>=19?"strong":sourceQuality>=10?"moderate":"weak";
  const ready = readiness>=8 && total>=60 && items.length>=2;
  const missing=[];
  if(!pack.claim_title) missing.push("Claim title");
  if(pack.claim_description.length<20) missing.push("A clear, detailed claim description");
  if(items.length<2) missing.push("At least two evidence items");
  if(!independent) missing.push("An independent source on a different public domain");
  if(!hasRelevant) missing.push("Evidence matched to the selected GenLayer use case");
  if(!items.some(item=>TIMESTAMPED.has(item.type)&&item.url)) missing.push("Timestamped proof such as a release, test run, transaction, or log");
  let verdict;
  if(risk==="high"&&items.length) verdict="high_manipulation_risk";
  else if(!ready&&total>=50) verdict="not_genlayer_ready";
  else if(items.length<2) verdict="needs_more_sources";
  else if(sourceQuality<10||total<50) verdict="weak_evidence";
  else verdict=total>=75?"evidence_ready":"needs_more_sources";
  const recommendation=verdict==="evidence_ready"?"Package is ready for Intelligent Contract review; preserve source URLs and timestamps.":missing.length?`Add: ${missing.slice(0,3).join("; ")}.`:"Add stronger public, timestamped, and independently verifiable evidence.";
  return {evidence_score:total,completeness_score:completeness,source_quality_score:sourceQuality,relevance_score:relevance,manipulation_resistance_score:resistance,genlayer_readiness_score:readiness,source_quality:quality,manipulation_risk:risk,genlayer_ready:ready,verdict,missing_evidence:missing,recommendation};
}

function render(pack, review) {
  const labels={evidence_ready:"Evidence ready",needs_more_sources:"Needs more sources",weak_evidence:"Weak evidence",high_manipulation_risk:"High manipulation risk",not_genlayer_ready:"Not GenLayer ready"};
  document.querySelector("#emptyState").hidden=true;
  document.querySelector("#results").hidden=false;
  document.querySelector("#verdictLabel").textContent=labels[review.verdict];
  document.querySelector("#totalScore").textContent=review.evidence_score;
  document.querySelector("#qualityBadge").textContent=`${review.source_quality} sources`;
  const riskBadge=document.querySelector("#riskBadge");
  riskBadge.textContent=`${review.manipulation_risk} risk`;riskBadge.className=`risk-${review.manipulation_risk}`;
  document.querySelector("#readyBadge").textContent=review.genlayer_ready?"GenLayer ready":"Not ready";
  const scores=[
    ["Completeness","completeness_score",30],["Source quality","source_quality_score",25],["Relevance","relevance_score",20],["Manipulation resistance","manipulation_resistance_score",15],["GenLayer readiness","genlayer_readiness_score",10]
  ];
  document.querySelector("#scoreList").innerHTML=scores.map(([label,key,max])=>`<div class="score-row"><div class="score-meta"><span>${label}</span><strong>${review[key]} / ${max}</strong></div><div class="score-track"><i style="--score:${review[key]/max*100}%"></i></div></div>`).join("");
  document.querySelector("#missingList").innerHTML=review.missing_evidence.length?review.missing_evidence.map(item=>`<li>${escapeHtml(item)}</li>`).join(""):"<li>No material gaps detected.</li>";
  document.querySelector("#recommendation").textContent=review.recommendation;
  const evidencePackage={schema_version:"evidencegraph.v1",generated_at:new Date().toISOString(),pack,review,contract_input:{claim:{title:pack.claim_title,description:pack.claim_description,expected_outcome:pack.expected_outcome},target_use_case:pack.target_use_case,evidence:pack.evidence_items,quality_gate:{score:review.evidence_score,verdict:review.verdict,manipulation_risk:review.manipulation_risk,genlayer_ready:review.genlayer_ready}}};
  lastJson=JSON.stringify(evidencePackage,null,2);
  document.querySelector("#jsonPreview").textContent=lastJson;
  refreshRegistryPreview();
  if(innerWidth<850) document.querySelector("#resultPanel").scrollIntoView({behavior:"smooth",block:"start"});
}

function escapeHtml(value){const div=document.createElement("div");div.textContent=value;return div.innerHTML;}
function setValue(id,value){document.querySelector(`#${id}`).value=value;}
function loadSample(sample){
  setValue("claimTitle",sample.title);setValue("claimDescription",sample.description);setValue("targetUseCase",sample.useCase);setValue("expectedOutcome",sample.outcome||"");itemsHost.innerHTML="";sample.items.forEach(addEvidence);document.querySelector("#builder").scrollIntoView({behavior:"smooth"});
}

function registryValue(id, placeholder) {
  return document.querySelector(`#${id}`).value.trim() || placeholder;
}

function refreshRegistryPreview() {
  const jsonPreview=document.querySelector("#registryJsonPreview");
  jsonPreview.textContent=lastJson||'{\n  "status": "Review an evidence pack to populate this preview."\n}';
  const block=[
    "EvidenceGraph v1.1 — On-chain Evidence Registry",
    `Network: ${registryValue("registryNetwork","[NETWORK]")}`,
    `Contract address: ${registryValue("registryContractAddress","[CONTRACT_ADDRESS]")}`,
    `Deploy transaction hash: ${registryValue("registryDeployTx","[DEPLOY_TRANSACTION_HASH]")}`,
    `Register evidence transaction hash: ${registryValue("registryRegisterTx","[REGISTER_EVIDENCE_TRANSACTION_HASH]")}`,
    `Review transaction hash: ${registryValue("registryReviewTx","[REVIEW_TRANSACTION_HASH]")}`,
    `Evidence package JSON: ${lastJson?"prepared (evidencegraph.v1)":"[REVIEW_A_PACKAGE_FIRST]"}`,
    "Frontend: https://evidencegraph-genlayer.vercel.app",
    "Registry status: deployed and verified on GenLayer Bradbury Testnet"
  ].join("\n");
  document.querySelector("#deploymentEvidencePreview").textContent=block;
  return block;
}

document.querySelector("#addEvidence").addEventListener("click",()=>addEvidence());
form.addEventListener("submit",event=>{event.preventDefault();const pack={claim_title:document.querySelector("#claimTitle").value.trim(),claim_description:document.querySelector("#claimDescription").value.trim(),evidence_items:readItems(),target_use_case:document.querySelector("#targetUseCase").value,expected_outcome:document.querySelector("#expectedOutcome").value.trim()};render(pack,scorePack(pack));});
document.querySelector("#copyJson").addEventListener("click",async event=>{try{await navigator.clipboard.writeText(lastJson);event.target.textContent="Copied";setTimeout(()=>event.target.textContent="Copy JSON",1400);}catch{event.target.textContent="Select JSON below";}});
document.querySelectorAll("#registryNetwork,#registryContractAddress,#registryDeployTx,#registryRegisterTx,#registryReviewTx").forEach(input=>input.addEventListener("input",refreshRegistryPreview));
document.querySelector("#copyDeploymentEvidence").addEventListener("click",async event=>{try{await navigator.clipboard.writeText(refreshRegistryPreview());event.target.textContent="Copied";setTimeout(()=>event.target.textContent="Copy block",1400);}catch{event.target.textContent="Select block below";}});
document.querySelector("#weakSample").addEventListener("click",()=>loadSample({title:"I completed the milestone",description:"I built everything promised and it works.",useCase:"milestone_proof",outcome:"Approve milestone",items:[{type:"other",url:"",description:"My own statement that the work is complete"}]}));
document.querySelector("#strongSample").addEventListener("click",()=>loadSample({title:"Milestone shipped with reproducible tests",description:"The public v1.0 release implements the agreed milestone, passes its automated tests, and is demonstrated in a public walkthrough.",useCase:"milestone_proof",outcome:"Approve milestone",items:[{type:"github_repo",url:"https://github.com/example/project",description:"Public source repository"},{type:"commit_release",url:"https://github.com/example/project/releases/tag/v1.0.0",description:"Timestamped release"},{type:"documentation",url:"https://docs.example.org/milestone",description:"Public implementation documentation"},{type:"demo_video",url:"https://youtu.be/example",description:"Working product walkthrough"},{type:"test_result",url:"https://ci.example.org/runs/123",description:"Public automated test result"}]}));

addEvidence();
addEvidence({type:"documentation"});
refreshRegistryPreview();
