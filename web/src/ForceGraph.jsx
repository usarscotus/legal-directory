import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

const width = 600;
const height = 400;

export default function ForceGraph({ caseId, onSelectNode }) {
  const ref = useRef();
  const [data, setData] = useState(null);

  useEffect(() => {
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    fetch(`${API_URL}/cases/${caseId}/citations`)
      .then((res) => res.json())
      .then(setData)
      .catch((err) => console.error('Failed to load citations', err));
  }, [caseId]);

  useEffect(() => {
    if (!data) return;
    const nodes = [{ id: String(caseId), main: true }];
    const links = [];

    data.incoming.forEach((id) => {
      nodes.push({ id: String(id) });
      links.push({ source: String(id), target: String(caseId) });
    });
    data.outgoing.forEach((id) => {
      nodes.push({ id: String(id) });
      links.push({ source: String(caseId), target: String(id) });
    });

    const svg = d3.select(ref.current);
    svg.selectAll('*').remove();
    svg.attr('viewBox', [0, 0, width, height]);

    const simulation = d3
      .forceSimulation(nodes)
      .force('link', d3.forceLink(links).id((d) => d.id).distance(80))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg
      .append('g')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(links)
      .join('line');

    const node = svg
      .append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', (d) => (d.main ? 8 : 5))
      .attr('fill', (d) => (d.main ? 'red' : 'steelblue'))
      .call(
        d3
          .drag()
          .on('start', (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on('drag', (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on('end', (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      )
      .on('click', (_, d) => onSelectNode && onSelectNode(d.id));

    simulation.on('tick', () => {
      link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      node.attr('cx', (d) => d.x).attr('cy', (d) => d.y);
    });

    return () => simulation.stop();
  }, [data, caseId, onSelectNode]);

  return <svg ref={ref} width={width} height={height}></svg>;
}

