import { useState } from 'react'
import './SplitUpload.css'

function MergeUpload() {
  const [questionsFile, setQuestionsFile] = useState(null)
  const [answersFile, setAnswersFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [downloadUrl, setDownloadUrl] = useState('')

  const handleFileChange = (event, setter) => {
    const selectedFile = event.target.files[0]
    if (selectedFile) {
      setter(selectedFile)
      setError('')
      setDownloadUrl('')
    }
  }

  const handleMerge = async () => {
    if (!questionsFile || !answersFile) {
      setError('Please select both PDF files.')
      return
    }

    setLoading(true)
    setError('')
    setDownloadUrl('')

    const formData = new FormData()
    formData.append('question_file', questionsFile)
    formData.append('answer_file', answersFile)

    try {
      const response = await fetch('https://qa-pdf-splitter.onrender.com/merge', {
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
        Upload two separate PDFs — one with numbered questions, one with numbered answers.
        We'll match them by number and create one combined PDF.
      </p>

      <div className="upload-grid">
        <div>
          <p className="upload-label">Questions PDF</p>
          <div
            className="upload-area"
            onClick={() => document.getElementById('questions-file-input').click()}
          >
            <input
              type="file"
              id="questions-file-input"
              accept=".pdf"
              onChange={(e) => handleFileChange(e, setQuestionsFile)}
              hidden
            />
            <div className="upload-icon">📝</div>
            <p className="upload-text">
              {questionsFile ? questionsFile.name : 'Select questions'}
            </p>
          </div>
        </div>

        <div>
          <p className="upload-label">Answers PDF</p>
          <div
            className="upload-area"
            onClick={() => document.getElementById('answers-file-input').click()}
          >
            <input
              type="file"
              id="answers-file-input"
              accept=".pdf"
              onChange={(e) => handleFileChange(e, setAnswersFile)}
              hidden
            />
            <div className="upload-icon">✅</div>
            <p className="upload-text">
              {answersFile ? answersFile.name : 'Select answers'}
            </p>
          </div>
        </div>
      </div>

      <button
        className="action-button"
        onClick={handleMerge}
        disabled={!questionsFile || !answersFile || loading}
      >
        {loading && <span className="spinner"></span>}
        {loading ? 'Processing...' : '🔗 Merge PDFs'}
      </button>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {downloadUrl && (
        <div className="success-area">
          <p className="success-text">✅ Done! Your combined PDF is ready.</p>
          <a
            href={downloadUrl}
            download="combined_qa.pdf"
            className="download-button"
          >
            📥 Download Combined PDF
          </a>
        </div>
      )}
    </div>
  )
}

export default MergeUpload