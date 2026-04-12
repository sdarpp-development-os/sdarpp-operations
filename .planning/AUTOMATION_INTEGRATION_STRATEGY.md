# Automation Integration Strategy — NDIS SDA Specialist Consultant Platform

**Status**: Strategic Planning Phase  
**Document**: Integration Architecture & Roadmap  
**Owner**: Solo Lead Developer (Sugi Gunamijaya)  
**Created**: 11 Apr 2026  
**Revision**: 1.0

---

## Executive Summary

Your automation infrastructure is **sophisticated but fragmented**. You have:
- ✅ 13+ GitHub Actions workflows
- ✅ 7 AI agents with governance contracts
- ✅ OneDrive document management system
- ✅ Microsoft 365 integration
- ✅ Production feasibility dashboard
- ❌ **BUT**: Agents don't run continuously, no knowledge indexing, no real-time dispatch, no unified control hub

**The Problem**: Everything is documented and partially built, but **not talking to each other**. You manually trigger workflows. Agents process files on-demand. Knowledge base isn't indexed. Dashboard is read-only.

**The Vision**: A **Mission Control Hub** where you:
1. Upload data/documents
2. Dispatch instructions to agents
3. Monitor agent execution
4. Approve decisions
5. Access unified project view across all systems

**This Plan**: 4-phase roadmap to reconnect everything into a coherent automated consultant platform.

---

## Current Architecture Map

```
CURRENT STATE: Disconnected Systems

┌──────────────────────────────────────────────────────────────┐
│                     YOUR SYSTEMS (ISOLATED)                  │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  GITHUB (Manual Triggers)                                     │
│  ├─ 13+ Actions (need manual activation)                      │
│  ├─ Wiki markdown files (SSoT)                                │
│  └─ Agent contracts (defined, not running)                    │
│                                                                │
│  OneDrive (Manual File Drops)                                 │
│  ├─ _AI_AUTOMATION/IN/ (Hermes inbox)                        │
│  └─ Documents (manually processed)                            │
│                                                                │
│  Agents (On-Demand)                                           │
│  ├─ Hermes (manual file routing)                              │
│  ├─ Compliance Agent (not active)                             │
│  ├─ Planning Agent (not active)                               │
│  └─ Feasibility Agent (not active)                            │
│                                                                │
│  NotebookLM (Unused)                                          │
│  └─ Knowledge corpus created but not integrated               │
│                                                                │
│  Dashboard (Read-Only)                                        │
│  ├─ Feasibility data (stale, manual updates)                  │
│  └─ No agent dispatch, no approvals                           │
│                                                                │
└──────────────────────────────────────────────────────────────┘

RESULT: You must manually orchestrate everything. No continuous automation.
```

---

## Target Architecture

