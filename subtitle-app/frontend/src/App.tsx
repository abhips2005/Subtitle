import React from 'react';
import SubtitleGenerator from './components/SubtitleGenerator';
import { AuthProvider } from './contexts/AuthContext';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <SubtitleGenerator />
      </div>
    </AuthProvider>
  );
}

export default App;
