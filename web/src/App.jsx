import { useState } from 'react';
import ForceGraph from './ForceGraph';
import './App.css';

function App() {
  const [caseId, setCaseId] = useState(1);
  const [input, setInput] = useState('1');

  const handleSubmit = (e) => {
    e.preventDefault();
    const id = parseInt(input, 10);
    if (!isNaN(id)) setCaseId(id);
  };

  return (
    <div>
      <h1>Citation Graph</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Case ID:
          <input value={input} onChange={(e) => setInput(e.target.value)} />
        </label>
        <button type="submit">Load</button>
      </form>
      <ForceGraph caseId={caseId} onSelectNode={(id) => setCaseId(Number(id))} />
    </div>
  );
}

export default App;
