import { useState } from 'react'
import './SplitUpload.css'

function SplitUpload() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [downloadUrl, setDownloadUrl] = useState('')

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError('')
      setDownloadUrl('')
    }
  }

  const handleSplit = async () => {
    if (!file) {
      setError('Please select a PDF file first.')
      return
    }

    setLoading(true)
    setError('')
    setDownloadUrl('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('https://qa-pdf-splitter.onrender.com/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Something went wrong.')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      setDownloadUrl(url)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <p className="card-description">
        Upload a PDF with numbered questions and <strong>Ans:</strong> answers. 
        We'll create two separate PDFs — one with questions only, one with answers only.
      </p>

      <div
        className="upload-area"
        onClick={() => document.getElementById('split-file-input').click()}
      >
        <input
          type="file"
          id="split-file-input"
          accept=".pdf"
          onChange={handleFileChange}
          hidden
        />
        <div className="upload-icon">📄</div>
        <p className="upload-text">
          {file ? file.name : 'Click to select a PDF'}
        </p>
        {file && (
          <p className="file-size">{(file.size / 1024).toFixed(1)} KB</p>
        )}
      </div>

      <button
        className="action-button"
        onClick={handleSplit}
        disabled={!file || loading}
      >
        {loading && <span className="spinner"></span>}
        {loading ? 'Processing...' : '✂️ Split PDF'}
      </button>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {downloadUrl && (
        <div className="success-area">
          <p className="success-text">✅ Done! Your PDFs are ready.</p>
          <a
            href={downloadUrl}
            download="qa_results.zip"
            className="download-button"
          >
            📥 Download Results (ZIP)
          </a>
        </div>
      )}
    </div>
  )
}

export default SplitUpload