import { useState } from 'react';

export default function SearchBar({ onSearch }) {
  const [term, setTerm] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(term);
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Search Supreme Court cases..."
        value={term}
        onChange={(e) => setTerm(e.target.value)}
      />
      <button type="submit">Search</button>
    </form>
  );
}
