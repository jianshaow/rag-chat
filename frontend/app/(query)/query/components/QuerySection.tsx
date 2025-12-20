import { QueryProvider } from '../context/query-context';

export default function QuerySection(props: React.PropsWithChildren) {
  return (
    <QueryProvider>
      {props.children}
    </QueryProvider>
  );
}
