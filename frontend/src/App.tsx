import './App.css';
import { useState } from 'react';
import MessageSection from './components/message-section';
import ResponseSection from './components/response-section';
import type { HistoryContentType } from './types';


function App() {
  const [conversationId, setConversationId] = useState("");
  const [responseContent, setResponseContent] = useState<string | HistoryContentType>("");
  const [conversations, setConversations] = useState<{id: string, messages: []}[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");


  const postNewConversation = () => {
    setLoading(true);
    const url = import.meta.env.VITE_API_BASE_URL;
    fetch(url + "/conversations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => response.json())
    .then((data) => setConversationId(data.conversation_id))
    .finally(() => {
      setLoading(false);
      setResponseContent("");
    })
    .catch((error) => setError(error.toString()));
  }

  const listConversations = () => {
    setLoading(true);
    const url = import.meta.env.VITE_API_BASE_URL;
    fetch(url + "/conversations", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => response.json())
    .then((data) => setConversations(data.conversations))
    .finally(() => setLoading(false))
    .catch((error) => setError(error.toString()));
  }

  const conversationClickHandler = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    e.preventDefault();

    // Set the selected conversation
    setConversationId((e.target as HTMLButtonElement).textContent);

    // Reset the list
    setConversations([]);
  };

  const showHistory = () => {
    setLoading(true);
    const url = import.meta.env.VITE_API_BASE_URL;
    fetch(url + "/conversations/" + conversationId, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => response.json())
    .then((data) => {
      setResponseContent(data);
    })
    .finally(() => setLoading(false))
    .catch((error) => setError(error.toString()));
  }

  const resetConversation = () => {
    setLoading(true);
    const url = import.meta.env.VITE_API_BASE_URL;
    fetch(url + "/conversations/" + conversationId, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => response.json())
    .then(() => {
      setResponseContent("");
    })
    .finally(() => setLoading(false))
    .catch((error) => setError(error.toString()));
  }


  return (
    <>
      <header>
        <h1>Chat avec Cohere</h1>
      </header>
      <main>
        <div className="control-section">
          <button type="submit" onClick={() => postNewConversation()}>Nouvelle conversation</button>
          <button type="submit" onClick={() => listConversations()}>Liste des conversations</button>
          <button type="submit" onClick={() => showHistory()}>Historique</button>
          <button type="submit" onClick={() => resetConversation()}>Réinitialiser</button>
        </div>

        {(conversations && conversations.length > 0) &&
        <ul className='conversation-list'>
          {conversations.map((conversation) => (
            <li key={conversation.id}>
              <button onClick={conversationClickHandler}>{conversation.id}</button>
            </li>
          ))}
        </ul>}

        {loading && <div className="loading">Chargement...</div>}
        {error && <div className="error">Impossible d'appeler l'API. Error found: {error}!</div>}

        <ResponseSection conversationId={conversationId} responseContent={responseContent}/>

        {conversationId && <MessageSection conversationId={conversationId} setResponseContent={setResponseContent}/>}
      </main>
      <footer>@Copyright 2025</footer>
    </>
  )
}

export default App
