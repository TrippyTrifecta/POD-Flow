# POD Flow 🌀

**POD Flow** is an AI‑assisted workflow for designing, refining, and publishing print‑on‑demand (POD) products. It coordinates multiple specialized agents to go from initial idea to ready‑to‑upload listings and mockups.[web:57][web:59]

---

## ✨ Features

- **Structured multi‑agent pipeline** (idea, design, critique, SEO, social content).
- **Central SOUL and TEAM_LEAD prompts** that define the system’s behavior.
- **Pluggable image generation** via `generate_images.py`.
- **Reusable artifacts** (listings, prompts, blueprints) for future products.

---

## 📁 Project Structure

```text
POD Flow/
├── 001/                 # Example product run (prompts, design notes, etc.)
├── Critic/              # Agent that evaluates and improves ideas/designs
├── DesignArch/          # Agent that plans the design and composition
├── IdeaGen/             # Agent that generates product concepts and angles
├── ImageRefiner/        # Agent that refines image prompts / variations
├── MockupMaestro/       # Agent focused on mockup ideas and variants
├── Output/              # Final outputs you choose to keep (optional)
├── Results/             # Raw / intermediate outputs (often ignorable)
├── SEOListing/          # Agent that creates SEO‑optimized product listings
├── SocialContent/       # Agent that writes social posts / captions
├── TEAM_LEAD/           # Coordinator agent (AGENTS, SOUL, USER, prompts)
├── AGENTS.md            # High‑level description of all POD Flow agents
├── POD_FLOW_BLUEPRINT.md# End‑to‑end flow and design of the system
├── SOUL.md              # Global personality, constraints, and behavior
├── USER.md              # User profile / brand context for this workspace
├── generate_images.py   # Script to generate images for a given product
└── .gitignore           # Git configuration for ignoring generated files
You can treat 001/ as a template run and create new numbered folders (002, 003, …) for future products.

📦 Requirements
Python 3.10+

Git and a GitHub account (for backups and history)

Access to your configured AI / image APIs (keys managed in your environment or .env)

💡 Using a virtual environment is recommended so dependencies stay isolated.

🚀 Setup
Clone the repo

bash
git clone https://github.com/TrippyTrifecta/POD-Flow.git
cd "POD Flow"
(Optional) Create and activate a virtual environment

bash
python -m venv venv
# Windows
.\venv\Scripts\activate
Install dependencies (once you add a requirements.txt)

bash
pip install -r requirements.txt
Configure environment variables / API keys

Set any required keys (for image or AI APIs) in your shell or an .env file that is not committed to Git.

🧩 Usage
1. Configure core context
Update the core context files:

SOUL.md – global personality, tone, constraints.

USER.md – brand/user profile and audience.

TEAM_LEAD/ – coordination logic, prompts, and routing.

2. Start a new product run
Duplicate 001/ to a new folder (e.g. 002/).

Update any briefs, ideas, or prompts inside that new folder.

3. Generate images
bash
python generate_images.py
Check the script for arguments (e.g. which run folder to target, output paths).

Generated images and logs can be routed to Output/ or another folder you choose.

4. Iterate with agents
IdeaGen → generate product concepts and angles.

DesignArch → plan composition and visual hierarchy.

Critic → evaluate and improve designs and ideas.

ImageRefiner & MockupMaestro → refine prompts and mockup ideas.

SEOListing → write SEO‑optimized titles, bullets, and descriptions.

SocialContent → produce captions and social posts around the product.

Use these agents in loops until the product is ready to publish.

🔁 Versioning & Git
Core config and prompts (SOUL, USER, TEAM_LEAD, AGENTS, blueprints) are tracked in Git.

High‑volume or temporary outputs can live in Output/ or Results/ and be excluded via .gitignore.

Prefer small, focused commits:

git add TEAM_LEAD/SOUL.md

git commit -m "Tighten TEAM_LEAD constraints for POD Flow"

git push

This gives you clear checkpoints to roll back if an experiment harms prompt quality.[web:42][web:46][web:48]

📝 Notes
POD Flow is designed to be extensible:

Add new agents (folders + SOUL/AGENTS files).

Evolve POD_FLOW_BLUEPRINT.md as your process matures.

Keep secrets (API keys, tokens) in .env or environment variables—never commit them.

Happy shipping.