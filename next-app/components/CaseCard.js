import styles from '../styles/CaseCard.module.css';

export default function CaseCard({ opinion, onSelect }) {
  const { id, caseName, citation, dateFiled } = opinion;

  return (
    <div
      className={styles.card}
      onClick={() => onSelect(id)}
      role="button"
      tabIndex={0}
      onKeyPress={(e) => {
        if (e.key === 'Enter') onSelect(id);
      }}
    >
      <h3>{caseName}</h3>
      {citation && (
        <div className={styles.meta}>{citation.join(', ')}</div>
      )}
      {dateFiled && (
        <div className={styles.meta}>Filed: {new Date(dateFiled).toLocaleDateString()}</div>
      )}
    </div>
  );
}
