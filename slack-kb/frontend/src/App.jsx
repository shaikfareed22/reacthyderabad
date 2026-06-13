import { useState } from "react";
import axios from "axios";
import "./App.css";

const API = "https://supreme-enigma-jjp6pj7479g3564w-8000.app.github.dev";

export default function App() {
  const [file, setFile] = useState(null);
  const [uploaded, setUploaded] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    await axios.post(`${API}/upload`, formData);
    setUploaded(true);
    setLoading(false);
  };

  const handleAsk = async () => {
    if (!question) return;
    setLoading(true);
    const res = await axios.post(`${API}/ask?question=${encodeURIComponent(question)}`);
    setAnswer(res.data.answer);
    setSources(res.data.sources);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>📚 Intelligent Knowledge Base</h1>

      <div className="card">
        <h2>1. Upload PDF</h2>
        <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Processing..." : "Upload & Process"}
        </button>
        {uploaded && <p className="success">✅ Document indexed!</p>}
      </div>

      <div className="card">
        <h2>2. Ask a Question</h2>
        <input
          type="text"
          placeholder="What is this document about?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={handleAsk} disabled={loading || !uploaded}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {answer && (
        <div className="card">
          <h2>Answer</h2>
          <p>{answer}</p>
          <h3>Sources</h3>
          {sources.map((s, i) => (
            <div key={i} className="source">
              <strong>Page {s.page}</strong>: {s.snippet}...
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
