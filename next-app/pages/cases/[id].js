import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { getOpinion, getOpinionsByUris } from '../../lib/courtlistener';
import CaseCard from '../../components/CaseCard';

export default function CaseDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [opinion, setOpinion] = useState(null);
  const [cites, setCites] = useState([]);
  const [citedBy, setCitedBy] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;
    async function load() {
      try {
        const data = await getOpinion(id);
        setOpinion(data);
        const citedCases = await getOpinionsByUris(data.cites || []);
        setCites(citedCases);
        const citingCases = await getOpinionsByUris(data.cited_by || []);
        setCitedBy(citingCases);
      } catch (e) {
        setError(e.message);
      }
    }
    load();
  }, [id]);

  if (error) return <p>{error}</p>;
  if (!opinion) return <p>Loading...</p>;

  return (
    <>
      <Head>
        <title>{opinion.case_name}</title>
      </Head>
      <header>
        <h1>{opinion.case_name}</h1>
      </header>
      <main>
        {opinion.citation && (
          <p><strong>Citation:</strong> {opinion.citation.join(', ')}</p>
        )}
        {opinion.date_filed && (
          <p><strong>Date Filed:</strong> {new Date(opinion.date_filed).toLocaleDateString()}</p>
        )}

        <section>
          <h2>Cited Cases</h2>
          <div className="case-grid">
            {cites.map((c) => (
              <CaseCard key={c.id} opinion={c} />
            ))}
            {!cites.length && <p>No cited cases found.</p>}
          </div>
        </section>

        <section>
          <h2>Cited By</h2>
          <div className="case-grid">
            {citedBy.map((c) => (
              <CaseCard key={c.id} opinion={c} />
            ))}
            {!citedBy.length && <p>No citing cases found.</p>}
          </div>
        </section>

        <p>
          <Link href="/">&larr; Back to search</Link>
        </p>
      </main>
    </>
  );
}
