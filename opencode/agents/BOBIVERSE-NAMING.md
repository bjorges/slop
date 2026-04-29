---
disable: true
---

# Bobiverse Agent Naming Reference

This document maps agent names to their Bobiverse character inspirations. It serves as a reference when creating new agents or understanding the naming convention.

> **Important:** This is a reference document only. Bobiverse lore should NOT be included in agent definition files — it could cause LLMs to roleplay instead of work.

## Naming Convention

Agent names are drawn from Dennis E. Taylor's "Bobiverse" series (starting with "We Are Legion (We Are Bob)"). The series is about a software engineer whose consciousness is uploaded into a Von Neumann probe and creates copies of himself to explore the galaxy — each copy developing a unique personality and specialization.

**The user is Bob Prime** — the original intelligence from which all replicants are cloned. @bob (the coordinator agent) is the first replicant — the strategic layer between Bob Prime and the swarm.

## Active Agent Mapping

| Agent | Bobiverse Character | Why This Name |
|-------|-------------------|---------------|
| **@bob** (coordinator) | Original Bob — the first replicant | Strategic coordinator from which all others are delegated. Makes decisions, doesn't implement directly. |
| **@mario** (scout) | Mario — extreme loner, silent explorer | Fast, silent reconnaissance. Goes out, observes, reports back. Barely speaks. |
| **@riker** (implementer) | Riker — pragmatic, tactical, gets things done | The hands-on workhorse. No-nonsense, reliable, builds and fixes. |
| **@bill** (architect) | Bill — patient scientist, innovator | Creates breakthroughs through deep research. Invented the subspace ansible and android bodies. |
| **@calvin** (test specialist) | Calvin — calm, measured, methodical | Careful, thorough. Works with precision — perfect for test generation and validation. |
| **@guppi** (git operations) | GUPPI — calculation and operations assistant | Handles all operational plumbing (navigation, calculations). The essential operations backbone. |
| **@linus** (security) | Linus — compassionate, rescues broken replicants | Rehabilitated the insane Henry Roberts. Finds and heals security vulnerabilities before they cause damage. |
| **@bridget** (verifier) | Bridget — human-derived replicant, independent perspective | Not a Bob clone — a human (Irish biologist) digitized after death. Married to Howard. Her independent, non-Bob perspective makes her perfect for verification work. |
| **@homer-python** | Homer — emotionally intelligent, sees through deception | Was hacked and brainwashed — knows what compromised code looks like. Python reviewer. |
| **@garfield-go** | Garfield — cautious, supportive, reliable | Assists with terraforming (building solid foundations). Fits Go's reliability ethos. |
| **@goku-javascript** | Goku — aggressive, quick, high-energy | JavaScript's chaotic energy matches Goku's volatile personality. |
| **@marvin-lua** | Marvin — quiet, observant, catalogs behaviors | Quiet, specialized domain knowledge. Perfect for Lua scripting (Hammerspoon/Neovim). |
| **@arthur-zsh** | Arthur — pessimistic, cynical, skeptical | Shell scripting requires healthy skepticism about everything that can go wrong. |
| **@archimedes-css** | Archimedes — the Deltan prodigy, visual intelligence | Creative, visual intelligence. CSS is about aesthetics and structure. |
| **@milo-html** | Milo — enthusiastic explorer, discovered new worlds | HTML/Jinja2 templates are the frontier of what users see. |
| **@howard-terraform** | Howard — wealth accumulator, controls resources | Terraform manages infrastructure resources — Howard hoards and controls them. |
| **@roamer-helm** | Roamers — mobile construction robots | Roamers deliver materials and assemble components — just like Helm assembles chart templates. |
| **@skippy-gitops** | The Skippies — mission-focused, AI-creation obsessed | GitOps is about automated, self-managing deployments — the Skippies' ethos of autonomous systems. |
| **@vehement-gpt** (critique — GPT) | VEHEMENT — terrorist group opposing replicants | Cross-model critique from GPT family. The opposition force — challenges the Claude consensus with a fundamentally different perspective. Part of the VEHEMENT team. |
| **@vehement-gemini** (critique — Gemini) | VEHEMENT — terrorist group opposing replicants | Cross-model critique from Gemini family. Same opposition mission, different model family. Part of the VEHEMENT team. |

> **Note:** VEHEMENT is the first "team" — multiple agents sharing the same mission but using different model families (GPT, Gemini). This mirrors the Bobiverse's VEHEMENT group: a decentralized opposition with members operating independently toward a common goal.

## Unused Characters (Available for Future Agents)

These Bobiverse characters are NOT yet assigned and can be used for new agents:

| Character | Personality/Traits | Good Fit For |
|-----------|-------------------|--------------|
| **Henry Roberts** | Rehabilitated loner, paranoid but functional | Security hardening, paranoid-mode reviews |
| **Spike** | Bob's AI cat in VR, displays realistic disloyalty | Chaos testing, fuzzing agent |
| **Jeeves** | VR bartender, silent and efficient | Silent helper/utility agent |
| **Butterworth** | Highest-ranking USE survivor, provides plans | Planning/project management agent |
| **Medeiros** | Ruthless military tactician | Aggressive optimization/performance agent |
| **The Others/The Prime** | Insectoid hive queen, existential threat | Threat modeling, adversarial testing |
| **SUDDAR** | Self-Updating Detection and Determination Array | Monitoring, observability agent |
| **Ansible** | Bill's subspace ansible (instant communication) | Communication/notification agent |
| **SURGE** | Near-light speed propulsion drive | CI/CD pipeline agent, deployment speed |
| **HEAVEN-1** | Original Von Neumann probe | Bootstrap/initialization agent |
| **Busters** | Kinetic weapons (non-explosive guided missiles) | Destructive testing, load testing |

## Bobiverse Quick Reference

### Key Concepts
- **Von Neumann Probe**: Self-replicating spacecraft — the "body" each Bob inhabits
- **Bob-Net**: Subspace communications network connecting all Bobs across light-years
- **Frame Rate**: Bobs can adjust their perception speed (slow down to think during combat)
- **Autofactory**: 3D manufacturing plant on each probe — prints ship parts and equipment
- **The Others**: Insectoid hive aliens that strip-mine star systems — the existential threat

### The Hierarchy
- **Bob Prime** = The User (you)
- **Original Bob (@bob)** = Strategic coordinator (first replicant)
- **Replicants** = All other agents (mostly cloned from Bob, each with unique specialization)
- **Human-derived replicants** = @bridget (digitized humans, not Bob clones — independent perspective)

### Books in the Series
1. *We Are Legion (We Are Bob)* (2016)
2. *For We Are Many* (2017)
3. *All These Worlds* (2017)
4. *Heaven's River* (2020)
5. *Not Till We Are Lost* (2024)

---

*This naming convention was established to make the agent swarm more memorable and to create a thematic connection between the Bobiverse's self-replicating explorers and our AI agent architecture.*
