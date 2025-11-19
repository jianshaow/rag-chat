import React, { useEffect, useRef } from "react";
import './Events.css';

interface EventViewerProps {
  events: string[];
  height?: number | string;
}

const EventViewer: React.FC<EventViewerProps> = ({ events, height = "3em" }) => {
  const eventsRef = useRef<HTMLDivElement>(null);

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

export default EventViewer
