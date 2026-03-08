# Lightweight AI Agent Framework Research Report
**Research Date:** March 1, 2026  
**Researcher:** Pre-Planning Research Agent  
**For:** Solo founder/developer evaluating frameworks for investment

---

## Executive Summary

This report analyzes 7 AI agent frameworks for a solo founder deciding where to invest development time. Of the 7 frameworks researched:

- **6 are viable** (1 deprecated: OpenAI Swarm)
- **5 are production-ready** (smolagents, LangGraph, CrewAI, Agno, LiteLLM as base)
- **1 is experimental/educational** (PocketFlow)
- **Size range:** 100 lines (PocketFlow) to 37,000 lines (LangGraph)
- **Popularity leader:** CrewAI (44k+ stars)
- **Enterprise leader:** LangGraph (400+ companies including Uber, LinkedIn, Replit)

**Quick Decision Guide:**
- **Want minimal, code-based agents?** → smolagents
- **Want to learn/full control?** → PocketFlow
- **Need enterprise-grade state management?** → LangGraph
- **Want fast multi-agent prototyping?** → CrewAI
- **Building production agentic systems?** → Agno
- **Building custom from scratch?** → LiteLLM as base
- **Considering OpenAI Swarm?** → DON'T (deprecated)

---

## 1. smolagents (HuggingFace)

### Overview
HuggingFace's minimalist framework where agents "think in code" - they write actions as Python code snippets rather than JSON tool calls. This approach uses 30% fewer steps than traditional JSON-based agents.

### Technical Details
- **Language:** Python
- **GitHub:** https://github.com/huggingface/smolagents
- **Stars:** 25.7k | **Forks:** 2.3k | **Contributors:** 205
- **License:** Apache-2.0
- **Core Code:** ~1,000 lines (agents.py)
- **Total Size:** +198MB installed
- **Last Activity:** Very active - last commit Feb 21, 2026
- **Commits:** 1,020+
- **Latest Release:** v1.24.0 (Jan 16, 2026)

### Features & Capabilities

#### Tool Calling Support
- **Built-in:** Yes - dual approach
  - CodeAgent: writes actions as Python code
  - ToolCallingAgent: traditional JSON/text tool calls
- Code execution is demonstrably more efficient (30% fewer LLM calls)

#### Memory System
- **Built-in:** None
- **DIY Required:** Yes - you implement conversation history and state management
- Memory is user-managed through conversation context

#### Multi-Agent / Swarm Support
- **Yes** - agent handoffs supported
- Agents can transfer execution to other agents
- Hierarchical agent structures possible

#### Streaming Support
- **Yes** - full streaming support with `stream=True`
- Real-time output as agents think and execute

#### Self-Hosting Viability & Cost
- **Excellent** - multiple sandboxed execution options:
  - E2B (cloud sandbox)
  - Blaxel (cloud sandbox)
  - Modal (serverless)
  - Docker (local/cloud)
  - Pyodide+Deno (WebAssembly, in-browser)
  - Secure Python interpreter (less secure, local)
- Cost depends on chosen execution environment
- Can run fully local with transformers models

#### LLM Provider Support
- **Multi-provider excellence:**
  - InferenceClientModel (HuggingFace providers)
  - LiteLLM integration (100+ models)
  - OpenAI (direct + compatible servers)
  - Anthropic
  - Azure OpenAI
  - Amazon Bedrock
  - Local transformers models
  - Ollama for local models
- Model-agnostic by design

#### Production Readiness
- **Yes** - production deployments confirmed
- Used by AWS (documented case study)
- Multiple production examples in wild
- Security considerations addressed via sandboxing
- Benchmark: beats other frameworks on GAIA benchmark

#### Learning Curve / Time to First Agent
- **Low** - minimal abstractions
- ~1,000 lines of core code to understand
- Simple agent setup:
  ```python
  agent = CodeAgent(tools=[WebSearchTool()], model=model)
  agent.run("Your task")
  ```
- Time to first agent: **~30 minutes**
- CLI tools available for quick testing

#### Best Use Case / Sweet Spot
- Code-executing agents with sandboxed safety
- Model-agnostic deployments
- Vision/multimodal agents (supports text, vision, video, audio)
- Integration with existing tools (MCP servers, LangChain tools, Hub Spaces)
- Developers comfortable with code-based agent reasoning

#### Major Weaknesses / Red Flags
- **No built-in memory** - you implement persistence
- **No built-in knowledge base** - RAG is DIY
- **Security risk** if code execution not sandboxed properly
- **Code agent debugging** can be harder than JSON debugging
- Smaller ecosystem than LangChain/LangGraph

#### Unique Differentiators
1. **Code-based reasoning:** Agents write Python code, not JSON
2. **30% more efficient** than JSON tool calling
3. **Modality-agnostic:** native support for vision, audio, video
4. **Hub integration:** share/load agents and tools from HuggingFace Hub
5. **MCP server support:** use Model Context Protocol servers as tools
6. **LangChain compatibility:** can use LangChain tools directly

