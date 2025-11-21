import './Question.css';

export default function Question(props: React.PropsWithChildren) {
  return (
    <div className='question-block'>
      <label>Question</label>
      {props.children}
    </div>
  );
}
