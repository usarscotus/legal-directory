import { useState } from 'react';
import Head from 'next/head';
import SearchBar from '../components/SearchBar';
import CaseCard from '../components/CaseCard';
import CaseDetail from '../components/CaseDetail';
import { searchOpinions, getOpinion, getOpinionsByUris } from '../lib/courtlistener';


export default function Home() {
  const [cases, setCases] = useState([]);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(null);
  const [cites, setCites] = useState([]);
  const [citedBy, setCitedBy] = useState([]);

  const handleSearch = async (term) => {
    setError(null);
    setSelected(null);
    try {
      const results = await searchOpinions(term);
      setCases(results);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleSelect = async (id) => {
    setError(null);
    try {
      const data = await getOpinion(id);
      setSelected(data);
      const [citedCases, citingCases] = await Promise.all([
        getOpinionsByUris(data.cites || []),
        getOpinionsByUris(data.cited_by || [])
      ]);
      setCites(citedCases);
      setCitedBy(citingCases);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleBack = () => {
    setSelected(null);
    setCites([]);
    setCitedBy([]);
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
            <CaseCard key={opinion.id} opinion={opinion} onSelect={handleSelect} />
          ))}
        </div>
        {selected && (
          <CaseDetail
            opinion={selected}
            cites={cites}
            citedBy={citedBy}
            onBack={handleBack}
            onSelect={handleSelect}
          />
        )}
      </main>
    </>
  );
}
