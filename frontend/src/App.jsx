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

  const getRiskClass = (level) => {
    if (!level) {
      return "";
    }

    return level.toLowerCase();
  };

  const getFileSize = (size) => {
    if (!size) return "";

    if (size < 1024) {
      return `${size} B`;
    }

    if (size < 1024 * 1024) {
      return `${(size / 1024).toFixed(1)} KB`;
    }

    return `${(size / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="brand">
            <div className="brand-icon">AI</div>

            <div>
              <h1>Contract Intelligence</h1>
              <p>AI-Powered Contract Risk Analysis</p>
            </div>
          </div>

          <div className="status-badge">
            <span className="status-dot"></span>
            System Online
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="main-content">
        <div className="page-container">
          {/* Hero */}
          <section className="hero-section">
            <div>
              <span className="eyebrow">CONTRACT ANALYSIS PLATFORM</span>

              <h2>
                Understand your contracts
                <span> faster and smarter.</span>
              </h2>

              <p>
                Upload a contract and let our AI-powered analysis pipeline
                identify clauses, detect potential risks, and calculate an
                overall risk score.
              </p>
            </div>
          </section>

          {/* Upload Section */}
          <section className="upload-card">
            <div className="section-heading">
              <div className="section-icon">↑</div>

              <div>
                <h3>Upload Contract</h3>
                <p>Choose a document to begin analysis</p>
              </div>
            </div>

            <div className="upload-box">
              <div className="upload-large-icon">📄</div>

              <h3>Drop your contract here</h3>

              <p>
                Supported formats: <strong>PDF, DOCX, TXT</strong>
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
                  <div className="file-info">
                    <div className="file-icon">📄</div>

                    <div>
                      <strong>{selectedFile.name}</strong>

                      <span>
                        {getFileSize(selectedFile.size)} •{" "}
                        {selectedFile.type || "Contract document"}
                      </span>
                    </div>
                  </div>

                  <span className="file-ready">Ready</span>
                </div>
              )}
            </div>

            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={!selectedFile || loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing Contract...
                </>
              ) : (
                <>
                  Analyze Contract
                  <span className="button-arrow">→</span>
                </>
              )}
            </button>

            {error && (
              <div className="error-message">
                <span>⚠</span>
                {error}
              </div>
            )}
          </section>

          {/* Results */}
          {result && result.analysis && (
            <section className="dashboard">
              <div className="dashboard-header">
                <div>
                  <span className="eyebrow">ANALYSIS COMPLETE</span>

                  <h2>Contract Analysis Results</h2>

                  <p>
                    Analyzed document: <strong>{result.filename}</strong>
                  </p>
                </div>

                <div className="analysis-complete">
                  ✓ Analysis Complete
                </div>
              </div>

              {/* Summary Cards */}
              <div className="summary-grid">
                <div className="summary-card score-card">
                  <div className="card-top">
                    <span>Risk Score</span>
                    <span className="card-icon">◎</span>
                  </div>

                  <strong className="risk-score">
                    {result.analysis.risk_score}
                  </strong>

                  <span className="card-description">
                    Overall contract risk
                  </span>
                </div>

                <div
                  className={`summary-card level-card ${getRiskClass(
                    result.analysis.risk_level
                  )}`}
                >
                  <div className="card-top">
                    <span>Risk Level</span>
                    <span className="card-icon">●</span>
                  </div>

                  <strong className="risk-level">
                    {result.analysis.risk_level}
                  </strong>

                  <span className="card-description">
                    Current risk classification
                  </span>
                </div>

                <div className="summary-card">
                  <div className="card-top">
                    <span>Risks Found</span>
                    <span className="card-icon">!</span>
                  </div>

                  <strong>
                    {result.analysis.risk_count}
                  </strong>

                  <span className="card-description">
                    Potential risk indicators
                  </span>
                </div>

                <div className="summary-card">
                  <div className="card-top">
                    <span>Clauses</span>
                    <span className="card-icon">§</span>
                  </div>

                  <strong>
                    {result.analysis.clauses?.length || 0}
                  </strong>

                  <span className="card-description">
                    Contract clauses detected
                  </span>
                </div>
              </div>

              {/* Risk Section */}
              <section className="result-section">
                <div className="result-heading">
                  <div>
                    <h3>Detected Risks</h3>
                    <p>
                      Potential issues identified in the contract
                    </p>
                  </div>

                  <span className="count-badge">
                    {result.analysis.risk_count} detected
                  </span>
                </div>

                {result.analysis.risks?.length > 0 ? (
                  <div className="risk-list">
                    {result.analysis.risks.map((risk, index) => (
                      <div className="risk-item" key={index}>
                        <div className="risk-main">
                          <div className="risk-number">
                            {index + 1}
                          </div>

                          <div>
                            <strong>
                              {risk.risk_type || "Potential Risk"}
                            </strong>

                            {risk.matched_text && (
                              <p>
                                "{risk.matched_text}"
                              </p>
                            )}

                            {risk.description && (
                              <small>{risk.description}</small>
                            )}
                          </div>
                        </div>

                        <span
                          className={`severity ${getRiskClass(
                            risk.severity
                          )}`}
                        >
                          {risk.severity}
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="empty-message">
                    <span>✓</span>
                    No potential risks were detected.
                  </div>
                )}
              </section>

              {/* Clause Section */}
              <section className="result-section">
                <div className="result-heading">
                  <div>
                    <h3>Detected Clauses</h3>
                    <p>
                      Contract sections identified by the analysis pipeline
                    </p>
                  </div>

                  <span className="count-badge">
                    {result.analysis.clauses?.length || 0} clauses
                  </span>
                </div>

                {result.analysis.clauses?.length > 0 ? (
                  <div className="clause-list">
                    {result.analysis.clauses.map((clause, index) => (
                      <div className="clause-item" key={index}>
                        <span className="clause-number">
                          {clause.clause_id || index + 1}
                        </span>

                        <div>
                          <strong>
                            {clause.clause_type || "Contract Clause"}
                          </strong>

                          {clause.text && (
                            <p>{clause.text}</p>
                          )}
                        </div>

                        <span className="clause-arrow">→</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="empty-message">
                    No clauses were detected.
                  </div>
                )}
              </section>
            </section>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer>
        <div>
          <strong>AI Contract Intelligence</strong>
          <span>•</span>
          <span>Contract Risk Analysis Platform</span>
        </div>

        <p>Powered by NLP &amp; Machine Learning</p>
      </footer>
    </div>
  );
}

export default App;