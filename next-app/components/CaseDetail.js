import CaseCard from './CaseCard';

export default function CaseDetail({ opinion, cites, citedBy, onBack, onSelect }) {
  return (
    <section>
      <button onClick={onBack}>Back to results</button>
      <h2>{opinion.case_name}</h2>
      {opinion.citation && (
        <p><strong>Citation:</strong> {opinion.citation.join(', ')}</p>
      )}
      {opinion.date_filed && (
        <p><strong>Date Filed:</strong> {new Date(opinion.date_filed).toLocaleDateString()}</p>
      )}

      <div>
        <h3>Cited Cases</h3>
        <div className="case-grid">
          {cites.map((c) => (
            <CaseCard key={c.id} opinion={c} onSelect={onSelect} />
          ))}
          {!cites.length && <p>No cited cases found.</p>}
        </div>
      </div>

      <div>
        <h3>Cited By</h3>
        <div className="case-grid">
          {citedBy.map((c) => (
            <CaseCard key={c.id} opinion={c} onSelect={onSelect} />
          ))}
          {!citedBy.length && <p>No citing cases found.</p>}
        </div>
      </div>
    </section>
  );
}