### Production Examples
- AWS blog: "Agentic AI with multi-model framework using Hugging Face smolagents on AWS"
- Multiple open-source projects on GitHub
- Educational content and courses

### Verdict
**Production-ready, minimal framework ideal for developers who want code-based agents with maximum flexibility and model-agnostic deployments. Best for solo developers who value simplicity over batteries-included features.**

---

## 2. PocketFlow

### Overview
The most minimal framework in this analysis - just 100 lines of code modeling workflows as graphs. Philosophy: "Let AI agents build agents" through agentic coding with tools like Cursor AI.

### Technical Details
- **Language:** Python (primary), also TypeScript, Java, C++, Go, Rust, PHP
- **GitHub:** https://github.com/The-Pocket/PocketFlow
- **Stars:** 10.1k | **Forks:** 1.1k | **Contributors:** 23
- **License:** MIT
- **Core Code:** 100 lines (pocketflow/__init__.py)
- **Total Size:** +56KB (smallest in analysis)
- **Last Activity:** Active - last commit Feb 16, 2026
- **Commits:** 638
- **Latest Release:** v0.0.3 (Jul 27, 2025)

### Features & Capabilities

#### Tool Calling Support
- **DIY:** You implement tool calls as functions in nodes
- Framework provides graph structure, you provide logic
- No abstraction layer - direct Python functions

#### Memory System
- **DIY:** Shared store abstraction provided
- You implement memory as graph state
- Flow-level state management available

#### Multi-Agent / Swarm Support
- **Yes** - via graph composition
- Agents are nodes in workflows
- Complex multi-agent patterns possible through graph design

#### Streaming Support
- **Yes** - async and parallel execution supported
- AsyncNode for concurrent operations
- Demonstrated 3x-8x speedups with parallelization

#### Self-Hosting Viability & Cost
- **Excellent** - zero dependencies
- Can literally copy the 100-line source file
- No vendor lock-in whatsoever
- Cost = your LLM API costs only

#### LLM Provider Support
- **Provider-agnostic:** You bring your own LLM calls
- No built-in LLM integrations
- Use any library (openai, anthropic, litellm, etc.)
- Complete flexibility

#### Production Readiness
- **Experimental/Educational** - not production deployments known
- Used extensively in tutorials and learning
- Production maturity unknown
- Community-driven examples

#### Learning Curve / Time to First Agent
- **Very Low** - only 100 lines to understand
- Graph mental model (nodes, edges, flows)
- Time to first agent: **~1 hour** (including learning)
- Extensive cookbook with 30+ examples

#### Best Use Case / Sweet Spot
- **Learning** how agent frameworks work
- **Rapid prototyping** with full control
- **Agentic coding** with Cursor AI or similar
- Projects where you want **zero dependencies**
- Understanding agent architecture deeply
- Multi-language projects (ports available)

#### Major Weaknesses / Red Flags
- **No batteries included** - everything is DIY
- **No production track record** - experimental status
- **No built-in tools, memory, or integrations**
- You build ALL agent logic yourself
- Limited community support vs larger frameworks
- Not suitable for fast production deployment

#### Unique Differentiators
1. **Only 100 lines** - truly minimal
2. **Zero dependencies** - no vendor lock-in
3. **Agentic coding philosophy** - humans design, AI codes
4. **Multi-language ports** - Python, TS, Java, C++, Go, Rust, PHP
5. **Educational focus** - learn by understanding every line
6. **Graph abstraction** - universal workflow model

### Philosophy: Agentic Coding
PocketFlow embraces "agentic coding" where:
- Humans specify high-level design and requirements
- AI agents (like Cursor AI) fill in technical details
- Iterative development with human-AI collaboration
- Framework is simple enough for AI to reason about

### Verdict
**Best framework for learning agent architectures and rapid prototyping with full control. Not recommended for production unless you're willing to build everything yourself. Ideal for solo developers who want to deeply understand agent systems or work with AI coding assistants.**

---

## 3. LiteLLM (as Agent Base)

### Overview
**IMPORTANT:** LiteLLM is NOT an agent framework - it's a library for calling 100+ LLM providers with a unified interface. Included here because it can serve as a foundation for custom agent loops.

### Technical Details
- **Language:** Python
- **GitHub:** https://github.com/BerriAI/litellm
- **Stars:** ~14k+ (estimated)
- **License:** MIT (core), Proprietary (proxy features)
- **Core Code:** Not applicable - library, not framework
- **Last Activity:** Very active - continuous development

### Features & Capabilities

#### Tool Calling Support
- **DIY:** You build the agent loop
- LiteLLM handles model calls, you handle tool orchestration

#### Memory System
- **None** - you implement all state management

#### Multi-Agent / Swarm Support
- **DIY** - you build orchestration logic

#### Streaming Support
- **Yes** - proxies streaming from all providers

