import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

/**
 * API client for backend communication.
 */
export const apiClient = {
  /**
   * Check backend health status.
   */
  async getHealth(): Promise<{ status: string; service: string }> {
    const response = await axios.get(`${API_URL}/health`)
    return response.data
  },

  /**
   * Send a chat message and get a response.
   */
  async chat(message: string): Promise<string> {
    const response = await axios.post(`${API_URL}/chat`, {
      messages: [{ role: 'user', content: message }],
    })
    
    // Extract the assistant's message from the response
    const assistantMessage = response.data?.message?.content || ''
    return assistantMessage
  },
}
