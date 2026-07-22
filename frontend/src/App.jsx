import { useState } from 'react'
import SplitUpload from './components/SplitUpload'
import MergeUpload from './components/MergeUpload'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('split')

  return (
    <div className='app'>
      <header className='header'>
      <h1 className='title'>
        <span className="title-icon">📄</span> Q&A PDF Splitter
      </h1>
      <p className='subtitle'>
        Split or merge your question-and-answer PDFs in seconds
      </p>
      </header>

      <div className='tabs'> 
        <button
        className={`tab ${activeTab === 'split' ? 'active' : ''}`}
        onClick={() => setActiveTab('split')}
        > 
         ✂️ Split PDF
        </button>

       <button
          className={`tab ${activeTab === 'merge' ? 'active' : ''}`}
          onClick={() => setActiveTab('merge')}
        >
          🔗 Merge PDFs
        </button>
      </div>

      <main className="content">
        {activeTab === 'split' ? <SplitUpload /> : <MergeUpload />}
      </main>

      <footer className="footer">
        © 2026 w/AD
      </footer>
    </div>
  )
}

export default App