#### Self-Hosting Viability & Cost
- **Excellent** - LiteLLM proxy can run locally
- Acts as OpenAI-compatible server for any model
- Cost = underlying LLM API costs

#### LLM Provider Support
- **100+ models** including:
  - OpenAI (GPT-3.5, GPT-4, GPT-4o, o1)
  - Anthropic (Claude)
  - Google (Gemini, Vertex AI)
  - Amazon Bedrock
  - Azure OpenAI
  - Hugging Face
  - Ollama (local)
  - Replicate
  - Cohere
  - And 90+ more

#### Production Readiness
- **Yes** - widely used as LLM abstraction layer
- Production-grade features:
  - Load balancing across providers
  - Fallback handling
  - Retry logic
  - Cost tracking
  - Rate limiting

#### Learning Curve / Time to First Agent
- **Medium** - you build everything
- Learning the library: ~1-2 hours
- Building a functional agent: **~4-8 hours** (DIY loop)

#### Best Use Case / Sweet Spot
- **Base for custom agent loops** with full control
- **Multi-provider abstraction** - switch models easily
- **Cost tracking** across different providers
- Projects needing **load balancing** and **fallbacks**
- Integration with OpenAI Agents SDK for multi-model

#### Major Weaknesses / Red Flags
- **Not an agent framework** - significant DIY effort
- You implement: agent loop, tools, memory, orchestration
- Learning curve for building from scratch
- No built-in agent patterns

#### Unique Differentiators
1. **100+ LLM providers** unified interface
2. **Cost tracking** built-in
3. **Load balancing** and fallbacks
4. **OpenAI-compatible proxy** server
5. **Router** for intelligent model selection

### Integration with Agent Frameworks
- Used by OpenAI Agents SDK for multi-model support
- Can integrate with smolagents
- Acts as model layer for custom frameworks

### Verdict
**Not an agent framework, but an excellent foundation for custom agent loops. Choose this if you want full control and are willing to build agent orchestration yourself. Best combined with other tools or as part of a custom solution.**

---

## 4. LangGraph

### Overview
Enterprise-grade framework for building stateful, long-running agents as directed graphs. The production evolution of LangChain's agent capabilities, officially v1.0 as of October 2025.

### Technical Details
- **Language:** Python, TypeScript
- **GitHub:** https://github.com/langchain-ai/langgraph
- **Stars:** 25.3k | **Forks:** 4.4k | **Contributors:** 286
- **License:** MIT
- **Core Code:** 37,000 lines (core libs)
- **Total Size:** +51MB (core only, without LangChain)
- **Last Activity:** Very active - daily commits, last Feb 27, 2026
- **Commits:** 6,549+
- **Latest Release:** langgraph==1.0.10 (Feb 27, 2026)

### Features & Capabilities

#### Tool Calling Support
- **Built-in:** Yes - native function/tool calling
- Integrates with LangChain's extensive tool ecosystem
- Custom tool definitions supported

#### Memory System
- **Built-in:** Comprehensive
  - **Checkpointing:** automatic state persistence
  - **Short-term memory:** working context
  - **Long-term memory:** persistent across sessions
  - **Multiple backends:** PostgresStore, SqliteSaver, InMemory

#### Multi-Agent / Swarm Support
- **Yes** - robust multi-agent orchestration
- Supervisor patterns
- Hierarchical agent teams
- Graph-based agent coordination

#### Streaming Support
- **Yes** - full streaming with events
- Stream intermediate steps
- Real-time agent reasoning visibility

#### Self-Hosting Viability & Cost
- **Good** - can self-host Python/TypeScript apps
- Also: **LangGraph Cloud** (hosted deployment platform)
- Self-hosted: your infrastructure costs
- LangGraph Cloud: proprietary pricing

#### LLM Provider Support
- **Multi-provider** via LangChain integrations
- OpenAI, Anthropic, Google, Azure, Bedrock, local models
- Any LangChain-compatible model

#### Production Readiness
- **Yes - Enterprise Grade**
- **v1.0 released:** October 2025
- **400+ companies** using LangGraph deployment platform
- **Major users:** Uber, LinkedIn, Replit, AppFolio, Klarna, Elastic, Cisco, The Home Depot
- Designed for production from the ground up

#### Learning Curve / Time to First Agent
- **Medium-High**
- Graph mental model required
- StateGraph, nodes, edges concepts
- Time to first agent: **~2-4 hours**
- Time to production-grade: **~1-2 days**
- Extensive documentation and examples

#### Best Use Case / Sweet Spot
- **Enterprise production agents** requiring reliability
- **Complex stateful workflows** with branching logic
- **Human-in-the-loop** applications
- **Durable execution** - agents that survive failures
- **Long-running workflows** (hours/days)
- Teams needing **observability** (LangSmith integration)

#### Major Weaknesses / Red Flags
- **More complex** than minimal frameworks
- **LangChain ecosystem coupling** (though optional)
- **Larger dependencies** (+51MB minimum)
- **Learning curve** steeper than simpler frameworks
- Can be **overkill for simple agents**

