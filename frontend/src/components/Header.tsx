import React from 'react'
import './Header.css'

/**
 * Header component displaying application title and status.
 */
function Header(): React.ReactElement {
  return (
    <header className="header">
      <div className="header-container">
        <h1>Backend Oracle</h1>
        <p>RAG-powered coding assistant for backend developers</p>
      </div>
    </header>
  )
}

export default Header