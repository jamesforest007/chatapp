import React from 'react';
import './App.css';
import ChatBox from './components/ChatBox';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Chat Box</h1>
      </header>
      <main>
        <ChatBox />
      </main>
    </div>
  );
}

export default App; 