#### Unique Differentiators
1. **Durable execution:** agents resume from failures automatically
2. **Human-in-the-loop:** built-in breakpoints and approvals
3. **Checkpointing:** automatic state persistence
4. **LangSmith integration:** deep observability and tracing
5. **Graph-based architecture:** inspired by Google's Pregel
6. **Production deployment platform:** LangGraph Cloud
7. **v1.0 maturity:** production-ready with stability guarantees

### Architecture Philosophy
- Deprecates LangChain's AgentExecutor
- Cyclic, stateful graph-based workflows preferred
- Explicit state management over hidden state
- Control and visibility over magic abstractions

### Verdict
**Production-grade framework for enterprise teams building complex, stateful agents. Best choice for applications requiring reliability, observability, and human oversight. Worth the learning curve for serious production deployments.**

---

## 5. CrewAI

### Overview
The most popular agent framework (44k+ GitHub stars) focused on role-based multi-agent collaboration. Emphasizes rapid prototyping and intuitive agent team design.

### Technical Details
- **Language:** Python
- **GitHub:** https://github.com/crewAIInc/crewAI
- **Stars:** 44,285+ (as of March 2026) - highest in this analysis
- **License:** MIT
- **Core Code:** 18,000 lines
- **Total Size:** +173MB
- **Last Activity:** Very active - continuous development
- **Latest Release:** Continuous releases

### Features & Capabilities

#### Tool Calling Support
- **Built-in:** Yes - extensive tool library
- Pre-built tools for common tasks
- Custom tool integration easy
- Tool delegation between agents

#### Memory System
- **Built-in:** Yes - sophisticated
  - **Short-term memory:** task execution context
  - **Long-term memory:** cross-session persistence
  - **Entity memory:** tracking specific entities
- Memory shared across crew members

#### Multi-Agent / Swarm Support
- **Yes - Core Feature**
- Role-based crew design (agents have specific roles)
- Sequential and hierarchical task execution
- Built-in task delegation and collaboration
- Agent autonomy levels configurable

#### Streaming Support
- **Yes** - streaming responses

#### Self-Hosting Viability & Cost
- **Good** - Python package, self-hostable
- Also: **CrewAI Cloud** (managed deployment)
- Self-hosted: your infrastructure
- CrewAI Cloud: proprietary pricing

#### LLM Provider Support
- **Multi-provider:**
  - OpenAI
  - Anthropic
  - Others via LangChain integrations
- Model selection per agent

#### Production Readiness
- **Yes** - used in production
- Focus on **rapid prototyping** that ships
- Production deployments confirmed
- Community reports good production stability

#### Learning Curve / Time to First Agent
- **Low-Medium**
- Role-based abstraction is intuitive
- Clear separation: Agents → Tasks → Crew
- Time to first agent: **~1-2 hours**
- Time to production: **~1-3 days**

#### Best Use Case / Sweet Spot
- **Rapid multi-agent prototyping**
- **Role-based workflows** (clear agent responsibilities)
- **Fast deployment** requirements
- Teams wanting **intuitive abstractions**
- Projects with **collaborative agent patterns**
- Startups moving fast

#### Major Weaknesses / Red Flags
- **Less explicit state control** than LangGraph
- **Abstraction can limit flexibility** in complex scenarios
- **Larger framework** (18k lines, 173MB)
- **Vendor direction** (CrewAI Inc. controls roadmap)
- Some report production edge cases

#### Unique Differentiators
1. **Role-based design:** agents have roles, goals, backstories
2. **44k+ stars:** most popular framework in this analysis
3. **Intuitive abstractions:** easy mental model
4. **Built-in collaboration:** task delegation between agents
5. **Sequential & hierarchical modes:** flexible execution patterns
6. **Fast to production:** rapid prototyping focus

### Industry Perception (2026)
- Excellent for **rapid prototyping**
- Good for **production** but LangGraph preferred for complex state
- Best **developer experience** for multi-agent teams
- Strong community and ecosystem

### Verdict
**Best framework for rapid multi-agent prototyping with intuitive role-based abstractions. Great for solo founders who need to ship fast. Choose over LangGraph for simpler use cases where speed matters more than explicit state control.**

---

## 6. Agno (formerly Phidata)

### Overview
Production-first framework rebranded from Phidata in late 2025/early 2026. Three-layer architecture: Framework + Runtime + Control Plane. Designed as "the runtime for agentic software" with enterprise deployment focus.

### Technical Details
- **Language:** Python
- **GitHub:** https://github.com/agno-agi/agno (redirects from phidatahq/phidata)
- **Stars:** 38.3k | **Forks:** 5.1k | **Contributors:** 405
- **License:** Apache-2.0
- **Core Code:** Unknown (substantial codebase)
- **Last Activity:** Very active - last commit Feb 27, 2026
- **Commits:** 5,226+
- **Latest Release:** v2.5.5 (Feb 25, 2026)

### Features & Capabilities

