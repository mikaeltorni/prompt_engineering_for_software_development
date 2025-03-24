To run this script, you need to have the following:

- Conda (Miniconda or Anaconda) installed on your system
- Python 3.12.4

### Setting up the environment

1. Install Conda:
   - Download and install Miniconda from: https://docs.conda.io/en/latest/miniconda.html
   - Or download and install Anaconda from: https://www.anaconda.com/products/distribution

2. Create a new Conda environment with Python 3.12.4:
   ```bash
   conda create -n masfp python=3.12.4
   ```

3. Activate the environment:
   ```bash
   conda activate masfp
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Setting Up Environment Variables for API Keys on Linux

To run this project, you need to set `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` as environment variables.

### User-Specific Setup

1. Open your shell's config file (e.g., `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc`):

   ```bash
   nano ~/.bashrc
   ```

2. Add the following lines at the end:

   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export ANTHROPIC_API_KEY="your_anthropic_api_key"
   ```

3. Save and apply the changes:

   ```bash
   source ~/.bashrc
   ```