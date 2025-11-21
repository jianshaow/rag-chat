import { ChangeEvent } from "react";
import { useQuery } from "../context/query-context";
import './Question.css';

export default function Answer({ children }: React.PropsWithChildren) {
  const { agentic, setAgentic, streaming, setStreaming } = useQuery();

  return (
    <div className='answer-block'>
      <div className='between-container'>
        <label>Answer</label>
        <div className='right-group'>
          <label>Agentic: </label>
          <input type='checkbox' onChange={(e: ChangeEvent<HTMLInputElement>) => {
            setAgentic(e.target.checked);
          }} checked={agentic} />
          <label>Streaming: </label>
          <input type='checkbox' onChange={(e: ChangeEvent<HTMLInputElement>) => {
            setStreaming(e.target.checked);
          }} checked={streaming} disabled={agentic} />
        </div>
      </div>
      {children}
    </div>
  );
}
