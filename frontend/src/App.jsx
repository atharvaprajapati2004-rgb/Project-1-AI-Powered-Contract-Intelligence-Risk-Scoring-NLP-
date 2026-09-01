import { useState } from "react";
import axios from "axios";
import "./App.css";


function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");


  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);
    setResult(null);
    setError("");
  };


  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError("Please select a contract file first.");
      return;
    }

    setLoading(true);
    setResult(null);
    setError("");

    const formData = new FormData();

    formData.append("file", selectedFile);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/analyze-file",
        formData
      );

      setResult(response.data);
    } catch (err) {
      if (err.response) {
        setError(
          err.response.data.detail ||
          "The server could not analyze the contract."
        );
      } else {
        setError(
          "Unable to connect to the backend. Make sure FastAPI is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="app">

      <header className="header">
        <h1>AI Contract Intelligence</h1>
        <p>
          Contract Risk Analysis &amp; Intelligence Platform
        </p>
      </header>


      <main className="main-content">

        <section className="upload-card">

          <h2>Analyze Your Contract</h2>

          <p className="description">
            Upload a contract document to identify clauses,
            detect potential risks, and calculate an overall
            risk score.
          </p>


          <div className="upload-box">

            <div className="upload-icon">
              📄
            </div>

            <h3>Upload Contract</h3>

            <p>
              Select a PDF, DOCX, or TXT contract file
            </p>


            <label className="file-button">

              Choose Contract

              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileChange}
              />

            </label>


            {selectedFile && (
              <div className="selected-file">

                <strong>
                  Selected file:
                </strong>

                <span>
                  {selectedFile.name}
                </span>

              </div>
            )}

          </div>


          <button
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={!selectedFile || loading}
          >

            {loading
              ? "Analyzing Contract..."
              : "Analyze Contract"}

          </button>


          {error && (
            <div className="error-message">
              {error}
            </div>
          )}


          {result && (
            <div className="result-summary">

              <h3>
                Analysis Completed
              </h3>

              <p>
                <strong>File:</strong>{" "}
                {result.filename}
              </p>

              <p>
                <strong>Risk Score:</strong>{" "}
                {result.analysis.risk_score}
              </p>

              <p>
                <strong>Risk Level:</strong>{" "}
                {result.analysis.risk_level}
              </p>

              <p>
                <strong>Risks Found:</strong>{" "}
                {result.analysis.risk_count}
              </p>

            </div>
          )}


          <p className="supported">
            Supported formats: PDF, DOCX, TXT
          </p>

        </section>

      </main>


      <footer>
        <p>
          AI-Powered Contract Intelligence
        </p>
      </footer>

    </div>
  );
}


export default App;
