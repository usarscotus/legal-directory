import { useState } from 'react';
import Head from 'next/head';
import SearchBar from '../components/SearchBar';
import CaseCard from '../components/CaseCard';
import { searchOpinions } from '../lib/courtlistener';

export default function Home() {
  const [cases, setCases] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async (term) => {
    setError(null);
    try {
      const results = await searchOpinions(term);
      setCases(results);
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <>
      <Head>
        <title>Supreme Court Case Search</title>
      </Head>
      <header>
        <h1>Supreme Court Case Search</h1>
      </header>
      <main>
        <SearchBar onSearch={handleSearch} />
        {error && <p>{error}</p>}
        <div className="case-grid">
          {cases.map((opinion) => (
            <CaseCard key={opinion.id} opinion={opinion} />
          ))}
        </div>
      </main>
    </>
  );
}