```
FUTURE STATE: Integrated Mission Control

┌──────────────────────────────────────────────────────────────┐
│                   MISSION CONTROL HUB                         │
│              (Dashboard + Orchestration Engine)               │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  YOU (Solo Developer)                                         │
│  └─ Upload data → Dispatch instructions → Monitor → Approve  │
│                                                                │
│  ↓↓↓ Unified API ↓↓↓                                          │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ORCHESTRATION ENGINE (New)                              │ │
│  │ ├─ Agent Manager (dispatch, queue, status)              │ │
│  │ ├─ Workflow Engine (trigger, retry, escalate)           │ │
│  │ ├─ Data Pipeline (ETL from sources → destinations)      │ │
│  │ └─ Knowledge Router (route to right knowledge base)      │ │
│  └─────────────────────────────────────────────────────────┘ │
│           ↓           ↓           ↓           ↓               │
│        GitHub     OneDrive    NotebookLM   Supabase           │
│        ├─ Wiki    ├─ Docs     ├─ RAG       ├─ Dashboard       │
│        ├─ Issues  ├─ _AI_AUTO │Index       └─ Data Store     │
│        └─ Agents  └─ Registry └─ LLM                          │
│                                                                │
│  AI AGENTS (Continuous + Responsive)                         │
│  ├─ Hermes (Smart Router)                                     │
│  ├─ Compliance Agent (SDA auditing)                           │
│  ├─ Planning Agent (DA assessment)                            │
│  ├─ Feasibility Agent (Financial)                             │
│  ├─ Reporting Agent (Synthesis)                               │
│  └─ Master Agent (Governance coordination)                    │
│                                                                │
│  OUTPUT CHANNELS                                              │
│  ├─ GitHub Issues (decisions, escalations)                    │
│  ├─ Email (notifications)                                     │
│  ├─ Slack (real-time alerts)                                  │
│  └─ Dashboard (visual status)                                 │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## The Core Problem

**Current Workflow (Manual):**
```
Day 1: You manually upload document to OneDrive _AI_AUTOMATION/IN/
Day 2: You manually trigger GitHub Action "Route Document"
Day 3: Hermes processes it (runs Python script)
Day 4: File appears in _AI_AUTOMATION/OUT/
Day 5: You manually move it to correct OneDrive folder
Day 6: You manually update GitHub wiki with findings
```

**Desired Workflow (Automated):**
```
Day 1 9:00am: You upload document to OneDrive _AI_AUTOMATION/IN/ (or via Dashboard)
Day 1 9:05am: Orchestration Engine detects file → queues Hermes
Day 1 9:10am: Hermes processes → routes to correct folder → updates GitHub issue
Day 1 9:15am: Compliance Agent auto-runs against SDA Design Standard
Day 1 9:20am: Results posted to Slack + GitHub + Dashboard
Day 1 10:00am: You review findings on Dashboard → approve/escalate
```

---

## Phase 1: Foundation (Weeks 1-2) — Make Automation Runnable

### Goal
Get agents running **continuously and responsively**, not on-demand.

### What's Needed

#### 1.1 Agent Runtime Infrastructure
**Current State**: Agents are defined in markdown, no persistent execution environment  
**Need**: Background service that executes agents

**Options**:
- **Option A (Recommended)**: GitHub Actions + scheduled workflows
  - Pros: Zero infrastructure, uses existing GitHub setup, free
  - Cons: 5-min minimum interval, not real-time
  - Cost: $0 (included in GitHub)
  
- **Option B**: Heroku/Railway background workers
  - Pros: Real-time, better for continuous listening
  - Cons: Costs money, requires deployment
  - Cost: $5-20/month
  
- **Option C**: AWS Lambda + EventBridge
  - Pros: Highly scalable, event-driven
  - Cons: Complex setup, cost varies
  - Cost: $1-10/month

**Recommendation**: Start with **Option A** (GitHub Actions) + add webhook listeners for real-time events

#### 1.2 Document Queue System
**Current State**: Manual file drops in OneDrive folder  
**Need**: Automated queue + worker

**Implementation**:
- Create `_AI_AUTOMATION/QUEUE/` folder in OneDrive
- Schedule GitHub Action to run every 5 minutes: "Check document queue"
- If new files exist → add to GitHub Issues queue
- Worker agents consume from GitHub Issues queue
- Processed files → move to `_AI_AUTOMATION/OUT/` + create GitHub Issue with results

**Files to Create**:
- `.github/workflows/document-queue-monitor.yml` (triggers every 5 min)
- `automation/scripts/monitor_onedrive_queue.py` (lists new files)
- `automation/scripts/queue_to_github_issues.py` (creates queue issues)

#### 1.3 Agent Daemon
**Current State**: Agents defined in contracts, no executor  
**Need**: Simple daemon that watches for work and dispatches

**Implementation**:
- Create `.github/workflows/agent-executor.yml` (runs every 10 min)
- Watch GitHub Issues with label `agent:hermes`, `agent:compliance`, etc.
- Dispatch appropriate agent based on label + issue content
- Update issue with agent results as comments
- Move to `agent:completed` label when done

**Files to Create**:
- `.github/workflows/agent-executor.yml`
- `automation/scripts/dispatch_agent_by_issue.py`
- `automation/agent_executor.py` (main agent coordination)

---

### Deliverables for Phase 1

| File | Purpose |
|------|---------|
| `.github/workflows/document-queue-monitor.yml` | Monitors OneDrive queue folder every 5 min |
| `.github/workflows/agent-executor.yml` | Executes queued agents every 10 min |
| `automation/scripts/monitor_onedrive_queue.py` | Lists new files in OneDrive queue |
| `automation/scripts/queue_to_github_issues.py` | Creates GitHub Issues from queued files |
| `automation/agent_executor.py` | Routes issues to correct agents + captures results |
| `automation/agents/hermes-executor.py` | Executes Hermes document routing logic |
| `automation/agents/compliance-executor.py` | Executes Compliance auditing logic |
| Updated `AGENTS.md` | Documents how agents are now dispatched |

### Success Criteria
- ✅ Upload document to OneDrive → GitHub Issue created within 5 min
- ✅ GitHub Issue processed by agent → Results posted as comment within 10 min
- ✅ No manual GitHub Action triggers needed
- ✅ Agents run 24/7 on schedule

### Estimated Effort
- **Developer Time**: 40-60 hours
- **Complexity**: Medium (Python + GitHub Actions + OneDrive API)
- **Risk**: Low (all existing APIs, well-documented)

---

## Phase 2: Knowledge Integration (Weeks 3-4) — Index & Access Knowledge

### Goal
Make your knowledge base **searchable and accessible to agents**.

### What's Needed

#### 2.1 NotebookLM Integration
**Current State**: NotebookLM project created but not connected  
**Need**: Index knowledge for RAG (Retrieval Augmented Generation)

**Implementation**:
- Extract all documents from NotebookLM project
- Create Pinecone index: "NDIS_SDA_knowledge_base"
- Embed documents with OpenAI embeddings
- Query API for agents to retrieve relevant knowledge

**Files to Create**:
- `automation/scripts/extract_notebooklm_docs.py` (download documents)
- `automation/scripts/index_to_pinecone.py` (create vector index)
- `automation/utils/knowledge_retriever.py` (query API for agents)

#### 2.2 GitHub Wiki Synchronization
**Current State**: Wiki in markdown, not indexed  
**Need**: Sync wiki to Pinecone for searchability

**Implementation**:
- Schedule GitHub Actions to read all wiki markdown
- Extract sections (project_state, decisions, risks, budget)
- Embed and upload to Pinecone
- Update daily

**Files to Create**:
- `.github/workflows/sync-wiki-to-pinecone.yml`
- `automation/scripts/extract_github_wiki.py`

#### 2.3 Agent Knowledge Prompts
**Current State**: Agents have hardcoded knowledge  
**Need**: Agents dynamically retrieve relevant knowledge

**Implementation**:
- Update agent executor to: before running agent, query Pinecone for relevant docs
- Inject retrieved knowledge into agent system prompt
- Agents now have real-time access to latest knowledge

**Files to Create**:
- `automation/agents/hermes-with-rag.py` (updated with knowledge retrieval)
- `automation/agents/compliance-with-rag.py` (updated)
- `automation/agents/planning-with-rag.py` (updated)

---

### Deliverables for Phase 2

| Component | Purpose |
|-----------|---------|
| Pinecone Index (NDIS_SDA_knowledge_base) | Vector store for all knowledge |
| `automation/scripts/extract_notebooklm_docs.py` | Download and prepare documents |
| `automation/scripts/index_to_pinecone.py` | Create vector embeddings |
| `.github/workflows/sync-wiki-to-pinecone.yml` | Keep Pinecone index fresh |
| `automation/utils/knowledge_retriever.py` | Query API for agents |
| Updated agent executors | Agents now retrieve knowledge before running |

### Success Criteria
- ✅ Upload SDA Design Standard doc → Pinecone indexes within 1 hour
- ✅ Compliance Agent runs → Retrieves relevant SDA sections automatically
- ✅ Search for "occupancy requirements" → Returns relevant docs
- ✅ Agents cite source documents in findings

### Estimated Effort
- **Developer Time**: 30-40 hours
- **Complexity**: Medium (Pinecone API, embeddings, prompt engineering)
- **Cost**: Pinecone subscription ($20-50/month) + OpenAI embeddings ($0.10/1K vectors, negligible)

---

## Phase 3: Dashboard as Mission Control (Weeks 5-6) — Dispatch & Monitor

### Goal
Transform dashboard from **read-only to operational command center**.

### What's Needed

#### 3.1 Agent Dispatch Interface
**Current State**: Dashboard shows data only  
**Need**: UI to send instructions to agents

**Implementation**:
- Add "Dispatch Agent" modal to dashboard
- Select agent (Hermes, Compliance, Planning, etc.)
- Upload document or select from GitHub
- Submit → creates GitHub Issue with agent label
- Monitor execution in real-time

**Components to Build**:
- `src/components/AgentDispatch.tsx` (modal UI)
- `src/components/AgentStatus.tsx` (shows running/completed agents)
- `src/app/api/dispatch-agent.ts` (API endpoint to create issue)

#### 3.2 Decision Approval Workflow
**Current State**: Decisions tracked in markdown, no approval workflow  
**Need**: Dashboard to approve/escalate decisions

**Implementation**:
- Pull decisions from GitHub wiki daily
- Show "Pending Approval" decisions on dashboard
- Click "Approve" → update wiki + post to Slack
- Click "Escalate" → create escalation issue with reasons
- Track decision metrics (approval time, % escalations)

**Components to Build**:
- `src/components/DecisionQueue.tsx` (shows pending decisions)
- `src/components/DecisionApprovalFlow.tsx` (approve/reject/escalate)
- `src/app/api/approve-decision.ts` (updates wiki)

#### 3.3 Real-Time Agent Monitor
**Current State**: No visibility into agent execution  
**Need**: See what agents are doing right now

**Implementation**:
- Query GitHub Issues with agent labels
- Show status: queued → running → completed
- Display agent output/findings in real-time
- Show errors/failures with debug info

**Components to Build**:
- `src/components/AgentMonitor.tsx` (real-time dashboard)
- `src/app/api/get-agent-status.ts` (queries GitHub)
- `src/hooks/useAgentStream.ts` (polling hook)

#### 3.4 Unified Data View
**Current State**: Data split across GitHub wiki, OneDrive, Supabase  
**Need**: Single pane of glass

**Implementation**:
- Dashboard fetches from all sources:
  - Project status from GitHub wiki (project_state.md)
  - Financial data from Supabase
  - Recent decisions/risks from GitHub Issues
  - Agent execution history
- Merge into unified project view
- Show data freshness (when last synced)

**API Endpoints Needed**:
- `GET /api/project/overview` (aggregates all sources)
- `GET /api/project/decisions` (from wiki + issues)
- `GET /api/project/risks` (from wiki + issues)
- `GET /api/project/financials` (from Supabase)
- `GET /api/agents/history` (from GitHub Issues)

---

### Deliverables for Phase 3

| Component | Purpose |
|-----------|---------|
| AgentDispatch.tsx | Send instructions to agents |
| AgentStatus.tsx | Monitor running agents |
| DecisionQueue.tsx | Review pending decisions |
| DecisionApprovalFlow.tsx | Approve/escalate decisions |
| AgentMonitor.tsx | Real-time agent execution dashboard |
| API endpoints | Data aggregation from all sources |
| `/api/dispatch-agent.ts` | Create agent execution job |
| `/api/approve-decision.ts` | Update decision status |
| `/api/get-agent-status.ts` | Query agent execution |

### Success Criteria
- ✅ Click "Dispatch Compliance Agent" → runs within 10 min
- ✅ See agent running in real-time on monitor
- ✅ Review agent findings on dashboard
- ✅ Approve decision → wiki updated + Slack notified
- ✅ View unified project overview (status, decisions, risks, finances)

### Estimated Effort
- **Developer Time**: 60-80 hours
- **Complexity**: High (multiple integrations, real-time updates)
- **Infrastructure**: Minimal (uses existing Vercel)

---

## Phase 4: Advanced Automation (Weeks 7-8) — Self-Orchestration

### Goal
Agents become **proactive**, automating routine decisions and escalations.

### What's Needed

#### 4.1 Automated Risk Escalation
**Current State**: Risk register in markdown, no escalation  
**Need**: Risks automatically escalate when thresholds hit

**Implementation**:
- Schedule job: every day at 9am, calculate risk scores
- Risk score = probability × impact
- If risk_score > 0.6 → create "escalation" GitHub Issue
- Assign to you, tag as urgent, post to Slack
- Track when each risk was last reviewed

**Files to Create**:
- `.github/workflows/daily-risk-escalation.yml`
- `automation/scripts/calculate_risk_scores.py`
- `automation/scripts/escalate_high_risks.py`

#### 4.2 Automated Compliance Drift Detection
**Current State**: Compliance check script exists but incomplete  
**Need**: Weekly audit that checks all projects against SDA Standard

**Implementation**:
- Every Monday 22:00 UTC: run compliance drift check
- Compare current design against SDA Design Standard
- Generate audit report with confidence scores
- Findings < 80% confidence → escalate
- Post summary to GitHub + email

**Files to Create**:
- `.github/workflows/weekly-compliance-audit.yml` (reimplement properly)
- `automation/scripts/compliance_drift_check.py` (complete implementation)
- `automation/agents/compliance-audit-report.py`

#### 4.3 Automated Decision Synthesis
**Current State**: You manually synthesize project status  
**Need**: Automated weekly summary

**Implementation**:
- Every Friday 5pm: Reporting Agent synthesizes week
- Pulls: recent decisions, completed risks, financial changes, agent findings
- Generates executive summary with key insights
- Posts to GitHub wiki + Slack + email
- Includes recommendations for Monday actions

**Files to Create**:
- `.github/workflows/weekly-synthesis.yml`
- `automation/agents/reporting-agent-executor.py`
- `automation/scripts/generate_weekly_summary.py`

#### 4.4 Automated Data Pipeline
**Current State**: Dashboard data is stale  
**Need**: ETL that keeps all systems in sync

**Implementation**:
- Every 4 hours: ETL pipeline runs
- Extract from: GitHub wiki, OneDrive docs, agent findings
- Transform into: standardized format
- Load into: Supabase (dashboard), GitHub Issues (tracking)
- Update data freshness timestamps

**Files to Create**:
- `.github/workflows/etl-pipeline.yml` (runs every 4 hours)
- `automation/scripts/etl_github_to_supabase.py`
- `automation/scripts/etl_onedrive_to_supabase.py`

---

### Deliverables for Phase 4

| Automation | Purpose |
|-----------|---------|
| Daily Risk Escalation | Auto-escalate high-risk items |
| Weekly Compliance Audit | Detect SDA compliance drift |
| Weekly Synthesis Report | Executive summary of week |
| ETL Data Pipeline | Keep systems in sync |
| Escalation Rules Engine | Define thresholds for auto-escalation |
| Notification Router | Send alerts to right channels (Slack, email, GitHub) |

### Success Criteria
- ✅ Risk hits high score → you get Slack alert same day
- ✅ Compliance issue detected → escalation issue created auto
- ✅ Every Friday 5pm → weekly summary posted automatically
- ✅ Dashboard always shows current data (max 4 hours old)
- ✅ 80% of routine decisions handled without your input

### Estimated Effort
- **Developer Time**: 50-70 hours
- **Complexity**: High (logic-heavy, scheduling)
- **Infrastructure**: Minimal

---

## Implementation Roadmap

### Timeline Overview

```
PHASE 1: Foundation (Weeks 1-2)
├─ Mon-Fri Week 1: Agent runtime + document queue
├─ Mon-Fri Week 2: Agent executor + completion
└─ Goal: Agents run continuously

