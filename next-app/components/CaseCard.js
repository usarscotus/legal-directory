import styles from '../styles/CaseCard.module.css';
import Link from 'next/link';

export default function CaseCard({ opinion }) {
  const { id, caseName, citation, dateFiled } = opinion;
  return (
    <div className={styles.card}>
      <h3>{caseName}</h3>
      {citation && (
        <div className={styles.meta}>{citation.join(', ')}</div>
      )}
      {dateFiled && (
        <div className={styles.meta}>Filed: {new Date(dateFiled).toLocaleDateString()}</div>
      )}
      <Link href={`/cases/${id}`}>View Details</Link>
    </div>
  );
}
