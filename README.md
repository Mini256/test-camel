# CamelAI + TiDB Demo

### 1. Install dependencies

**Temporary**: Because PR has not been merged yet, you need to clone PR locally.

```sh
# Clone github repo
git clone https://github.com/Mini256/camel.git

# Change directory into project directory
cd camel

# Checkout to the development branch
git checkout add-tidb-vector-storage

# Install uv if you don't have it already
pip install uv

# Create a virtual environment and install dependencies
# We support using Python 3.10, 3.11, 3.12
uv venv .venv --python=3.10

# Activate the virtual environment
# For macOS/Linux
source .venv/bin/activate
# For Windows
.venv\Scripts\activate

# Install CAMEL with all dependencies
uv pip install -e ".[all, dev, docs]"
```

Go back test-camel:

```bash
cd ../test-camel
uv sync
```

### 2. Prepare a TiDB cluster

#### 2.1 (Option1) TiDB on local

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup playground v8.5.0 --tag local-test
```

#### 2.1 (Option1) TiDB Cloud Serverless

1. Go to [TiDB Cloud](https://tidbcloud.com/console/clusters)
2. Create a serverless cluster in a few seconds

### 3. Setup environment variable

Fill in the connection information of TiDB cluster and the OpenAI API Key into **.env** file:

```bash
cp .env.example .env
vi .env
```

### 4. Run the script

```bash
python main.py
```

Test:

Provide some information with the AI:

```bash
(.venv) ~/Projects/test-camel git:[main]
python main.py
Chat with AI (type 'exit' to quit)
You: I am Mini256
AI: Hello, Mini256! It's great to meet you. What would you like to talk about today?
You: Today is 2025-01-01, I was born in 2000-01-01.
AI: That's interesting! So, you just turned 25 years old today. How does it feel to reach this milestone?
You: exit
Goodbye!
```

Open another session:

```bash
(.venv) ~/Projects/test-camel git:[main]
python main.py
Chat with AI (type 'exit' to quit)
You: Who am I and how old am I?
AI: You are Mini256, and you just turned 25 years old today! How does it feel to celebrate this milestone?
You: exit
Goodbye!
```