#### Tool Calling Support
- **Built-in:** Yes - extensive
  - 100+ tool integrations
  - MCP (Model Context Protocol) support
  - Custom tool decorator `@tool`
- Tool caching and optimization

#### Memory System
- **Built-in:** Sophisticated
  - **Short-term memory:** conversation context
  - **Long-term memory:** persistent storage
  - **User memories:** per-user personalization
  - **Session-scoped memory**
  - Database backends: SQLite, PostgreSQL

#### Multi-Agent / Swarm Support
- **Yes** - comprehensive
  - **Agents:** individual units
  - **Teams:** coordinated agent groups
  - **Workflows:** structured execution
  - Per-agent and per-team configuration

#### Streaming Support
- **Yes** - streaming events system
- Real-time event emission
- `stream_events=True` for all components

#### Self-Hosting Viability & Cost
- **Excellent** - designed for self-hosting
  - **Stateless FastAPI runtime**
  - **Horizontally scalable**
  - **Your infrastructure, your rules**
- AgentOS UI connects to your deployment
- Cost = infrastructure + LLM APIs

#### LLM Provider Support
- **Multi-provider extensive:**
  - OpenAI
  - Anthropic (Claude)
  - Google (Gemini)
  - AWS Bedrock
  - Azure OpenAI
  - Local models (Ollama, etc.)
  - Many more via integrations

#### Production Readiness
- **Yes - Production-First Design**
- Built specifically for production deployment
- **Stateless runtime** enables horizontal scaling
- **Per-user, per-session isolation**
- **50+ APIs** for agent management
- Native tracing and auditability
- Used in real production systems

#### Learning Curve / Time to First Agent
- **Medium**
- Three layers to understand:
  1. Framework (Agent, Team, Workflow)
  2. Runtime (FastAPI, AgentOS)
  3. Control Plane (AgentOS UI)
- Time to first agent: **~2-3 hours**
- Time to production API: **~4-6 hours**

#### Best Use Case / Sweet Spot
- **Production agentic systems** at scale
- **Multi-agent teams** with coordination
- **Enterprise deployment** with governance
- **Stateless, scalable services**
- Teams needing **approval workflows**
- Applications requiring **full auditability**
- **Knowledge-based agents** (built-in RAG)

#### Major Weaknesses / Red Flags
- **Larger framework** - more to learn
- **Newer branding** (Phidata → Agno rebrand in 2025/2026)
- **More concepts** than simpler frameworks
- **Opinionated architecture** (three layers)
- Less community content than LangChain ecosystem

#### Unique Differentiators
1. **Three-layer architecture:** Framework + Runtime + Control Plane
2. **Stateless FastAPI runtime:** horizontal scalability built-in
3. **AgentOS UI:** management and testing interface
4. **Per-user, per-session isolation:** built-in multi-tenancy
5. **Approval workflows:** human-in-the-loop governance
6. **Native guardrails:** safety and compliance built-in
7. **Knowledge integration:** RAG out of the box
8. **Full auditability:** trace every action

### Architecture Philosophy
- Agents run as **stateless services** (not long-running processes)
- State stored in **your database** (SQLite, PostgreSQL)
- **Session-scoped execution** with isolation
- **Governance as code:** approvals, guardrails, evals built-in

### Production Features
- 50+ REST APIs for agent management
- Background task execution
- Real-time monitoring
- Session management
- User authentication integration
- Trace storage and analysis

### Verdict
**Production-grade runtime for building, deploying, and managing agentic systems at scale. Best for teams serious about production deployment with governance, scalability, and auditability requirements. Worth the learning curve for enterprise applications.**

---

## 7. OpenAI Swarm (DEPRECATED)

### Overview
**⚠️ DEPRECATED - DO NOT USE FOR NEW PROJECTS**

OpenAI's experimental, educational framework for lightweight multi-agent orchestration. **Officially replaced by OpenAI Agents SDK in 2026.** Included only for historical context.

### Technical Details
- **Language:** Python
- **GitHub:** https://github.com/openai/swarm
- **Stars:** 21k | **Forks:** 2.2k
- **License:** MIT
- **Core Code:** ~500 lines (estimated)
- **Last Activity:** **DEPRECATED** - last commit Mar 11, 2025
- **Status:** Replaced by OpenAI Agents SDK

### Deprecation Notice
From the official repo:
> "Swarm is now replaced by the OpenAI Agents SDK, which is a production-ready evolution of Swarm. The Agents SDK features key improvements and will be actively maintained by the OpenAI team. We recommend migrating to the Agents SDK for all production use cases."

### Why It Was Popular
- Simple agent + handoff primitives
- Educational framework for learning
- OpenAI's official experimental release
- Clean API design

### Why You Should NOT Use It
1. **Deprecated** - no future updates
2. **Replaced** - OpenAI Agents SDK is successor
3. **OpenAI-only** - no multi-provider support
4. **Experimental** - never production-ready
5. **Stateless** - no built-in memory

