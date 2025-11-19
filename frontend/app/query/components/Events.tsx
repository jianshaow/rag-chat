import React from "react";
import './Events.css';

interface EventViewerProps {
  events: string[];
  height?: number | string;
}

const EventViewer: React.FC<EventViewerProps> = ({ events, height = "100px" }) => {

  return (
    <div className='events-block'>
      <label>Events</label>
      <div className='events-view' style={{ height: height }}>
        {events.map((event, index) => (
          <div key={index}>{event}</div>
        ))}
      </div>
    </div>
  );
}

export default EventViewer
