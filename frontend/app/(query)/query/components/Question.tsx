import '../page.css';

export default function Question({ children }: React.PropsWithChildren) {
  return (
    <div className='question-block'>
      <label>Question</label>
      {children}
    </div>
  );
}
