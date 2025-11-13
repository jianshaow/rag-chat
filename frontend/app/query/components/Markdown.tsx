import 'github-markdown-css/github-markdown-light.css';
import "highlight.js/styles/github.css";
import React, { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import remarkRehype from "remark-rehype";
import './Markdown.css';

interface MarkdownViewerProps {
  content: string;
  height?: number;
}

const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ content, height = 200 }) => {
  const markdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = markdownRef.current;
    if (el) {
      requestAnimationFrame(() => {
        el.scrollTop = el.scrollHeight;
      });
    }
  }, [content]);

  return (
    <div ref={markdownRef} className="markdown-frame markdown-body" style={{ height: height }}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath, remarkRehype]}
        rehypePlugins={[rehypeHighlight]}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownViewer;
