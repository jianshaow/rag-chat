"use client";

import { ChatInput, useChatUI, useFile } from "@llamaindex/chat-ui";
import { DocumentInfo, ImagePreview } from "@llamaindex/chat-ui/widgets";
import { useClientConfig } from "./hooks/use-config";

export default function CustomChatInput() {
  const { requestData, isLoading, input } = useChatUI();
  const { backend } = useClientConfig();
  const {
    image,
    setImage,
    uploadFile,
    files,
    removeDoc,
    reset,
    getAttachments,
  } = useFile({ uploadAPI: `${backend}/api/chat/upload` });

  const handleUploadFile = async (file: File) => {
    if (image?.url) {
      alert("You can only upload one image at a time.");
      return;
    }

    try {
      await uploadFile(file, requestData);
    } catch (error: unknown) {
      if (error instanceof Error) {
        alert(error.message);
      }
    }
  };

  const annotations = getAttachments();

  return (
    <ChatInput
      className="shadow-xl rounded-xl"
      resetUploadedFiles={reset}
      attachments={annotations}
    >
      <div>
        {image?.url && (
          <ImagePreview url={image.url} onRemove={() => setImage(null)} />
        )}
        {files.length > 0 && (
          <div className="flex gap-4 w-full overflow-auto py-2">
            {files.map((file) => (
              <DocumentInfo
                key={file.id}
                document={{ url: file.url, sources: [] }}
                className="mb-2 mt-2"
                onRemove={() => removeDoc(file)}
              />
            ))}
          </div>
        )}
      </div>
      <ChatInput.Form>
        <ChatInput.Field />
        <ChatInput.Upload onUpload={handleUploadFile} />
        <ChatInput.Submit
          disabled={
            isLoading || (!input.trim() && files.length === 0 && !image?.url)
          }
        />
      </ChatInput.Form>
    </ChatInput>
  );
}
