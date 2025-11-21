import { useChatContext } from "@/context/chat-context";
import { useConfig } from "@/context/config-context";
import { useEffect } from "react";
import './Question.css';

export default function AgentForm() {
  const {
    input,
    setInput,
    handleInputChange,
    handleSubmit,
  } = useChatContext();

  useEffect(() => {
    const { chatConfig } = useConfig();
    if (chatConfig && chatConfig.starterQuestions && chatConfig.starterQuestions.length > 0) {
      setInput(chatConfig.starterQuestions[0]);
    }
  }, []);

  return (
    <form onSubmit={handleSubmit}>
      <div className='question-bar'>
        <input type='text' value={input}
          onChange={handleInputChange}
          style={{ width: '100%' }} />
        <button type='submit'>Submit</button>
      </div>
    </form>
  );
}
