# NexusAI: Advanced Agentic Chatbot

NexusAI is a powerful, production-ready AI Chatbot platform built with **Streamlit** and the **Groq Llama 3** engine. It features 
autonomous tool execution, document parsing, and vision AI capabilities.

---

## 🚀 Key Features

*   **Agentic Intelligence**: NexusAI autonomously decides when to use tools (Search, Math, Code) to answer complex queries.
*   **Real-Time Knowledge**: Integrated **Web Search** (Tavily/Google) providing up-to-the-minute info for April 2026.
*   **Multimodal Input**:
    *   **PDF Summarization**: Upload PDFs to extract context and summarize large documents.
    *   **Image Vision**: Leverages `llama-3.2- vision` to "see" and describe uploaded images.
*   **Python Sandbox**: Securely execute and test Python code within the chat.
*   **Role Personas**: Switch between specialized roles like *Data Scientist*, *Python Tutor*, or *General Assistant*.
*   **Local Fine-tuning**: Includes a dedicated script to train your own DialoGPT model.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here  # Optional for enhanced web search
```
*   **Get Groq Key**: [console.groq.com](https://console.groq.com/)
*   **Get Tavily Key**: [tavily.com](https://tavily.com/)

---

## 📽️ How to Run

To launch the primary chatbot interface:
```bash
streamlit run app.py
```
After running, the UI will be available at `http://localhost:8501`.

---

## 🧠 How to Train (Fine-tuning)

You can customize the model's personality using the local training script:

1.  Open `train.py`.
2.  Modify the `data` dictionary with your desired conversational examples.
3.  Run the training:
    ```bash
    python train.py
    ```
4.  The fine-tuned model will be saved to the `./custom_model` folder.
5.  In the Streamlit app, select **"Custom Transformer (Local)"** as the engine to use your trained model.

---

## 📂 Project Structure

*   `app.py`: Main Streamlit application and Agent logic.
*   `tools.py`: Collection of 7+ Agentic tools (Weather, Search, Code, etc.).
*   `train.py`: Local model fine-tuning engine using HuggingFace Transformers.
*   `requirements.txt`: Full list of necessary Python libraries.
*   `.env`: API security configuration.

---

## 🛡️ Security Note
The **Code Executor** tool runs Python in a subprocess. Use with caution in production environments.