PHASE 2: Knowledge (Weeks 3-4)
├─ Mon-Fri Week 3: Pinecone setup + NotebookLM integration
├─ Mon-Fri Week 4: Wiki sync + agent RAG integration
└─ Goal: Knowledge is searchable and accessible

PHASE 3: Control (Weeks 5-6)
├─ Mon-Fri Week 5: Dispatch UI + agent monitor
├─ Mon-Fri Week 6: Decision workflow + data aggregation
└─ Goal: Dashboard is operational command center

PHASE 4: Autonomy (Weeks 7-8)
├─ Mon-Fri Week 7: Risk escalation + compliance audit
├─ Mon-Fri Week 8: Synthesis + ETL pipeline
└─ Goal: Routine automation handles 80% of work

TOTAL: 8 weeks | ~250-300 hours of development | Solo developer
```

### Critical Path

```
MUST HAPPEN FIRST:
1. Phase 1 complete (agents running) → blocks everything else
2. Phase 2 complete (knowledge indexed) → agents are effective
3. Phase 3 complete (dashboard control) → you can operate it

OPTIONAL BUT VALUABLE:
4. Phase 4 (advanced automation) → reduces your daily effort
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| GitHub API rate limits | Low | Medium | Use GitHub token with higher limits |
| OneDrive sync fails | Medium | Low | Add error logging + Slack alerts |
| Agent accuracy poor | Medium | High | Include feedback loop (Phase 4) |
| Knowledge index stale | Low | Medium | Run sync weekly automatically |
| Dashboard performance | Low | Medium | Use Vercel caching + pagination |
| Agent conflicts (running same file twice) | Medium | Medium | Add locking mechanism to queue |
| Notification fatigue (too many Slack alerts) | High | Low | Implement alert deduplication |

