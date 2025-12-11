'use client'

import { useState, useRef } from 'react'
import axios from 'axios'

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [result, setResult] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

  const handleFileSelect = (file: File) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      setError(null)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    } else {
      setError('Please select a valid image file')
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) {
      handleFileSelect(file)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFileSelect(file)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await axios.post(
        `${API_URL}/api/personalize`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          responseType: 'blob',
        }
      )

      const imageUrl = URL.createObjectURL(response.data)
      setResult(imageUrl)
    } catch (err: any) {
      setError(
        err.response?.data?.detail || err.message || 'Failed to process image'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (result) {
      const link = document.createElement('a')
      link.href = result
      link.download = 'personalized-illustration.png'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  return (
    <div className="container">
      <h1 className="title">🎨 Illustration Personalizer</h1>
      
      <div className="card">
        <div
          className={`upload-area ${isDragging ? 'dragover' : ''}`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="upload-icon">📸</div>
          <div className="upload-text">
            {selectedFile ? selectedFile.name : 'Click or drag to upload a photo'}
          </div>
          <div className="upload-hint">
            Supports JPG, PNG, and other image formats
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileInputChange}
            className="file-input"
          />
        </div>

        {error && <div className="error">❌ {error}</div>}

        {preview && (
          <div className="preview-section">
            <h2 className="preview-title">Preview</h2>
            <div className="preview-grid">
              <div className="preview-item">
                <div className="preview-label">Original Photo</div>
                <img
                  src={preview}
                  alt="Preview"
                  className="preview-image"
                />
              </div>
              {result && (
                <div className="preview-item">
                  <div className="preview-label">Personalized Illustration</div>
                  <img
                    src={result}
                    alt="Result"
                    className="preview-image"
                  />
                </div>
              )}
            </div>
          </div>
        )}

        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button
            className="button"
            onClick={handleUpload}
            disabled={!selectedFile || loading}
          >
            {loading ? (
              <>
                <span className="loading"></span>
                Processing...
              </>
            ) : (
              '✨ Personalize Illustration'
            )}
          </button>

          {result && (
            <button
              className="button"
              onClick={handleDownload}
              style={{ marginLeft: '1rem', background: '#28a745' }}
            >
              💾 Download Result
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

