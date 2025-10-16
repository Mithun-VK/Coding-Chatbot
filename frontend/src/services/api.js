import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 60000, // 60 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      // Server responded with error
      const message = error.response.data?.error || 'An error occurred';
      throw new Error(message);
    } else if (error.request) {
      // No response received
      throw new Error('No response from server. Please check your connection.');
    } else {
      // Error setting up request
      throw new Error(error.message);
    }
  }
);

/**
 * Generate code based on prompt
 */
export async function generateCode(prompt, language = 'auto', temperature = 0.2) {
  try {
    const response = await apiClient.post('/generate', {
      prompt,
      language,
      temperature,
    });
    return response;
  } catch (error) {
    throw error;
  }
}

/**
 * Chat with the bot (multi-turn conversation)
 */
export async function chatWithBot(message, history = [], language = 'auto') {
  try {
    const response = await apiClient.post('/chat', {
      message,
      history,
      language,
    });
    return response;
  } catch (error) {
    throw error;
  }
}

/**
 * Explain existing code
 */
export async function explainCode(code, language = 'auto') {
  try {
    const response = await apiClient.post('/explain', {
      code,
      language,
    });
    return response;
  } catch (error) {
    throw error;
  }
}

/**
 * Improve existing code
 */
export async function improveCode(code, language = 'auto', focus = 'general') {
  try {
    const response = await apiClient.post('/improve', {
      code,
      language,
      focus,
    });
    return response;
  } catch (error) {
    throw error;
  }
}

/**
 * Get available models
 */
export async function getAvailableModels() {
  try {
    const response = await apiClient.get('/models');
    return response.models;
  } catch (error) {
    throw error;
  }
}

export default {
  generateCode,
  chatWithBot,
  explainCode,
  improveCode,
  getAvailableModels,
};
