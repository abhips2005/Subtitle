import React, { useState } from 'react';
import SubtitleGenerator from './components/SubtitleGenerator';
import Dashboard from './components/Dashboard';
import { AuthProvider } from './contexts/AuthContext';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState<'generator' | 'dashboard'>('generator');

  return (
    <AuthProvider>
      <div className="App">
        {currentView === 'generator' ? (
          <SubtitleGenerator onNavigateToDashboard={() => setCurrentView('dashboard')} />
        ) : (
          <Dashboard onNavigateToGenerator={() => setCurrentView('generator')} />
        )}
      </div>
    </AuthProvider>
  );
}

export default App;
