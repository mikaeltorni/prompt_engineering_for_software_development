# Prompt Engineering for Software Development — Multi-Agent LLM Research

[![Last commit](https://img.shields.io/github/last-commit/mikaeltorni/prompt_engineering_for_software_development)](https://github.com/mikaeltorni/prompt_engineering_for_software_development/commits/main)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mikaeltorni/prompt_engineering_for_software_development)](https://github.com/mikaeltorni/prompt_engineering_for_software_development/graphs/commit-activity)
[![Issues](https://img.shields.io/github/issues/mikaeltorni/prompt_engineering_for_software_development)](https://github.com/mikaeltorni/prompt_engineering_for_software_development/issues)

Prompt Engineering for Software Development is a research repository that evaluates prompt engineering for software development with a multi-agent LLM system for software teams.

The Bachelor's thesis artifacts study project manager, coder, tester, and
debugger agents, together with the prompt-development and evaluation harness
used to measure prompt quality.

**Topics:** prompt-engineering · large-language-models · llm-agents ·
multi-agent-systems · ai-coding-assistant · promptfoo · prompt-evaluation ·
software-development · thesis · gpt

## Quickstart

Clone the thesis artifacts and inspect the two research components:

```bash
git clone https://github.com/mikaeltorni/prompt_engineering_for_software_development.git
cd prompt_engineering_for_software_development
find multi_agentic_system_for_programming prompt_development_and_testing -maxdepth 2 -type f | sort | head -20
```

Run each subproject with the dependencies and evaluation instructions in its
own directory.

## 📄 Thesis

Read the full thesis: **["Prompt engineering for software development"](https://www.theseus.fi/handle/10024/894216)**
(Theseus open repository).

Follow-up work optimizing production coding prompts continues in
[`programming_prompts`](https://github.com/mikaeltorni/programming_prompts).

For reusable challenge-generation assets, see the related
[Prompt Challenge Generator](https://github.com/mikaeltorni/prompt_challenge_generator).

## Features

This repository holds the two artifacts produced for the thesis:

### 1. `multi_agentic_system_for_programming/`

A prototype **multi-agent system** where specialized LLM agents collaborate to
build software from a task description. Its structure:

- `data/agents.py`, `data/models.py`, `data/project_config.py` — agent
  definitions, model configuration, and per-project settings.
- `data/prompts/system/` — the system prompts that define each role:
  `project_manager_prompt.md`, `coder_agentic_part.xml`, `tester_prompt.md`,
  and `debugger_prompt.xml`.
- `scripts/` — tooling the agents use: `agent_chat_tools.py`, `agent_tools.py`,
  `file_tools.py`, `project_tools.py`, and `xml_parsing_tools.py`.
- `main.py` — entry point that wires the agents together.

### 2. `prompt_development_and_testing/`

The **prompt evaluation harness** used to develop and validate the prompts
above with [promptfoo](https://www.promptfoo.dev/):

- `evals/eval_configs/` — promptfoo configurations for the `coding` and
  `project_manager` prompts.
- `evals/assertion_prompts/` — LLM-graded assertion prompts that score outputs.
- `evals/eval_data/` — test tasks, CSV samples, and captured results, including
  passing/failing test extractions.
- `evals/instructions_for_running_evals.md` — how to reproduce the evaluations.

## Installation and usage examples

Each subproject has its own `requirements.txt`:

```bash
cd multi_agentic_system_for_programming   # or prompt_development_and_testing/evals
pip install -r requirements.txt
```

See `prompt_development_and_testing/evals/instructions_for_running_evals.md` for
running the promptfoo evaluations.

## Configuration

The multi-agent prototype keeps project settings in
`multi_agentic_system_for_programming/data/project_config.py`. The evaluation
harness documents the model keys, promptfoo configuration, and environment
variables in its running instructions; do not commit API credentials.

## Troubleshooting and FAQ

### What is this repository for?

It contains the research artifacts for a Bachelor's thesis on prompt engineering
for software development. The artifacts are a multi-agent programming prototype
and a prompt-development/evaluation harness.

### Which agents are included?

The prototype defines project manager, coder, tester, and debugger roles in the
`data/` and `scripts/` directories. Their prompts and tool integrations are
part of the thesis artifact rather than a hosted coding service.

### How do I run the prompt evaluation harness?

Install the dependencies described in
`prompt_development_and_testing/evals/instructions_for_running_evals.md`, then
run one of its promptfoo commands from the `evals/` directory.

### Does this repository provide a production coding agent?

No. It documents an experimental thesis system and its evaluation assets.
Follow-up production prompt work lives in the related `programming_prompts`
repository.

### Where is the full thesis?

The full thesis is available through the [Theseus open repository](https://www.theseus.fi/handle/10024/894216), which is the canonical publication record.

## Contributing

Contributions should identify the affected thesis artifact, preserve the
reproducibility instructions, and explain any model or prompt changes. Keep
credentials and generated evaluation data out of commits.

## License

Released under the [MIT License](LICENSE).
