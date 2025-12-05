export type MessageType = { id: string,role: string, content: string };

export type HistoryContentType = {
  history: MessageType[],
};