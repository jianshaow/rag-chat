import { QueryProvider } from '../context/query-context';
import './Question.css';

export default function QuerySection(props: React.PropsWithChildren) {
  return (
    <QueryProvider>
      <div>
        {props.children}
      </div>
    </QueryProvider>
  );
}
