import { QueryProvider } from '../context/query-context';
import './Question.css';

export default function QuerySection(props: React.PropsWithChildren) {
  return (
    <QueryProvider>
      <div className='container-column'>
        {props.children}
      </div>
    </QueryProvider>
  );
}
