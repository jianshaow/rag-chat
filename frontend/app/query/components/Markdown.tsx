import 'github-markdown-css/github-markdown-light.css';
import "highlight.js/styles/github.css";
import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import { useQuery } from '../context/query-context';
import './Markdown.css';

interface MarkdownProps {
  height?: number | string;
}

export default function Markdown({ height = "200px" }: MarkdownProps) {
  const markdownRef = useRef<HTMLDivElement>(null);
  const { answer } = useQuery();

  useEffect(() => {
    const elemnet = markdownRef.current;
    if (elemnet) {
      requestAnimationFrame(() => {
        elemnet.scrollTop = elemnet.scrollHeight;
      });
    }
  }, [answer]);

  return (
    <div ref={markdownRef} className="markdown-frame markdown-body" style={{ height: height }}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeHighlight]}
      >
        {answer || ''}
      </ReactMarkdown>
    </div>
  );
};
