# Prompt Engineering for Software Development

Bachelor's thesis research project exploring **prompt engineering for software
development**: how carefully designed prompts and a **multi-agent LLM system**
(project manager, coder, tester, and debugger agents) can plan, write, test, and
debug code — plus the prompt-development and evaluation harness used to measure
prompt quality.

**Topics:** prompt-engineering · large-language-models · llm-agents ·
multi-agent-systems · ai-coding-assistant · promptfoo · prompt-evaluation ·
software-development · thesis · gpt

## 📄 Thesis

Read the full thesis: **["Prompt engineering for software development"](https://www.theseus.fi/handle/10024/894216)**
(Theseus open repository).

Follow-up work optimizing production coding prompts continues in
[`programming_prompts`](https://github.com/mikaeltorni/programming_prompts).

## What's inside

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

## Getting started

Each subproject has its own `requirements.txt`:

```bash
cd multi_agentic_system_for_programming   # or prompt_development_and_testing/evals
pip install -r requirements.txt
```

See `prompt_development_and_testing/evals/instructions_for_running_evals.md` for
running the promptfoo evaluations.

## License

Released under the [MIT License](LICENSE).