### Migration Path
**Use OpenAI Agents SDK instead:**
- https://github.com/openai/openai-agents-python
- Production-ready evolution
- Active maintenance
- Better features

### Verdict
**DO NOT USE. If you want OpenAI's agent framework, use the OpenAI Agents SDK. If you want lightweight multi-agent orchestration, use smolagents, CrewAI, or LangGraph instead.**

---

## Comparison Matrix

### By Lines of Code (Minimalism)
1. **PocketFlow:** 100 lines ⭐ Most minimal
2. **OpenAI Swarm:** ~500 lines (deprecated)
3. **smolagents:** ~1,000 lines
4. **LiteLLM:** N/A (library, not framework)
5. **CrewAI:** 18,000 lines
6. **LangGraph:** 37,000 lines
7. **Agno:** Unknown (large)

### By GitHub Stars (Popularity)
1. **CrewAI:** 44,285+ ⭐ Most popular
2. **Agno:** 38,300+
3. **smolagents:** 25,700
4. **LangGraph:** 25,300
5. **OpenAI Swarm:** 21,000 (deprecated)
6. **LiteLLM:** ~14,000 (estimated)
7. **PocketFlow:** 10,100

### By Production Readiness
**Production-Ready (5):**
- ✅ **smolagents** - Yes, AWS deployments
- ✅ **LangGraph** - Yes, 400+ companies
- ✅ **CrewAI** - Yes, confirmed usage
- ✅ **Agno** - Yes, production-first design
- ✅ **LiteLLM** - Yes, as base layer

**Experimental (1):**
- ⚠️ **PocketFlow** - Educational

**Deprecated (1):**
- ❌ **OpenAI Swarm** - Do not use

### By Learning Curve (Easiest First)
1. **PocketFlow** - 1 hour (only 100 lines)
2. **smolagents** - 30 min to 1 hour
3. **CrewAI** - 1-2 hours (intuitive roles)
4. **LiteLLM** - 1-2 hours (but then DIY)
5. **LangGraph** - 2-4 hours (graph concepts)
6. **Agno** - 2-3 hours (three layers)

### By Self-Hosting Viability
**Excellent:**
- ✅ **PocketFlow** - Zero dependencies
- ✅ **smolagents** - Multiple sandbox options
- ✅ **Agno** - Stateless runtime designed for it
- ✅ **LiteLLM** - Proxy runs anywhere

**Good:**
- ✅ **LangGraph** - Can self-host or use Cloud
- ✅ **CrewAI** - Can self-host or use Cloud

### By Multi-Provider Support (LLM Flexibility)
**Best:**
- ⭐ **LiteLLM** - 100+ providers (purpose-built)
- ⭐ **smolagents** - 10+ provider types
- ⭐ **Agno** - Extensive multi-provider

**Good:**
- ✅ **LangGraph** - Via LangChain integrations
- ✅ **CrewAI** - Via LangChain integrations

**DIY:**
- 🔧 **PocketFlow** - You bring your own

**Limited:**
- ❌ **OpenAI Swarm** - OpenAI only (deprecated anyway)

---

## Decision Framework for Solo Founders

