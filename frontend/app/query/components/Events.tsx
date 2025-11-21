import { useEffect, useRef } from "react";
import { useQuery } from "../context/query-context";
import './Events.css';

interface EventViewerProps {
  height?: number | string;
}

export default function EventViewer({ height = "3em" }: EventViewerProps) {
  const eventsRef = useRef<HTMLDivElement>(null);

  const { events } = useQuery();

  useEffect(() => {
    const elemnet = eventsRef.current;
    if (elemnet) {
      requestAnimationFrame(() => {
        elemnet.scrollTop = elemnet.scrollHeight;
      });
    }
  }, [events]);

  return (
    <div className='events-block'>
      <label>Events</label>
      <div ref={eventsRef} className='events-view' style={{ height: height }}>
        {events.map((event, index) => (
          <div key={index}>{event}</div>
        ))}
      </div>
    </div>
  );
}