---

## Success Metrics

### Phase 1 Success
- [ ] All 5 workflows executing without manual intervention
- [ ] Document upload → queue detection within 5 min
- [ ] Agent execution → completion within 15 min
- [ ] Zero manual workflow triggers in 1 week
- [ ] Agent executor running 24/7 with <1% failure rate

### Phase 2 Success
- [ ] Pinecone index contains 100+ documents
- [ ] RAG queries return relevant knowledge within 2 seconds
- [ ] Agents reference source documents in findings
- [ ] Wiki index stays <4 hours old

### Phase 3 Success
- [ ] You can dispatch agents without GitHub access
- [ ] 5+ decision approvals per week via dashboard
- [ ] Agent monitor shows 95%+ uptime visibility
- [ ] Dashboard data reflects actual project state

### Phase 4 Success
- [ ] 3+ automated escalations triggered correctly per week
- [ ] Compliance audit identifies real issues (validated by you)
- [ ] Weekly synthesis provides actionable insights
- [ ] ETL pipeline maintains <4hr data freshness
- [ ] 80%+ of routine decisions made without your input

---

## Resource Requirements

### Infrastructure Costs
- **GitHub**: Included (already paying)
- **Supabase**: $25/month (included in existing)
- **Pinecone**: $20/month starter
- **OpenAI API**: ~$5-10/month (embeddings)
- **OneDrive**: Included (M365)
- **Vercel**: Included (free tier)