### Choose smolagents if:
- ✅ You want **minimal abstractions** (~1,000 lines)
- ✅ You like the idea of **code-based reasoning** (agents write Python)
- ✅ You need **model-agnostic** deployments
- ✅ You value **sandboxed security** options
- ✅ You want **multimodal** support (vision, audio, video)
- ✅ You're comfortable reading framework source code
- ❌ You need built-in memory/knowledge (you'll build it)

**Time investment:** Low, but DIY memory  
**Production path:** Clear (AWS, others using it)  
**Risk:** Low - HuggingFace backing, active development

---

### Choose PocketFlow if:
- ✅ You want to **deeply understand** agent architecture
- ✅ You're using **AI coding assistants** (Cursor, etc.)
- ✅ You want **zero dependencies** and vendor lock-in
- ✅ You value **learning** over shipping fast
- ✅ You need **full control** over every aspect
- ✅ You're building a **custom framework** anyway
- ❌ You need production-ready in days/weeks
- ❌ You want batteries-included

**Time investment:** Low to learn, high to build  
**Production path:** Unclear - you're on your own  
**Risk:** Medium - experimental, limited support

---

### Choose LiteLLM (as base) if:
- ✅ You want to **build custom agent loops** from scratch
- ✅ You need **100+ LLM providers** with unified API
- ✅ You want **load balancing** and **fallbacks**
- ✅ You need **cost tracking** across providers
- ✅ You're experienced and want **full control**
- ❌ You want a complete framework (this isn't one)
- ❌ You need fast time-to-market

**Time investment:** High (build everything)  
**Production path:** DIY but proven base  
**Risk:** Low - widely used library

---

### Choose LangGraph if:
- ✅ You need **enterprise-grade production** reliability
- ✅ You have **complex stateful workflows**
- ✅ You need **human-in-the-loop** built-in
- ✅ You want **durable execution** (survive failures)
- ✅ You value **observability** (LangSmith)
- ✅ You're building for **scale** (400+ companies use it)
- ❌ You want simple, minimal code
- ❌ You're prototyping and need speed

**Time investment:** Medium-High (learning curve)  
**Production path:** Clear (Uber, LinkedIn using it)  
**Risk:** Low - v1.0, enterprise backing

---

### Choose CrewAI if:
- ✅ You need **rapid multi-agent prototyping**
- ✅ You like **role-based abstractions** (intuitive)
- ✅ You want to **ship fast**
- ✅ You need **multi-agent teams** working together
- ✅ You value **developer experience** over control
- ✅ Community and popularity matter (44k+ stars)
- ❌ You need explicit state management (use LangGraph)
- ❌ You're worried about vendor direction

**Time investment:** Low-Medium  
**Production path:** Good (confirmed production use)  
**Risk:** Medium - company-controlled roadmap

---

### Choose Agno if:
- ✅ You're building **production agentic systems** for scale
- ✅ You need **governance** (approvals, guardrails)
- ✅ You want **stateless, scalable** architecture
- ✅ You need **multi-tenancy** (per-user isolation)
- ✅ You value **auditability** and tracing
- ✅ You want **knowledge/RAG** built-in
- ❌ You want the simplest option
- ❌ You're just prototyping

**Time investment:** Medium (three-layer model)  
**Production path:** Excellent (purpose-built)  
**Risk:** Medium - recent rebrand, smaller ecosystem than LangChain

---

### DON'T Choose OpenAI Swarm:
- ❌ **Deprecated** - use OpenAI Agents SDK instead
- ❌ **No maintenance**
- ❌ **Better alternatives exist**

---

## Solo Founder Recommendation Matrix

### "I want to ship FAST" (MVP in 1-2 weeks)
**→ CrewAI** (rapid prototyping, intuitive)  
**Alternative:** smolagents (if you want minimal)

### "I want to LEARN deeply" (understand agents)
**→ PocketFlow** (100 lines, zero magic)  
**Alternative:** smolagents (readable, minimal)

### "I want PRODUCTION SCALE" (enterprise-grade)
**→ LangGraph** (400+ companies, proven)  
**Alternative:** Agno (if you want governance/runtime)

### "I want FULL CONTROL" (custom everything)
**→ LiteLLM + custom loop** (DIY approach)  
**Alternative:** PocketFlow (minimal starting point)

### "I want MODEL FLEXIBILITY" (switch providers)
**→ smolagents** (multi-provider by design)  
**Alternative:** LiteLLM (100+ providers)

### "I want MINIMAL CODE" (small footprint)
**→ PocketFlow** (100 lines)  
**Alternative:** smolagents (1,000 lines)

### "I want COMMUNITY & SUPPORT" (largest ecosystem)
**→ CrewAI** (44k stars)  
**Alternative:** LangGraph (LangChain ecosystem)

### "I want SECURITY & GOVERNANCE" (enterprise needs)
**→ Agno** (built-in approvals, guardrails)  
**Alternative:** LangGraph (enterprise deployments)

---

## Cost Comparison

All frameworks primarily cost LLM API usage. Differences:

### Infrastructure Costs
- **PocketFlow, smolagents, LiteLLM:** Your servers only
- **LangGraph:** Self-host OR LangGraph Cloud (proprietary pricing)
- **CrewAI:** Self-host OR CrewAI Cloud (proprietary pricing)
- **Agno:** Your infrastructure (stateless design scales cheaply)

### Execution Efficiency (LLM Token Usage)
- **smolagents:** 30% fewer LLM calls than JSON-based (documented)
- **Others:** Standard token usage for agent loops

### Hidden Costs
- **Learning time:** PocketFlow/LiteLLM require building everything
- **Maintenance:** More complex frameworks = more updates
- **Vendor lock-in:** CrewAI/LangGraph clouds vs self-hosted options

**Winner for cost:** smolagents (30% fewer calls) or PocketFlow (zero dependencies)

---

## Red Flags & Risks

### smolagents
- ⚠️ Code execution security if not sandboxed
- ⚠️ Smaller ecosystem than LangChain
- ✅ But: HuggingFace backing reduces risk

### PocketFlow
- ⚠️ No production track record
- ⚠️ Experimental status
- ⚠️ Build everything yourself
- ✅ But: So simple, low risk of abandonment

### LiteLLM
- ⚠️ Not actually a framework (major DIY effort)
- ⚠️ Building agent logic from scratch is complex
- ✅ But: Widely used, stable library

### LangGraph
- ⚠️ Complexity for simple use cases (overkill)
- ⚠️ LangChain ecosystem coupling
- ✅ But: Enterprise backing, v1.0 stability

### CrewAI
- ⚠️ Company-controlled roadmap
- ⚠️ Less state control than LangGraph
- ⚠️ Abstraction limits flexibility in edge cases
- ✅ But: Strong community, good production use

### Agno
- ⚠️ Recent rebrand (Phidata → Agno)
- ⚠️ Smaller community vs LangChain
- ⚠️ More concepts to learn
- ✅ But: Production-first design, active development

### OpenAI Swarm
- 🚫 **DEPRECATED - DO NOT USE**

---

## Final Recommendations

### For Solo Founders (General)
**Top 3 Picks:**
1. **smolagents** - Balance of minimal + production-ready
2. **CrewAI** - Fast prototyping to production
3. **LangGraph** - If you need enterprise features

**Avoid:**
- OpenAI Swarm (deprecated)
- LiteLLM alone (unless you want to build everything)

### For Specific Founder Profiles

#### "Hacker/Builder" (likes to understand code)
**→ smolagents** or **PocketFlow**  
Why: Minimal code, readable, hackable

#### "Ship Fast" (need MVP quickly)
**→ CrewAI**  
Why: Intuitive, rapid prototyping, good DX

#### "Enterprise Ambitions" (scaling from day one)
**→ LangGraph** or **Agno**  
Why: Production-grade, governance, scalability

#### "Indie Hacker" (cost-conscious, self-hosted)
**→ smolagents** or **PocketFlow**  
Why: No vendor lock-in, cheap to run, self-hosted

#### "AI-First Developer" (using Cursor/AI coding)
**→ PocketFlow**  
Why: Designed for agentic coding paradigm

---

## Where NOT to Use Each

### Don't use smolagents if:
- You need batteries-included memory/knowledge
- You're uncomfortable with code-based reasoning
- You want the largest ecosystem

### Don't use PocketFlow if:
- You need production ASAP
- You want community support
- You don't want to build everything

### Don't use LiteLLM if:
- You want a complete framework (it's not one)
- You're not experienced with agent patterns

### Don't use LangGraph if:
- You have simple use cases (overkill)
- You want minimal dependencies
- Learning curve is a blocker

### Don't use CrewAI if:
- You need explicit state machine control
- You're worried about vendor lock-in
- Abstractions limit you

### Don't use Agno if:
- You want the simplest option
- You're just experimenting
- Recent rebrand concerns you

### Don't use OpenAI Swarm:
- Ever (it's deprecated)

---

## Conclusion

**For most solo founders in 2026, the best choice is:**

### 🥇 **smolagents** if you value:
- Minimalism (1,000 lines)
- Model flexibility
- Production readiness
- Code-based reasoning
- HuggingFace ecosystem

### 🥈 **CrewAI** if you value:
- Speed to market
- Intuitive abstractions
- Multi-agent teams
- Community size
- Developer experience

### 🥉 **LangGraph** if you value:
- Enterprise features
- State management
- Human-in-the-loop
- Battle-tested at scale
- Observability

**For learning:** PocketFlow  
**For custom builds:** LiteLLM + DIY  
**For governance:** Agno  
**For anything:** NOT OpenAI Swarm

---

## Research Methodology

This research was conducted on March 1, 2026, using:

1. **GitHub repository analysis**
   - Official repos examined for all frameworks
   - Stars, forks, commits, activity analyzed
   - Source code size measured

2. **Official documentation review**
   - Each framework's docs examined
   - Feature sets catalogued
   - Examples analyzed

3. **Recent articles & blog posts (2025-2026)**
   - Production use cases
   - Framework comparisons
   - Developer experiences

4. **Community feedback**
   - GitHub issues/discussions
   - Blog posts from practitioners
   - Comparison articles

All facts are sourced from official repositories, documentation, or credible recent sources. Where information was unavailable, it is explicitly marked as "unknown."

---

## Additional Resources

### smolagents
- Docs: https://huggingface.co/docs/smolagents
- GitHub: https://github.com/huggingface/smolagents
- Blog: https://huggingface.co/blog/smolagents

### PocketFlow
- Docs: https://the-pocket.github.io/PocketFlow/
- GitHub: https://github.com/The-Pocket/PocketFlow
- Philosophy: "Agentic Coding" approach

### LiteLLM
- Docs: https://docs.litellm.ai/
- GitHub: https://github.com/BerriAI/litellm

### LangGraph
- Docs: https://docs.langchain.com/oss/python/langgraph/
- GitHub: https://github.com/langchain-ai/langgraph
- LangGraph Cloud: https://langchain.com/langgraph

### CrewAI
- Docs: https://docs.crewai.com/
- GitHub: https://github.com/crewAIInc/crewAI
- Website: https://www.crewai.com

### Agno
- Docs: https://docs.agno.com/
- GitHub: https://github.com/agno-agi/agno
- Website: https://www.agno.com

### OpenAI Agents SDK (Swarm replacement)
- Docs: https://openai.github.io/openai-agents-python/
- GitHub: https://github.com/openai/openai-agents-python

---

**End of Report**

*This research was conducted by the Pre-Planning Research Agent on March 1, 2026, for a solo founder/developer evaluating AI agent frameworks. All information is accurate as of the research date based on publicly available sources.*
