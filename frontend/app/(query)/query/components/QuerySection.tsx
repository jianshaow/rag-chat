import { QueryProvider } from '../context/query-context';

export default function QuerySection(props: React.PropsWithChildren) {
  return (
    <QueryProvider>
      <div>
        {props.children}
      </div>
    </QueryProvider>
  );
}
