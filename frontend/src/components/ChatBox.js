import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { toast } from 'react-toastify';
import { generateCode, chatWithBot, explainCode, improveCode } from '../services/api';

function ChatBox({ 
  addMessage, 
  setCurrentCode, 
  loading, 
  setLoading, 
  activeMode,
  chatHistory,
  setChatHistory,
  selectedLanguage 
}) {
  const [input, setInput] = useState('');
  const [codeInput, setCodeInput] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    adjustTextareaHeight();
  }, [input, codeInput]);

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const currentInput = activeMode === 'explain' || activeMode === 'improve' 
      ? codeInput.trim() 
      : input.trim();

    if (!currentInput || loading) return;

    setLoading(true);

    try {
      let result;
      
      switch (activeMode) {
        case 'generate':
          addMessage({ role: 'user', content: input, type: 'prompt' });
          result = await generateCode(input, selectedLanguage);
          addMessage({ role: 'assistant', content: result.code, type: 'code', language: result.language });
          setCurrentCode(result.code);
          toast.success(`Code generated in ${result.execution_time}s!`);
          break;

        case 'chat':
          addMessage({ role: 'user', content: input, type: 'message' });
          result = await chatWithBot(input, chatHistory, selectedLanguage);
          addMessage({ role: 'assistant', content: result.response, type: 'message' });
          setChatHistory(result.history);
          toast.success('Response received!');
          break;

        case 'explain':
          addMessage({ role: 'user', content: 'Explain this code', type: 'prompt' });
          addMessage({ role: 'user', content: codeInput, type: 'code' });
          result = await explainCode(codeInput, selectedLanguage);
          addMessage({ role: 'assistant', content: result.explanation, type: 'explanation' });
          toast.success('Code explained!');
          break;

        case 'improve':
          addMessage({ role: 'user', content: 'Improve this code', type: 'prompt' });
          addMessage({ role: 'user', content: codeInput, type: 'code' });
          result = await improveCode(codeInput, selectedLanguage);
          addMessage({ role: 'assistant', content: result.improved_code, type: 'code' });
          addMessage({ role: 'assistant', content: result.suggestions, type: 'explanation' });
          setCurrentCode(result.improved_code);
          toast.success('Code improved!');
          break;

        default:
          toast.error('Invalid mode selected');
      }

      setInput('');
      setCodeInput('');
    } catch (error) {
      toast.error(error.message || 'Something went wrong');
      addMessage({ 
        role: 'assistant', 
        content: `Error: ${error.message}`, 
        type: 'error' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const placeholderText = {
    generate: 'Describe the code you want to generate... (e.g., "Create a React component for a todo list")',
    chat: 'Ask me anything about programming...',
    explain: 'Paste the code you want explained...',
    improve: 'Paste the code you want to improve...'
  };

  const isCodeMode = activeMode === 'explain' || activeMode === 'improve';

  return (
    <motion.div 
      className="chat-box"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.2 }}
    >
      <form onSubmit={handleSubmit}>
        <div className="input-container">
          <textarea
            ref={textareaRef}
            value={isCodeMode ? codeInput : input}
            onChange={(e) => isCodeMode ? setCodeInput(e.target.value) : setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholderText[activeMode]}
            disabled={loading}
            className={`chat-input ${isCodeMode ? 'code-input' : ''}`}
            rows="1"
          />
          
          <motion.button
            type="submit"
            className="send-button"
            disabled={loading || (isCodeMode ? !codeInput.trim() : !input.trim())}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {loading ? (
              <div className="spinner"></div>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            )}
          </motion.button>
        </div>
        
        <div className="input-hints">
          <span className="hint">
            <kbd>Enter</kbd> to send
          </span>
          <span className="hint">
            <kbd>Shift</kbd> + <kbd>Enter</kbd> for new line
          </span>
        </div>
      </form>
    </motion.div>
  );
}

export default ChatBox;
