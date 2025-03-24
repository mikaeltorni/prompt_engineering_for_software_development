Before starting, set up the OPENAI_API_KEY and ANTHROPIC_API_KEY environment variables if not done already.

# Linux install instructions

## Remove old Node.js version (if it exists)
```bash
sudo apt-get remove nodejs
```

Note that using earlier versions of Node.js might cause errors with promptfoo.

## Use Node Version Manager (nvm) to install the latest Node.js
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
```

not tested for a while, and might vary depending on the distros too.

# Windows install instructions
Download Node.js from https://nodejs.org/en/download

# Change the directory this folder where these instructions are located
```bash
cd [PATH_TO_THE_PROJECT_LOCATION]\prompt_development_and_testing\evals
```	

# Run the evaluations
BEWARE, PARAMETER --repeat 10 WILL USE ATLEAST +150K TOTAL TOKENS (~2-5$ per run, without - with the coder system prompt) Optionally, you can reduce the --repeat value.
Additionally, all of the eval data are available in the eval_data folder available to be imported to the Promptfoo UI.

With the coder system prompt:   
```bash
npx promptfoo@0.107.1 eval -c eval_configs/coding/coder_regular_eval.yaml --max-concurrency 1 --repeat 10 --delay 10000
```

Without the coder system prompt:
```bash
npx promptfoo@0.107.1 eval -c eval_configs/coding/coding_tasks_eval_without_coder_prompt.yaml --max-concurrency 1 --repeat 10 --delay 10000
```

Project manager eval (a lot cheaper eval to run because using gpt-4o-mini):
```bash
npx promptfoo@0.107.1 eval -c eval_configs/project_manager/project_manager_eval.yaml --max-concurrency 10 --repeat 100
```

You might increase the concurrency if you are not running in to rate limit errors.
However, I ran to rate limits even with concurrency 1 on the lowest Anthropic tier with 8000 output tokens per minute, so delay was added to the command.

# To view the results: open a new terminal and run:
```bash
npx promptfoo@0.107.1 view -y
```
(advised to open a new terminal for this, since it's a server that needs to be running all the time)

# Validating the evals / getting code out of them
Change the directory to:
```bash
cd [PATH_TO_THE_PROJECT_LOCATION]\prompt_development_and_testing\evals\eval_data\completed_tests_and_validation
```

## Project Manager Tests and XML validation

Extract from the existing, premade tests for the Project Manager:
```bash
python test_output_extraction.py project_manager_tests.json --output-dir new_extracted_tests/project_manager_tests --language xml --tests-per-category 100 
```
(tests per category 100 is used here because there are 1000 tests in the JSON file)

Parse the project manager XML tests to make sure that there aren't any inconsistencies with the XML output (otherwise the agent system would fail).

From the existing tests in the folder:
```bash
python parse_xml_files_to_the_task_format.py -d extracted_tests/project_manager_tests -o new_extracted_tests_results.txt
```

From your extracted test results:
```bash
python parse_xml_files_to_the_task_format.py -d new_extracted_tests/project_manager_tests -o your_extracted_tests_results.txt
```

You can use the tests you ran yourself by exporting the JSON file out of promptfoo too:
```bash
python test_output_extraction.py your_project_manager_tests.json --output-dir your_extracted_tests/project_manager_tests --language xml --tests-per-category [INSERT NUMBER OF TOTAL TEST RUNS IN THAT JSON FILE DIVIDED BY 10, ASSUMING THAT THERE WERE 10 DIFFERENT USER PROMPTS]
```

I've tampered with the following files to confirm that the XML validator works:
For example: contact_book_1.xml (<project_plan> -> <projet_plan>)
and additionally other files: csv_file_analysis_1.xml, quiz_game_1.xml, temperature_converter_1.xml with various changes that will cause failure upon running the script.

```bash
python parse_xml_files_to_the_task_format.py -d failing_xml_tests -o new_extracted_failed_tests_results.txt
```
or enter your own tests there

Otherwise just validate the existing working (or new tests that you just created):
```bash
python parse_xml_files_to_the_task_format.py -d extracted_tests -o new_extracted_tests_results.txt
```

# Extracing Coder Tests
```bash
python test_output_extraction.py coder_system_prompt_tests.json --output-dir new_extracted_tests/coder_system_prompt_tests --language python --tests-per-category 10
```
100/100 succeed and the code extracts successfully. On rare occasions the LLM might write ```python to for example, quiz questions, and it might mess up this script (since there are two instances in one test). To fix this, a solution was added to only take the first backtick block out of a single test.

```bash
python test_output_extraction.py coding_tests_without_system_prompt.json --output-dir new_extracted_tests/coding_tests_without_system_prompt --language python --tests-per-category 10
```
Fails as expected, the LLM format is not consistent without the system prompt so the code can't be extracted out of the tests, but most of the code is available (in extracted_tests folder, or do it with that command) to be compared for the effect of the coding system prompt.