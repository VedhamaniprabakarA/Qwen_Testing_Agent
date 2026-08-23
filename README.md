# 🤖 AI Web Testing Agent

An AI-powered web testing automation framework that uses **Qwen3** to generate test cases and **Playwright** automation scripts from a live webpage.

The system inspects a webpage, captures and stores its page snapshot, uses **Qwen3** to generate test cases and Playwright automation code, and finally executes the generated automation against the webpage.

---

## 🚀 Project Overview

Traditional web automation requires testers to manually:

1. Inspect webpage elements
2. Identify locators
3. Write test cases
4. Develop automation scripts
5. Execute the scripts
6. Validate the application

This project automates most of this workflow using an **AI-driven testing pipeline**.

### AI Web Testing Workflow

```text
                 ┌─────────────────────┐
                 │     User Prompt      │
                 │  Webpage / Test Goal │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Playwright        │
                 │   Browser Launch    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Webpage           │
                 │   Inspection        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Page Snapshot      │
                 │  JSON Storage       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Qwen3          │
                 │   Test Generation   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Qwen3          │
                 │ Playwright Script   │
                 │     Generation      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Playwright Executor │
                 │  Run Automation     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Test Results      │
                 │   / Logs / Report   │
                 └─────────────────────┘
```

---

## ✨ Key Features

* 🌐 Automatic webpage inspection
* 🔍 Automatic extraction of webpage elements
* 📸 Page snapshot generation
* 💾 Persistent JSON page snapshots
* 🧠 AI-generated test cases using Qwen3
* 🧠 AI-generated Playwright automation scripts
* 🎭 Playwright browser automation
* ▶️ Automatic execution of generated test scripts
* 🔄 Snapshot-based automation workflow
* 📁 Organized test artifacts and generated files
* 🐍 Python-based implementation

---

## 🛠️ Technologies Used

| Technology     | Purpose                                |
| -------------- | -------------------------------------- |
| **Python**     | Core application development           |
| **Qwen3**      | AI test-case and automation generation |
| **Playwright** | Browser automation                     |
| **JSON**       | Page snapshot storage                  |
| **Ollama**     | Local Qwen3 model execution            |
| **Chromium**   | Browser execution                      |

---

## 🔄 Workflow

The complete execution process is divided into six major stages.

### 1. Inspect Webpage

The agent receives a webpage URL and launches a browser using Playwright.

Example:

```text
URL:
https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
```

The agent opens the webpage and identifies the available interactive elements.

Example output:

```text
[1] Inspecting webpage...

Opening browser...
URL: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

Found 10 elements.
```

---

### 2. Store Page Snapshot

The extracted webpage information is converted into a structured JSON snapshot.

Example:

```text
[2] Storing page snapshot...

Page snapshot saved:
data/page_snapshots/page_xxxxxxxxxxxxxxxx.json
```

The snapshot can contain information such as:

* Element type
* Tag name
* Text
* ID
* Name
* Class
* XPath
* CSS selector
* Placeholder
* Input type
* Accessibility information
* Other useful DOM attributes

This allows the automation generation process to work from a consistent representation of the webpage.

---

### 3. Load Stored Snapshot

The previously generated snapshot is loaded back into the application.

```text
[3] Loading stored page snapshot...

Stored page snapshot loaded.
```

This separates **webpage inspection** from **AI test generation**.

The stored snapshot can also be reused for debugging and future automation generation.

---

### 4. Generate Test Cases with Qwen3

The snapshot information is provided to the Qwen3 model.

```text
[4] Qwen3 generating test cases...
```

Qwen3 analyzes the webpage and generates functional test scenarios.

Example:

```text
Test Case 1:
Verify successful login with valid credentials

Test Case 2:
Verify login failure with invalid credentials

Test Case 3:
Verify validation when username is empty

Test Case 4:
Verify validation when password is empty
```

The generated test cases become the logical foundation for the automation script.

---

### 5. Generate Playwright Automation

Qwen3 converts the generated test cases into executable Python Playwright automation.

```text
[5] Qwen3 generating Playwright automation...
```

The generated automation can include operations such as:

```python
page.goto(url)

page.locator("#username").fill("Admin")
page.locator("#password").fill("admin123")

page.get_by_role("button", name="Login").click()
```

The goal is to allow the AI to determine appropriate locators and automation actions from the captured webpage information.

---

### 6. Execute Playwright Automation

The generated Playwright script is executed automatically.

```text
[6] Executing Playwright automation...
```

The browser is launched and the generated automation interacts with the webpage.

The execution flow is:

```text
Generated Test Case
        ↓
Generated Playwright Code
        ↓
Playwright
        ↓
Browser
        ↓
Web Application
        ↓
Execution Result
```

---

# 📂 Project Structure

A typical project structure looks like:

```text
AI-Web-Testing-Agent/
│
├── app/
│   ├── ...
│
├── data/
│   └── page_snapshots/
│       └── page_xxxxxxxxxxxxxxxx.json
│
├── generated/
│   └── ...
│
├── tests/
│   └── ...
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

> The exact structure may vary depending on the current implementation.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>.git
cd <YOUR_REPOSITORY>
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Playwright Browsers

```bash
playwright install
```

---

# 🧠 Configure Qwen3

This project is designed to work with a locally running Qwen3 model.

If using Ollama, install Ollama and pull the required Qwen3 model.

Example:

```bash
ollama pull qwen3
```

Verify that the model is available:

```bash
ollama list
```

The application should be configured to communicate with the locally running Qwen3 model.

---

# ▶️ Running the Project

Start the application:

```bash
python main.py
```

Example:

```text
============================================================
AI WEB TESTING WORKFLOW
============================================================

[1] Inspecting webpage...

Opening browser...
URL: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

Found 10 elements.

[2] Storing page snapshot...

Page snapshot saved:
data/page_snapshots/page_xxxxxxxxxxxxxxxx.json

[3] Loading stored page snapshot...

Stored page snapshot loaded.

[4] Qwen3 generating test cases...

[5] Qwen3 generating Playwright automation...

[6] Executing Playwright automation...
```

---

# 🧪 Example Test Target

The project can be tested using the OrangeHRM demo application:

```text
https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
```

The agent can inspect the login page and identify elements such as:

```text
Username
Password
Login button
```

It can then generate corresponding test cases and Playwright automation.

---

# 🏗️ Architecture

The project follows an AI-assisted test automation architecture:

```text
                  Web Application
                         │
                         ▼
                ┌─────────────────┐
                │    Playwright   │
                │  Page Inspector │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  DOM / Element  │
                │     Parser      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Page Snapshot   │
                │      JSON       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     Qwen3       │
                │                 │
                │ Test Generation │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     Qwen3       │
                │ Playwright Code │
                │   Generation    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Playwright    │
                │    Executor     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Test Execution  │
                │     Result      │
                └─────────────────┘
```

---

# 🔐 Page Snapshot Approach

Instead of continuously asking the AI to inspect the live webpage, the application captures the relevant webpage information into a structured snapshot.

For example:

```json
{
    "url": "https://example.com/login",
    "elements": [
        {
            "tag": "input",
            "type": "text",
            "id": "username",
            "name": "username",
            "placeholder": "Username"
        },
        {
            "tag": "input",
            "type": "password",
            "id": "password",
            "name": "password",
            "placeholder": "Password"
        },
        {
            "tag": "button",
            "text": "Login"
        }
    ]
}
```

This approach provides several advantages:

* Reduces repeated webpage inspection
* Gives the AI structured input
* Makes debugging easier
* Preserves webpage information
* Separates inspection from test generation
* Makes the automation pipeline more deterministic

---

# 🎯 Project Goals

The primary goal of this project is to build an **AI-driven software testing agent** capable of transforming a webpage and testing requirement into executable browser automation.

### Current Pipeline

```text
Webpage
   ↓
Inspection
   ↓
Snapshot
   ↓
Qwen3
   ↓
Test Cases
   ↓
Qwen3
   ↓
Playwright Script
   ↓
Execution
```

### Future Vision

```text
Natural Language Requirement
             ↓
          AI Agent
             ↓
       Webpage Analysis
             ↓
      Test Case Generation
             ↓
     Locator Identification
             ↓
    Playwright Code Generation
             ↓
       Test Execution
             ↓
      Result Verification
             ↓
        Test Report
```

---

# 🔮 Future Enhancements

Planned improvements include:

* [ ] Automatic test result validation
* [ ] Automatic failure analysis
* [ ] Screenshot capture on failure
* [ ] HTML test reports
* [ ] Video recording of test execution
* [ ] Multiple browser support
* [ ] Login/session handling
* [ ] Dynamic locator recovery
* [ ] Self-healing Playwright locators
* [ ] Test case prioritization
* [ ] Regression test generation
* [ ] API testing integration
* [ ] CI/CD integration
* [ ] GitHub Actions integration
* [ ] Test execution history
* [ ] AI-based failure explanation
* [ ] Automatic test report generation

---

# 💡 Why This Project?

Modern software applications require large amounts of repetitive testing and automation development.

This project explores how **Large Language Models + Browser Automation** can reduce the manual effort required to create functional UI automation.

Instead of manually converting:

```text
Requirement → Test Case → Locator → Automation Code
```

the system aims to automate the workflow:

```text
Requirement
     ↓
    AI
     ↓
Test Cases
     ↓
Playwright Code
     ↓
Execution
```

---

# 🧰 Development Stack

```text
Language       : Python
AI Model       : Qwen3
LLM Runtime    : Ollama
Automation     : Playwright
Browser        : Chromium
Data Format    : JSON
Environment    : Python Virtual Environment
```

---

# 📌 Disclaimer

This project is intended for **software testing, automation research, and development purposes**.

When testing real applications, ensure that you have appropriate authorization to access and automate the target system.

---

# 👨‍💻 Author

**Vedhamani Prabakar**

Python Developer | AI/ML Enthusiast | Test Automation
