"use client";

import { useEffect, useRef } from "react";
import { useQuery } from "../context/query-context";
import '../query.css';

interface EventsProps {
  style?: React.CSSProperties;
}

export default function Events({ style = { height: "3em" } }: EventsProps) {
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
      <div ref={eventsRef} className='events-view' style={style}>
        {events.map((event, index) => (
          <div key={index}>{event}</div>
        ))}
      </div>
    </div>
  );
}
