import React from 'react'
import './App.css'
import ChatInterface from './components/ChatInterface'
import Header from './components/Header'

/**
 * Main application component.
 */
function App(): React.ReactElement {
  return (
    <div className="app">
      <Header />
      <ChatInterface />
    </div>
  )
}

export default App