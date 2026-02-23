import type { HistoryContentType } from '../types';

interface ResponseSectionProps {
  conversationId: string;
  responseContent: HistoryContentType | string;
}

export default function ResponseSection({
  conversationId,
  responseContent
}: Readonly<ResponseSectionProps>) {
  return (
    <div className="response-section">
      {conversationId && <h3>Conversation: {conversationId}</h3>}
      <div id="response-content">
        {(typeof responseContent === "string") ? responseContent
        :
        responseContent.history.map((message) =>
          <p key={message.id}>{message.role}: {message.content}</p>
        )}
      </div>
    </div>
  );
}