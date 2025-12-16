import React, { useState, useRef, useEffect } from 'react'
import { apiClient } from '../lib/api'
import './ChatInterface.css'

interface Message {
  id: string
  text: string
  sender: 'user' | 'assistant'
  timestamp: Date
}

/**
 * Clean markdown formatting: remove bold markers and inline backticks
 */
function cleanMarkdown(text: string): string {
  // Remove bold markers (**text** -> text)
  text = text.replace(/\*\*(.+?)\*\*/g, '$1')
  // Remove italic markers (*text* -> text)
  text = text.replace(/\*(.+?)\*/g, '$1')
  // Remove inline backticks (`text` -> text)
  text = text.replace(/`([^`]+)`/g, '$1')
  return text
}

/**
 * Parse and render message content with support for code blocks and formatting.
 */
function MessageRenderer({ text }: { text: string }): React.ReactElement {
  const parts: React.ReactElement[] = []
  const codeBlockRegex = /```(\w*)\n([\s\S]*?)```/g
  let lastIndex = 0
  let match

  while ((match = codeBlockRegex.exec(text)) !== null) {
    // Add text before code block
    if (match.index > lastIndex) {
      const textBefore = cleanMarkdown(text.substring(lastIndex, match.index))
      parts.push(
        <p key={`text-${lastIndex}`} className="message-text">
          {textBefore}
        </p>
      )
    }

    // Add code block
    const language = match[1] || 'plain'
    const code = match[2].trim()
    parts.push(
      <div key={`code-${match.index}`} className="code-block">
        <div className="code-header">
          <span className="code-language">{language}</span>
          <button
            className="copy-button"
            onClick={() => {
              navigator.clipboard.writeText(code)
            }}
            title="Copy code"
          >
            Copy
          </button>
        </div>
        <pre className="code-content">
          <code>{code}</code>
        </pre>
      </div>
    )

    lastIndex = codeBlockRegex.lastIndex
  }

  // Add remaining text
  if (lastIndex < text.length) {
    const remainingText = cleanMarkdown(text.substring(lastIndex))
    parts.push(
      <p key={`text-${lastIndex}`} className="message-text">
        {remainingText}
      </p>
    )
  }

  // If no code blocks found, return cleaned text
  if (parts.length === 0) {
    return <p className="message-text">{cleanMarkdown(text)}</p>
  }

  return <>{parts}</>
}

/**
 * Chat interface component for interacting with the RAG assistant.
 */
function ChatInterface(): React.ReactElement {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [connected, setConnected] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Check backend connection on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await apiClient.getHealth()
        setConnected(true)
        setMessages([
          {
            id: '0',
            text: 'Backend Oracle is online. How can I help you today?',
            sender: 'assistant',
            timestamp: new Date(),
          },
        ])
      } catch (error) {
        setConnected(false)
        setMessages([
          {
            id: '0',
            text: 'Unable to connect to Backend Oracle. Please ensure the backend is running.',
            sender: 'assistant',
            timestamp: new Date(),
          },
        ])
      }
    }

    checkHealth()
  }, [])

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  /**
   * Handle sending a chat message.
   */
  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!input.trim() || loading || !connected) {
      return
    }

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await apiClient.chat(input)
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response,
        sender: 'assistant',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text:
          error instanceof Error
            ? error.message
            : 'An error occurred while processing your request.',
        sender: 'assistant',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-container">
      <div className={`messages ${!connected ? 'disconnected' : ''}`}>
        {messages.map((msg) => (
          <div key={msg.id} className={`message message-${msg.sender}`}>
            <div className="message-content">
              <MessageRenderer text={msg.text} />
            </div>
            <div className="message-time">
              {msg.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message message-assistant">
            <div className="message-content loading">
              <span className="loading-dots">●●●</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            connected ? 'Ask Backend Oracle...' : 'Backend is offline...'
          }
          disabled={loading || !connected}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={loading || !connected || !input.trim()}
          className="send-button"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  )
}

export default ChatInterface