**Total New Cost**: ~$25-30/month

### Development Resources
- **You**: ~250-300 hours over 8 weeks (30-40 hrs/week)
- **AI Tools**: Claude (this), ChatGPT, GitHub Copilot (optional)
- **Infrastructure**: Minimal (all cloud)

---

## Decision: Which Phase Starts First?

### Recommendation: **START WITH PHASE 1**

**Why?**
1. Unblocks all other phases
2. Lowest risk (proven GitHub APIs)
3. Biggest immediate impact (agents run 24/7)
4. Foundation for everything else

**Next Step**: I can immediately help you with Phase 1:
- [ ] A) **Build Phase 1 now** (agent runtime + document queue) — 40-60 hours
- [ ] B) **Plan Phase 1 in detail** first (architecture + file listing)
- [ ] C) **Start smaller** (just Hermes automation first, ignore other agents)

---

## Your Role

As **solo lead developer**, you need to:

1. **Week 1-2**: Implement Phase 1 (agent runtime)
2. **Week 3-4**: Implement Phase 2 (knowledge integration)
3. **Week 5-6**: Implement Phase 3 (dashboard control)
4. **Week 7-8**: Implement Phase 4 (advanced automation)

**Effort**: 30-40 hours/week (full-time equivalent)  
**Timeline**: 8 weeks (2 months)  
**Support**: I can help with code, debugging, architecture

---

## Questions for You

Before we proceed to Phase 1 details, clarify:

1. **Timeline**: Can you dedicate 30-40 hrs/week for 8 weeks? Or need to go slower?
2. **Automation Scope**: Should all 7 agents run, or start with just Hermes?
3. **Knowledge Priority**: NotebookLM critical, or can defer knowledge integration?
4. **Risk Appetite**: Comfortable with experimental automation, or prefer proven-only?
5. **Self-Operation**: You'll write this code? Or want me to write it + you review?

---

## Next Steps

**If approved, I will:**
1. Break down Phase 1 into detailed tasks with code templates
2. Show you file structure + what gets created
3. Start implementation immediately
4. Deliver working Phase 1 within 2-3 weeks

**Are you ready to reconnect your automation? Let me know:**
- ✅ Proceed with Phase 1 plan
- ❓ Want to modify the roadmap
- ⏸️ Need more time to decide

