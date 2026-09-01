import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      setSelectedFile(file);
    }
  };

  const handleAnalyze = () => {
    if (!selectedFile) {
      alert("Please select a contract file first.");
      return;
    }

    alert(`Ready to analyze: ${selectedFile.name}`);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>AI Contract Intelligence</h1>
        <p>Contract Risk Analysis &amp; Intelligence Platform</p>
      </header>

      <main className="main-content">
        <section className="upload-card">
          <h2>Analyze Your Contract</h2>

          <p className="description">
            Upload a contract document to identify clauses, detect potential
            risks, and calculate an overall risk score.
          </p>

          <div className="upload-box">
            <div className="upload-icon">📄</div>

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
                <strong>Selected file:</strong>
                <span>{selectedFile.name}</span>
              </div>
            )}
          </div>

          <button
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={!selectedFile}
          >
            Analyze Contract
          </button>

          <p className="supported">
            Supported formats: PDF, DOCX, TXT
          </p>
        </section>
      </main>

      <footer>
        <p>AI-Powered Contract Intelligence</p>
      </footer>
    </div>
  );
}

export default App;
